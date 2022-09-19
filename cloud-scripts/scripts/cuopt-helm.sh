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

NAMESPACE=cuopt-server
kubectl create namespace $NAMESPACE

helm fetch https://helm.ngc.nvidia.com/nvidia/cuopt/charts/cuopt-22.08.0.tgz --username='$oauthtoken' --password=$API_KEY --untar

case $SERVER_TYPE in
  "jupyter")
    helm install --namespace $NAMESPACE --set ngc.apiKey=$API_KEY --set enable_nodeport=true nvidia-cuopt-chart cuopt --values cuopt/values_notebook.yaml
    ;;

  "both")
    helm install --namespace $NAMESPACE --set ngc.apiKey=$API_KEY --set enable_nodeport=true --set enable_notebook_server=true nvidia-cuopt-chart cuopt --values cuopt/values.yaml
    ;;

  # default to api server in all other cases
  *)
    helm install --namespace $NAMESPACE --set ngc.apiKey=$API_KEY --set enable_nodeport=true nvidia-cuopt-chart cuopt --values cuopt/values.yaml
    ;;
esac
