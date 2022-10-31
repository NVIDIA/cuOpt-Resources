#!/usr/bin/env python

# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from scipy.spatial import distance
import numpy as np
import requests
import pandas as pd
import os
import json
import sys

def show_results(res):
    print("\n====================== Response ===========================\n")
    print("Solver status: ", res["status"])
    if res["status"] == 0:
        print("Cost         : ", res["solution_cost"])
        print("Vehicle count: ", res["num_vehicles"])
        for vehid in res["vehicle_data"].keys():
            print("\nVehicle ID: ", vehid)
            print("----------")
            data = [str(x) for x in res["vehicle_data"][vehid]["route"]]
            print(" -> ".join(data))
    else:
        print("Error: ", res["error"])
    print("\n======================= End ===============================\n")

# Reads one of the homberger's instance definition to read dataset
# This function is specifically designed only to read
# homberger's instance definition
def create_from_file(file_path):
    node_list = []
    with open(file_path, 'rt') as f:
        count = 1
        for line in f:
            if count == 5:
                vehicle_num, vehicle_capacity = line.split()
                vehicle_num = int(vehicle_num)
                vehicle_capacity = int(vehicle_capacity)
            elif count >= 10:
                node_list.append(line.split())
            count += 1
            # if count == 36:
            #     break

    df = pd.DataFrame(columns=['vertex', 'x', 'y', 'demand',
                               'earliest_time', 'latest_time',
                               'service_time'])

    for item in node_list:
       df = df.append({
            "vertex": int(item[0]),
            "x": float(item[1]),
            "y": float(item[2]),
            "demand": int(item[3]),
            "earliest_time": int(item[4]),
            "latest_time": int(item[5]),
            "service_time": int(item[6]),
           }, ignore_index=True)

    return df, vehicle_capacity, vehicle_num

def read_data(filename):
    df, vehicle_capacity, n_vehicles = create_from_file(filename)
    return df, vehicle_capacity, n_vehicles

# Build euclidean distance matrix from the x, y coordinates
# obtained from the dataset. This later helps in mapping.
def build_matrix(df):
    coords = list(zip(df['x'].tolist(),
    df['y'].tolist()))
    distances = distance.cdist(coords, coords, 'euclidean')
    return pd.DataFrame(distances).astype(np.float32)

def url():
    ip = "127.0.0.1"
    port = "5000"
    return "http://" + ip + ":" + port + "/cuopt/"

def post_cost_matrix(matrix, data_params):
    cost_matrix_response = requests.post(
        url() + "add_cost_matrix",
        params=data_params,
        json={"cost_matrix": {"0": matrix}})
    print(f"\nCOST MATRIX ENDPOINT RESPONSE: {cost_matrix_response.json()}\n")

def post_fleet_data(locations, capacities, data_params):
    fleet_response = requests.post(
        url() + "set_fleet_data",
        params = data_params,
        json = {"vehicle_locations": locations,
                "capacities": capacities})
    print(f"FLEET ENDPOINT RESPONSE: {fleet_response.json()}\n")

def post_task_data(locations, demand, time_windows, service_times, data_params):
    task_response = requests.post(
        url() + "set_task_data",
        params =data_params,
        json = {
            "task_locations": locations,
            "demand": demand,
            "task_time_windows": time_windows,
            "service_times": service_times
        })
    print(f"TASK ENDPOINT RESPONSE: {task_response.json()}\n")

def post_solver_config(config, data_params):
    solver_config = {"time_limit": 0.01, "number_of_climbers": 128}

    solver_config_response = requests.post(
        url() + "set_solver_config",
        params = data_params,
        json = config)
    print(f"SOLVER CONFIG ENDPOINT RESPONSE: {solver_config_response.json()}\n")


infile = 'C1_SMALL.TXT'
if not os.path.exists(infile):
    print("File does not exist %s" % infile)
    sys.exit(1)

# Extract the data
df, vehicle_capacity, n_vehicles = read_data(infile)

distances = build_matrix(df)
num_locations = df["demand"].shape[0]
time_window = df[['earliest_time', 'latest_time', 'service_time']]
data_params = {"return_data_state": False}

# Our vehicles all start and end at the depot
post_cost_matrix(distances.values.tolist(), data_params)
post_fleet_data(locations = [[0, 0]] * n_vehicles,
                capacities = [[vehicle_capacity] * n_vehicles],
                data_params = data_params)

# We don't have any tasks at the depot, so we drop location 0 from all of our lists
post_task_data(locations = list(range(num_locations))[1:],
               demand = [df['demand'].values.tolist()[1:]],
               time_windows = list(zip(time_window['earliest_time'].values.tolist()[1:],
                                       time_window['latest_time'].values.tolist()[1:])),
               service_times = time_window['service_time'].values.tolist()[1:],
               data_params = data_params)

post_solver_config(config = {"time_limit": 0.01,
                             "number_of_climbers": 128},
                   data_params = data_params)

solve_parameters = {
    # Uncomment to disable/ignore constraints.

    # "ignore_capacities": True,
    # "ignore_vehicle_time_windows": True,
    # "ignore_vehicle_break_time_windows": True,
    # "ignore_task_time_windows": True,
    # "ignore_pickup_and_delivery": True,
    "return_status": False,
    "return_data_state": False,
}

solver_response = requests.get(
    url() + "get_optimized_routes",
    params = solve_parameters
)

import json
print(json.dumps(solver_response.json(), indent=4))

show_results(solver_response.json()["response"]["solver_response"])
