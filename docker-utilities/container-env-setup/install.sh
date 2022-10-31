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

rel=$(lsb_release -rs)
case $rel in
    22.04|20.04|18.04)
        ;;
    *)
        echo "This script is for Ubuntu 18.04, 20.04 or 22.04"
        exit 0
        ;;
esac

# Instructions for installing docker and nvidia-container-toolkit are based on 
# "Installing Docker and The Docker Utility Engine for NVIDIA GPUs — NVIDIA AI Enterprise documentation"
# https://docs.nvidia.com/ai-enterprise/deployment-guide/dg-docker.html

# Add docker repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Add nvidia-container-toolkit repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update

# Add docker and nvidia-container-toolkit and their dependencies, and dependencies for cuda toolkit install
sudo apt install -y gcc make docker-ce docker-ce-cli containerd.io apt-transport-https ca-certificates curl gnupg-agent software-properties-common nvidia-container-toolkit
sudo systemctl restart docker
sudo usermod -aG docker $USER

# Install nvidia driver via cuda toolkit runfile
wget https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_515.65.01_linux.run
sudo sh cuda_11.7.1_515.65.01_linux.run --driver --silent

echo "##############################################################"
echo
echo "Log out, then log back in again for all changes to take effect."
echo
echo "##############################################################"

