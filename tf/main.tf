# variables
variable "project_name" {
  type = string
  default = "dump"
}

variable "port_number" {
  type = string
  default = "5000"
}

variable "boot_image_name" {
  type = string
  default = "projects/cos-cloud/global/images/cos-stable-69-10895-62-0"
}

provider "google"{
  # credentials = file("~/.gcp_creds.json")
  project = var.project_name
  region = "us-east1-b"
}

# docker
variable "docker_declaration" {
  type = string
  # Change the image: string to match the Docker image you want to use
  default = "spec:\n  containers:\n    - name: test-docker\n      image: 'gtarpenning/fastapi-image-test'\n      stdin: false\n      tty: false\n  restartPolicy: Always\n"
}

# data "google_compute_network" "default" {
#  name = "default"
#}

# VPC shit
resource "google_compute_network" "vpc_network" {
  name                    = "my-custom-mode-network"
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "default" {
  name          = "my-custom-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-west1"
  network       = google_compute_network.vpc_network.id
}

# Compute shit
resource "google_compute_instance" "default" {
  name = "default"
  machine_type = "g1-small"
  zone = "us-east1-b"
  tags =[
      "name","default"
  ]

  boot_disk {
    auto_delete = true
    initialize_params {
      image = var.boot_image_name
      type = "pd-standard"
    }
  }

  metadata = {
    gce-container-declaration = var.docker_declaration
  }

  labels = {
    container-vm = "cos-stable-69-10895-62-0"
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral IP
    }
  }
}

# Ingress
resource "google_compute_firewall" "http-5000" {
  name    = "http-5000"
  network = resource.google_compute_network.vpc_network.name

  source_tags = ["web", "ssh"]

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = [var.port_number]
  }
}

# A variable for extracting the external IP address of the VM
output "Web-server-URL" {
 value = join("",["http://",google_compute_instance.default.network_interface.0.access_config.0.nat_ip,":5000"])
}
