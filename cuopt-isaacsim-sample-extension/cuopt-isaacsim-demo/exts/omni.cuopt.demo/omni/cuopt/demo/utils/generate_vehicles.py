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

from .common import read_json

class TransportVehicles():


    def __init__(self):
        self.num_vehicles = None
        self.vehicle_xyz_locations = None
        self.graph_locations = None
        self.vehicle_capacities = None
        self.vehicle_time_windows = None


    # Load Fleet info from json data
    def load_sample(self, vehicles_json_path):
        vehicles_data = read_json(vehicles_json_path)

        self.num_vehicles = len(vehicles_data["vehicle_locations"])
        self.vehicle_xyz_locations = vehicles_data["vehicle_locations"]
        self.vehicle_capacities = vehicles_data["capacities"]
        if "vehicle_time_windows" in vehicles_data:
            self.vehicle_time_windows = vehicles_data["vehicle_time_windows"]
        
        self.graph_locations = vehicles_data["vehicle_locations"]
