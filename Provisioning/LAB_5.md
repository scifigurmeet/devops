# CSV 404 - System Provisioning & Code Quality Testing Lab
## Unit 5: AWS Identity and Storage

### Introduction

In this lab, we'll explore how to use Terraform to manage AWS Identity and Access Management (IAM) policies and Amazon Simple Storage Service (S3) buckets. These are crucial components in AWS for managing access control and storing data securely in the cloud.

### Objectives

By the end of this lab, you will be able to:
1. Configure AWS credentials in Terraform
2. Create an AWS IAM policy using Terraform
3. Create an AWS S3 bucket using Terraform
4. Apply best practices for IAM and S3 management
5. Use Terraform to manage and version your infrastructure

### Prerequisites

- AWS account with appropriate permissions
- Terraform installed on your local machine
- Basic understanding of AWS services and Terraform syntax

### Part 1: Setting Up the Terraform Project

1. Create a new directory for your project and navigate into it:
   ```bash
   mkdir aws-iam-s3-terraform
   cd aws-iam-s3-terraform
   ```

2. Create a `variables.tf` file for your Terraform variables:
   ```bash
   touch variables.tf
   ```

3. Open `variables.tf` and add the following content:
   ```hcl
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
     default     = "us-west-2"  # or your preferred region
   }

   variable "bucket_name" {
     description = "Name of the S3 bucket"
     type        = string
     default     = "my-unique-bucket-name-12345"  # Replace with your unique bucket name
   }
   ```

4. Create a `terraform.tfvars` file to store your actual AWS credentials:
   ```bash
   touch terraform.tfvars
   ```

5. Open `terraform.tfvars` and add your AWS credentials:
   ```hcl
   aws_access_key = "YOUR_AWS_ACCESS_KEY"
   aws_secret_key = "YOUR_AWS_SECRET_KEY"
   aws_region     = "us-west-2"  # or your preferred region
   ```

   Note: Make sure to add `terraform.tfvars` to your `.gitignore` file to avoid accidentally committing your AWS credentials to version control.

6. Create a `main.tf` file for your Terraform configuration:
   ```bash
   touch main.tf
   ```

7. Open `main.tf` and add the AWS provider configuration:
   ```hcl
   provider "aws" {
     access_key = var.aws_access_key
     secret_key = var.aws_secret_key
     region     = var.aws_region
   }
   ```

### Part 2: Creating an AWS IAM Policy

Add the following Terraform code to your `main.tf` to create an IAM policy:

```hcl
resource "aws_iam_policy" "s3_read_only" {
  name        = "s3_read_only"
  path        = "/"
  description = "Allow read-only access to specific S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Resource = [
          "arn:aws:s3:::${var.bucket_name}",
          "arn:aws:s3:::${var.bucket_name}/*"
        ]
      },
    ]
  })
}
```

### Part 3: Creating an AWS S3 Bucket

Add the following Terraform code to your `main.tf` to create an S3 bucket:

```hcl
resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_public_access_block" "my_bucket" {
  bucket = aws_s3_bucket.my_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "my_bucket" {
  bucket = aws_s3_bucket.my_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

### Part 4: Applying the Terraform Configuration

1. Initialize the Terraform working directory:
   ```bash
   terraform init
   ```

2. Review the planned changes:
   ```bash
   terraform plan
   ```

3. Apply the changes:
   ```bash
   terraform apply
   ```

   When prompted, type `yes` to confirm the changes.

### Part 5: Verifying the Resources

1. Check the created IAM policy:
   ```bash
   aws iam get-policy --policy-arn $(terraform output -raw iam_policy_arn)
   ```

2. List the contents of your S3 bucket:
   ```bash
   aws s3 ls s3://$(terraform output -raw s3_bucket_name)
   ```

### Part 6: Clean Up

To avoid unnecessary AWS charges, destroy the created resources when you're done:

```bash
terraform destroy
```

When prompted, type `yes` to confirm the deletion of resources.

### Exercises

1. Modify the IAM policy to allow write access to the S3 bucket. Update the Terraform code and apply the changes.

2. Create a new IAM user and attach the S3 read-only policy to this user using Terraform.

3. Enable server-side encryption for the S3 bucket using AWS Key Management Service (KMS).

4. Set up S3 bucket logging to track all requests made to the S3 bucket.

5. Create a lifecycle rule for the S3 bucket to transition objects to Glacier storage class after 90 days.

### Best Practices

1. Always use the principle of least privilege when creating IAM policies.
2. Enable versioning on S3 buckets to protect against accidental deletions and overwrites.
3. Use strong, unique names for your S3 buckets to avoid naming conflicts.
4. Block public access to S3 buckets unless public access is explicitly required.
5. Use variables in your Terraform configurations to make them more flexible and reusable.
6. Store your Terraform state file securely, preferably using remote state storage like S3 with state locking.
7. In production environments, avoid hardcoding AWS credentials. Instead, use AWS IAM roles, environment variables, or a secure secrets management system.

### Security Note

The method of storing AWS credentials in a `terraform.tfvars` file, as shown in this lab, is for educational purposes only. In real-world scenarios, especially in production environments, it's crucial to use more secure methods of authentication:

- Use IAM roles for EC2 instances or other AWS services.
- Use environment variables or AWS credentials file with appropriate permissions.
- For CI/CD pipelines, use the built-in secrets management of your CI/CD tool.
- Consider using AWS Secrets Manager or HashiCorp Vault for managing secrets.

Always follow your organization's security policies and AWS best practices for managing credentials.

### Conclusion

In this lab, you've learned how to configure AWS credentials in Terraform and use it to create and manage AWS IAM policies and S3 buckets. These skills are crucial for managing access control and data storage in AWS environments. Remember to always follow AWS best practices and regularly review and update your IAM policies and S3 bucket configurations to maintain a secure and efficient cloud infrastructure.
