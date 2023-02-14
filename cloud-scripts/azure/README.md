# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

# AZURE
A collection of scripts and resources to spin-up Azure cuOpt instances

## Resource groups

All of the Azure infrastructure for the cuOpt server is created in
a resource group with the prefix "cuopt".  This resource group
is displayed in the output from the Terraform script.

The Azure script creates a new VPC in the resoure group.

The Azure resource group location may be changed in *terraform.tfvars* (default eastus)
```bash
resource_group_location = "westus"
```

## Setting the user

The admin user on the instance can be changed in *terraform.tfvars* (default azureuser)
```bash
user = cuopt-user
```

## Setting the OS image

If you would like to set the OS image, look at the following variables in *variables.tf* and then override
their defaults in *terraform.tfvars*.

* instance_image_publisher
* instance_image_offer
* instance_image_sku
* instance_image_version

## Setting the root volume size

The root volume size may be set in *terraform.tfvars* (default is 128)
```bash
instance_root_volume_size = 64
```

## Setting the instance size

The instance size may be set in *terraform.tfvars* (default is Standard_NC6s_v2)
```bash
instance_size = "Standard_NC12s_v2"
```

## Setting the network and subnet address blocks

The network and subnet address blocks of the VPC can be set in *terraform.tfvars* using the following
variables. The value for each of these variables is a list of CIDR blocks. See *variables.tf* for defaults.

* network_address_space
* subnet_address_prefixes

