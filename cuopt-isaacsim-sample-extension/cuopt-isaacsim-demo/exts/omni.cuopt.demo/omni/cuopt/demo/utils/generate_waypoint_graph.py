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

from pxr import Gf

import json

from .visualize_waypoint_graph import NetworkSimpleViz
from .common import check_build_base_path, edge_in_volume, get_prim_translation


class WaypointGraphModel():


    def __init__(self):

        self.visualization = NetworkSimpleViz()

        self.nodes = []
        self.offsets = []
        self.edges = [] 
        self.weights = []

        self.node_count = 0
        self.edge_count = 0

        self.node_path_map = {}
        self.path_node_map = {}
        self.node_edge_map = {}
        self.edge_path_map = {}
        self.path_edge_map = {}


    def visualize_and_record_node(self, stage, node_prim_path, translation):
        
        self.visualization.add_node_to_scene(stage, node_prim_path, translation)
        
        # Data recording
        self.node_path_map[self.node_count] = node_prim_path
        self.path_node_map[node_prim_path] = self.node_count
        
        self.node_count += 1


    def visualize_and_record_edge(self, stage, edge_prim_path, point_from, point_to):
            
        weight = self.visualization.add_edge_to_scene(stage, edge_prim_path, point_from, point_to)      

        # Data recording
        self.edge_path_map[self.edge_count] = edge_prim_path
        self.path_edge_map[edge_prim_path] = self.edge_count
        self.weights.append(weight)
        self.edge_count = self.edge_count + 1


    def update_weights(self, stage, semantics):
        
        edges = self.path_edge_map.keys()

        # Only calculate for visible semantic zones
        vis_vol_paths = [] 
        for vol_path in semantics:
            prim_is_visible = True
            vol_prim = stage.GetPrimAtPath(vol_path)

            # check the prim
            vis_status = vol_prim.GetAttribute("visibility").Get()

            # if it's inherited check all parents
            if vis_status == "inherited":

                # check parents until root path
                while vol_prim.GetPath().pathString != "/":
                    parent = vol_prim.GetParent()
                    vis_status = parent.GetAttribute("visibility").Get()
                    if vis_status == "invisible":
                        prim_is_visible = False
                    vol_prim = parent
            else:
                prim_is_visible = False
                

            # if the prim and all it's parents are visible
            if prim_is_visible:
                vis_vol_paths.append(vol_path)
            else:
                print(f"{vol_path} is not visible at some level so will not be used")


        for i, edge_path in enumerate(edges):
            edge_prim = stage.GetPrimAtPath(edge_path)
            base_weight = edge_prim.GetAttribute("baseweight").Get()
            edge_prim.GetAttribute("weight").Set(base_weight)
            current_weight = edge_prim.GetAttribute("weight").Get()

            for vol_path in vis_vol_paths:
                # print(vol_path, edge_path)
                vol_prim = stage.GetPrimAtPath(vol_path)
                #               
                is_true, perc = edge_in_volume(edge_prim, vol_prim)
                if is_true:
                    print("edge_in volume: ", perc * 100, " %")
                    semantic_weight = vol_prim.GetAttribute("mfgstd:properties:semantic_weight").Get()
                    current_weight = current_weight + base_weight * (semantic_weight - 1.0) * perc
                    print("Base edge weight:", base_weight, "Semantic weight:", semantic_weight, "New edge weight:", current_weight)
            edge_prim.GetAttribute("weight").Set(current_weight)
            self.weights[i] = edge_prim.GetAttribute("weight").Get()


    # Get Nodes closest to point (x,y,z)
    def get_closest_node(self, stage, point):
        min_dist = None
        closest_node_path = None
        for node_path in self.path_node_map:
            node_prim = stage.GetPrimAtPath(node_path)
            node_point = get_prim_translation(node_prim)
            distance = (node_point-point).GetLength()
            if min_dist is None:
                min_dist = distance
                closest_node_path = node_path
            elif min_dist > distance:
                min_dist = distance
                closest_node_path = node_path
        return closest_node_path



def load_waypoint_graph_from_file(stage, 
                                  waypoint_graph_json,
                                  waypoint_graph_node_path,
                                  waypoint_graph_edge_path):

    model = WaypointGraphModel()

    with open(waypoint_graph_json) as graph_file:
            waypoint_graph_data = json.load(graph_file)
    model.nodes = waypoint_graph_data["node_locations"]

    graph = waypoint_graph_data["graph"]
    
    # Convert the graph to CSR and save it to the graph model
    offsets = []
    edges = []
    cur_offset = 0
    offset_node_lookup = {}
    ordered_keys = sorted([int(x) for x in graph.keys()])
    for i,node in enumerate(ordered_keys):
        offsets.append(cur_offset)
        cur_offset += len(graph[str(node)]["edges"])
        
        edges = edges + graph[str(node)]["edges"]
        offset_node_lookup[i] = node
        
    offsets.append(cur_offset)

    model.offsets = offsets
    model.edges =   edges

    check_build_base_path(stage, waypoint_graph_node_path, final_xform=True)
    stage.DefinePrim(waypoint_graph_node_path, "Xform")
    for i, node_loc in enumerate(model.nodes):                           
        node_prim_path= f'{waypoint_graph_node_path}/Node_{model.node_count}'
        model.visualize_and_record_node(stage, node_prim_path, node_loc)


    check_build_base_path(stage, waypoint_graph_edge_path, final_xform=True)
    stage.DefinePrim(waypoint_graph_edge_path, "Xform")
    for i in range(0, len(model.offsets)-1):
        for j in range(model.offsets[i], model.offsets[i+1]):
            edge_prim_path= f'{waypoint_graph_edge_path}/Edge_{offset_node_lookup[i]}_{model.edges[j]}'
            
            if str(offset_node_lookup[i]) not in model.node_edge_map:
                model.node_edge_map[str(offset_node_lookup[i])] = [model.edges[j]]
            else:
                model.node_edge_map[str(offset_node_lookup[i])].append(model.edges[j])

            point_from = Gf.Vec3d(model.nodes[int(offset_node_lookup[i])])
            point_to = Gf.Vec3d(model.nodes[model.edges[j]])
            model.visualize_and_record_edge(stage,edge_prim_path, point_from, point_to)

    return model
