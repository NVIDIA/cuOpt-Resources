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

from pxr import UsdGeom, UsdLux
import omni.ext
from omni.kit.menu.utils import add_menu_items, remove_menu_items, MenuItemDescription

import omni.ui as ui
from omni.isaac.ui.ui_utils import setup_ui_headers, get_style, btn_builder, str_builder

import gc
import weakref
import requests

from .utils.common import check_build_base_path
from .utils.generate_warehouse_building import generate_building_structure
from .utils.generate_warehouse_assets import generate_shelves_assets, generate_conveyor_assets
from .utils.generate_waypoint_graph import WaypointGraphModel, load_waypoint_graph_from_file
from .utils.visualize_waypoint_graph import NetworkSimpleViz
from .utils.generate_orders import TransportOrders
from .utils.generate_vehicles import TransportVehicles
from .utils.generate_semantics import generate_semantic_zones

from .run_cuopt.cuopt_data_proc import preprocess_cuopt_data
from .run_cuopt.cuopt_microservice_manager import cuOptRunner


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.

EXTENSION_NAME = "cuOpt Isaac Sim Demo"

class cuOptMicroserviceExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        self._ext_id = ext_id

        ext_manager = omni.kit.app.get_app().get_extension_manager()
        self._extension_path = ext_manager.get_extension_path(ext_id)
        self._extension_data_path = f"{self._extension_path}/omni/cuopt/demo/demo_data/"

        self._window = None
        self._usd_context = omni.usd.get_context()

        self._cuopt_ip_promt = "Enter IP"
        self._cuopt_port_promt = "Enter Port"


        base_asset_path = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/"
 
        self._isaac_asset_path = base_asset_path + "Isaac/2022.1/Isaac/"
        self._isaac_nvidia_asset_path = base_asset_path + "Isaac/2022.1/NVIDIA/"
        self._nvidia_digital_twin_path = base_asset_path + "DigitalTwin/Assets/Warehouse/"

        print(f"\n\nAssets will be retrieved from the following locations:\
                                \n-Isaac Path : {self._isaac_asset_path}\
                                \n-Isaac NVIDIA Path : {self._isaac_nvidia_asset_path}\
                                \n-NVIDIA Digtal Twin Path : {self._nvidia_digital_twin_path}\n\n")

        self.waypoint_graph_node_path = "/World/Warehouse/Transportation/WaypointGraph/Nodes"
        self.waypoint_graph_edge_path = "/World/Warehouse/Transportation/WaypointGraph/Edges"
        
        self.warehouse_building_config = "warehouse_building_data.json"
        self.warehouse_shelves_config = "warehouse_shelves_data.json"
        self.warehouse_conveyors_config = "warehouse_conveyors_data.json"
        self.waypoint_graph_config = "waypoint_graph.json"
        self.semantic_config = "semantics_data.json"
        self.orders_config = "orders_data.json"
        self.vehicles_config = "vehicle_data.json"

        self._waypoint_graph_model = WaypointGraphModel()
        self._orders_obj = TransportOrders()
        self._vehicles_obj = TransportVehicles()
        self._semantics = []

        menu_items = [
            MenuItemDescription(name=EXTENSION_NAME, onclick_fn=lambda a=weakref.proxy(self): a._menu_callback())
        ]
        self._menu_items = [MenuItemDescription(name="cuOpt Microservice", sub_menu=menu_items)]
        add_menu_items(self._menu_items, "NVIDIA cuOpt")

        self._build_ui()


    def _menu_callback(self):
        self._window.visible = not self._window.visible

    
    def _on_window(self, visible):
        if self._window.visible:
            self._sub_stage_event = self._usd_context.get_stage_event_stream().create_subscription_to_pop(
                self._on_stage_event
            )
        else:
            self._sub_stage_event = None


    def _build_ui(self):

        if not self._window:
            self._window = ui.Window(
                title=EXTENSION_NAME, width=0, height=0, visible=False, dockPreference=ui.DockPreference.LEFT_BOTTOM
            )
            self._window.set_visibility_changed_fn(self._on_window)
            
        with self._window.frame:
                with ui.VStack(spacing=5, height=0):
                    title = "cuOpt Extension Code and Docs"
                    doc_link = "https://github.com/NVIDIA/cuOpt-Resources"

                    overview = "This example shows how to connect the "
                    overview += "NVIDIA cuOpt microservice to Omniverse Isaac Sim"
                    overview += "\n\nPress the 'Open Source Code' button to view the source code."

                    setup_ui_headers(self._ext_id, __file__, title, doc_link, overview)

                    # Setting up the UI to connect to cuOpt Microservice
                    connect_cuOpt_frame = ui.CollapsableFrame(
                        title="Connect to cuOpt Microservice",
                        height=0,
                        collapsed=False,
                        style=get_style(),
                        style_type_name_override="CollapsableFrame",
                        horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
                        vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
                    )
                    with connect_cuOpt_frame:
                        with ui.VStack(style=get_style(), spacing=5, height=0):

                            kwargs = {
                                "label": "cuOpt IP",
                                "type": "stringfield",
                                "default_val": self._cuopt_ip_promt,
                                "tooltip": "IP for cuOpt microservice",
                                "on_clicked_fn": None,
                                "use_folder_picker": False,
                                "read_only": False,
                                }
                            self._cuopt_ip = str_builder(**kwargs)

                            kwargs = {
                                "label": "cuOpt Port",
                                "type": "stringfield",
                                "default_val": self._cuopt_port_promt,
                                "tooltip": "Port for cuOpt microservice",
                                "on_clicked_fn": None,
                                "use_folder_picker": False,
                                "read_only": False,
                                }
                            self._cuopt_port = str_builder(**kwargs)

                            kwargs = {
                                "label": "Test cuOpt Connection ",
                                "type": "button",
                                "text": "Test",
                                "tooltip": "Test to verify cuOpt microservice is reachabel",
                                "on_clicked_fn": self._test_cuopt_connection,
                            }
                            btn_builder(**kwargs)

                            self._cuopt_status_info = ui.Label(" ")

                    # Setting up the UI setup the optimization problem
                    setup_frame = ui.CollapsableFrame(
                        title="Optimization Problem Setup",
                        height=0,
                        collapsed=False,
                        style=get_style(),
                        style_type_name_override="CollapsableFrame",
                        horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
                        vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
                    )
                    with setup_frame:
                        with ui.VStack(style=get_style(), spacing=5, height=0):

                            ui_data_style={"font_size": 14, "color": 0x88888888, "alignment": ui.Alignment.LEFT}

                            kwargs = {
                                "label": "Load Sample Warehouse ",
                                "type": "button",
                                "text": "Load",
                                "tooltip": "Loads an example warehouse environment",
                                "on_clicked_fn": self._build_warehouse_environment,
                            }
                            btn_builder(**kwargs)
                            self._warehouse_ui_data = ui.Label("No Warehouse Loaded", width=350,
                                word_wrap=True, style=ui_data_style)

                            kwargs = {
                                "label": "Load Waypoint Graph ",
                                "type": "button",
                                "text": "Load",
                                "tooltip": "Loads a waypoint graph for the sample environment",
                                "on_clicked_fn": self._load_waypoint_graph,
                            }
                            btn_builder(**kwargs)
                            self._network_ui_data = ui.Label("No Waypoint Graph network Loaded", width=350,
                                word_wrap=True, style=ui_data_style)

                            kwargs = {
                                "label": "Load Orders ",
                                "type": "button",
                                "text": "Load",
                                "tooltip": "Loads sample orders",
                                "on_clicked_fn": self._load_orders,
                            }
                            btn_builder(**kwargs)
                            self._orders_ui_data = ui.Label("No Orders Loaded", width=350,
                                word_wrap=True, style=ui_data_style)

                            kwargs = {
                                "label": "Load Vehicles ",
                                "type": "button",
                                "text": "Load",
                                "tooltip": "Loads sample vehicle data",
                                "on_clicked_fn": self._load_vehicles,
                            }
                            btn_builder(**kwargs)
                            self._vehicle_ui_data = ui.Label("No Vehilces Loaded", width=350,
                                word_wrap=True, style=ui_data_style)

                            kwargs = {
                                "label": "Load Semantic Zone ",
                                "type": "button",
                                "text": "Load",
                                "tooltip": "Loads a sample semantics zone",
                                "on_clicked_fn": self._load_semantic_zone,
                            }
                            btn_builder(**kwargs)
                            self._semantic_ui_data = ui.Label("No Semantic Zones Loaded", width=350,
                                word_wrap=True, style=ui_data_style)

                            

                    # Setting up the UI setup the optimization problem
                    run_frame = ui.CollapsableFrame(
                        title="Update/Run cuOpt",
                        height=0,
                        collapsed=False,
                        style=get_style(),
                        style_type_name_override="CollapsableFrame",
                        horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
                        vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
                    )
                    with run_frame:
                        with ui.VStack(style=get_style(), spacing=5, height=0):

                            ui_data_style={"font_size": 14, "color": 0xBBBBBBBB, "alignment": ui.Alignment.LEFT}

                            kwargs = {
                                "label": "Update Weights ",
                                "type": "button",
                                "text": "Update",
                                "tooltip": "Update the waypoint graph weights",
                                "on_clicked_fn": self._update_weights,
                            }
                            btn_builder(**kwargs)

                            kwargs = {
                                "label": "Run cuOpt ",
                                "type": "button",
                                "text": "Solve",
                                "tooltip": "Run the cuOpt solver based on current data",
                                "on_clicked_fn": self._run_cuopt,
                            }
                            btn_builder(**kwargs)
                            self._routes_ui_message = ui.Label("Run cuOpt for solution", width=350,
                                word_wrap=True, style=ui_data_style)


    
    def _on_stage_event(self, event):
        '''
        Function for monitoring stage events
        '''
        print(f'stage event type int: {event.type}')


    def _form_cuopt_url(self):
        cuopt_ip = self._cuopt_ip.get_value_as_string()
        cuopt_port = self._cuopt_port.get_value_as_string()
        cuopt_url = f"http://{cuopt_ip}:{cuopt_port}/cuopt/"
        return cuopt_url


    # Test if cuopt microservice is up and running
    def _test_cuopt_connection(self):
        cuopt_ip = self._cuopt_ip.get_value_as_string()
        cuopt_port = self._cuopt_port.get_value_as_string()

        if (cuopt_ip == self._cuopt_ip_promt) or (cuopt_port == self._cuopt_port_promt):
            self._cuopt_status_info.text = "FAILURE: Please set both an IP and Port"
            return

        cuopt_url = self._form_cuopt_url()

        self._cuopt_status_info.text = f"working"

        try:
            cuopt_response = requests.get(cuopt_url + "health")
            if cuopt_response.status_code == 200:
                self._cuopt_status_info.text = "SUCCESS: cuOpt Microservice is Running"
            else:
                self._cuopt_status_info.text = "FAILURE: cuOpt Microservice found but not running correctly"
        
        except:
            self._cuopt_status_info.text = f"FAILURE: cuOpt Microservice was not found running at {cuopt_url}"


    def _build_warehouse_environment(self):
        print("building environment") 
          
        building_json_path = f"{self._extension_data_path}{self.warehouse_building_config}"
        shelves_json_path = f"{self._extension_data_path}{self.warehouse_shelves_config}"
        conveyors_json_path = f"{self._extension_data_path}{self.warehouse_conveyors_config}"

        self._stage = self._usd_context.get_stage()

        building_prim_path = '/World/Warehouse/Building'
        check_build_base_path(self._stage, building_prim_path, final_xform=True)

        generate_building_structure(self._stage, 
                                               building_prim_path, 
                                               building_json_path, 
                                               self._isaac_asset_path)

        
        shelves_prim_path = '/World/Warehouse/Assets/Shelves'
        check_build_base_path(self._stage, shelves_prim_path, final_xform=True)

        generate_shelves_assets(self._stage,
                                            shelves_prim_path, 
                                            shelves_json_path, 
                                            self._isaac_nvidia_asset_path)


        conveyor_prim_path = '/World/Warehouse/Assets/Conveyors'
        check_build_base_path(self._stage, conveyor_prim_path, final_xform=True)

        generate_conveyor_assets(self._stage,
                                            conveyor_prim_path, 
                                            conveyors_json_path, 
                                            self._nvidia_digital_twin_path)

        # Add outdoor lighting via hdr
        sky_light_stage_path = "/World/ExteriorHDR"

        hdr_path = self._isaac_nvidia_asset_path+"Assets/Skies/Clear/noon_grass_4k.hdr"

        omni.kit.commands.execute(
            "CreatePrim",
            prim_path=sky_light_stage_path,
            prim_type="DomeLight",
            select_new_prim=False,
            attributes={
                UsdLux.Tokens.intensity: 1000,
                UsdLux.Tokens.specular: 1,
                UsdLux.Tokens.textureFile: hdr_path,
                UsdLux.Tokens.textureFormat: UsdLux.Tokens.latlong,
                UsdGeom.Tokens.visibility: "inherited",
            },
            create_default_xform=True,
        )
        self._warehouse_ui_data.text = f"Warehouse loaded" 


    def _load_waypoint_graph(self):
        print("loading waypoint graph")
        self._stage = self._usd_context.get_stage()
        waypoint_graph_data_path = f"{self._extension_data_path}{self.waypoint_graph_config}"
        self._waypoint_graph_model = load_waypoint_graph_from_file(self._stage, 
                                                                   waypoint_graph_data_path,
                                                                   self.waypoint_graph_node_path,
                                                                   self.waypoint_graph_edge_path)
        self._network_ui_data.text = f"Waypoint Graph Network Loaded: {len(self._waypoint_graph_model.nodes)} nodes, {len(self._waypoint_graph_model.edges)} edges"                                                       
    
    
    def _load_orders(self):
        print("Loading Orders")
        orders_path = f"{self._extension_data_path}{self.orders_config}"
        self._orders_obj.load_sample(orders_path)
        self._orders_obj.show_order_locations(self._stage, self._waypoint_graph_model)
        self._orders_ui_data.text = f"Orders Loaded: {len(self._orders_obj.graph_locations)} tasks at nodes {self._orders_obj.graph_locations}"

    
    def _load_vehicles(self):
        print("Loading Vehicles")
        vehicle_data_path = f"{self._extension_data_path}{self.vehicles_config}"
        self._vehicles_obj.load_sample(vehicle_data_path)
        start_locs = [locs[0] for locs in self._vehicles_obj.graph_locations]
        self._vehicle_ui_data.text = f"Vehicles Loaded: {len(self._vehicles_obj.graph_locations)} vehicles at nodes {start_locs}"

    
    def _load_semantic_zone(self):
        semantics_json_path = f"{self._extension_data_path}{self.semantic_config}"
        semantic_prim_path = '/World/Warehouse/Semantics'
        check_build_base_path(self._stage, semantic_prim_path, final_xform=True)

        self._semantics = generate_semantic_zones(self._stage, semantic_prim_path, semantics_json_path)
        self._semantic_ui_data.text = f"Semantic Zones loaded"


    # Update the network edge weights based on semantics
    def _update_weights(self):
        print("updating weights")
        stage = self._usd_context.get_stage()
        self._waypoint_graph_model.update_weights(stage, self._semantics)


    def _run_cuopt(self):
        print("Running cuOpt")

        cuopt_url = self._form_cuopt_url()

        self._stage = self._usd_context.get_stage()

        # Solver Settings
        solver_config = {
            "time_limit": 0.01,
            "number_of_climbers": 128,
            "min_vehicles": None,
            "max_slack": None,
            "solution_scope": None,
            "max_lateness_per_route": None
            }

        # Preprocess network, fleet and task data
        waypoint_graph_data, fleet_data, task_data = preprocess_cuopt_data(self._waypoint_graph_model,
                                                                           self._orders_obj,
                                                                           self._vehicles_obj)

        cuopt_server = cuOptRunner(cuopt_url)
        
        # Initialize server data and call for solve
        cuopt_server.set_environment_data(waypoint_graph_data)
        cuopt_server.set_fleet_data(fleet_data)
        cuopt_server.set_task_data(task_data)
        cuopt_server.set_solver_config(solver_config)
        cuopt_solution = cuopt_server.solve()
        routes = cuopt_solution
    
        # Visualize the optimized routes
        NetworkSimpleViz().display_routes(self._stage, 
                                          self._waypoint_graph_model, 
                                          self.waypoint_graph_edge_path, 
                                          routes)

        
        # Display the routes on UI
        def show_vehicle_routes(routes):
            message = f"Solution found using {routes['num_vehicles']} vehicles \nSolution cost: {routes['solution_cost']} \n\n"  
            for v_id, data in routes['vehicle_data'].items():
                message = message + "For vehicle -" + str(v_id) + " route is: \n"
                path = ""
                route_ids = data["routes"]
                for index, route_id in enumerate(route_ids):
                    path += str(route_id)
                    if index != (len(route_ids) - 1):
                        path += "-> "
                message = message + path + "\n\n"
            return message
        self._routes_ui_message.text = show_vehicle_routes(routes)


    def on_shutdown(self):
        remove_menu_items(self._menu_items, "NVIDIA cuOpt")
        self._window = None
        gc.collect()
        print(f"{self._ext_id} MyExtension shutdown")
