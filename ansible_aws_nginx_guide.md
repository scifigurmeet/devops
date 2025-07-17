# Complete Beginner's Guide: Ansible + AWS + Nginx

## What You'll Build
By the end of this guide, you'll have:
- An EC2 server running on AWS
- Nginx web server installed and running
- A custom webpage accessible from the internet
- All deployed using Ansible automation

## Prerequisites
- A computer with internet access
- An AWS account (free tier is fine)
- Basic command line knowledge

---

## Part 1: Setting Up Your Local Environment

### Step 1: Install Python and pip

#### On Windows:
1. Go to https://python.org/downloads/
2. Download Python 3.8 or newer
3. Run the installer and **check "Add Python to PATH"**
4. Open Command Prompt and verify: `python --version`

#### On macOS:
1. Install Homebrew first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Install Python:
```bash
brew install python3
```
3. Verify: `python3 --version`

#### On Ubuntu/Linux:
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

### Step 2: Create Project Folder
```bash
# Create a new folder for your project
mkdir my-ansible-project
cd my-ansible-project

# On Windows, use:
# mkdir my-ansible-project
# cd my-ansible-project
```

### Step 3: Install Required Software
```bash
# Install Ansible and AWS tools
pip install ansible boto3 botocore

# Install AWS collection for Ansible
ansible-galaxy collection install amazon.aws

# Verify installation
ansible --version
```

---

## Part 2: AWS Account Setup

### Step 4: Create AWS Account
1. Go to https://aws.amazon.com
2. Click "Create an AWS Account"
3. Follow the signup process (you'll need a credit card, but we'll use free tier)

