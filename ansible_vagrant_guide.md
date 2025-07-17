# Using Ansible with Vagrant - Setup and Usage Guide

## Overview
This guide demonstrates how to integrate Ansible with Vagrant for automated infrastructure provisioning and configuration management. Vagrant creates and manages virtual machines while Ansible handles configuration.

## Prerequisites
- VirtualBox or VMware installed
- Vagrant installed
- Ansible installed on host machine
- Basic understanding of Vagrant and Ansible

## What is Vagrant?
Vagrant is a tool for building and managing virtual machine environments. It provides:
- Reproducible development environments
- Consistent VM configurations
- Easy sharing of environments
- Integration with configuration management tools

## Integration Benefits
```mermaid
graph LR
    A[Vagrant] -->|Creates VMs| B[Virtual Machines]
    B -->|Provisions with| C[Ansible]
    C -->|Configures| D[Ready Infrastructure]
    
    style A fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#e1f5fe
```

## 1. Basic Vagrant + Ansible Setup

### Step 1: Create Project Directory
```bash
mkdir ansible-vagrant-demo
cd ansible-vagrant-demo
```

### Step 2: Initialize Vagrant
```bash
# Create basic Vagrantfile
vagrant init ubuntu/focal64
```

### Step 3: Configure Vagrantfile with Ansible
```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  # Base box
  config.vm.box = "ubuntu/focal64"
  
  # VM configuration
  config.vm.hostname = "ansible-managed"
  config.vm.network "private_network", ip: "192.168.56.10"
  
  # VM resources
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 2
    vb.name = "ansible-vagrant-vm"
  end
  
  # Ansible provisioning
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "site.yml"
    ansible.inventory_path = "inventory.ini"
    ansible.limit = "all"
    ansible.verbose = "v"
  end
end
```

### Step 4: Create Ansible Files

#### Create inventory.ini
```bash
cat > inventory.ini << 'EOF'
[vagrant_vms]
ansible-managed ansible_host=192.168.56.10 ansible_user=vagrant

[vagrant_vms:vars]
ansible_ssh_private_key_file=.vagrant/machines/default/virtualbox/private_key
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF
```

#### Create site.yml playbook
```bash
cat > site.yml << 'EOF'
---
- name: Configure Vagrant VM with Ansible
  hosts: vagrant_vms
  become: yes
  
  vars:
    packages:
      - nginx
      - git
      - curl
      - vim
      
  tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
        
    - name: Install packages
      apt:
        name: "{{ packages }}"
        state: present
        
    - name: Create web directory
      file:
        path: /var/www/html
        state: directory
        owner: www-data
        group: www-data
        mode: '0755'
        
    - name: Deploy custom index page
      copy:
        content: |
          <!DOCTYPE html>
          <html>
          <head>
              <title>Vagrant + Ansible Demo</title>
              <style>
                  body { font-family: Arial, sans-serif; margin: 40px; }
                  .header { background: #2E8B57; color: white; padding: 20px; text-align: center; }
                  .info { background: #f0f0f0; padding: 20px; margin: 20px 0; }
              </style>
          </head>
          <body>
              <div class="header">
                  <h1>Vagrant + Ansible Integration</h1>
                  <p>VM provisioned with Vagrant, configured with Ansible</p>
              </div>
              <div class="info">
                  <h3>System Information</h3>
                  <p><strong>Hostname:</strong> {{ ansible_hostname }}</p>
                  <p><strong>OS:</strong> {{ ansible_distribution }} {{ ansible_distribution_version }}</p>
                  <p><strong>IP Address:</strong> {{ ansible_default_ipv4.address }}</p>
                  <p><strong>Provisioned:</strong> {{ ansible_date_time.iso8601 }}</p>
              </div>
          </body>
          </html>
        dest: /var/www/html/index.html
        owner: www-data
        group: www-data
        mode: '0644'
        
    - name: Start and enable nginx
      service:
        name: nginx
        state: started
        enabled: yes
        
    - name: Display access information
      debug:
        msg: |
          VM is ready!
          Access the web server at: http://192.168.56.10
          SSH into VM: vagrant ssh
EOF
```

### Step 5: Start and Provision
```bash
# Start VM and run Ansible provisioning
vagrant up
```

## 2. Multi-VM Environment

