#!/bin/bash
NAMESPACE=cuopt-server
kubectl delete secret nvidia-registrykey-secret -n $NAMESPACE
