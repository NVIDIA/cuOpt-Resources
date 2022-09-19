# The following variables are required for GCP and have no defaults

#public_key_path = "~/.ssh/id_rsa.pub"
#private_key_path = "~/.ssh/id_rsa"
#gcp_project = "my-project"
#user = "my-user"

# Optional settings

# List of CIDR blocks and/or IP addresses to allow to connect to the ports listed in additional_ports
# By default additional_ports includes port 22 for ssh
# If building the cuOpt server from a cloud shell, the public IP address of the cloud shell must be included here
#additional_ports_source_ranges = ["0.0.0.0/0"]

# List of CIDR blocks and/or IP addresses to allow to connect to the cuOpt server ports
# Additional info at https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_firewall
#cuopt_ports_source_ranges = ["0.0.0.0/0"]

# If your default network has existing rules that you would like to use for the cuOpt ports or port 22,
# uncomment the following lines to create empty port lists. This prevents Terraform from creating new rules.

# Uncomment to prevent creation of cuopt port rules
#cuopt_ports = []

# Uncomment to prevent creation of port rules for port 22
#additional_ports = []
