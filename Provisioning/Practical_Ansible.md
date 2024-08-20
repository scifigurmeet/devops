# Ansible Beginner's Guide with Practical Exercises

## Introduction

Welcome to this beginner's guide on Ansible! This document is designed for DevOps students who have Docker installed on their Windows PCs. We'll explore Ansible through practical exercises, each with a clear intention, explanation, and interpretation.

## What is Ansible?

Ansible is an open-source automation tool that simplifies configuration management, application deployment, and task automation. It uses a declarative language to describe system configurations and a push-based mechanism to apply changes.

## Setup

Before we begin, let's set up our environment using Docker. We'll use Docker Compose to create a small network of containers that will serve as our Ansible control node and managed nodes.

### docker-compose.yml

Create a file named `docker-compose.yml` with the following content:

```yaml
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

This Docker Compose file creates three containers: one control node and two managed nodes.

To start the containers, run:

```
docker-compose up -d
```

## Exercise 1: Installing Ansible and Basic Configuration

**Intention:** Set up Ansible on the control node and configure it to communicate with managed nodes.

**Why:** This exercise demonstrates the basic setup required for Ansible and introduces the concept of inventory.

**Steps:**

1. Access the control node:
   ```
   docker exec -it ansible-control bash
   ```

2. Install Ansible:
   ```
   apt update && apt install -y ansible
   ```

3. Create an inventory file `/ansible/inventory.ini`:
   ```ini
   [webservers]
   node1 ansible_host=ansible-node1
   node2 ansible_host=ansible-node2
   ```

4. Create an Ansible configuration file `/ansible/ansible.cfg`:
   ```ini
   [defaults]
   inventory = /ansible/inventory.ini
   host_key_checking = False
   ```

**What it demonstrates:** This exercise shows how to set up Ansible and define an inventory of managed nodes.

**Interpretation:** The inventory file defines the hosts Ansible will manage, while the configuration file sets global options for Ansible.

**Innovative fact:** Ansible uses SSH for communication by default, but in containerized environments like this, it can use the Docker connection plugin to communicate directly with containers without SSH.

## Exercise 2: Your First Ansible Playbook

**Intention:** Create and run a simple Ansible playbook to install and configure a web server.

**Why:** This exercise introduces the concept of playbooks, which are Ansible's configuration, deployment, and orchestration language.

**Steps:**

1. Create a playbook file `/ansible/webserver.yml`:
   ```yaml
   ---
   - hosts: webservers
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
           content: "Hello from {{ inventory_hostname }}"
           dest: /var/www/html/index.html
   ```

2. Run the playbook:
   ```
   ansible-playbook /ansible/webserver.yml
   ```

**What it demonstrates:** This exercise shows how to define tasks in a playbook and apply them to multiple hosts simultaneously.

**Interpretation:** The playbook installs Apache, ensures it's running, and creates a custom homepage on each managed node.

**Innovative fact:** Ansible's "idempotent" nature means you can run this playbook multiple times without changing the result after the first successful run.

## Exercise 3: Using Ansible Roles

**Intention:** Refactor the webserver playbook into an Ansible role for better organization and reusability.

**Why:** Roles are a way of organizing playbooks and related files to facilitate sharing and reuse of Ansible code.

**Steps:**

1. Create a role structure:
   ```
   mkdir -p /ansible/roles/webserver/{tasks,handlers,templates}
   ```

2. Create the main task file `/ansible/roles/webserver/tasks/main.yml`:
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

3. Create a handler file `/ansible/roles/webserver/handlers/main.yml`:
   ```yaml
   ---
   - name: Restart Apache
     service:
       name: apache2
       state: restarted
   ```

4. Create a template file `/ansible/roles/webserver/templates/index.html.j2`:
   ```html
   <html>
   <body>
     <h1>Hello from {{ inventory_hostname }}</h1>
     <p>This server is managed by Ansible!</p>
   </body>
   </html>
   ```

5. Update the playbook `/ansible/webserver.yml`:
   ```yaml
   ---
   - hosts: webservers
     become: yes
     roles:
       - webserver
   ```

6. Run the updated playbook:
   ```
   ansible-playbook /ansible/webserver.yml
   ```

**What it demonstrates:** This exercise shows how to organize Ansible code into roles, use templates, and implement handlers.

**Interpretation:** Roles provide a way to modularize Ansible code, making it more maintainable and reusable. Templates allow for dynamic content generation, and handlers provide a way to respond to changes.

**Innovative fact:** Ansible Galaxy is a repository of community-contributed roles that you can use in your projects, significantly speeding up development time.

## Conclusion

This guide has introduced you to Ansible through practical exercises. You've learned how to set up Ansible, create and run playbooks, and organize your code using roles. As you continue your Ansible journey, explore more advanced topics like variables, conditionals, loops, and custom modules.

Remember to clean up your Docker environment when you're done:

```
docker-compose down
```

Happy automating with Ansible!
