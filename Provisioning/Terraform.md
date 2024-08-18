# Terraform Learning Guide: From Beginner to Master

## Table of Contents
1. [Introduction to Terraform](#introduction-to-terraform)
2. [Setting Up Your Environment](#setting-up-your-environment)
3. [Basic Terraform Concepts](#basic-terraform-concepts)
4. [Writing Your First Terraform Configuration](#writing-your-first-terraform-configuration)
5. [Terraform State Management](#terraform-state-management)
6. [Variables and Outputs](#variables-and-outputs)
7. [Modules](#modules)
8. [Remote State and Backends](#remote-state-and-backends)
9. [Terraform Workspaces](#terraform-workspaces)
10. [Advanced Topics](#advanced-topics)

## 1. Introduction to Terraform

Terraform is an Infrastructure as Code (IaC) tool that allows you to define and manage your infrastructure using a declarative language. It supports multiple cloud providers and services, making it a versatile choice for managing complex infrastructures.

### Key Concepts:
- Infrastructure as Code (IaC)
- Declarative vs Imperative programming
- Providers
- Resources
- State management

## 2. Setting Up Your Environment

Before we begin with the exercises, let's set up our environment.

### Exercise 2.1: Installing Terraform

1. Download Terraform from the official website: https://www.terraform.io/downloads.html
2. Extract the zip file and add the Terraform binary to your system PATH.
3. Open a command prompt and verify the installation:

```
terraform version
```

### Exercise 2.2: Setting Up a Docker Provider

Since we're using Docker on Windows 11, we'll use the Docker provider for our exercises.

1. Ensure Docker Desktop is installed and running on your Windows 11 PC.
2. Create a new directory for your Terraform projects:

```
mkdir terraform-exercises
cd terraform-exercises
```

3. Create a file named `main.tf` with the following content:

```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}

provider "docker" {}
```

4. Initialize the Terraform working directory:

```
terraform init
```

**Intention:** Set up the necessary tools and environment for working with Terraform.

**Interpretation:** After completing these exercises, you should have Terraform installed and a basic project structure set up with the Docker provider.

## 3. Basic Terraform Concepts

### Exercise 3.1: Understanding Terraform Workflow

1. Create a new file named `docker_container.tf` with the following content:

```hcl
resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "tutorial"
  ports {
    internal = 80
    external = 8000
  }
}
```

2. Run the following commands and observe the output:

```
terraform fmt
terraform validate
terraform plan
terraform apply
```

3. Verify that the container is running:

```
docker ps
```

4. Clean up the resources:

```
terraform destroy
```

**Intention:** Understand the basic Terraform workflow and commands.

**Interpretation:** This exercise demonstrates the typical Terraform workflow: writing configuration, formatting, validating, planning, applying, and destroying resources.

## 4. Writing Your First Terraform Configuration

### Exercise 4.1: Creating Multiple Resources

1. Modify the `docker_container.tf` file to create multiple containers:

```hcl
resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  count = 3
  image = docker_image.nginx.image_id
  name  = "tutorial-${count.index}"
  ports {
    internal = 80
    external = 8000 + count.index
  }
}
```

2. Apply the changes:

```
terraform apply
```

3. Verify that three containers are running:

```
docker ps
```

**Intention:** Learn how to create multiple similar resources using the `count` parameter.

**Interpretation:** This exercise shows how to use the `count` parameter to create multiple instances of a resource with slight variations.

## 5. Terraform State Management

### Exercise 5.1: Inspecting and Manipulating State

1. Inspect the current state:

```
terraform show
```

2. List the resources in the state:

```
terraform state list
```

3. Remove a resource from the state without destroying it:

```
terraform state rm docker_container.nginx[2]
```

4. Observe that one container is no longer managed by Terraform:

```
terraform show
docker ps
```

5. Import the unmanaged container back into Terraform state:

```
terraform import docker_container.nginx[2] $(docker ps -aqf "name=tutorial-2")
```

**Intention:** Understand how Terraform manages state and learn basic state manipulation commands.

**Interpretation:** This exercise demonstrates how to inspect and manipulate Terraform state, which is crucial for managing long-lived infrastructure.

## 6. Variables and Outputs

### Exercise 6.1: Using Input Variables

1. Create a new file named `variables.tf`:

```hcl
variable "container_count" {
  description = "Number of containers to create"
  type        = number
  default     = 3
}

variable "external_port_start" {
  description = "Starting external port number"
  type        = number
  default     = 8000
}
```

2. Modify `docker_container.tf` to use these variables:

```hcl
resource "docker_container" "nginx" {
  count = var.container_count
  image = docker_image.nginx.image_id
  name  = "tutorial-${count.index}"
  ports {
    internal = 80
    external = var.external_port_start + count.index
  }
}
```

3. Apply the changes:

```
terraform apply
```

### Exercise 6.2: Defining Output Values

1. Create a new file named `outputs.tf`:

```hcl
output "container_ids" {
  description = "IDs of created containers"
  value       = docker_container.nginx[*].id
}

output "container_ports" {
  description = "Exposed ports of created containers"
  value       = docker_container.nginx[*].ports[0].external
}
```

2. Apply the changes and observe the outputs:

```
terraform apply
```

**Intention:** Learn how to use input variables to make your configuration more flexible and how to define output values to extract useful information.

**Interpretation:** These exercises show how to parameterize your Terraform configurations using input variables and how to extract and display important information using output values.

## 7. Modules

### Exercise 7.1: Creating and Using a Module

1. Create a new directory for your module:

```
mkdir -p modules/nginx
```

2. Create a file `modules/nginx/main.tf`:

```hcl
resource "docker_container" "nginx" {
  count = var.container_count
  image = docker_image.nginx.image_id
  name  = "${var.container_name_prefix}-${count.index}"
  ports {
    internal = 80
    external = var.external_port_start + count.index
  }
}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}
```

3. Create a file `modules/nginx/variables.tf`:

```hcl
variable "container_count" {
  description = "Number of containers to create"
  type        = number
  default     = 1
}

variable "container_name_prefix" {
  description = "Prefix for container names"
  type        = string
  default     = "nginx"
}

variable "external_port_start" {
  description = "Starting external port number"
  type        = number
  default     = 8000
}
```

4. Create a file `modules/nginx/outputs.tf`:

```hcl
output "container_ids" {
  description = "IDs of created containers"
  value       = docker_container.nginx[*].id
}

output "container_ports" {
  description = "Exposed ports of created containers"
  value       = docker_container.nginx[*].ports[0].external
}
```

5. Modify your root `main.tf` to use this module:

```hcl
module "nginx_app" {
  source = "./modules/nginx"

  container_count       = 2
  container_name_prefix = "myapp"
  external_port_start   = 9000
}

output "app_container_ids" {
  value = module.nginx_app.container_ids
}

output "app_container_ports" {
  value = module.nginx_app.container_ports
}
```

6. Apply the changes:

```
terraform apply
```

**Intention:** Learn how to create and use Terraform modules to organize and reuse your infrastructure code.

**Interpretation:** This exercise demonstrates how to create a reusable module and how to use it in your main configuration, promoting code reuse and organization.

## 8. Remote State and Backends

### Exercise 8.1: Using a Local Backend

1. Create a new directory for backend experiments:

```
mkdir backend-demo
cd backend-demo
```

2. Create a `main.tf` file:

```hcl
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "nginx-backend-demo"
  ports {
    internal = 80
    external = 8080
  }
}
```

3. Initialize and apply:

```
terraform init
terraform apply
```

4. Observe the created `terraform.tfstate` file.

### Exercise 8.2: Simulating a Remote Backend with Docker

1. Create a Docker volume to simulate a remote backend:

```
docker volume create terraform-backend
```

2. Run a container with the volume mounted:

```
docker run -d --name terraform-backend -v terraform-backend:/data -p 8081:80 nginx
```

3. Modify the backend configuration in `main.tf`:

```hcl
terraform {
  backend "http" {
    address = "http://localhost:8081/terraform.tfstate"
    lock_address = "http://localhost:8081/terraform.lock"
    unlock_address = "http://localhost:8081/terraform.lock"
  }
}
```

4. Reinitialize Terraform:

```
terraform init
```

**Intention:** Understand the concept of Terraform backends and how to configure them.

**Interpretation:** These exercises introduce the concept of Terraform backends for storing state. The first exercise uses a local backend, while the second simulates a remote backend using a Docker container.

## 9. Terraform Workspaces

### Exercise 9.1: Using Workspaces

1. Create a new `main.tf` file:

```hcl
resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "nginx-${terraform.workspace}"
  ports {
    internal = 80
    external = 8080 + index(["default", "staging", "production"], terraform.workspace)
  }
}
```

2. Create and switch to a new workspace:

```
terraform workspace new staging
```

3. Apply the configuration:

```
terraform apply
```

4. Create another workspace and apply:

```
terraform workspace new production
terraform apply
```

5. List and switch between workspaces:

```
terraform workspace list
terraform workspace select staging
```

**Intention:** Learn how to use Terraform workspaces to manage multiple environments.

**Interpretation:** This exercise demonstrates how to use Terraform workspaces to manage different environments (e.g., staging, production) using the same configuration files.

## 10. Advanced Topics

### Exercise 10.1: Using Data Sources

1. Create a new file `data.tf`:

```hcl
data "docker_network" "bridge" {
  name = "bridge"
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "nginx-data-source-demo"
  networks_advanced {
    name = data.docker_network.bridge.name
  }
}
```

2. Apply the configuration:

```
terraform apply
```

### Exercise 10.2: Using Provisioners

1. Modify your `main.tf`:

```hcl
resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "nginx-provisioner-demo"
  ports {
    internal = 80
    external = 8082
  }

  provisioner "local-exec" {
    command = "echo Container ${self.name} created with ID ${self.id}"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "echo Container ${self.name} destroyed"
  }
}
```

2. Apply and then destroy the configuration:

```
terraform apply
terraform destroy
```

**Intention:** Explore advanced Terraform features like data sources and provisioners.

**Interpretation:** These exercises introduce two advanced concepts: data sources for querying existing resources, and provisioners for executing actions on resource creation or destruction.

This comprehensive guide covers the essential aspects of Terraform, from basic concepts to advanced topics. Each exercise is designed to build upon the previous ones, helping you gradually master Terraform. Remember to experiment with these concepts and adapt them to your specific use cases.
