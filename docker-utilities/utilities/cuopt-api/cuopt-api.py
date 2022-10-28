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

import cudf
import os
import cuopt.routing.vehicle_routing
from scipy.spatial import distance
import numpy as np
import pandas as pd
import helper_function.helper_data as helper_data

CUOPT_PROG_DIR=os.environ.get("CUOPT_PROG_DIR", "./")
CUOPT_LOCAL_DIR=os.environ.get("CUOPT_LOCAL_DIR", "./")

# Extract the data
df, vehicle_capacity, n_vehicles = helper_data.read_data('data/homberger_1000_customer_instances/C1_10_1.TXT')

# Build euclidean distance matrix from the x, y coordinates obtained from the dataset
# This later helps in mapping.
def build_matrix(df):
    coords = list(zip(df['xcord'].to_arrow().to_pylist(),
                      df['ycord'].to_arrow().to_pylist()))
    distances = distance.cdist(coords, coords, 'euclidean')
    return cudf.DataFrame(distances).astype(np.float32)

def data_model_initialization(df, nodes, n_vehicles, vehicle_priorities, vehicle_capacity,
                              vehicle_skip_first_trips, vehicle_locations,
                              node_precedence):

    my_data_model = cuopt.routing.vehicle_routing.DataModel(nodes, n_vehicles)

    # Add cost matrix information
    distances = build_matrix(df)
    my_data_model.add_cost_matrix(distances)
    # If you wish to directly use the x, y coordinates you can use the set_coordinates API as below:
    # my_data_model.set_coordinates(df['x'], df['y'])

    # Set vehicle priorities
    if len(vehicle_priorities) > 0:
        my_data_model.set_vehicle_priorities(vehicle_priorities)

    # Set start and return locations for vehicles
    if vehicle_locations:
        my_data_model.set_vehicle_locations(vehicle_locations["start"],
                                            vehicle_locations["return"])

    # Set node precedence. Each key is a node, and the value is the list
    # of nodes that have precedence
    if node_precedence:
        for key, value in node_precedence.items():
            my_data_model.add_order_precedence(key, value)

    # Set vehicle skip first trips
    if len(vehicle_skip_first_trips) > 0:
        my_data_model.set_skip_first_trips(vehicle_skip_first_trips)
        
    capacity = cudf.Series(vehicle_capacity)
    
    # Add capacity dimension
    my_data_model.add_capacity_dimension("demand", df['demand'], capacity)
    
    # Add delivery time windows
    my_data_model.set_order_time_windows(df['earliest_time'], df['latest_time'], df['service_time'])

    return my_data_model

def solver_initialization(df):
    solver_settings = cuopt.routing.SolverSettings()
    
    # Set seconds update and climbers
    solver_settings.set_time_limit(1)
    solver_settings.set_number_of_climbers(2048)

    # Set max_distance_per_route to something > 0 to put an upper bound
    # on the distance traveled for each route. This might result in no solution.
    max_distance_per_route=0.0
    if max_distance_per_route > 0.0:
        solver_settings.set_max_distance_per_route(max_distance_per_route)

    return solver_settings

def call_solve(my_data_model, solver_settings):
    routing_solution = cuopt.routing.Solve(my_data_model, solver_settings)
    final_cost = routing_solution.get_cost()
    vehicle_count = routing_solution.get_vehicle_count()
    cu_status = routing_solution.get_status()
    if cu_status != 0:
        print("""
        --------------------------------------------------------------------------------------------------
          !!!!!!!!!!!!        Failed: Solution within constraints could not be found     !!!!!!!!!!!!!!!!
        -------------------------------------------------------------------------------------------------- """)
    else:
        print("Final Cost         : ", final_cost) 
        print("Number of Vehicles : ", vehicle_count)
    return routing_solution

# Run NVIDIA cuopt on given dataset, for number vehicles with particular capacity and vehicle_priorities.
def run_cuopt(df, n_vehicles, vehicle_capacity, vehicle_priorities=[], vehicle_skip_first_trips=[],
              vehicle_locations={}, node_precedence={}):

    nodes = df["demand"].shape[0]

    my_data_model = data_model_initialization(df, nodes, n_vehicles, vehicle_priorities, vehicle_capacity,
                                              vehicle_skip_first_trips, vehicle_locations, node_precedence)

    solver_settings =  solver_initialization(df)

    # Solve for routes and cost
    routing_solution = call_solve(my_data_model, solver_settings)
    
    return routing_solution

vehicle_capacity = cudf.Series([vehicle_capacity]*n_vehicles)

# This will cause the first half of the vehicles to start at location 0 (the default)
# and the rest of the vehicles to start at the last location. The return locations
# will be swapped.
vehicle_locations = {}
last_location = df["demand"].shape[0] - 1
vehicle_locations["start"] = cudf.Series([0] * (n_vehicles // 2) + [last_location] *  (n_vehicles - n_vehicles // 2))
vehicle_locations["return"] = cudf.Series([last_location] * (n_vehicles // 2) + [0] *  (n_vehicles - n_vehicles // 2))

# This will cause the first half of the vehicles to not include the trip from the depot
# to the first location in the route and the cost calculations via the "DataModelView.skip_first_trips()" method.
# For the default behavior, set all the entries in the series to False or don't pass vehicle_skip_first_trips
# to the run_cuopt method.
vehicle_skip_first_trips = cudf.Series([True] * (n_vehicles // 2) + [False] * (n_vehicles - n_vehicles // 2))

solution = run_cuopt(df, n_vehicles, vehicle_capacity, vehicle_skip_first_trips=vehicle_skip_first_trips,
                     vehicle_locations=vehicle_locations)
print("""
------------------------------------------------------------------------------------
                                     Routes
------------------------------------------------------------------------------------
""")

import json
#print(json.dumps(solution.get_route().to_pandas().to_dict(), indent=4))
solution.display_routes()

# To write out results
#f=open(LOCAL_DIR+"/results","w")
#f.write(json.dumps(solution.get_route().to_pandas().to_dict(), indent=4))
#f.close()
