# Terraform Assignment (with Answers)

This assignment contains Terraform code examples and related multiple-choice questions to test your understanding of Infrastructure as Code, cloud provisioning, and DevOps concepts.

## Section 1: Basic Terraform Concepts

1. What does the following Terraform code block represent?

```hcl
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
```

a) A data source
b) A provider block
c) A resource block
d) A variable declaration

Answer: c) A resource block

2. Which of the following Terraform commands is used to create an execution plan?

a) terraform apply
b) terraform plan
c) terraform init
d) terraform validate

Answer: b) terraform plan

3. What is the purpose of the following Terraform block?

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}
```

a) To specify the required version of Terraform
b) To define the AWS provider
c) To declare variables
d) To specify the required provider and its version

Answer: d) To specify the required provider and its version

4. Which Terraform command is used to initialize a working directory containing Terraform configuration files?

a) terraform init
b) terraform apply
c) terraform plan
d) terraform validate

Answer: a) terraform init

5. What does the following Terraform code snippet do?

```hcl
variable "instance_count" {
  type    = number
  default = 2
}
```

a) Creates two EC2 instances
b) Declares a variable named "instance_count" with a default value of 2
c) Sets the maximum number of instances to 2
d) Defines a list with two elements

Answer: b) Declares a variable named "instance_count" with a default value of 2

## Section 2: AWS Resource Provisioning

6. What AWS resource does the following Terraform code create?

```hcl
resource "aws_s3_bucket" "example" {
  bucket = "my-tf-test-bucket"
  acl    = "private"
}
```

a) An EC2 instance
b) A VPC
c) An S3 bucket
d) A security group

Answer: c) An S3 bucket

7. Which Terraform resource type is used to create an AWS VPC?

a) aws_vpc
b) aws_ec2_vpc
c) aws_network
d) aws_virtual_network

Answer: a) aws_vpc

8. What does the following Terraform code create in AWS?

```hcl
resource "aws_security_group" "allow_tls" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  
  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}
```

a) A VPC
b) A security group
c) A network ACL
d) A subnet

Answer: b) A security group

9. Which of the following is NOT a valid attribute for the aws_instance resource?

a) ami
b) instance_type
c) vpc_id
d) key_name

Answer: c) vpc_id

10. What does the count parameter do in the following Terraform code?

```hcl
resource "aws_instance" "example" {
  count         = 3
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
```

a) Creates 3 identical EC2 instances
b) Specifies the number of CPUs for the instance
c) Sets the maximum number of instances that can be created
d) Defines the number of subnets to create

Answer: a) Creates 3 identical EC2 instances

## Section 3: Azure Resource Provisioning

11. Which Terraform provider block is used for Azure resources?

a) provider "azure" {}
b) provider "azurerm" {}
c) provider "microsoft" {}
d) provider "azure_rm" {}

Answer: b) provider "azurerm" {}

12. What Azure resource does the following Terraform code create?

```hcl
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}
```

a) A virtual machine
b) A resource group
c) A storage account
d) A virtual network

Answer: b) A resource group

13. Which Terraform resource type is used to create an Azure Virtual Network?

a) azurerm_virtual_network
b) azurerm_vnet
c) azure_network
d) azurerm_network

Answer: a) azurerm_virtual_network

14. What does the following Terraform code create in Azure?

```hcl
resource "azurerm_storage_account" "example" {
  name                     = "examplestoracc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}
```

a) A virtual machine
b) A resource group
c) A storage account
d) A SQL database

Answer: c) A storage account

15. Which of the following is NOT a valid attribute for the azurerm_virtual_machine resource?

a) name
b) location
c) resource_group_name
d) instance_type

Answer: d) instance_type

## Section 4: Google Cloud Platform (GCP) Resource Provisioning

16. Which Terraform provider block is used for Google Cloud Platform resources?

a) provider "gcp" {}
b) provider "google" {}
c) provider "googlecloud" {}
d) provider "gcloud" {}

Answer: b) provider "google" {}

17. What GCP resource does the following Terraform code create?

```hcl
resource "google_compute_network" "vpc_network" {
  name                    = "terraform-network"
  auto_create_subnetworks = "true"
}
```

a) A Compute Engine instance
b) A VPC network
c) A Cloud Storage bucket
d) A Cloud SQL instance

Answer: b) A VPC network

18. Which Terraform resource type is used to create a GCP Compute Engine instance?

a) google_compute_instance
b) google_vm_instance
c) gcp_compute_instance
d) google_instance

Answer: a) google_compute_instance

19. What does the following Terraform code create in GCP?

```hcl
resource "google_storage_bucket" "example" {
  name     = "my-unique-bucket-name"
  location = "US"
}
```

a) A Compute Engine instance
b) A VPC network
c) A Cloud Storage bucket
d) A Cloud SQL instance

Answer: c) A Cloud Storage bucket

20. Which of the following is NOT a valid attribute for the google_compute_instance resource?

a) name
b) machine_type
c) zone
d) vpc_id

Answer: d) vpc_id

## Section 5: Terraform State Management

21. What is the purpose of the Terraform state file?

a) To store sensitive information
b) To track the current state of managed infrastructure
c) To define the desired infrastructure configuration
d) To log Terraform operations

Answer: b) To track the current state of managed infrastructure

22. Which command is used to show the current state of the Terraform-managed infrastructure?

a) terraform show
b) terraform state
c) terraform output
d) terraform refresh

Answer: a) terraform show

23. What does the following Terraform code block represent?

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-west-2"
  }
}
```

a) A resource block for an S3 bucket
b) A data source for retrieving S3 bucket information
c) A backend configuration for storing Terraform state in S3
d) A provider block for AWS

