#!/bin/bash
NAMESPACE=cuopt-server
helm list -n $NAMESPACE
echo Waiting for cuOpt pod to be created ...
i=0
while true
do
    pods=$(kubectl get -n $NAMESPACE pod --selector app.kubernetes.io/name=cuopt)
    if [ -n "$pods" ]; then
	break
    fi
    i=$((i+1))
    if [ "$i" -eq 6 ]; then
        echo cuOpt pod not created in five minutes, exiting
        exit -1
    fi
    sleep 60
done
echo Waiting for cuOpt pod to be 'Running' ...
kubectl -n $NAMESPACE wait pod --for=jsonpath='{.status.phase}'=Running --selector app.kubernetes.io/name=cuopt --timeout=1800s
