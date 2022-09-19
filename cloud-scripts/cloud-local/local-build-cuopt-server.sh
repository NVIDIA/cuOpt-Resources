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


if [ "$API_KEY" == "" ]; then
    read -sp 'Enter a NGC api-key to access cuOpt resources: ' API_KEY
    echo
fi
SERVER_TYPE="${SERVER_TYPE:-api}"
DIR=$(dirname $(dirname $(realpath "$0")))/scripts

mkdir logs
$DIR/install-cnc.sh 2>&1 | tee logs/install-cnc.log
$DIR/wait-cnc.sh 2>&1 | tee logs/wait-cnc.log
API_KEY=$API_KEY SERVER_TYPE=$SERVER_TYPE $DIR/cuopt-helm.sh 2>&1 | tee logs/cuopt-helm.log
$DIR/wait-cuopt.sh 2>&1 | tee logs/wait-cuopt.log
$DIR/delete-secret.sh 2>&1 | tee logs/delete-secret.log

ip=localhost
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
echo -e $msg 2>&1 | tee local-build-cuopt-server.log
