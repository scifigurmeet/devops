# Ansible Advanced Concepts - Essential Guide

## Overview
This guide covers essential Ansible features for writing robust, maintainable playbooks: Handlers, Environment Variables, Variables, Facts, Prompts, Tags, and Blocks.

## Prerequisites
- Basic Ansible setup (from Unit V)
- Understanding of playbooks and tasks
- Working Docker environment or inventory

---

## 1. Handlers

### What are Handlers?
Handlers are tasks that run only when notified by other tasks, typically for service restarts.

### Key Characteristics
- Run only when notified
- Execute once per play (even if notified multiple times)
- Run at the end of the play

### Basic Example
```yaml
---
- name: Web Server with Handlers
  hosts: managed_nodes
  become: yes
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        
    - name: Copy nginx config
      copy:
        content: |
          server {
              listen 80;
              server_name _;
              root /var/www/html;
              index index.html;
          }
        dest: /etc/nginx/sites-available/default
      notify: restart nginx
      
    - name: Update website content
      copy:
        content: "<h1>Updated by Ansible</h1>"
        dest: /var/www/html/index.html
      notify: restart nginx
      
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

### Multiple Handlers Example
```yaml
tasks:
  - name: Update application
    copy:
      src: app.tar.gz
      dest: /tmp/
    notify:
      - stop app
      - extract app
      - start app
      
handlers:
  - name: stop app
    service:
      name: myapp
      state: stopped
      
  - name: extract app
    unarchive:
      src: /tmp/app.tar.gz
      dest: /opt/myapp
      
  - name: start app
    service:
      name: myapp
      state: started
```

---

## 2. Environment Variables

### Setting Environment Variables
Environment variables configure applications and provide runtime settings.

### Task-level Environment
```yaml
---
- name: Environment Variables Example
  hosts: managed_nodes
  
  tasks:
    - name: Run command with environment
      shell: echo "Database URL: $DB_URL"
      environment:
        DB_URL: "postgresql://user:pass@localhost/mydb"
        API_KEY: "secret123"
        DEBUG: "true"
```

### Play-level Environment
```yaml
---
- name: Global Environment Example
  hosts: managed_nodes
  environment:
    PATH: "{{ ansible_env.PATH }}:/usr/local/bin"
    PYTHONPATH: "/opt/myapp"
    
  tasks:
    - name: Check Python path
      command: python3 -c "import sys; print(sys.path)"
      
    - name: Task with additional environment
      shell: echo "Custom var: $CUSTOM_VAR"
      environment:
        CUSTOM_VAR: "task-specific-value"
```

### Creating Environment Files
```yaml
- name: Create application environment file
  copy:
    content: |
      # Application Environment
      DATABASE_URL={{ database_url }}
      SECRET_KEY={{ app_secret_key }}
      DEBUG={{ debug_mode | default('false') }}
      PORT=8080
    dest: /opt/myapp/.env
    mode: '0600'
```

---

## 3. Variables

### Variable Types and Usage

#### Simple Variables
```yaml
---
- name: Variable Examples
  hosts: managed_nodes
  vars:
    app_name: "mywebapp"
    app_version: "1.0.0"
    http_port: 80
    
  tasks:
    - name: Display variables
      debug:
        msg: "Deploying {{ app_name }} version {{ app_version }} on port {{ http_port }}"
```

#### Complex Variables
```yaml
vars:
  database:
    host: "localhost"
    port: 5432
    name: "myapp_db"
    user: "dbuser"
  
  users:
    - name: "alice"
      role: "admin"
    - name: "bob"
      role: "user"
      
tasks:
  - name: Connect to database
    debug:
      msg: "Connecting to {{ database.host }}:{{ database.port }}/{{ database.name }}"
      
  - name: Create users
    debug:
      msg: "Creating user {{ item.name }} with role {{ item.role }}"
    loop: "{{ users }}"
```

#### Registered Variables
```yaml
tasks:
  - name: Get current date
    command: date +%Y%m%d
    register: build_date
    
  - name: Use registered variable
    debug:
      msg: "Build date is {{ build_date.stdout }}"
      
  - name: Check if file exists
    stat:
      path: /etc/nginx/nginx.conf
    register: nginx_config
    
  - name: Display file status
    debug:
      msg: "Nginx config exists: {{ nginx_config.stat.exists }}"
```

### Variable Precedence (High to Low)
1. Command line (`-e var=value`)
2. Task vars
3. Block vars
4. Role vars
5. Play vars
6. Host vars
7. Group vars
8. Role defaults

---

## 4. Facts

### What are Facts?
Facts are system information automatically gathered by Ansible.

### Common Facts
```yaml
---
- name: Display System Facts
  hosts: managed_nodes
  
  tasks:
    - name: Show basic system information
      debug:
        msg: |
          Hostname: {{ ansible_hostname }}
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          Architecture: {{ ansible_architecture }}
          IP Address: {{ ansible_default_ipv4.address }}
          Memory: {{ ansible_memtotal_mb }}MB
          CPU Cores: {{ ansible_processor_cores }}
