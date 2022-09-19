#!/bin/bash
#!/bin/bash

echo Waiting for operator validator to start ...
i=0
while true
do
    pods=$(kubectl get -n nvidia-gpu-operator pod --selector app=nvidia-operator-validator)
    i=$((i+1))
    if [ -n "$pods" ] || [ "$i" -eq 15 ]; then
	break
    fi
    sleep 60
done
kubectl -n nvidia-gpu-operator wait pod --for=jsonpath='{.status.phase}'=Running --selector app=nvidia-operator-validator --timeout 1800s

echo Waiting for device plugin validator to complete ...
i=0
while true
do
    pods=$(kubectl get -n nvidia-gpu-operator pod --selector app=nvidia-device-plugin-validator)
    i=$((i+1))
    if [ -n "$pods" ] || [ "$i" -eq 15 ]; then
	break
    fi
    sleep 60
done
kubectl -n nvidia-gpu-operator wait pod --for=jsonpath='{.status.phase}'=Succeeded --selector app=nvidia-device-plugin-validator --timeout 1800s
