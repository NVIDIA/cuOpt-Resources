#!/bin/bash

# SPDX-FileCopyrightText: Copyright (c) 2022-2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

# Call these out so we can reference them easily
SERVER_DEFAULT=30000
NOTEBOOK_DEFAULT=30001
CHART_DEFAULT="cuopt-22.12.0.tgz"

CUOPT_CHART=${CUOPT_CHART:-"$CHART_DEFAULT"}
NAMESPACE=${NAMESPACE:-cuopt-server}
NODE_PORT_SERVER=${NODE_PORT_SERVER:-"$SERVER_DEFAULT"}
NODE_PORT_NOTEBOOK=${NODE_PORT_NOTEBOOK:-"$NOTEBOOK_DEFAULT"}
SERVER_TYPE=${SERVER_TYPE:-"api"}

function help {
    echo "Convenience script for running the cuopt helm chart"
    echo
    echo "usage: cuopt-helm.sh [-h] [-n NAMESPACE] [-s NODE_PORT_SERVER]] [-j NODE_PORT_NOTEBOOK]] [-t SERVER_TYPE] [-c CUOPT_CHART]"
    echo
    echo "options:"
    echo "  -n NAMESPACE          Deploy the helm chart in the specified namespace (default is cuopt-server)"
    echo "  -s NODE_PORT_SERVER   The nodeport to use for the cuopt API server if deployed (default 30000)"
    echo "  -j NODE_PORT_NOTEBOOK The nodeport to use for the cuopt Jupyter server if deployed (default 30001)"
    echo "  -t SERVER_TYPE        The type of server to deploy, may be 'api', 'jupyter', or 'both' (default api)"
    echo "  -c CUOPT_CHART        The cuopt helm chart to use (default $CHART_DEFAULT)"
}

while getopts "hn:s:j:t:c:" option; do
   case $option in
      h) # display Help
         help
         exit;;
      n)
         NAMESPACE=$OPTARG;;
      s)
         NODE_PORT_SERVER=$OPTARG;;
      j)
         NODE_PORT_NOTEBOOK=$OPTARG;;
      t)
         SERVER_TYPE=$OPTARG;;
      c)
	 CUOPT_CHART=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

echo "Chart is: $CUOPT_CHART"
echo "Namespace is: $NAMESPACE"
echo "Server type is: $SERVER_TYPE"
echo "API server port: $NODE_PORT_SERVER"
echo "Jupyter server port: $NODE_PORT_NOTEBOOK"

kubectl create namespace $NAMESPACE

if [ ! -d "$CUOPT_CHART" ]; then
    helm fetch https://helm.ngc.nvidia.com/nvstaging/cuopt/charts/$CUOPT_CHART --username='$oauthtoken' --password=$API_KEY --untar
fi

# Always set the port for each service, even if the service is not enabled.
# In a future version of the chart, this will not be necessary if the
# service is not enabled.
server_str="--set node_port_server=$NODE_PORT_SERVER"
notebook_str="--set node_port_notebook=$NODE_PORT_NOTEBOOK"

case $SERVER_TYPE in
  "jupyter")
    helm install --namespace $NAMESPACE --set ngc.apiKey=$API_KEY --set enable_nodeport=true $server_str $notebook_str nvidia-cuopt-chart cuopt --values cuopt/values_notebook.yaml
    ;;

  "both")
    helm install --namespace $NAMESPACE --set ngc.apiKey=$API_KEY --set enable_nodeport=true --set enable_notebook_server=true $server_str $notebook_str nvidia-cuopt-chart cuopt --values cuopt/values.yaml
    ;;

  # default to api server in all other cases
  *)
    helm install --namespace $NAMESPACE --set ngc.apiKey=$API_KEY --set enable_nodeport=true $server_str $notebook_str nvidia-cuopt-chart cuopt --values cuopt/values.yaml
    ;;
esac
