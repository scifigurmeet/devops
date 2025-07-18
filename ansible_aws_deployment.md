# Ansible AWS EC2 Deployment - Minimal Example

## Prerequisites

1. **AWS Account** with programmatic access
2. **AWS CLI** installed and configured
3. **Ansible** installed with AWS collection
4. **Python boto3** library

## Setup Commands

```bash
# Install Ansible and AWS dependencies
pip install ansible boto3 botocore

# Install Ansible AWS collection
ansible-galaxy collection install amazon.aws

# Configure AWS credentials (run aws configure)
aws configure
```

## Project Structure

```
ansible-aws-deploy/
├── inventory.yml
├── playbook.yml
├── group_vars/
│   └── all.yml
└── app/
    └── index.html
```

## Step 1: Create group_vars/all.yml

```yaml
---
# AWS Configuration
aws_region: us-east-1
key_name: my-ansible-key  # Change this to your key pair name
instance_type: t2.micro
ami_id: ami-0c02fb55956c7d316  # Amazon Linux 2 AMI (us-east-1)
security_group_name: ansible-web-sg

# Application Configuration
app_port: 80
```

## Step 2: Create inventory.yml

```yaml
---
all:
  children:
    aws_instances:
      hosts:
        web_server:
          ansible_host: "{{ hostvars['localhost']['ec2_public_ip'] }}"
          ansible_user: ec2-user
          ansible_ssh_private_key_file: ~/.ssh/{{ key_name }}.pem
          ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
```

## Step 3: Create app/index.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Ansible AWS Deployment</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
        h1 { color: #232f3e; }
        .container { max-width: 600px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Success!</h1>
        <h2>Web App Deployed with Ansible on AWS</h2>
        <p>This application was automatically deployed to EC2 using Ansible.</p>
        <p><strong>Server:</strong> {{ ansible_hostname }}</p>
        <p><strong>Deployed at:</strong> {{ ansible_date_time.iso8601 }}</p>
    </div>
</body>
</html>
```

## Step 4: Create playbook.yml

```yaml
---
- name: Deploy Web Application to AWS EC2
  hosts: localhost
  gather_facts: no
  vars:
    ansible_python_interpreter: "{{ ansible_playbook_python }}"
  
  tasks:
    - name: Create security group
      amazon.aws.ec2_security_group:
        name: "{{ security_group_name }}"
        description: "Security group for web application"
        region: "{{ aws_region }}"
        rules:
          - proto: tcp
            ports:
              - 22
              - 80
            cidr_ip: 0.0.0.0/0
        tags:
          Name: "{{ security_group_name }}"
    
    - name: Launch EC2 instance
      amazon.aws.ec2_instance:
        name: "ansible-web-server"
        key_name: "{{ key_name }}"
        instance_type: "{{ instance_type }}"
        image_id: "{{ ami_id }}"
        region: "{{ aws_region }}"
        security_group: "{{ security_group_name }}"
        wait: true
        wait_timeout: 300
        tags:
          Environment: demo
          Application: web-app
      register: ec2_result
    
    - name: Set EC2 public IP fact
      set_fact:
        ec2_public_ip: "{{ ec2_result.instances[0].public_ip_address }}"
    
    - name: Wait for SSH to be available
      wait_for:
        host: "{{ ec2_public_ip }}"
        port: 22
        timeout: 300
        state: started
    
    - name: Add EC2 instance to inventory
      add_host:
        name: web_server
        ansible_host: "{{ ec2_public_ip }}"
        ansible_user: ec2-user
        ansible_ssh_private_key_file: "~/.ssh/{{ key_name }}.pem"
        ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
        groups: aws_instances

- name: Configure and Deploy Application
  hosts: aws_instances
  become: yes
  gather_facts: yes
  
  tasks:
    - name: Update system packages
      yum:
        name: '*'
        state: latest
        update_cache: yes
    
    - name: Install Apache web server
      yum:
        name: httpd
        state: present
    
    - name: Start and enable Apache
      service:
        name: httpd
        state: started
        enabled: yes
    
    - name: Deploy application files
      template:
        src: app/index.html
        dest: /var/www/html/index.html
        owner: apache
        group: apache
        mode: '0644'
    
    - name: Restart Apache
      service:
        name: httpd
        state: restarted
    
    - name: Display application URL
      debug:
        msg: "Application deployed! Visit: http://{{ ansible_host }}"
```

## Step 5: Before Running - AWS Setup

1. **Create AWS Key Pair**:
   ```bash
   # In AWS Console: EC2 → Key Pairs → Create Key Pair
   # Name it 'my-ansible-key' and download the .pem file
   # Move it to ~/.ssh/ and set permissions
   chmod 400 ~/.ssh/my-ansible-key.pem
   ```

2. **Configure AWS Credentials**:
   ```bash
   aws configure
   # Enter your AWS Access Key ID
   # Enter your AWS Secret Access Key
   # Enter region: us-east-1
   # Enter output format: json
   ```

## Step 6: Deploy Commands

```bash
# Navigate to project directory
cd ansible-aws-deploy

# Run the deployment
ansible-playbook -i inventory.yml playbook.yml

# Check deployment status
ansible -i inventory.yml aws_instances -m ping

# Clean up resources when done
ansible-playbook -i inventory.yml cleanup.yml
```

## Step 7: Create cleanup.yml (Optional)

```yaml
---
- name: Clean up AWS resources
  hosts: localhost
  gather_facts: no
  vars:
    ansible_python_interpreter: "{{ ansible_playbook_python }}"
  
  tasks:
    - name: Terminate EC2 instances
      amazon.aws.ec2_instance:
        region: "{{ aws_region }}"
        filters:
          "tag:Name": "ansible-web-server"
        state: terminated
    
    - name: Delete security group
      amazon.aws.ec2_security_group:
        name: "{{ security_group_name }}"
        region: "{{ aws_region }}"
        state: absent
```

## Expected Output

After running the playbook, you'll get:
- A running EC2 instance with Apache
- Your web application accessible via public IP
- Security group with HTTP and SSH access
- Automatic server configuration and app deployment

## Key Features Demonstrated

- **Infrastructure Provisioning**: Creates EC2 instance and security group
- **Configuration Management**: Installs and configures Apache
- **Application Deployment**: Deploys HTML application
- **Dynamic Inventory**: Adds created instance to Ansible inventory
- **Idempotency**: Can run multiple times safely

## Costs

This uses t2.micro instances which are free tier eligible. Remember to run cleanup when done to avoid charges!