```

### Using Facts for Decisions
```yaml
tasks:
  - name: Install package based on OS
    apt:
      name: apache2
      state: present
    when: ansible_os_family == "Debian"
    
  - name: Install package on Red Hat systems
    yum:
      name: httpd
      state: present
    when: ansible_os_family == "RedHat"
    
  - name: Set service name based on OS
    set_fact:
      web_service: "{{ 'apache2' if ansible_os_family == 'Debian' else 'httpd' }}"
      
  - name: Start web service
    service:
      name: "{{ web_service }}"
      state: started
```

### Custom Facts
```yaml
- name: Create custom facts
  set_fact:
    app_environment: "{{ 'production' if ansible_hostname.startswith('prod') else 'development' }}"
    deployment_id: "{{ ansible_hostname }}-{{ ansible_date_time.epoch }}"
    
- name: Use custom facts
  debug:
    msg: "Deploying to {{ app_environment }} environment with ID {{ deployment_id }}"
```

---

## 5. Prompts

### Interactive Input
Prompts allow user input during playbook execution.

### Basic Prompts
```yaml
---
- name: Interactive Deployment
  hosts: managed_nodes
  vars_prompt:
    - name: app_version
      prompt: "Which version to deploy?"
      default: "latest"
      private: no
      
    - name: confirm_deployment
      prompt: "Deploy to production? (yes/no)"
      private: no
      
  tasks:
    - name: Validate confirmation
      fail:
        msg: "Deployment cancelled"
      when: confirm_deployment != "yes"
      
    - name: Deploy application
      debug:
        msg: "Deploying version {{ app_version }}"
```

### Secure Prompts
```yaml
vars_prompt:
  - name: database_password
    prompt: "Enter database password"
    private: yes
    encrypt: "sha512_crypt"
    confirm: yes
    
  - name: api_key
    prompt: "Enter API key"
    private: yes
    
tasks:
  - name: Configure database
    copy:
      content: "DB_PASSWORD={{ database_password }}"
      dest: /etc/myapp/db.conf
      mode: '0600'
```

---

## 6. Tags

### What are Tags?
Tags allow selective execution of tasks or plays.

### Basic Tagging
```yaml
---
- name: Web Server Setup
  hosts: managed_nodes
  become: yes
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
      tags:
        - install
        - webserver
        
    - name: Configure nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      tags:
        - configure
        - webserver
      notify: restart nginx
        
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
      tags:
        - start
        - webserver
        
    - name: Install monitoring tools
      apt:
        name: htop
        state: present
      tags:
        - monitoring
        - tools
        
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
      tags:
        - webserver
```

### Running with Tags
```bash
# Run only install tasks
ansible-playbook site.yml --tags "install"

# Run multiple tags
ansible-playbook site.yml --tags "install,configure"

# Skip specific tags
ansible-playbook site.yml --skip-tags "monitoring"

# List available tags
ansible-playbook site.yml --list-tags
```

### Advanced Tagging
```yaml
- name: Multi-service deployment
  hosts: all
  tasks:
    - name: Deploy web application
      include_tasks: web_tasks.yml
      tags: [web, application]
      
    - name: Deploy database
      include_tasks: db_tasks.yml
      tags: [database, application]
      
    - name: Run tests
      include_tasks: test_tasks.yml
      tags: [testing, never]  # 'never' tag skips by default
```

---

## 7. Blocks

### What are Blocks?
Blocks group tasks and provide error handling capabilities.

### Basic Block with Error Handling
```yaml
---
- name: Database Setup with Error Handling
  hosts: managed_nodes
  become: yes
  
  tasks:
    - name: Database installation and configuration
      block:
        - name: Install MySQL
          apt:
            name: mysql-server
            state: present
            
        - name: Start MySQL
          service:
            name: mysql
            state: started
            enabled: yes
            
        - name: Create database
          shell: mysql -e "CREATE DATABASE IF NOT EXISTS myapp_db;"
          
      rescue:
        - name: Log installation failure
          debug:
            msg: "MySQL installation failed, attempting cleanup"
            
        - name: Stop MySQL service
          service:
            name: mysql
            state: stopped
          ignore_errors: yes
          
        - name: Remove MySQL packages
          apt:
            name: mysql-server
            state: absent
            
      always:
        - name: Clean temporary files
          file:
            path: /tmp/mysql_install.log
            state: absent
            
        - name: Send notification
          debug:
            msg: "Database setup process completed"