### Enhanced Vagrantfile for Multiple VMs
```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  # Define multiple VMs
  config.vm.define "web1" do |web1|
    web1.vm.box = "ubuntu/focal64"
    web1.vm.hostname = "web1"
    web1.vm.network "private_network", ip: "192.168.56.11"
    web1.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
      vb.name = "web1"
    end
  end
  
  config.vm.define "web2" do |web2|
    web2.vm.box = "ubuntu/focal64"
    web2.vm.hostname = "web2"
    web2.vm.network "private_network", ip: "192.168.56.12"
    web2.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
      vb.name = "web2"
    end
  end
  
  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/focal64"
    db.vm.hostname = "database"
    db.vm.network "private_network", ip: "192.168.56.13"
    db.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.name = "database"
    end
    
    # Provision all VMs after the last one is up
    db.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.playbook = "multi_vm_site.yml"
      ansible.inventory_path = "multi_vm_inventory.ini"
      ansible.groups = {
        "webservers" => ["web1", "web2"],
        "databases" => ["db"],
        "all:vars" => {
          "ansible_ssh_private_key_file" => ".vagrant/machines/default/virtualbox/private_key"
        }
      }
    end
  end
end
```

### Multi-VM Inventory
```bash
cat > multi_vm_inventory.ini << 'EOF'
[webservers]
web1 ansible_host=192.168.56.11
web2 ansible_host=192.168.56.12

[databases]
db ansible_host=192.168.56.13

[all:vars]
ansible_user=vagrant
ansible_ssh_private_key_file=.vagrant/machines/default/virtualbox/private_key
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF
```

### Multi-VM Playbook
```bash
cat > multi_vm_site.yml << 'EOF'
---
# Web servers configuration
- name: Configure Web Servers
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
        
    - name: Create load balancer status page
      copy:
        content: |
          <!DOCTYPE html>
          <html>
          <head><title>{{ inventory_hostname }}</title></head>
          <body>
              <h1>Web Server: {{ inventory_hostname }}</h1>
              <p>IP: {{ ansible_default_ipv4.address }}</p>
              <p>Status: Active</p>
          </body>
          </html>
        dest: /var/www/html/index.html
        
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes

# Database server configuration
- name: Configure Database Server
  hosts: databases
  become: yes
  
  tasks:
    - name: Install MySQL
      apt:
        name:
          - mysql-server
          - python3-pymysql
        state: present
        update_cache: yes
        
    - name: Start MySQL
      service:
        name: mysql
        state: started
        enabled: yes
        
    - name: Create application database
      mysql_db:
        name: webapp_db
        state: present
        login_unix_socket: /var/run/mysqld/mysqld.sock
        
    - name: Display database info
      debug:
        msg: "Database server {{ inventory_hostname }} configured with webapp_db"

# Verification tasks
- name: Verify Deployment
  hosts: all
  tasks:
    - name: Check services status
      service_facts:
      
    - name: Display service status
      debug:
        msg: |
          Host: {{ inventory_hostname }}
          Nginx: {{ 'Running' if ansible_facts.services['nginx.service'].state == 'running' else 'Not Running' }}
          MySQL: {{ 'Running' if ansible_facts.services['mysql.service'].state == 'running' else 'Not Available' }}
      when: inventory_hostname in groups['webservers'] or inventory_hostname in groups['databases']
EOF
```

## 3. Vagrant Commands with Ansible

### Basic Operations
```bash
# Start all VMs and provision
vagrant up

# Start specific VM
vagrant up web1

# Re-run Ansible provisioning only
vagrant provision

# Re-provision specific VM
vagrant provision web1

# SSH into VM
vagrant ssh web1

# Check VM status
vagrant status

# Stop VMs
vagrant halt

# Destroy VMs
vagrant destroy
```

### Ansible-specific Operations
```bash
# Run Ansible manually after VMs are up
vagrant up --no-provision
ansible-playbook -i multi_vm_inventory.ini multi_vm_site.yml

# Test connectivity
ansible all -i multi_vm_inventory.ini -m ping

# Run specific tags
ansible-playbook -i multi_vm_inventory.ini multi_vm_site.yml --tags "webserver"
```

## 4. Advanced Configuration

### Ansible Configuration in Vagrantfile
```ruby
config.vm.provision "ansible" do |ansible|
  ansible.playbook = "site.yml"
  ansible.inventory_path = "inventory"
  ansible.limit = "all"
  ansible.verbose = "v"
  ansible.ask_vault_pass = true
  ansible.vault_password_file = "vault_pass.txt"
  ansible.extra_vars = {
    "environment" => "development",
    "app_version" => "1.0.0"
  }
  ansible.tags = ["setup", "configuration"]
  ansible.skip_tags = ["testing"]
  ansible.groups = {
    "webservers" => ["web1", "web2"],
    "databases" => ["db1"]
  }
end
```

### Using Ansible Local Provisioner
```ruby
# Run Ansible inside the VM instead of from host
config.vm.provision "ansible_local" do |ansible|
  ansible.playbook = "local_playbook.yml"
  ansible.install = true
  ansible.install_mode = "pip"
  ansible.version = "latest"
end
```

