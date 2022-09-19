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