```

### Block with Conditional Logic
```yaml
- name: Application deployment with rollback
  block:
    - name: Stop application
      service:
        name: myapp
        state: stopped
        
    - name: Backup current version
      command: cp -r /opt/myapp /opt/myapp.backup
      
    - name: Deploy new version
      unarchive:
        src: myapp-v2.tar.gz
        dest: /opt/myapp
        
    - name: Start application
      service:
        name: myapp
        state: started
        
    - name: Test application
      uri:
        url: http://localhost:8080/health
        status_code: 200
        
  rescue:
    - name: Rollback on failure
      command: rm -rf /opt/myapp && mv /opt/myapp.backup /opt/myapp
      
    - name: Restart old version
      service:
        name: myapp
        state: started
        
    - name: Notify failure
      debug:
        msg: "Deployment failed, rolled back to previous version"
        
  always:
    - name: Cleanup backup
      file:
        path: /opt/myapp.backup
        state: absent
      when: deployment_success is defined
```

---

## 8. Complete Example: Combining All Concepts

```yaml
---
- name: Advanced Web Application Deployment
  hosts: managed_nodes
  become: yes
  vars_prompt:
    - name: app_version
      prompt: "Enter application version"
      default: "1.0.0"
      private: no
      
  vars:
    app_name: "webapp"
    app_user: "webuser"
    
  environment:
    DEPLOYMENT_ENV: "production"
    
  tasks:
    - name: Deployment process
      block:
        - name: Create application user
          user:
            name: "{{ app_user }}"
            system: yes
            home: "/opt/{{ app_name }}"
            create_home: yes
          tags: [setup, users]
          
        - name: Install packages
          apt:
            name: [nginx, python3, python3-pip]
            state: present
            update_cache: yes
          tags: [install, packages]
          
        - name: Deploy application
          copy:
            content: |
              #!/usr/bin/env python3
              print("{{ app_name }} v{{ app_version }}")
              print("Deployed on {{ ansible_hostname }}")
              print("Environment: {{ ansible_env.DEPLOYMENT_ENV }}")
            dest: "/opt/{{ app_name }}/app.py"
            owner: "{{ app_user }}"
            mode: '0755'
          tags: [deploy, application]
          notify: restart app service
          register: app_deployed
          
        - name: Configure nginx
          copy:
            content: |
              server {
                  listen 80;
                  server_name _;
                  location / {
                      proxy_pass http://127.0.0.1:8080;
                  }
              }
            dest: /etc/nginx/sites-available/{{ app_name }}
          tags: [configure, nginx]
          notify: restart nginx
          
        - name: Enable nginx site
          file:
            src: /etc/nginx/sites-available/{{ app_name }}
            dest: /etc/nginx/sites-enabled/{{ app_name }}
            state: link
          tags: [configure, nginx]
          notify: restart nginx
          
        - name: Set deployment facts
          set_fact:
            deployment_time: "{{ ansible_date_time.iso8601 }}"
            deployment_host: "{{ ansible_hostname }}"
            deployment_success: true
          tags: [always]
          
      rescue:
        - name: Handle deployment failure
          debug:
            msg: "Deployment failed on {{ ansible_hostname }}"
            
        - name: Set failure facts
          set_fact:
            deployment_success: false
            
      always:
        - name: Log deployment result
          copy:
            content: |
              Deployment Log
              ==============
              App: {{ app_name }}
              Version: {{ app_version }}
              Host: {{ deployment_host | default(ansible_hostname) }}
              Time: {{ deployment_time | default(ansible_date_time.iso8601) }}
              Success: {{ deployment_success | default(false) }}
            dest: "/tmp/deployment-{{ ansible_date_time.epoch }}.log"
          tags: [always]
          
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
      tags: [nginx]
      
    - name: restart app service
      debug:
        msg: "Application service restarted"
      tags: [application]
```

### Running the Complete Example
```bash
# Run full deployment
ansible-playbook advanced_deployment.yml

# Run only setup tasks
ansible-playbook advanced_deployment.yml --tags "setup"

# Skip nginx configuration
ansible-playbook advanced_deployment.yml --skip-tags "nginx"

# Check mode (dry run)
ansible-playbook advanced_deployment.yml --check
```

---

## Summary

This guide covered essential Ansible concepts:

- ✅ **Handlers**: Event-driven task execution for service management
- ✅ **Environment Variables**: Runtime configuration for applications
- ✅ **Variables**: Dynamic values and data structures
- ✅ **Facts**: Automatic system information gathering
- ✅ **Prompts**: Interactive user input during execution
- ✅ **Tags**: Selective task execution for flexible deployments
- ✅ **Blocks**: Task grouping with comprehensive error handling

### Key Benefits:
- **Robust Error Handling**: Graceful failure management
- **Flexible Execution**: Run specific parts of playbooks
- **Dynamic Configuration**: Adapt to different environments
- **Interactive Control**: User input for deployment decisions
- **Maintainable Code**: Organized, reusable playbook structure

These concepts enable writing production-ready Ansible playbooks that are reliable, maintainable, and adaptable to various deployment scenarios.