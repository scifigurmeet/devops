# Complete Ansible Docker Setup Guide

## Overview
This guide creates a minimal Ansible setup with Docker Compose featuring one master node and two managed nodes, with manual file creation inside containers to avoid volume mapping issues.

## Prerequisites
- Docker and Docker Compose installed
- Basic understanding of Docker and Ansible

## Directory Structure
```
ansible-docker-demo/
├── docker-compose.yml
├── Dockerfile.master
└── Dockerfile.node
```

## File Contents

### docker-compose.yml
```yaml
version: '3.8'

services:
  ansible-master:
    build:
      context: .
      dockerfile: Dockerfile.master
    container_name: ansible-master
    hostname: ansible-master
    networks:
      - ansible-network
    stdin_open: true
    tty: true
    depends_on:
      - node1
      - node2

  node1:
    build:
      context: .
      dockerfile: Dockerfile.node
    container_name: node1
    hostname: node1
    networks:
      - ansible-network
    stdin_open: true
    tty: true

  node2:
    build:
      context: .
      dockerfile: Dockerfile.node
    container_name: node2
    hostname: node2
    networks:
      - ansible-network
    stdin_open: true
    tty: true

networks:
  ansible-network:
    driver: bridge
```

### Dockerfile.master
```dockerfile
FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openssh-client \
    sshpass \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install Ansible
RUN pip3 install ansible

# Create ansible user
RUN useradd -m -s /bin/bash ansible

# Create ansible working directory with proper permissions
RUN mkdir -p /home/ansible/ansible-work && \
    chown ansible:ansible /home/ansible/ansible-work && \
    chmod 755 /home/ansible/ansible-work

# Switch to ansible user
USER ansible
WORKDIR /home/ansible

# Create .ssh directory
RUN mkdir -p /home/ansible/.ssh

# Set working directory
WORKDIR /home/ansible/ansible-work

CMD ["/bin/bash"]
```

### Dockerfile.node
```dockerfile
FROM ubuntu:22.04

# Install SSH server and other utilities
RUN apt-get update && apt-get install -y \
    openssh-server \
    python3 \
    sudo \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Create ansible user with password
RUN useradd -m -s /bin/bash ansible && \
    echo 'ansible:ansible123' | chpasswd && \
    usermod -aG sudo ansible

# Allow ansible user to sudo without password
RUN echo 'ansible ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Configure SSH
RUN mkdir /var/run/sshd && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]
```

## Step-by-Step Instructions

### Step 1: Create Project Directory
```bash
mkdir ansible-docker-demo
cd ansible-docker-demo
```

### Step 2: Create Docker Files
Create the three files above (`docker-compose.yml`, `Dockerfile.master`, `Dockerfile.node`) in your project directory.

### Step 3: Start the Containers
```bash
# Build and start all containers
docker-compose up -d

# Verify all containers are running
docker-compose ps
```

Expected output:
```
NAME              IMAGE                           COMMAND                  SERVICE           CREATED          STATUS          PORTS
ansible-master    ansible-docker-demo-ansible-master   "/bin/bash"               ansible-master    2 minutes ago    Up 2 minutes
node1             ansible-docker-demo-node1             "/usr/sbin/sshd -D"       node1             2 minutes ago    Up 2 minutes    22/tcp
node2             ansible-docker-demo-node2             "/usr/sbin/sshd -D"       node2             2 minutes ago    Up 2 minutes    22/tcp
```

### Step 4: Connect to Ansible Master
```bash
# Connect to the ansible-master container
docker-compose exec ansible-master bash

OR

#alternative command
docker exec -it ansible-master bash
```

You should now be in the container as the ansible user at `/home/ansible/ansible-work`.

### Step 5: Create Ansible Configuration Files Inside the Container

#### Create inventory.ini
```bash
cat > inventory.ini << 'EOF'
[managed_nodes]
node1 ansible_host=node1 ansible_user=ansible ansible_ssh_pass=ansible123
node2 ansible_host=node2 ansible_user=ansible ansible_ssh_pass=ansible123

[all:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF
```

#### Create ansible.cfg
```bash
cat > ansible.cfg << 'EOF'
[defaults]
inventory = inventory.ini
host_key_checking = False
deprecation_warnings = False
timeout = 30

[ssh_connection]
ssh_args = -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
EOF
```

