# The following variables are required for AWS and have no defaults

#private_key_path = "~/.ssh/id_rsa"
#public_key_path = "~/.ssh/id_rsa.pub"

# Optional settings

# List of CIDR block values for addresses allowed to connect to the ssh port.
# If installing from a cloud shell, the public IP address of the cloud shell must be included here
# Individual IP addresses must be expressed as CIDRs in the form 1.2.3.4/32
#ssh_cidr_blocks = ["0.0.0.0/0"]

# List of CIDR block values for addresses allowed to connect to the cuOpt server.
# Individual IP addresses must be expressed as CIDRs in the form 1.2.3.4/32
# More info at https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group
#cuopt_server_cidr_blocks = ["0.0.0.0/0"]

# Additional notes on CIDR blocks

# If your default network has default rules for port 22 that you would like to use instead,
# set this value to [] to prevent creation of the rule for port 22.
#ssh_cidr_blocks = []

# If your default network has default rules for ports 30000-30001 that you would like to use instead,
# set this value to [] to prevent creation of the rule for ports 30000-30001
#cuopt_server_cidr_blocks = []

# If your default network has default rules for outgoing traffic that you would like to use instead,
# set this value to [] to prevent creation of the rule for outgoing traffic (default unrestricted)
#outgoing_cidr_blocks = []

# If your default network has existing security groups you would like to apply to this instance,
# list their names in this value
#additional_security_groups = ["my-security-group"]
