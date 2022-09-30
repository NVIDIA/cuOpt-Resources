from pxr import Gf, UsdGeom, UsdLux
import omni.ext

from .common import read_json, translate_rotate_scale_prim


def generate_building_structure(stage, building_prim_path, building_json_path, building_asset_path):
    building_data = read_json(building_json_path)

    building_semantics = {}

    build_direction = building_data.pop("build_direction")

    shift = [0.0, 0.0, 0.0]
    for building_segment in building_data.keys():
        segment_stage_path =f'{building_prim_path}/{building_segment}'

        segment_asset_path = building_asset_path + \
                                        building_data[building_segment]["asset_path_extension"]

        building_segment_prim = stage.DefinePrim(segment_stage_path, "Xform")
        building_segment_prim.GetReferences().AddReference(segment_asset_path)
        
        segment_rot = [0,0,0]

        translate_rotate_scale_prim(stage, 
                                    prim=building_segment_prim, 
                                    translate_set=shift, 
                                    rotate_set=segment_rot, 
                                    scale_set=None)

        if "lights" in building_data[building_segment]:

            lights_parent_path = segment_stage_path + "/Lights"

            stage.DefinePrim(lights_parent_path, "Xform")

            segment_lights = building_data[building_segment]["lights"]

            for light_num, light in enumerate(segment_lights):

                light_path = f"{lights_parent_path}/Light_{light_num}"
                light_intensity = light["intensity"]
                light_color = Gf.Vec3f(tuple(light["color"]))

                omni.kit.commands.execute(
                    "CreatePrim",
                    prim_path=light_path,
                    prim_type="DiskLight",
                    select_new_prim=False,
                    attributes={
                        UsdLux.Tokens.intensity: light_intensity,
                        UsdLux.Tokens.color: light_color,
                        UsdLux.Tokens.specular: 1,
                        UsdLux.Tokens.diffuse: 10,
                        UsdGeom.Tokens.visibility: "inherited"
                        },
                    create_default_xform=True
                )

                translate_rotate_scale_prim(stage, 
                                    prim_path=light_path, 
                                    translate_set=light["position"], 
                                    rotate_set=None, 
                                    scale_set=light["scale"],
                                    clear_orient=True)

        shift[build_direction] += building_data[building_segment]["extent_max"][build_direction]

    return building_semantics