Answer: c) A backend configuration for storing Terraform state in S3

24. Which Terraform command is used to manually modify the state?

a) terraform state
b) terraform modify
c) terraform update
d) terraform edit

Answer: a) terraform state

25. What is the purpose of the terraform import command?

a) To download provider plugins
b) To create a new resource in Terraform
c) To bring existing infrastructure under Terraform management
d) To export Terraform configuration to other formats

Answer: c) To bring existing infrastructure under Terraform management

## Section 6: Terraform Modules

26. What is the purpose of Terraform modules?

a) To organize and reuse Terraform code
b) To create virtual machines
c) To manage state files
d) To define output variables

Answer: a) To organize and reuse Terraform code

27. How do you reference a module in Terraform?

```hcl
module "example" {
  source = "./modules/example"
  count  = 2
}
```

What does this code do?

a) Creates two instances of the "example" module
b) Defines a new module named "example"
c) Imports a module from the Terraform Registry
d) Outputs the result of the "example" module

Answer: a) Creates two instances of the "example" module

28. Which file is commonly used to define the inputs (variables) for a Terraform module?

a) main.tf
b) variables.tf
c) outputs.tf
d) providers.tf

Answer: b) variables.tf

29. How can you pass a variable to a module?

a) By using the var keyword
b) By defining the variable in the module block
c) By using environment variables
d) By using the tf_var prefix

Answer: b) By defining the variable in the module block

30. What is the purpose of the outputs.tf file in a Terraform module?

a) To define input variables for the module
b) To specify the required provider versions
c) To define values that can be used by other parts of your Terraform configuration
d) To create local variables within the module

Answer: c) To define values that can be used by other parts of your Terraform configuration

## Section 7: Terraform Workspaces

31. What is the purpose of Terraform workspaces?

a) To organize code into reusable modules
b) To manage multiple environments or configurations for the same infrastructure
c) To store sensitive information securely
d) To define provider-specific settings

Answer: b) To manage multiple environments or configurations for the same infrastructure

32. Which command is used to create a new Terraform workspace?

a) terraform workspace new
b) terraform new workspace
c) terraform create workspace
d) terraform workspace create

Answer: a) terraform workspace new

33. How can you reference the current workspace name in your Terraform configuration?

a) ${workspace.name}
b) ${var.workspace}
c) ${terraform.workspace}
d) ${env.workspace}

Answer: c) ${terraform.workspace}

34. What happens to the state file when you switch between Terraform workspaces?

a) It is deleted
b) It is renamed
c) A new state file is created for each workspace
d) The state file remains unchanged

Answer: c) A new state file is created for each workspace

35. Which of the following is NOT a valid Terraform workspace command?

a) terraform workspace list
b) terraform workspace select
c) terraform workspace delete
d) terraform workspace rename

Answer: d) terraform workspace rename

## Section 8: Terraform Functions and Expressions

36. What does the following Terraform expression do?

```hcl
locals {
  instance_names = [for i in range(3) : "instance-${i}"]
}
```

a) Creates a list of three instance names
b) Defines a local variable named "instance_names"
c) Creates three EC2 instances
d) Both a and b

Answer: d) Both a and b

37. Which Terraform function is used to join elements of a list into a string?

a) concat()
b) merge()
c) join()
d) split()

Answer: c) join()

38. What is the purpose of the coalesce() function in Terraform?

a) To combine two or more lists
b) To return the first non-null value from a list of expressions
c) To split a string into a list
d) To encrypt sensitive data

