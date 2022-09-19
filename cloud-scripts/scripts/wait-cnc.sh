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
