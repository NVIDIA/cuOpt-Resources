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


 variable "cuopt_server_type" {
   description = "The type of cuOpt server to run (jupyter, api, or both)"
   type        = string
   default     = "api"
}

variable "prefix_name" {
  description = "Prefix to append with random string for generating resource names (including instance name)"
  type        = string
  default     = "cuopt"
}

variable "gcp_region" {
  type        = string
  description = "The GCP zone to use"
  default     = "us-east1"
}

variable "gcp_zone" {
  type        = string
  description = "The GCP zone to use (appended to the region value)"
  default     = "c"
}

variable "gcp_project" {
  description = "The GCP project to use within your account"
  type        = string
}

variable "instance_machine_type" {
  description = "The machine type for the GCP instance"
  type        = string
  default     = "n1-standard-4"
}

variable "instance_os_image" {
  description = "The OS image to use for the GCP instance"
  type        = string
  default     = "ubuntu-2204-lts"
}

variable "root_volume_size" {
  description = "The size of the root volume in GB"
  type        = number
  default     = 128
}

variable "gpu_type" {
  description = "The type of the GPU in the instance"
  type        = string
  default     = "nvidia-tesla-t4"
}

variable "additional_ports" {
  description = "Additional ports to open on the instance. Defaulted to ssh (port 22)"
  type        = list
  default     = ["22"]
}

variable "additional_ports_source_ranges" {
  description = "The CIDR blocks identifying the allowed sources for connection to additional ports on the instance"
  type = list
  default = ["0.0.0.0/0"]
}

variable "cuopt_ports" {
  description = "The cuopt server ports to open on the instance"
  type        = list
  default     = ["30000", "30001"]
}

variable "cuopt_ports_source_ranges" {
  description = "The CIDR blocks identifying the allowed sources for connection to the cuopt ports on the instance"
  type = list
  default = ["0.0.0.0/0"]
}

variable "user" {
  type         = string
  description  = "A user with sudo privileges for Terraform to use to configure the instance"
}

variable "public_key_path" {
  description = "The path of the public key file to use for ssh, added to specified user"
  type        = string
}

variable "private_key_path" {
  description = "The path of the private key file to use for ssh, added to specified user"
  type        = string
}

variable "api_key" {
  description = "The NGC api-key for accessing cuOpt resources. Recommended to set this via an environment variable."
  type        = string
  sensitive   = true
}
