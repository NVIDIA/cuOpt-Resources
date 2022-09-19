# Copyright (c) 2022, NVIDIA CORPORATION.
# CONFIDENTIAL, provided under NDA.

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

# Used to plot the Co-ordinates
def gen_plot(df):
    plt.figure(figsize=(11, 11))
    plt.scatter(
        df["xcord"][:1],
        df["ycord"][:1],
        label="Depot",
        color="Green",
        marker="o",
        s=100,
    )
    plt.scatter(
        df["xcord"][1::],
        df["ycord"][1::],
        label="Locations",
        color="Red",
        marker="o",
        s=100,
    )
    plt.xlabel("x - axis")
    # frequency label
    plt.ylabel("y - axis")
    # plot title
    plt.title("Simplified Map")
    # showing legend
    plt.legend()

    for i, label in enumerate(df.index.values):
        plt.annotate(
            label,
            (df["xcord"][i], df["ycord"][i]),
            fontproperties=fm.FontProperties(size=16),
        )
    return plt

# Used to plot arrows
def add_arrows(df, routes, plt, color="green"):
    prev_cord = ()
    for i, label in enumerate(routes["route"].to_numpy()):
        if i > 0:
            plt.annotate(
                "",
                xy=(df["xcord"][label], df["ycord"][label]),
                xytext=prev_cord,
                arrowprops=dict(
                    arrowstyle="simple, head_length=0.5, head_width=0.5, tail_width=0.15",  # noqa
                    connectionstyle="arc3",
                    color=color,
                    mutation_scale=20,
                    ec="black",
                ),
                label="vehicle-1",
            )
        prev_cord = df["xcord"][label], df["ycord"][label]

    return plt


# Prints vehicle routes
def show_vehicle_routes(routes, locations):
    vehicles = routes.truck_id.unique()
    for id in vehicles:
        print("For vehicle -", id, "route is: \n")
        route = routes[routes.truck_id == id]
        path = ""
        route_ids = route.route.to_numpy()
        for index, route_id in enumerate(route_ids):
            path += locations[route_id]
            type(route_ids)
            if index != (len(route_ids) - 1):
                path += "->"
        print(path + "\n\n")


# Map vehicle routes
def map_vehicle_routes(df, route, colors):
    plt = gen_plot(df)
    veh_ids = route.truck_id.unique()
    idx = 0
    vid_map = {}
    for v_id in veh_ids:
        vid_map[v_id] = idx
        idx = idx + 1

    for v_id in veh_ids:
        plt = add_arrows(
            df, route[route.truck_id == v_id], plt, color=colors[vid_map[v_id]]
        )

    return plt


# Convert the solver response from the server to a cuDF dataframe
def create_solution_dataframe(solver_resp):
    solution = solver_resp["vehicle_data"]["location"]
    df = {}
    df["route"] = []
    df["truck_id"] = []
    df["location"] = []
    for vid, route in solution.items():
        df["location"] = df["location"] + route
        df["truck_id"] = df["truck_id"] + [vid] * len(route)
    df["route"] = df["location"]
    return pd.DataFrame(df)


# Convert the solver response from the server to a cuDF dataframe
# for waypoint graph problems
def get_solution_df(resp):
    solution = resp["vehicle_data"]

    df = {}
    df["route"] = []
    df["truck_id"] = []
    df["location"] = []
    df["types"] = []

    for vid, route in solution.items():
        df["location"] = df["location"] + route["routes"]
        df["truck_id"] = df["truck_id"] + [vid] * len(route["routes"])
        df["types"] = df["types"] + route["type"]

    df["route"] = df["location"]

    return pd.DataFrame(df)


def create_from_file(file_path, is_pdp=False):
    node_list = []
    with open(file_path, "rt") as f:
        count = 1
        for line in f:
            if is_pdp and count == 1:
                vehicle_num, vehicle_capacity, speed = line.split()
            elif not is_pdp and count == 5:
                vehicle_num, vehicle_capacity = line.split()
            elif is_pdp:
                node_list.append(line.split())
            elif count >= 10:
                node_list.append(line.split())
            count += 1
            # if count == 36:
            #     break

    vehicle_num = int(vehicle_num)
    vehicle_capacity = int(vehicle_capacity)
    df = pd.DataFrame(
        columns=[
            "vertex",
            "xcord",
            "ycord",
            "demand",
            "earliest_time",
            "latest_time",
            "service_time",
            "pickup_index",
            "delivery_index",
        ]
    )

    for item in node_list:
        row = {
            "vertex": int(item[0]),
            "xcord": float(item[1]),
            "ycord": float(item[2]),
            "demand": int(item[3]),
            "earliest_time": int(item[4]),
            "latest_time": int(item[5]),
            "service_time": int(item[6]),
        }
        if is_pdp:
            row["pickup_index"] = int(item[7])
            row["delivery_index"] = int(item[8])
        df = pd.concat(
            [df, pd.DataFrame(row, index=[0])],
            ignore_index=True,
        )

    return df, vehicle_capacity, vehicle_num
