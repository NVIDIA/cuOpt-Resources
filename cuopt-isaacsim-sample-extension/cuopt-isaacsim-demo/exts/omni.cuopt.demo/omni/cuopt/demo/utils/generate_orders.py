from pxr import Gf, Sdf, UsdShade, UsdGeom
from omni.kit.material.library import CreateAndBindMdlMaterialFromLibrary
from .common import translate_rotate_scale_prim
import json


class TransportOrders():


    def __init__(self):
        self.order_xyz_locations = None
        self.graph_locations = None
        self.order_demand = None
        self.order_time_windows = None
        self.order_service_times = None

        self.order_waypoint_material = None
        self.order_node_scale = [0.6,0.6,0.15]
        self.order_waypoint_color = [0.05,0.5,0.1]
        self.order_waypoint_intensity = 5000.0


    # Load Task info from json data
    def load_sample(self, orders_json):

        with open(orders_json) as orders_file:
            orders_data = json.load(orders_file)

        self.order_xyz_locations = orders_data["task_locations"]
        self.order_demand = orders_data["demand"]

        if "task_time_windows" in orders_data:
            self.order_time_windows = orders_data["task_time_windows"]
            self.order_service_times = orders_data["service_times"]

    
    # Assign Material to Waypoints representing order locations
    def add_order_waypoint_material(self, stage):
        order_waypoint_material_name = "order_material"
        CreateAndBindMdlMaterialFromLibrary(
                mdl_name="OmniPBR.mdl", 
                mtl_name="OmniPBR", 
                bind_selected_prims=False,
                prim_name=order_waypoint_material_name).do()
            
        order_waypoint_material_path = f"/World/Looks/{order_waypoint_material_name}"
        self.order_waypoint_material = UsdShade.Material(stage.GetPrimAtPath(order_waypoint_material_path))
        waypoint_shader = UsdShade.Shader(stage.GetPrimAtPath(f"{order_waypoint_material_path}/Shader"))
        waypoint_shader.CreateInput("enable_emission", Sdf.ValueTypeNames.Bool).Set(True)
        waypoint_shader.CreateInput("emissive_color", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(self.order_waypoint_color))
        waypoint_shader.CreateInput("emissive_intensity", Sdf.ValueTypeNames.Float).Set(self.order_waypoint_intensity)
        

    # Visualize order locations in loaded task data
    def show_order_locations(self, stage, waypoint_graph_model):

        # Material
        order_waypoint_material_name = "order_waypoint_material"
        order_waypoint_material_path = f"/World/Looks/{order_waypoint_material_name}"
        
        if not stage.GetPrimAtPath(order_waypoint_material_path).IsValid():
            self.add_order_waypoint_material(stage)
        elif self.order_waypoint_material is None:
            self.order_waypoint_material = UsdShade.Material(stage.GetPrimAtPath(order_waypoint_material_path))

        order_inds = []

        for xyz_loc in self.order_xyz_locations:
            closest_waypoint_path = \
                waypoint_graph_model.get_closest_node(stage, Gf.Vec3d(xyz_loc[0], xyz_loc[1], xyz_loc[2]))

            closest_node_prim = stage.GetPrimAtPath(closest_waypoint_path)
            
            order_inds.append(waypoint_graph_model.path_node_map[closest_waypoint_path])

            translate_rotate_scale_prim(stage=stage, prim=closest_node_prim, scale_set=self.order_node_scale)
            
            UsdShade.MaterialBindingAPI(closest_node_prim).Bind(self.order_waypoint_material)
        
        self.graph_locations = order_inds

        print(f"Orders have been assinged to the following nodes {self.graph_locations}")
