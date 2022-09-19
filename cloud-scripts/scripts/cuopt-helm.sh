#!/bin/bash
NAMESPACE=cuopt-server
kubectl create namespace $NAMESPACE

helm fetch https://helm.ngc.nvidia.com/nvstaging/cuopt/charts/cuopt-22.08.0.tgz --username='$oauthtoken' --password=$API_KEY --untar
# temporary
sed -i 's,nvcr.io/nvidia,nvcr.io/nvstaging,g' cuopt/values*.yaml

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
