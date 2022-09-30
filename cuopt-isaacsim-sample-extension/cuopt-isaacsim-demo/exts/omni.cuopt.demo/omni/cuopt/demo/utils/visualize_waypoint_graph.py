from pxr import UsdShade, UsdGeom, Gf, Sdf
from omni.kit.material.library import CreateAndBindMdlMaterialFromLibrary
from .common import translate_rotate_scale_prim


class NetworkSimpleViz:
    def __init__(self):
        self.node_scale = [0.4,0.4,0.15]
        self.waypoint_height = 0.15
        self.node_refinement_level = 2
        self.waypoint_color = [1, 1, 1]
        self.waypoint_intensity = 5000.0
        self.waypoint_material = None
        self.edge_radius = 0.2

        self.routes_color = [
                             [0.0, 0.00363, 0.07173],
                             [0.06329, 0.01282, 0.0], 
                             [0.008438826, 0.0016023085, 0.008179213],
                             [0.008438826, 0.0016023085, 0.0016023085],   
                             [0.0016023085, 0.008438826, 0.007833057],
                             [0.0017753834, 0.0016023085, 0.008438826],  
                             [0.10548526, 0.061421696, 0],
                             [0.0, 0.0, 0.0]
                            ]

    
    # Assign Material to Waypoints
    def add_waypoint_material(self, stage):
        waypoint_material_name = "waypoint_material"
        CreateAndBindMdlMaterialFromLibrary(
                mdl_name="OmniPBR.mdl", 
                mtl_name="OmniPBR", 
                bind_selected_prims=False,
                prim_name=waypoint_material_name).do()
            
        waypoint_material_path = f"/World/Looks/{waypoint_material_name}"
        self.waypoint_material = UsdShade.Material(stage.GetPrimAtPath(waypoint_material_path))
        waypoint_shader = UsdShade.Shader(stage.GetPrimAtPath(f"{waypoint_material_path}/Shader"))
        waypoint_shader.CreateInput("enable_emission", Sdf.ValueTypeNames.Bool).Set(True)
        waypoint_shader.CreateInput("emissive_color", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(self.waypoint_color))
        waypoint_shader.CreateInput("emissive_intensity", Sdf.ValueTypeNames.Float).Set(self.waypoint_intensity)


    # Visualize nodes in the Waypoint Graph network
    def add_node_to_scene(self, stage, node_prim_path, translation):
        node_prim_geom = UsdGeom.Sphere.Define(stage, node_prim_path)

        if self.waypoint_height is not None:
            translation[2] = self.waypoint_height

        translate_rotate_scale_prim(stage=stage, 
                                    prim_path=node_prim_path, 
                                    translate_set=translation, 
                                    scale_set=self.node_scale)

        
        node_prim_geom.GetPrim().CreateAttribute("refinementEnableOverride", Sdf.ValueTypeNames.Bool).Set(True)
        node_prim_geom.GetPrim().CreateAttribute("refinementLevel", Sdf.ValueTypeNames.Int).Set(self.node_refinement_level)
        
        semantic_prim = stage.GetPrimAtPath(node_prim_path)

        # Material
        waypoint_material_name = "waypoint_material"
        waypoint_material_path = f"/World/Looks/{waypoint_material_name}"
        
        if not stage.GetPrimAtPath(waypoint_material_path).IsValid():
            self.add_waypoint_material(stage)
        elif self.waypoint_material is None:
            self.waypoint_material = UsdShade.Material(stage.GetPrimAtPath(waypoint_material_path))

        UsdShade.MaterialBindingAPI(semantic_prim).Bind(self.waypoint_material)


    # Visualize edges in the Waypoint Graph network
    def add_edge_to_scene(self, stage, edge_prim_path, point_from, point_to):
        edge_prim_geom = UsdGeom.Cylinder.Define(stage, edge_prim_path)
        
        edge_vector = point_to-point_from
        edge_prim = edge_prim_geom.GetPrim()
        xf = UsdGeom.Xformable(edge_prim_geom)
        xf.ClearXformOpOrder () 
        xf.AddTranslateOp().Set(point_from + edge_vector*0.5)
        n = edge_vector.GetNormalized()
        r = Gf.Rotation(Gf.Vec3d(0,0,1), Gf.Vec3d(n[0],n[1],n[2]))
        xf.AddOrientOp(UsdGeom.XformOp.PrecisionDouble).Set(r.GetQuat())
        xf.AddScaleOp().Set(Gf.Vec3d(self.edge_radius/3, self.edge_radius/3, edge_vector.GetLength()/2))
        edge_prim.CreateAttribute("baseweight", Sdf.ValueTypeNames.Float).Set(edge_vector.GetLength())
        edge_prim.CreateAttribute("weight", Sdf.ValueTypeNames.Float).Set(edge_vector.GetLength())
        UsdShade.MaterialBindingAPI(edge_prim).Bind(self.waypoint_material)

        return edge_prim.GetAttribute("weight").Get()


    # Assign Material to routes and edges
    def get_route_material(self, stage, i):
        route_material_name = "route_material_"+str(i)
        CreateAndBindMdlMaterialFromLibrary(
                mdl_name="OmniPBR.mdl", 
                mtl_name="OmniPBR", 
                bind_selected_prims=False,
                prim_name=route_material_name).do()
            
        route_material_path = f"/World/Looks/{route_material_name}"
        route_material = UsdShade.Material(stage.GetPrimAtPath(route_material_path))
        route_shader = UsdShade.Shader(stage.GetPrimAtPath(f"{route_material_path}/Shader"))
        route_shader.CreateInput("enable_emission", Sdf.ValueTypeNames.Bool).Set(True)
        route_shader.CreateInput("emissive_color", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(self.routes_color[i]))
        route_shader.CreateInput("emissive_intensity", Sdf.ValueTypeNames.Float).Set(100000)
        return route_material


    # Visualize optimized routes
    def display_routes(self, stage, graph, waypoint_graph_edge_path, routes):

        all_edges = graph.path_edge_map.keys()
        for i, edge_path in enumerate(all_edges):
            edge_prim = stage.GetPrimAtPath(edge_path)
            # Material
            waypoint_material_name = "waypoint_material"
            waypoint_material_path = f"/World/Looks/{waypoint_material_name}"
            
            if not stage.GetPrimAtPath(waypoint_material_path).IsValid():
                self.add_waypoint_material(stage)
            elif self.waypoint_material is None:
                self.waypoint_material = UsdShade.Material(stage.GetPrimAtPath(waypoint_material_path))
            UsdShade.MaterialBindingAPI(edge_prim).Bind(self.waypoint_material)
        
        vehicle_data = routes["vehicle_data"]
        for i, v_id in enumerate(vehicle_data.keys()):
            route_material = self.get_route_material(stage, i)
            v_routes = vehicle_data[v_id]["routes"]
            for j in range(0, len(v_routes)-1):
                edge_prim_path = f'{waypoint_graph_edge_path}/Edge_{v_routes[j]}_{v_routes[j+1]}'
                edge_prim = stage.GetPrimAtPath(edge_prim_path)
                
                UsdShade.MaterialBindingAPI(edge_prim).Bind(route_material)
                edge_prim_path_bi = f'{waypoint_graph_edge_path}/Edge_{v_routes[j+1]}_{v_routes[j]}'
                edge_prim_bi = stage.GetPrimAtPath(edge_prim_path_bi)
                if edge_prim_bi.IsValid():
                    UsdShade.MaterialBindingAPI(edge_prim_bi).Bind(route_material)
