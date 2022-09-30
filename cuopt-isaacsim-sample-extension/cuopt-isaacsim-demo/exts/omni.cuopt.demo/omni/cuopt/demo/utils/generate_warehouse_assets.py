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

from ..utils.common import read_json, translate_rotate_scale_prim


def generate_shelves_assets(stage, shelves_prim_path, shelves_json_path, shelves_asset_path):
    shelves_data = read_json(shelves_json_path)

    for shelf_id, shelf_details in shelves_data.items():

        shelf_stage_path =f'{shelves_prim_path}/{shelf_id}'

        shelf_asset_path = shelves_asset_path + shelf_details["asset_path_extension"]

        shelf_prim = stage.DefinePrim(shelf_stage_path, "Xform")
        shelf_prim.GetReferences().AddReference(shelf_asset_path)
        
        translate_rotate_scale_prim(stage=stage, 
                                    prim=shelf_prim,
                                    translate_set=shelf_details["translation"], 
                                    scale_set= shelf_details["scale"])


def generate_conveyor_assets(stage, conveyor_prim_path, conveyor_json_path, conveyor_asset_path):
    conveyors_data = read_json(conveyor_json_path)

    for conveyor_id, conveyor_details in conveyors_data.items():

        shelf_stage_path =f'{conveyor_prim_path}/{conveyor_id}'

        shelf_asset_path = conveyor_asset_path + conveyor_details["asset_path_extension"]

        shelf_prim = stage.DefinePrim(shelf_stage_path, "Xform")
        shelf_prim.GetReferences().AddReference(shelf_asset_path)
        
        translate_rotate_scale_prim(stage=stage, 
                                    prim=shelf_prim,
                                    translate_set=conveyor_details["translation"], 
                                    rotate_set=conveyor_details["rotate"],
                                    scale_set=conveyor_details["scale"])