## 5. Development Workflow

### Project Structure
```
ansible-vagrant-demo/
├── Vagrantfile
├── site.yml
├── inventory.ini
├── group_vars/
│   ├── webservers.yml
│   └── databases.yml
├── host_vars/
│   └── web1.yml
├── roles/
│   ├── webserver/
│   └── database/
└── files/
    └── app_configs/
```

### Development Commands
```bash
# Quick development cycle
vagrant up                    # Create and provision
# Make changes to playbooks
vagrant provision             # Re-run Ansible
vagrant ssh web1              # Test changes
vagrant halt && vagrant up    # Full restart if needed
```

### Testing and Debugging
```bash
# Test Ansible syntax
ansible-playbook --syntax-check site.yml

# Run in check mode
ansible-playbook -i inventory.ini site.yml --check

# Verbose output
vagrant provision --debug

# Manual Ansible execution with verbosity
ansible-playbook -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory site.yml -vvv
```

## 6. Real-world Example: LAMP Stack

### Complete LAMP Stack Setup
```bash
cat > lamp_stack.yml << 'EOF'
---
- name: Deploy LAMP Stack on Vagrant
  hosts: all
  become: yes
  vars:
    mysql_root_password: "vagrant123"
    
  tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        
    - name: Install LAMP packages
      apt:
        name:
          - apache2
          - mysql-server
          - php
          - php-mysql
          - libapache2-mod-php
          - python3-pymysql
        state: present
        
    - name: Start services
      service:
        name: "{{ item }}"
        state: started
        enabled: yes
      loop:
        - apache2
        - mysql
        
    - name: Set MySQL root password
      mysql_user:
        name: root
        password: "{{ mysql_root_password }}"
        login_unix_socket: /var/run/mysqld/mysqld.sock
        
    - name: Create PHP test page
      copy:
        content: |
          <?php
          echo "<h1>LAMP Stack on Vagrant</h1>";
          echo "<p>PHP Version: " . phpversion() . "</p>";
          echo "<p>Server: " . gethostname() . "</p>";
          
          // Test MySQL connection
          $connection = new mysqli("localhost", "root", "{{ mysql_root_password }}");
          if ($connection->connect_error) {
              echo "<p style='color: red;'>MySQL Connection Failed</p>";
          } else {
              echo "<p style='color: green;'>MySQL Connection Successful</p>";
          }
          $connection->close();
          ?>
        dest: /var/www/html/test.php
        
    - name: Remove default Apache page
      file:
        path: /var/www/html/index.html
        state: absent
        
    - name: Create custom index
      copy:
        content: |
          <html>
          <head><title>Vagrant LAMP Stack</title></head>
          <body>
              <h1>Welcome to Vagrant LAMP Stack</h1>
              <p><a href="test.php">Test PHP and MySQL</a></p>
          </body>
          </html>
        dest: /var/www/html/index.html
EOF
```

## 7. Troubleshooting

### Common Issues and Solutions

#### SSH Key Issues
```bash
# If SSH key problems occur
vagrant ssh-config > ssh_config
ansible all -i inventory.ini -m ping --ssh-common-args="-F ssh_config"
```

#### Network Connectivity
```bash
# Test network from host
ping 192.168.56.10

# Check Vagrant network status
vagrant port
```

#### Provisioning Failures
```bash
# Re-run with verbose output
vagrant provision --debug

# Manual Ansible run
vagrant ssh -c "cd /vagrant && ansible-playbook site.yml"
```

### Debug Commands
```bash
# Check Vagrant status
vagrant global-status

# View Vagrant logs
vagrant up --debug

# Check VM network configuration
vagrant ssh -c "ip addr show"

# Test Ansible connectivity
ansible all -i inventory.ini -m setup --tree /tmp/facts
```

## Summary

This guide demonstrated:
- ✅ **Basic Integration**: Single VM with Ansible provisioning
- ✅ **Multi-VM Setup**: Complex environments with grouped VMs
- ✅ **Development Workflow**: Efficient development and testing cycle
- ✅ **Real-world Example**: Complete LAMP stack deployment
- ✅ **Troubleshooting**: Common issues and solutions

### Key Benefits of Vagrant + Ansible:
- **Reproducible Environments**: Consistent development setups
- **Team Collaboration**: Shareable VM configurations
- **Testing Infrastructure**: Safe testing of Ansible playbooks
- **Rapid Prototyping**: Quick infrastructure experiments
- **Production Parity**: Development environments matching production

### Next Steps:
- Explore Vagrant multi-provider setups (AWS, VMware)
- Integrate with CI/CD pipelines
- Use Vagrant for Ansible role testing
- Implement infrastructure testing with Test Kitchen