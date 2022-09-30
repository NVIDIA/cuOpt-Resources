from pxr import Gf, UsdGeom, Usd
from omni.isaac.core.utils.bounds import create_bbox_cache
import omni.ext
import math
import json


def read_json(json_file_path):

    with open(json_file_path) as json_file:
        json_data = json.load(json_file)

    return json_data


def translate_rotate_scale_prim(stage, 
                                prim=None, 
                                prim_path=None, 
                                translate_set=None, 
                                rotate_set=None, 
                                scale_set=None,
                                clear_orient=False):
    if prim is not None:
        xform = UsdGeom.Xformable(prim)
        prim_path = prim.GetPrimPath()
    elif prim_path is not None:
        prim = stage.GetPrimAtPath(prim_path)
        xform = UsdGeom.Xformable(prim)
    else:
        return "Need prim or prim path to manipulate"

    xform_ops = {op.GetBaseName(): op for op in xform.GetOrderedXformOps()}
    # note here
    if "translate" in xform_ops:
        translate = xform_ops["translate"]
    else:
            translate = xform.AddTranslateOp()

    if "rotateXYZ" in xform_ops:
        rotate = xform_ops["rotateXYZ"]
    else:
        rotate = xform.AddRotateXYZOp()

    if "scale" in xform_ops:
        scale = xform_ops["scale"]
    else:
        scale = xform.AddScaleOp()

    # Option to remove orient in favor of rotate
    if ("orient" in xform_ops) and clear_orient:
        omni.kit.commands.execute(
                "RemoveXformOp",
                op_order_attr_path=f"{prim_path}.xformOpOrder",
                op_name="xformOp:orient",
                op_order_index=1,
            )


    if translate_set is not None:
        translate.Set(Gf.Vec3d(translate_set))
    if rotate_set is not None:
        rotate.Set(Gf.Vec3d(rotate_set))
    if scale_set is not None:
        scale.Set(Gf.Vec3d(scale_set))


def check_build_base_path(stage, semantic_path, final_xform=True):
    path_components = semantic_path.split("/")
    check_path = ""

    for path_comp in path_components[1:-1]:
        check_path += f'/{path_comp}'
        if not stage.GetPrimAtPath(check_path).IsValid():
            stage.DefinePrim(check_path, "Xform")

    final_base_prim = f"{check_path}/{path_components[-1]}"

    if not stage.GetPrimAtPath(final_base_prim).IsValid():
            
            if final_xform:
                stage.DefinePrim(final_base_prim, "Xform")
            else:
                stage.DefinePrim(final_base_prim)


def get_prim_translation(prim):
        prim_tf = UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
        transform = Gf.Transform()
        transform.SetMatrix(prim_tf)
        prim_translation = transform.GetTranslation()
        return prim_translation


# Check if given edge is within Volume. Return the overlap percentage
def edge_in_volume(edge_prim, vol_prim):
        bbox_cache = create_bbox_cache()
        total_bounds = Gf.BBox3d(bbox_cache.ComputeWorldBound(vol_prim).ComputeAlignedRange())
        prim_tf = UsdGeom.Xformable(edge_prim).ComputeLocalToWorldTransform(Usd.TimeCode())
        p1 = prim_tf.Transform(Gf.Vec3d(0, 0, -1))
        p2 = prim_tf.Transform(Gf.Vec3d(0, 0, 1))
        myray = Gf.Ray().SetEnds(p1, p2)
        intersects, d1, d2 = myray.Intersect(total_bounds)
        i1 = myray.GetPoint(d1)
        i2 = myray.GetPoint(d2)
        if not intersects:
            return False, 0.0
        if 0<=d1<=1 and 0<=d2<=1:
            s1 = i1;  s2 = i2
        elif 0<=d1<=1: 
            s1 = i1; s2 = p2
        elif 0<=d2<=1:
            s1 = p1; s2 = i2
        else:
            return False, 0.0
        line_len = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
        seg_len = math.sqrt((s2[0]-s1[0])**2 + (s2[1]-s1[1])**2 + (s2[2]-s1[2])**2)
        return True, seg_len/line_len
