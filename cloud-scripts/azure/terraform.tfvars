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

# The following variables are required for Azure and have no defaults

private_key_path = "~/.ssh/id_rsa"
public_key_path = "~/.ssh/id_rsa.pub"

# Optional settings

# List of CIDR blocks and/or IP addresses to allow to connect to the ssh port
# If building the cuOpt server from a cloud shell, the public IP address of the cloud shell must be included here
#ssh_source_address_prefixes = ["0.0.0.0/0"]

# List of CIDR blocks and/or IP addresses to allow to connect to the cuOpt server  ports
# More info at https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_rule
#cuopt_source_address_prefixes = ["0.0.0.0/0"]
