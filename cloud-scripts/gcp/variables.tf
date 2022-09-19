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
