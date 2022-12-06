# Copyright (c) 2022, NVIDIA CORPORATION.
# CONFIDENTIAL, provided under NDA.

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Used to plot the Co-ordinates


def gen_plot(df):
    plt.figure(figsize=(11, 11))
    plt.scatter(
        df["xcord"][:1],
        df["ycord"][:1],
        label="Depot",
        color="Green",
        marker="o",
        s=25,
    )
    plt.scatter(
        df["xcord"][1::],
        df["ycord"][1::],
        label="Locations",
        color="Red",
        marker="o",
        s=25,
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
            fontproperties=fm.FontProperties(size=12),
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
    vehicles = routes.truck_id.unique().to_numpy()
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


def map_vehicle_routes(df, route, colors):
    plt = gen_plot(df)
    veh_ids = route.truck_id.unique().to_numpy()
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
