# Unit 4: AWS Network and Security Lab Guide

## Objectives
- Understand the concepts of AWS VPC and Security Groups
- Create an AWS VPC using Terraform
- Create an AWS Security Group using Terraform

## Prerequisites
- AWS account
- Terraform installed on your local machine
- Basic understanding of AWS services and Terraform syntax

## Key Concepts

### Virtual Private Cloud (VPC)

A Virtual Private Cloud (VPC) is a logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define. It provides control over your networking environment, including IP address ranges, subnets, route tables, and network gateways.

Key features of a VPC:
1. Isolation: Resources in one VPC are isolated from resources in other VPCs by default.
2. Customization: You can configure IP address ranges, create subnets, and configure route tables.
3. Security: VPCs allow you to control inbound and outbound traffic using security groups and network ACLs.
4. Connectivity: You can connect your VPC to your on-premises network or other VPCs.

### Security Groups

A security group acts as a virtual firewall for your EC2 instances to control inbound and outbound traffic. Security groups operate at the instance level and can be associated with multiple instances.

Key features of Security Groups:
1. Stateful: If you allow inbound traffic, the corresponding outbound traffic is automatically allowed.
2. Rule-based: You can specify allow rules, but you can't specify deny rules.
3. Instance-level: They are associated with EC2 instances, not with subnets.
4. Multiple groups: You can assign multiple security groups to an instance.

## Lab Instructions

### Step 1: Set up the Terraform configuration

1. Create a new directory for your Terraform project:
   ```
   mkdir aws-network-lab
   cd aws-network-lab
   ```

2. Create a file named `main.tf` and add the following content:

```hcl
# Provider configuration
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# Variables
variable "aws_access_key" {
  description = "AWS Access Key"
  type        = string
}

variable "aws_secret_key" {
  description = "AWS Secret Key"
  type        = string
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-west-2"
}

# VPC Resource
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "terraform-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "terraform-igw"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"

  tags = {
    Name = "terraform-public-subnet"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "terraform-public-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security Group
resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_ssh"
  }
}

# Output
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "security_group_id" {
  value = aws_security_group.allow_ssh.id
}
```

### Step 2: Create a `terraform.tfvars` file

Create a file named `terraform.tfvars` in the same directory and add your AWS credentials:

```hcl
aws_access_key = "YOUR_AWS_ACCESS_KEY"
aws_secret_key = "YOUR_AWS_SECRET_KEY"
aws_region     = "us-west-2"  # Change this if you want to use a different region
```

**Note:** Never commit this file to version control. Add it to your `.gitignore` file to prevent accidental commits.

### Step 3: Initialize Terraform

Run the following command to initialize Terraform:

```
terraform init
```

### Step 4: Plan the infrastructure

Run the following command to see what changes Terraform will make:

```
terraform plan
```

Review the output to ensure it matches your expectations.

### Step 5: Apply the changes

If the plan looks good, apply the changes:

```
terraform apply
```

Type "yes" when prompted to confirm the changes.

### Step 6: Verify the resources

1. Log in to the AWS Management Console.
2. Navigate to the VPC dashboard and verify that a new VPC has been created with the CIDR block 10.0.0.0/16.
3. Check that a public subnet, internet gateway, and route table have been created and associated with the VPC.
4. Go to the EC2 dashboard and verify that a new security group has been created allowing SSH access.

### Step 7: Clean up (Optional)

To avoid ongoing charges, you can destroy the resources created by Terraform:

```
terraform destroy
```

Type "yes" when prompted to confirm the destruction of resources.

## Explanation of Resources

1. **VPC (aws_vpc)**: This creates a Virtual Private Cloud with a CIDR block of 10.0.0.0/16, which allows for up to 65,536 IP addresses. The VPC is the foundation of your network in AWS, providing isolation and control over your resources.

2. **Internet Gateway (aws_internet_gateway)**: This allows communication between the VPC and the internet. It's a crucial component for resources in your VPC that need to be accessible from the internet or need to access the internet.

3. **Public Subnet (aws_subnet)**: A subnet with a CIDR block of 10.0.1.0/24 is created within the VPC, allowing for up to 256 IP addresses. This public subnet is where you would place resources that need to be directly accessible from the internet, such as web servers.

4. **Route Table (aws_route_table)**: This directs traffic from the subnet to the internet gateway. It ensures that resources in the public subnet can communicate with the internet.

5. **Security Group (aws_security_group)**: This acts as a virtual firewall for EC2 instances. In this example, it allows inbound SSH traffic from any IP address. Security groups are stateful, meaning if you allow inbound traffic, the corresponding outbound traffic is automatically allowed.

## Best Practices

1. **VPC Design**: 
   - Plan your IP address space carefully to allow for future growth.
   - Use private subnets for resources that don't need direct internet access.
   - Implement Network ACLs for an additional layer of security.

2. **Security Groups**:
   - Follow the principle of least privilege: only open ports that are necessary.
   - Use specific IP ranges instead of 0.0.0.0/0 when possible.
   - Regularly review and update your security group rules.

3. **Terraform**:
   - Use variables and locals to make your code more reusable and maintainable.
   - Organize your code into modules for complex infrastructures.
   - Use remote state storage (like S3) for team collaboration and state locking.

## Conclusion

In this lab, you've successfully created an AWS VPC and associated resources using Terraform. You've also created a security group that allows SSH access. This infrastructure can serve as a foundation for deploying EC2 instances or other AWS resources in a secure, isolated network environment.

Understanding VPCs and security groups is crucial for building secure and scalable applications in AWS. VPCs provide network isolation and control, while security groups offer fine-grained control over inbound and outbound traffic at the instance level.

Remember to always follow AWS best practices and security guidelines when working with real-world projects. Regularly review and update your network configurations to ensure they align with your security requirements and best practices.