Answer: b) To return the first non-null value from a list of expressions

39. How would you use a conditional expression in Terraform to set a value based on a condition?

a) if condition then value1 else value2
b) condition ? value1 : value2
c) switch(condition) { case true: value1, case false: value2 }
d) condition == true ? value1 : value2

Answer: b) condition ? value1 : value2

40. What does the following Terraform code do?

```hcl
variable "environment" {
  type = string
}

locals {
  is_production = var.environment == "prod"
}
```

a) Defines a variable named "environment"
b) Creates a local value that checks if the environment is production
c) Sets the environment to production
d) Both a and b

Answer: d) Both a and b

## Section 9: Terraform Provisioners

41. What is the purpose of provisioners in Terraform?

a) To create new resources
b) To manage state files
c) To execute scripts or commands on resources after creation
d) To define input variables

Answer: c) To execute scripts or commands on resources after creation

42. Which of the following is NOT a valid Terraform provisioner?

a) file
b) local-exec
c) remote-exec
d) cloud-init

Answer: d) cloud-init

43. What does the following Terraform code block represent?

```hcl
provisioner "remote-exec" {
  inline = [
    "sudo apt-get update",
    "sudo apt-get install -y nginx"
  ]
}
```

a) A file provisioner
b) A local-exec provisioner
c) A remote-exec provisioner
d) A cloud-init config

Answer: c) A remote-exec provisioner

44. When does a provisioner typically run in the Terraform resource lifecycle?

a) Before the resource is created
b) After the resource is created
c) When the resource is updated
d) When the resource is destroyed

Answer: b) After the resource is created

45. What is the purpose of the "when" attribute in a provisioner block?

a) To specify when the provisioner should run
b) To define a condition for running the provisioner
c) To set a timeout for the provisioner
d) To schedule the provisioner execution

Answer: a) To specify when the provisioner should run

## Section 10: Terraform and CI/CD

46. Which of the following is NOT typically a step in a Terraform CI/CD pipeline?

a) terraform init
b) terraform plan
c) terraform apply
d) terraform compile

Answer: d) terraform compile

47. What is the purpose of running "terraform plan" in a CI/CD pipeline?

a) To apply changes to the infrastructure
b) To generate an execution plan and identify changes
c) To initialize the Terraform working directory
d) To validate the Terraform configuration files

Answer: b) To generate an execution plan and identify changes

48. How can you automate Terraform runs in a CI/CD pipeline?

a) By using Terraform Enterprise
b) By using a CI/CD tool like Jenkins, GitLab CI, or GitHub Actions
c) By scheduling Terraform runs using cron jobs
d) All of the above

Answer: d) All of the above

49. What is the purpose of the -auto-approve flag in terraform apply?

a) To automatically approve and apply changes without user confirmation
b) To automatically rollback changes if there's an error
c) To enable automatic state locking
d) To approve only specific resources for application

Answer: a) To automatically approve and apply changes without user confirmation

50. Which Terraform command is typically used to clean up resources in a CI/CD pipeline when they are no longer needed?

a) terraform clean
b) terraform delete
c) terraform destroy
d) terraform remove

Answer: c) terraform destroy

51. What is the purpose of using a remote backend for Terraform state in a CI/CD pipeline?

a) To improve performance of Terraform operations
b) To enable collaboration and state sharing between team members and CI/CD jobs
c) To encrypt sensitive data in the state file
d) To automatically apply changes to the infrastructure

Answer: b) To enable collaboration and state sharing between team members and CI/CD jobs

52. Which of the following is a best practice when using Terraform in a CI/CD pipeline?

a) Committing the .terraform directory to version control
b) Using the same Terraform workspace for all environments
c) Storing Terraform state files in version control
d) Using separate state files for different environments

Answer: d) Using separate state files for different environments

53. What is the purpose of Terraform's remote backends in the context of CI/CD?

a) To store Terraform configurations
b) To execute Terraform commands remotely
c) To store and manage Terraform state files remotely
d) To provision cloud resources

Answer: c) To store and manage Terraform state files remotely

54. Which of the following is NOT a typical stage in a Terraform-based CI/CD pipeline?

a) Lint
b) Plan
c) Compile
d) Apply

Answer: c) Compile

55. What is the purpose of using Terraform workspaces in a CI/CD pipeline?

a) To organize Terraform modules
b) To manage different environments (e.g., dev, staging, prod) with the same configuration
c) To parallelize Terraform operations
d) To store sensitive variables

Answer: b) To manage different environments (e.g., dev, staging, prod) with the same configuration
