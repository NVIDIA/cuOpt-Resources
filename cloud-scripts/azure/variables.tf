variable "cuopt_server_type" {
  description = "The type of cuOpt server to run (jupyter, api, or both)"
  type        = string
  default     = "api"
}

variable "instance_name" {
  description = "Name of the linux virtual machine instance"
  type        = string
  default     = "cuopt"
}

# Publisher, offer, sku, and version are used together to identify the OS image
variable "instance_image_publisher" {
  description = "The 'publisher' attribute of the OS image"
  type        = string
  default     = "Canonical"
}

variable "instance_image_offer" {
  description = "The 'offer' attribute of the OS image"
  type        = string
  default     = "0001-com-ubuntu-server-jammy"
}

variable "instance_image_sku" {
  description = "The 'sku' attribute of the OS image"
  type        = string
  default     = "22_04-lts-gen2"
}

variable "instance_image_version" {
  description = "The 'version' attribute of the OS image"
  type        = string
  default     = "latest"
}

variable "instance_root_volume_size" {
  description = "The size of the root volume in gigabytes"
  type        = number
  default     = 128 # in GB
}

variable "instance_size" {
  description = "The size (type) of Azure instance to create. Must be an NC series size"
  type        = string
  default     = "Standard_NC6s_v2"
}

variable "network_address_space" {
  description = "A list of cidr values to define the address space in the resource group"
  type        = list
  default     = ["10.0.0.0/24"]
}

variable "subnet_address_prefixes" {
  description = "A list of cidr values to define the available address prefixes for the subnet"
  type        = list
  default     = ["10.0.0.0/29"]
}

variable "ssh_port_access" {
  description = "Access mode for ssh rule.  Allow or Deny. Applies to source and destination addresses"
  type = string
  default = "Allow"
}

variable "ssh_source_port_range" {
  description = "The source port range for ssh (port 22) connections to the instance"
  type = string
  default = "*"
}

variable "ssh_source_address_prefixes" {
  description = "The source address prefix for ssh (port 22) connections to the instance"
  type = list
  default = ["0.0.0.0/0"]
}

variable "ssh_destination_address_prefix" {
  description = "The destination address prefix for ssh (port 22) connections to the instance"
  type = string
  default = "*"
}

variable "cuopt_port_access" {
  description = "Access mode for cuopt rule.  Allow or Deny. Applies to source and destination addresses"
  type = string
  default = "Allow"
}

variable "cuopt_source_port_range" {
  description = "The source port range for cuopt server (ports 30000,30001) connections to the instance"
  type = string
  default = "*"
}

variable "cuopt_source_address_prefixes" {
  description = "The source address prefix for cuopt server (ports 30000,30001) connections to the instance"
  type = list
  default = ["0.0.0.0/0"]
}

variable "cuopt_destination_address_prefix" {
  description = "The destination address prefix for cuopt server (ports 30000,30001) connections to the instance"
  type = string
  default = "*"
}

variable "user" {
  description = "The default user account for the instance"
  type        = string
  default     = "azureuser"
}

variable "public_key_path" {
  description = "The path of the public key file to use for ssh"
  type        = string
}

variable "private_key_path" {
  description = "The path of the private key file to use for ssh"
  type        = string
}

variable "api_key" {
  description = "The NGC api-key for accessing cuOpt resources. Recommended to set this via an environment variable."
  type        = string
  sensitive   = true
}
variable "resource_group_location" {
  description = "Location of the resource group."
  type        = string
  default     = "eastus"
}

variable "resource_group_prefix" {
  description = "Resource group prefix which will be combined with a random id."
  type        = string
  default     = "cuopt"
}
