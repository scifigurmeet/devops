# Vagrant + Ansible Minimal Example for Windows 10

## Prerequisites

1. **Install VirtualBox**: Download from https://www.virtualbox.org/
2. **Install Vagrant**: Download from https://www.vagrantup.com/
3. **Install Git for Windows**: Download from https://git-scm.com/ (includes SSH)

## Project Structure

Create a new folder for your project and add these files:

```
vagrant-ansible-example/
├── Vagrantfile
├── playbook.yml
└── README.md
```

## Step 1: Create Vagrantfile

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end
  
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
  end
end
```

## Step 2: Create Ansible Playbook

```yaml
---
- name: Install and start nginx
  hosts: all
  become: yes
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
    
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Start nginx service
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: Create custom index page
      copy:
        content: |
          <html>
          <head><title>Hello from Vagrant + Ansible</title></head>
          <body>
          <h1>Success! Nginx installed via Ansible</h1>
          <p>This server was provisioned using Vagrant and Ansible.</p>
          </body>
          </html>
        dest: /var/www/html/index.html
        mode: '0644'
      notify: restart nginx
  
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

## Step 3: Commands to Run

Open **Command Prompt** or **PowerShell** as Administrator and navigate to your project folder:

```bash
# Navigate to project directory
cd path\to\vagrant-ansible-example

# Start the VM and run provisioning
vagrant up

# Check VM status
vagrant status

# SSH into the VM (optional)
vagrant ssh

# Destroy the VM when done
vagrant destroy
```

## Step 4: Verify Everything Works

1. After `vagrant up` completes, open your browser
2. Go to `http://localhost:8080`
3. You should see the custom HTML page served by nginx

## Key Points

- **ansible_local**: We use `ansible_local` provisioner which installs Ansible inside the VM, avoiding Windows compatibility issues
- **Port forwarding**: VM's port 80 is forwarded to host's port 8080
- **Minimal setup**: Just nginx installation with a custom index page
- **Idempotent**: Running `vagrant provision` multiple times is safe

## Troubleshooting

**If you get SSH errors on Windows:**
```bash
# Enable SSH agent
ssh-agent
```

**To re-run just the Ansible provisioning:**
```bash
vagrant provision
```

**To see detailed output:**
```bash
vagrant up --debug
```

This example demonstrates the core Vagrant + Ansible workflow: infrastructure as code with automated configuration management.