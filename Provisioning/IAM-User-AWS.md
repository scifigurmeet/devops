# Beginner's Guide to AWS IAM Users

## Table of Contents
1. [Introduction to IAM Users](#introduction-to-iam-users)
2. [IAM Users vs. Root User](#iam-users-vs-root-user)
3. [Creating an IAM User](#creating-an-iam-user)
4. [Using an IAM User](#using-an-iam-user)
5. [Best Practices](#best-practices)

## 1. Introduction to IAM Users

IAM (Identity and Access Management) is a service provided by Amazon Web Services (AWS) that helps you manage access to your AWS resources. An IAM user is an entity that you create in AWS to represent the person or application that uses it to interact with AWS.

IAM users are essential for providing secure and granular access to your AWS resources, allowing you to control and audit who can do what within your AWS environment.

## 2. IAM Users vs. Root User

### Root User
- The root user is created when you first set up your AWS account.
- It has complete access to all AWS services and resources.
- It's the only user that can perform certain tasks like changing account settings.

### IAM User
- Created within your AWS account to represent a person or application.
- Has limited permissions based on what you grant.
- Can be created, modified, or deleted as needed.

Key differences:
1. **Access Level**: Root has full access; IAM users have limited, customizable access.
2. **Security**: Using IAM users is more secure as it follows the principle of least privilege.
3. **Accountability**: IAM users provide better auditing and tracking of actions.

## 3. Creating an IAM User

Follow these steps to create an IAM user:

1. Sign in to the AWS Management Console.
2. Navigate to the IAM service.
3. In the navigation pane, choose "Users" and then "Add user".
4. Set the user details:
   - User name
   - Access type (AWS Management Console access and/or Programmatic access)
5. Set permissions:
   - Add user to a group (recommended)
   - Copy permissions from an existing user
   - Attach existing policies directly
6. Review and create the user.
7. Download or securely store the access key ID and secret access key (if you selected programmatic access).

## 4. Using an IAM User

### Console Access
1. Go to your AWS account's IAM user sign-in URL.
2. Enter your IAM user name and password.
3. You now have access based on your assigned permissions.

### Programmatic Access
1. Use the access key ID and secret access key with AWS SDK or CLI.
2. Configure your application or CLI with these credentials.
3. The user can now make API calls to AWS services as allowed by their permissions.

## 5. Best Practices

1. **Use IAM users instead of the root user** for everyday tasks.
2. **Grant least privilege**: Give users only the permissions they need.
3. **Use groups** to assign permissions to multiple users.
4. **Enable MFA** (Multi-Factor Authentication) for added security.
5. **Regularly rotate credentials** like access keys and passwords.
6. **Use IAM roles** for applications running on EC2 instances.
7. **Monitor user activity** using AWS CloudTrail.

By following these practices and understanding how to create and use IAM users, you can significantly enhance the security and manageability of your AWS resources.
