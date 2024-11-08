# Ansible Beginner's Guide with WSL

## Introduction

Welcome to this beginner's guide on Ansible! This document is designed for DevOps students who have Windows Subsystem for Linux (WSL) installed on their Windows PCs. We'll explore Ansible through practical exercises, each with a clear intention, explanation, and interpretation.

## What is Ansible?

Ansible is an open-source automation tool that simplifies configuration management, application deployment, and task automation. It uses a declarative language to describe system configurations and a push-based mechanism to apply changes.

## Setup

Before we begin, ensure you have Ubuntu WSL installed on your Windows machine. If you haven't installed it yet, you can do so by:

1. Opening PowerShell as Administrator and running:
   ```powershell
   wsl --install -d Ubuntu
   ```

2. After installation, launch Ubuntu WSL and create a user account when prompted.

## Setup Docker Nodes
Create a new folder on the desktop and create docker-compose.yml file and after saving it run the `docker-compose up -d` command.
```yml
version: '3'
services:
  control:
    image: ubuntu:latest
    container_name: ansible-control
    volumes:
      - ./ansible:/ansible
    tty: true

  node1:
    image: ubuntu:latest
    container_name: ansible-node1
    tty: true

  node2:
    image: ubuntu:latest
    container_name: ansible-node2
    tty: true
```

## Exercise 1: Installing Ansible and Basic Configuration

**Intention:** Set up Ansible on Ubuntu WSL and configure it for local execution.

**Why:** This exercise demonstrates the basic setup required for Ansible and introduces the concept of inventory.

**Steps:**

1. Update your Ubuntu WSL system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install Ansible:
   ```bash
   sudo apt install -y ansible
   ```

3. Create a directory for your Ansible project:
   ```bash
   mkdir ~/ansible
   cd ~/ansible
   ```

4. Create the inventory file `~/ansible/inventory.ini`:
   ```ini
   [local]
   localhost ansible_connection=local
   ```

5. Create the Ansible configuration file `~/ansible/ansible.cfg`:
   ```ini
   [defaults]
   inventory = inventory.ini
   host_key_checking = False
   ```

**What it demonstrates:** This exercise shows how to set up Ansible for local execution using WSL.

**Interpretation:** The inventory file defines localhost as the managed node, while the configuration file sets global options for Ansible.

**Innovative fact:** Using `ansible_connection=local` allows Ansible to execute tasks directly on the WSL instance without requiring SSH.

## Exercise 2: Your First Ansible Playbook

**Intention:** Create and run a simple Ansible playbook to install and configure a web server.

**Why:** This exercise introduces the concept of playbooks, which are Ansible's configuration, deployment, and orchestration language.

**Steps:**

1. Create a playbook file `~/ansible/webserver.yml`:
   ```yaml
   ---
   - hosts: local
     become: yes
     tasks:
       - name: Install Apache
         apt:
           name: apache2
           state: present

       - name: Start Apache service
         service:
           name: apache2
           state: started
           enabled: yes

       - name: Create a custom index.html
         copy:
           content: "Hello from WSL Ubuntu!\n"
           dest: /var/www/html/index.html
   ```

2. Run the playbook:
   ```bash
   ansible-playbook webserver.yml
   ```

**What it demonstrates:** This exercise shows how to define tasks in a playbook and apply them locally.

**Interpretation:** The playbook installs Apache, ensures it's running, and creates a custom homepage on your WSL instance.

**Innovative fact:** You can access the Apache server from Windows by navigating to `http://localhost` in your browser, as WSL automatically forwards ports to Windows.

## Exercise 3: Using Ansible Roles

**Intention:** Refactor the webserver playbook into an Ansible role for better organization and reusability.

**Why:** Roles are a way of organizing playbooks and related files to facilitate sharing and reuse of Ansible code.

**Steps:**

1. Create a role structure:
   ```bash
   mkdir -p ~/ansible/roles/webserver/{tasks,handlers,templates}
   ```

2. Create the main task file `~/ansible/roles/webserver/tasks/main.yml`:
   ```yaml
   ---
   - name: Install Apache
     apt:
       name: apache2
       state: present

   - name: Start Apache service
     service:
       name: apache2
       state: started
       enabled: yes

   - name: Create a custom index.html
     template:
       src: index.html.j2
       dest: /var/www/html/index.html
     notify: Restart Apache
   ```

3. Create a handler file `~/ansible/roles/webserver/handlers/main.yml`:
   ```yaml
   ---
   - name: Restart Apache
     service:
       name: apache2
       state: restarted
   ```

4. Create a template file `~/ansible/roles/webserver/templates/index.html.j2`:
   ```html
   <html>
   <body>
     <h1>Hello from WSL Ubuntu</h1>
     <p>This server is managed by Ansible!</p>
     <p>Hostname: {{ ansible_hostname }}</p>
   </body>
   </html>
   ```

5. Update the playbook `~/ansible/webserver.yml`:
   ```yaml
   ---
   - hosts: local
     become: yes
     roles:
       - webserver
   ```

6. Run the updated playbook:
   ```bash
   ansible-playbook webserver.yml
   ```

**What it demonstrates:** This exercise shows how to organize Ansible code into roles, use templates, and implement handlers in a local environment.

**Interpretation:** Roles provide a way to modularize Ansible code, making it more maintainable and reusable. Templates allow for dynamic content generation, and handlers provide a way to respond to changes.

**Innovative fact:** You can use `ansible-galaxy init rolename` to automatically create the role directory structure with all necessary files and folders.

## Testing Your Setup

To verify everything is working:

1. Check if Apache is running:
   ```bash
   sudo service apache2 status
   ```

2. View the webpage from Windows:
   - Open your browser and navigate to `http://localhost`
   - You should see your custom webpage

## Conclusion

This guide has introduced you to Ansible through practical exercises using WSL. You've learned how to:
- Set up Ansible in WSL
- Create and run playbooks
- Organize your code using roles
- Work with templates and handlers

As you continue your Ansible journey, explore more advanced topics like:
- Variables and facts
- Conditionals and loops
- Custom modules
- Vault for secret management
- Dynamic inventory

The WSL setup provides a perfect environment for learning and testing Ansible locally before deploying to production environments.

Happy automating with Ansible!

## Common Issues and Solutions

1. If Apache is not accessible from Windows:
   ```bash
   sudo service apache2 restart
   ```

2. If you get permission errors:
   ```bash
   sudo chown -R $USER:$USER ~/ansible
   ```

3. To check Ansible's version and installation:
   ```bash
   ansible --version
   ```
