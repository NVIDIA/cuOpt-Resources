from pxr import Gf, UsdGeom, Sdf, UsdShade
from omni.kit.material.library import CreateAndBindMdlMaterialFromLibrary

from .common import read_json, translate_rotate_scale_prim

def generate_semantic_zones(stage, semantic_prim_path, semantics_json_path):
    semantics_data = read_json(semantics_json_path)
    semantics = []
    for sematic_id, semantic_details in semantics_data.items():

        semantic_stage_path =f'{semantic_prim_path}/{sematic_id}'
        semantics.append(semantic_stage_path)

        corner1_x = semantic_details["min_extent"][0]
        corner1_y = semantic_details["min_extent"][1]
        corner1_z = semantic_details["min_extent"][2]
        corner2_x = semantic_details["max_extent"][0]
        corner2_y = semantic_details["max_extent"][1]
        corner2_z = semantic_details["max_extent"][2]

        x_size = abs(corner2_x - corner1_x)
        y_size = abs(corner2_y - corner1_y)
        z_size = abs(corner2_z - corner1_z)

        x_scale = x_size/2
        y_scale = y_size/2
        z_scale = z_size/2

        scale_vect = [x_scale, y_scale, z_scale]

        add_shift_x = x_scale/2
        add_shift_y = y_scale/2
        add_shift_z = z_scale

        translation_vect = [corner1_x + add_shift_x, corner1_y + add_shift_y, corner1_z + add_shift_z]

        UsdGeom.Cube.Define(stage, semantic_stage_path)

        translate_rotate_scale_prim(stage=stage, 
                                    prim_path=semantic_stage_path,
                                    translate_set=translation_vect,
                                    scale_set=scale_vect)

        semantic_prim = stage.GetPrimAtPath(semantic_stage_path)
            

        UsdGeom.PrimvarsAPI(semantic_prim).CreatePrimvar("doNotCastShadows", Sdf.ValueTypeNames.Bool).Set(True)

        CreateAndBindMdlMaterialFromLibrary(
            mdl_name="OmniGlass.mdl", 
            mtl_name="OmniGlass", 
            bind_selected_prims=False,
            prim_name=semantic_details["type"]).do()
        
        material_path = f"/World/Looks/{semantic_details['type']}"
        material = UsdShade.Material(stage.GetPrimAtPath(material_path))
        shader = UsdShade.Shader(stage.GetPrimAtPath(f"{material_path}/Shader"))
        shader.CreateInput("glass_color", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f([
                                                                            semantic_details['color'][0], 
                                                                            semantic_details['color'][1], 
                                                                            semantic_details['color'][2]]))
        shader.CreateInput("thin_walled", Sdf.ValueTypeNames.Bool).Set(True)
        shader.CreateInput("glass_ior", Sdf.ValueTypeNames.Float).Set(1.0)


        UsdShade.MaterialBindingAPI(semantic_prim).Bind(material)

        
        semantic_prim.CreateAttribute("mfgstd:schema", Sdf.ValueTypeNames.String).Set("SemanticRegion#1.0.0")
        semantic_prim.CreateAttribute("mfgstd:properties:name", Sdf.ValueTypeNames.String).Set(sematic_id)
        semantic_prim.CreateAttribute("mfgstd:properties:semantic_type", Sdf.ValueTypeNames.String).Set(semantic_details["type"])
        semantic_prim.CreateAttribute("mfgstd:properties:semantic_weight", Sdf.ValueTypeNames.Float).Set(semantic_details["weight"])

    return semantics
