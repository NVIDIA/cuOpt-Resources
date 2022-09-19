#!/bin/bash

# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

DIR=$(dirname $(realpath "$0"))
if [ "$API_KEY" == "" ]; then
    read -sp 'Enter a NGC api-key to access cuOpt resources: ' API_KEY
fi

TF_VAR_api_key=$API_KEY terraform apply --auto-approve
if [ "$?" -ne 0 ]; then
    exit -1
fi
terraform output --json outputs > values.json
$DIR/utilities/parse.py values.json values.sh
source values.sh

nmsg="The address of the cuOpt notebook server is $ip:30001"
amsg="The address of the cuOpt api server is $ip:30000"
case $cuopt_server_type in
  "jupyter")
     msg=$nmsg
     ;;
  "both")
     msg="$amsg\n$nmsg"
     ;;
  *)
     msg=$amsg
     ;;
esac
echo -e $msg
