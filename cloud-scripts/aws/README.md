# AWS
A collection of scripts and resources to spin-up AWS cuOpt instances

## Installing Terraform in CloudShell

Each time you open CloudShell, you will have to install Terraform.
The *aws-install-terraform.sh* convenience script will do this for you
```bash
# From a CloudShell Amazon Linux Terminal
$ ./aws-install-terraform.sh
```

## Default VPC

The Terraform scripts assume that your AWS account has a default VPC and
uses that for the server network. If your account does not have a default VPC,
see the Amazon documentation on how to create a default VPC.
If you do not want to use a default VPC, see the Terraform AWS documentation
on how to create a new VPC and modify the *main.tf* file accordingly.

## Setting your region

The AWS region may be set in *terraform.tfvars* (default is us-east-1)
```bash
instance_region = "us-west-2"
```

## Using existing security groups

If your VPC has existing security groups that  you would like to apply to your instance
you can set them with the `additional_security_groups` variable. See notes in *terraform.tfvars*

## Selecting the instance type

The instance type may be set in *terraform.tfvars* (default is g4dn.xlarge)
```bash
instance_type = "g4dn.2xlarge"
```

## Selecting an OS Image

The default OS image is Ubuntu-22.04-LTS. If you would like to change the OS,
look at the following variables in *variables.tf* and then override
their defaults in *terraform.tfvars*.

* `instance_ami_name`
* `instance_ami_arch`
* `instance_ami_owner`