#### Create a sample playbook
```bash
cat > hello-world.yml << 'EOF'
---
- name: Hello World Playbook
  hosts: managed_nodes
  become: yes
  tasks:
    - name: Print hello message
      debug:
        msg: "Hello from {{ inventory_hostname }}!"
    
    - name: Create a test file
      file:
        path: /tmp/ansible-test.txt
        state: touch
        mode: '0644'
    
    - name: Write content to test file
      copy:
        content: "This file was created by Ansible on {{ ansible_date_time.date }} at {{ ansible_date_time.time }}"
        dest: /tmp/ansible-test.txt
    
    - name: Install a package (vim-tiny)
      apt:
        name: vim-tiny
        state: present
        update_cache: yes
    
    - name: Display system information
      debug:
        msg: "System: {{ ansible_system }} | Architecture: {{ ansible_architecture }} | Distribution: {{ ansible_distribution }}"
EOF
```

### Step 6: Verify File Creation
```bash
# Check that all files were created
ls -la

# Verify file permissions
ls -la inventory.ini ansible.cfg hello-world.yml
```

### Step 7: Test Ansible Connectivity
```bash
# Test connection to all managed nodes
ansible all -m ping
```

Expected output:
```
node1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
node2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

### Step 8: Run the Sample Playbook
```bash
# Run the hello-world playbook
ansible-playbook hello-world.yml
```

### Step 9: Test Additional Ansible Commands
```bash
# Get system information from all nodes
ansible all -m setup -a "filter=ansible_os_family"

# Run a command on all nodes
ansible all -m shell -a "uptime"

# Check if the test file was created
ansible all -m shell -a "cat /tmp/ansible-test.txt"

# List installed packages
ansible all -m shell -a "dpkg -l | grep vim"
```

## Common Ansible Commands to Try

### Basic Commands
```bash
# Ping all hosts
ansible all -m ping

# Ping specific host
ansible node1 -m ping

# Get all facts about hosts
ansible all -m setup

# Get specific facts
ansible all -m setup -a "filter=ansible_distribution*"
```

### File Operations
```bash
# Create a directory
ansible all -m file -a "path=/tmp/test-dir state=directory"

# Create a file with content
ansible all -m copy -a "content='Hello World' dest=/tmp/hello.txt"

# Check file exists
ansible all -m stat -a "path=/tmp/hello.txt"

# Remove a file
ansible all -m file -a "path=/tmp/hello.txt state=absent"
```

### Package Management
```bash
# Update package cache
ansible all -m apt -a "update_cache=yes" --become

# Install a package
ansible all -m apt -a "name=htop state=present" --become

# Remove a package
ansible all -m apt -a "name=htop state=absent" --become
```

### Service Management
```bash
# Check service status
ansible all -m service -a "name=ssh state=started" --become

# Restart a service
ansible all -m service -a "name=ssh state=restarted" --become
```

### Running Shell Commands
```bash
# Execute shell command
ansible all -m shell -a "df -h"

# Execute command with sudo
ansible all -m shell -a "systemctl status ssh" --become

# Execute command and register output
ansible all -m shell -a "date" --become
```

## Troubleshooting

### If SSH connection fails:
1. **Check if nodes are running:**
   ```bash
   # Exit container first
   exit
   docker-compose ps
   ```

2. **Verify SSH service on nodes:**
   ```bash
   docker-compose exec node1 service ssh status
   ```

3. **Test manual SSH connection:**
   ```bash
   docker-compose exec ansible-master bash
   ssh ansible@node1  # Password: ansible123
   ```

### If Ansible commands fail:
1. **Check inventory syntax:**
   ```bash
   ansible-inventory --list
   ```

2. **Test with verbose output:**
   ```bash
   ansible all -m ping -v
   ```

3. **Verify ansible.cfg is being read:**
   ```bash
   ansible --version
   ```

### If containers don't start:
1. **Check container logs:**
   ```bash
   docker-compose logs ansible-master
   docker-compose logs node1
   docker-compose logs node2
   ```

2. **Rebuild containers:**
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

## Security Notes
- This setup uses password authentication for simplicity
- The ansible user has passwordless sudo access
- SSH host key checking is disabled
- **This configuration is for learning purposes only - not recommended for production**

## Clean Up
```bash
# Exit container
exit

# Stop and remove containers
docker-compose down

# Remove images (optional)
docker-compose down --rmi all

# Remove volumes (optional)
docker system prune -a
```

## Key Configuration Details

- **Master Node**: Ubuntu 22.04 with Ansible installed
- **Managed Nodes**: Ubuntu 22.04 with SSH server
- **Authentication**: Password-based (ansible/ansible123)
- **Network**: All containers on same Docker network
- **Working Directory**: `/home/ansible/ansible-work`
- **Ansible User**: Has sudo privileges without password

This setup provides a complete, working Ansible environment for learning and experimentation without the complexity of SSH key management or volume mounting issues.
