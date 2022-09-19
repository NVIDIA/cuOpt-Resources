terraform {
  required_version = "~> 1.0"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.11.0" # pinning version
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
}

resource "random_pet" "pet" {
  prefix = var.prefix_name
}


provider "google" {
  project     = var.gcp_project
  region      = var.gcp_region
}

resource "google_compute_firewall" "additional_rules" {
  name    = "${lower(random_pet.pet.id)}-other"
  network = "default"
  allow {
    protocol = "tcp"
    ports    = var.additional_ports
  }

  source_ranges = var.additional_ports_source_ranges
  target_tags = [lower(random_pet.pet.id)]
}

resource "google_compute_firewall" "cuopt_rules" {
  name    = "${lower(random_pet.pet.id)}-server"
  network = "default"
  allow {
    protocol = "tcp"
    ports    = var.cuopt_ports
  }
  
  source_ranges = var.cuopt_ports_source_ranges
  target_tags = [lower(random_pet.pet.id)]
}

# Ensure there is a public ip
resource "google_compute_address" "ip" {
  name = lower(random_pet.pet.id)
  project = var.gcp_project
  region = var.gcp_region
  depends_on = [ google_compute_firewall.cuopt_rules,
                 google_compute_firewall.additional_rules ]
}

resource "google_compute_instance" "cuopt_server" {
  name         = lower(random_pet.pet.id)
  machine_type = "n1-standard-4"
  zone         = "${var.gcp_region}-${var.gcp_zone}"
  tags         = [lower(random_pet.pet.id)]  

  boot_disk {
    initialize_params {
      image = "ubuntu-2204-lts"
      size  = 128
    }
  }  

  network_interface {
    network       = "default"
    access_config {
      nat_ip = google_compute_address.ip.address
    }
  }

  # required for guest_accelerators
  scheduling {
    on_host_maintenance = "TERMINATE"
  }

  guest_accelerator = [
    {
      type = "nvidia-tesla-t4"
      count = 1
    }
  ]

  metadata = {
    ssh-keys = "${var.user}:${file(var.public_key_path)}"
  }
}

output "outputs" {
  value = {
            "machine": google_compute_instance.cuopt_server.name,
            "ip": google_compute_address.ip.address,
            "user": var.user,
            "private_key_path": var.private_key_path
            "cuopt_server_type": var.cuopt_server_type
          }
}

resource "null_resource" "install-cnc" {
  depends_on = [
    google_compute_instance.cuopt_server
  ]
  connection {
    type        = "ssh"
    user        = var.user
    private_key = "${file(var.private_key_path)}"
    host        = google_compute_address.ip.address
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
    host        = google_compute_address.ip.address
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
    host        = google_compute_address.ip.address
  }

  provisioner "remote-exec" {
    inline = [<<EOT
      scripts/wait-cuopt.sh 2>&1 | tee logs/wait-for-cuopt.log
      scripts/delete-secret.sh 2>&1 | tee logs/delete-secret.log
    EOT
    ]
  }
}