### Step 5: Create AWS User with Permissions
1. Log into AWS Console
2. Go to IAM service
3. Click "Users" → "Add User"
4. Username: `ansible-user`
5. Access type: Check "Programmatic access"
6. Click "Next: Permissions"
7. Click "Attach existing policies directly"
8. Search and select: `AmazonEC2FullAccess`
9. Click "Next" → "Next" → "Create User"
10. **IMPORTANT**: Copy the Access Key ID and Secret Access Key (you won't see them again!)

### Step 6: Install and Configure AWS CLI
```bash
# Install AWS CLI
pip install awscli

# Configure AWS with your credentials
aws configure
```

When prompted, enter:
- **AWS Access Key ID**: [Paste your Access Key from Step 5]
- **AWS Secret Access Key**: [Paste your Secret Key from Step 5]
- **Default region name**: `us-east-1`
- **Default output format**: `json`

### Step 7: Test AWS Connection
```bash
# This should list your AWS regions
aws ec2 describe-regions
```

### Step 8: Create SSH Key for EC2
```bash
# Create SSH key pair
aws ec2 create-key-pair --key-name my-ansible-key --query 'KeyMaterial' --output text > my-ansible-key.pem

# Set correct permissions (Linux/Mac)
chmod 400 my-ansible-key.pem

# On Windows, use PowerShell as Administrator:
# icacls my-ansible-key.pem /inheritance:r /grant:r "%username%:R"
```

---

## Part 3: Create Ansible Configuration

### Step 9: Create ansible.cfg File
Create a file named `ansible.cfg`:
```ini
[defaults]
host_key_checking = False
private_key_file = ./my-ansible-key.pem
remote_user = ec2-user
inventory = inventory.yml
timeout = 30

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
```

### Step 10: Create Dynamic Inventory File
Create a file named `inventory.yml`:
```yaml
plugin: aws_ec2
regions:
  - us-east-1
filters:
  instance-state-name: running
  "tag:Name": my-nginx-server
compose:
  ansible_host: public_ip_address
keyed_groups:
  - key: tags.Name
    prefix: tag_name
```

---

## Part 4: Create the Deployment Playbook

### Step 11: Create Main Playbook
Create a file named `deploy-nginx.yml`:
```yaml
---
# First play: Create the EC2 instance
- name: Create EC2 Instance
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    - name: Create security group for web server
      amazon.aws.ec2_security_group:
        name: nginx-security-group
        description: Security group for nginx web server
        region: us-east-1
        rules:
          - proto: tcp
            ports:
              - 22  # SSH
            cidr_ip: 0.0.0.0/0
            rule_desc: Allow SSH
          - proto: tcp
            ports:
              - 80  # HTTP
            cidr_ip: 0.0.0.0/0
            rule_desc: Allow HTTP
        tags:
          Name: nginx-security-group

    - name: Launch EC2 instance
      amazon.aws.ec2_instance:
        name: my-nginx-server
        image_id: ami-0c02fb55956c7d316  # Amazon Linux 2
        instance_type: t2.micro  # Free tier eligible
        key_name: my-ansible-key
        security_groups:
          - nginx-security-group
        region: us-east-1
        wait: true
        wait_timeout: 300
        tags:
          Name: my-nginx-server
          Project: ansible-tutorial
      register: ec2_result

    - name: Show instance information
      debug:
        msg: 
          - "Instance created successfully!"
          - "Instance ID: {{ ec2_result.instances[0].instance_id }}"
          - "Public IP: {{ ec2_result.instances[0].public_ip_address }}"

    - name: Wait for SSH to be available
      wait_for:
        host: "{{ ec2_result.instances[0].public_ip_address }}"
        port: 22
        delay: 60
        timeout: 300
        state: started
      vars:
        ansible_connection: local

# Second play: Install and configure nginx
- name: Install and Configure Nginx
  hosts: aws_ec2
  become: yes  # Run commands as root
  gather_facts: yes
  
  tasks:
    - name: Update package manager
      yum:
        update_cache: yes

    - name: Install nginx
      yum:
        name: nginx
        state: present

    - name: Start and enable nginx
      systemd:
        name: nginx
        state: started
        enabled: yes

    - name: Create custom webpage
      copy:
        content: |
          <!DOCTYPE html>
          <html>
          <head>
              <title>My First Ansible Deployment!</title>
              <style>
                  body { font-family: Arial; text-align: center; margin-top: 50px; }
                  h1 { color: #2e8b57; }
                  .info { background: #f0f0f0; padding: 20px; margin: 20px; }
              </style>
          </head>
          <body>
              <h1>🎉 Success! Nginx is running! 🎉</h1>
              <div class="info">
                  <p><strong>Server:</strong> {{ inventory_hostname }}</p>
                  <p><strong>Deployed with:</strong> Ansible on AWS</p>
                  <p><strong>Date:</strong> {{ ansible_date_time.date }}</p>
              </div>
              <p>This webpage was automatically deployed using Ansible!</p>
          </body>
          </html>
        dest: /usr/share/nginx/html/index.html
        owner: nginx
        group: nginx
        mode: '0644'

    - name: Restart nginx to apply changes
      systemd:
        name: nginx
        state: restarted

    - name: Show success message
      debug:
        msg: 
          - "Nginx installed and configured successfully!"
          - "Visit http://{{ ansible_default_ipv4.address }} to see your website"
```

---

## Part 5: Deploy Everything

### Step 12: Run the Playbook
```bash
# Deploy everything with one command
ansible-playbook deploy-nginx.yml -v
```

This will:
1. Create a security group
2. Launch an EC2 instance
3. Wait for it to be ready
4. Install nginx
5. Create a custom webpage

### Step 13: Get Your Website URL
```bash
# Get the public IP of your server
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=my-nginx-server" "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].PublicIpAddress' \
  --output text
```

### Step 14: Test Your Website
1. Copy the IP address from Step 13
2. Open your web browser
3. Go to `http://[YOUR-IP-ADDRESS]`
4. You should see your custom webpage!

---

## Part 6: Verify and Manage

### Step 15: Check What You Created
```bash
# List your EC2 instances
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' --output table

# Test Ansible can connect to your server
ansible aws_ec2 -m ping
```

### Step 16: Make Changes (Optional)
Edit the HTML content in `deploy-nginx.yml` and run again:
```bash
# Re-run just the nginx configuration
ansible-playbook deploy-nginx.yml --tags nginx -v
```

---

## Part 7: Clean Up (Important!)

### Step 17: Delete Everything to Avoid Charges
```bash
# Get instance ID
INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=my-nginx-server" --query 'Reservations[*].Instances[*].InstanceId' --output text)

# Terminate the instance
aws ec2 terminate-instances --instance-ids $INSTANCE_ID

# Delete the security group (wait a few minutes after terminating)
aws ec2 delete-security-group --group-name nginx-security-group

# Delete the key pair
aws ec2 delete-key-pair --key-name my-ansible-key

# Remove local key file
rm my-ansible-key.pem
```

---

## Troubleshooting

### Common Issues:

**1. "Permission denied" when connecting:**
- Check your key file permissions: `chmod 400 my-ansible-key.pem`
- Verify your AWS credentials: `aws sts get-caller-identity`

**2. "No instances found":**
- Wait 2-3 minutes after creating the instance
- Check AWS console to see if instance is running

**3. "Module not found" errors:**
- Reinstall: `pip install --upgrade ansible boto3`
- Check: `ansible-galaxy collection list | grep amazon`

**4. Cannot access website:**
- Check security group allows port 80
- Verify nginx is running: `ansible aws_ec2 -m shell -a "sudo systemctl status nginx"`

### Get Help:
- Check AWS Free Tier usage in AWS Console
- Review Ansible documentation: https://docs.ansible.com
- AWS documentation: https://docs.aws.amazon.com

## Summary
Congratulations! You've successfully:
✅ Set up Ansible and AWS CLI  
✅ Created an EC2 instance automatically  
✅ Installed and configured nginx  
✅ Deployed a custom webpage  
✅ Learned infrastructure as code basics  

This is the foundation for more complex deployments!