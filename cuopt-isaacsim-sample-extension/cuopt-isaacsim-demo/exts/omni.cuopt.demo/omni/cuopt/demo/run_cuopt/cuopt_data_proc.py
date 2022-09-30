# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

def preprocess_cuopt_data(graph, task, fleet):

    waypoint_graph_data = {
        "offsets": graph.offsets,
        "edges":   graph.edges,
        "weights": graph.weights,
    }   

    fleet_data = {
        "vehicle_locations": fleet.graph_locations,
        "capacities": fleet.vehicle_capacities,
        "vehicle_time_windows": fleet.vehicle_time_windows,
    }
   
    task_data = {
        "task_locations": task.graph_locations,
        "demand": task.order_demand,
        "task_time_windows": task.order_time_windows,
        "service_times": task.order_service_times,
    }

    return waypoint_graph_data, fleet_data, task_data