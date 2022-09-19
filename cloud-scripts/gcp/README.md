# GCP
A collection of scripts and resources to spin-up GCP cuOpt instances

## Default VPC

The Terraform scripts assume that your GCP account has a default VPC and
uses that for the server network. If your account does not have a default VPC,
see the GCP documentation on how to create a default VPC.
If you do not want to use a default VPC, see the Terraform GCP documentation
on how to create a new VPC and modify the *main.tf* file accordingly.

## Setting the region and zone

The GCP region and/or zone may be set in *terraform.tfvars* (defaults are us-east1 and c)
```bash
gcp_region = "us-west1"
gcp_zone   = "b"
```

## Selecting the instance type

The instance type may be set in *terraform.tfvars* (default is n1-standard-4)
```bash
instance_machine_type = "n1-standard-8"
```

## Selecting an OS image

The instance OS may be set in *terraform.tfvars* (default is ubuntu-2204-lts)
```bash
instance_os_image = "ubuntu-someversion-lts"
```

## Setting the root volume size

The root volume size may be set in *terraform.tfvars* (default is 128)
```bash
root_volume_size = 64
```

## Setting the GPU type

The gpu type may be set in *terraform.tfvars* (default is nvidia-tesla-t4)
```bash
gpu_type = "nvidia-tesla-k80"
```

## Additional ports

The `additional_ports` variable holds a list of ports. Network access to these ports
is controlled with the `additional_ports_source_ranges` variable.

The default value of additional_ports is ["22"] which is the ssh port. If there are
additional ports you would like to open on the cuOpt server, not including 30000
and 30001, you may include them in the additional_ports list.