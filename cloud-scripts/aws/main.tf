terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.30"
    }   
    template = {
      source = "hashicorp/template"
      version = "~> 2.2.0"
    }
    random = {
      source = "hashicorp/random"
      version = "~> 3.4.3"
    }
    null = {
      source = "hashicorp/null"
      version = "~> 3.1.1"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = var.instance_region
}

resource "random_pet" "pet" {
  prefix = var.prefix_name
}

resource "aws_default_vpc" "default" {
}

resource "aws_security_group" "cuopt-server" {
  name = lower(random_pet.pet.id)
  vpc_id = "${aws_default_vpc.default.id}"

  #Incoming traffic
  ingress {
    from_port = 30000
    to_port = 30000
    protocol = "tcp"
    cidr_blocks = var.cuopt_server_cidr_blocks
  }

  ingress {
    from_port = 30001
    to_port = 30001
    protocol = "tcp"
    cidr_blocks = var.cuopt_server_cidr_blocks
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = var.ssh_cidr_blocks
  }

  #Outgoing traffic
  egress {
    from_port = 0
    protocol = "-1"
    to_port = 0
    cidr_blocks = var.outgoing_cidr_blocks
  }
}

data "aws_security_groups" "additional-security-groups" {
  filter {
     name = "group-name"
     values = var.additional_security_groups
  }
}

data "aws_ami" "osimage" {
  most_recent = true

  filter {
    name   = "name"
    values = var.instance_ami_name
  }

  filter {
    name = "architecture"
    values = var.instance_ami_arch
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = var.instance_ami_owner
}

resource "aws_key_pair" "cuopt" {
  key_name   = lower(random_pet.pet.id)
  public_key = file(var.public_key_path)
}

resource "aws_instance" "cuopt_server" {
  ami           = data.aws_ami.osimage.id
  instance_type = var.instance_type
  key_name = aws_key_pair.cuopt.key_name
  
  vpc_security_group_ids = concat([aws_security_group.cuopt-server.id], data.aws_security_groups.additional-security-groups.ids)
  root_block_device {
    volume_size = var.instance_root_volume_size 
  } 
  tags = {
    Name = lower(random_pet.pet.id)
  }
}

output "outputs" {
  value = {
            "machine": aws_instance.cuopt_server.tags.Name,
            "ip": aws_instance.cuopt_server.public_ip,
            "user": var.user,
            "private_key_path": var.private_key_path
            "cuopt_server_type": var.cuopt_server_type
          }
}

resource "null_resource" "install-cnc" {
  depends_on = [
    aws_instance.cuopt_server
  ]
  connection {
    type        = "ssh"
    user        = var.user
    private_key = "${file(var.private_key_path)}"
    host        = "${aws_instance.cuopt_server.public_ip}"
  }

  provisioner "file" {
    source      = "${path.module}/../scripts"
    destination = "scripts"
  }

  provisioner "remote-exec" {
    inline = [<<EOT
      chmod +x scripts/*.sh;
      mkdir logs;
      scripts/install-cnc.sh 2>&1 | tee logs/install-cnc.log;
      scripts/wait-cnc.sh   2>&1 | tee logs/wait-cnc.log;
    EOT
    ]
  }
}

# Break this out separately because the presence of var.api_key
# causes logging to be suppressed by Terraform
resource "null_resource" "start-cuopt" {
  depends_on = [
    null_resource.install-cnc
  ]
  connection {
    type        = "ssh"
    user        = var.user
    private_key = "${file(var.private_key_path)}"
    host        = "${aws_instance.cuopt_server.public_ip}"
  }

  provisioner "remote-exec" {
    inline = [<<EOT
      API_KEY=${var.api_key} SERVER_TYPE=${var.cuopt_server_type} scripts/cuopt-helm.sh 2>&1 | tee logs/cuopt-helm.log
    EOT
    ]
  }
}

resource "null_resource" "wait-cuopt" {
  depends_on = [
    null_resource.start-cuopt
  ]
  connection {
    type        = "ssh"
    user        = var.user
    private_key = "${file(var.private_key_path)}"
    host        = "${aws_instance.cuopt_server.public_ip}"
  }

  provisioner "remote-exec" {
    inline = [<<EOT
      scripts/wait-cuopt.sh 2>&1 | tee logs/wait-for-cuopt.log
      scripts/delete-secret.sh 2>&1 | tee logs/delete-secret.log
    EOT
    ]
  }
}
