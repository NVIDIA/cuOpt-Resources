# The following variables are required for Azure and have no defaults

#private_key_path = "~/.ssh/id_rsa"
#public_key_path = "~/.ssh/id_rsa.pub"

# Optional settings

# List of CIDR blocks and/or IP addresses to allow to connect to the ssh port
# If building the cuOpt server from a cloud shell, the public IP address of the cloud shell must be included here
#ssh_source_address_prefixes = ["0.0.0.0/0"]

# List of CIDR blocks and/or IP addresses to allow to connect to the cuOpt server  ports
# More info at https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_rule
#cuopt_source_address_prefixes = ["0.0.0.0/0"]
