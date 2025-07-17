# Unit VI: Advanced Ansible

## 1. Ansible Roles and Command Line Usage

### What are Roles?
Roles organize playbooks into reusable components with standardized directory structure.

### Role Structure
```
roles/
└── webserver/
    ├── tasks/main.yml          # Main tasks
    ├── handlers/main.yml       # Event handlers
    ├── templates/             # Jinja2 templates
    ├── files/                 # Static files
    ├── vars/main.yml          # Role variables
    ├── defaults/main.yml      # Default variables
    └── meta/main.yml          # Role metadata
```

### Creating a Role

#### Generate role structure
```bash
ansible-galaxy init webserver
```

#### Example: tasks/main.yml
```yaml
---
- name: Install nginx
  apt:
    name: nginx
    state: present
    update_cache: yes

- name: Copy configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx

- name: Start nginx
  service:
    name: nginx
    state: started
    enabled: yes
```

#### Example: handlers/main.yml
```yaml
---
- name: restart nginx
  service:
    name: nginx
    state: restarted
```

#### Using roles in playbook
```yaml
---
- name: Deploy Web Server
  hosts: webservers
  become: yes
  roles:
    - webserver
```

### Command Line Usage
```bash
# Basic execution
ansible-playbook site.yml

# Dry run
ansible-playbook site.yml --check

# Verbose output
ansible-playbook site.yml -v

# Run specific tags
ansible-playbook site.yml --tags "webserver"

# Limit to hosts
ansible-playbook site.yml --limit webservers

# Override variables
ansible-playbook site.yml -e "http_port=8080"
```

## 2. Playbooks: Structure, Writing and Running

### Basic Playbook Structure
```yaml
---
- name: Web Server Setup
  hosts: webservers
  become: yes
  vars:
    http_port: 80
    
  tasks:
    - name: Install Apache
      apt:
        name: apache2
        state: present
    
    - name: Start Apache
      service:
        name: apache2
        state: started
        enabled: yes

- name: Database Setup
  hosts: databases
  become: yes
  tasks:
    - name: Install MySQL
      apt:
        name: mysql-server
        state: present
```

### Playbook Components
| Component | Purpose | Required |
|-----------|---------|----------|
| `name` | Play description | No |
| `hosts` | Target hosts/groups | Yes |
| `become` | Privilege escalation | No |
| `vars` | Variables | No |
| `tasks` | Main task list | Yes |
| `handlers` | Event handlers | No |

### Advanced Features

#### Conditionals
```yaml
- name: Install package based on OS
  apt:
    name: apache2
    state: present
  when: ansible_os_family == "Debian"
```

#### Loops
```yaml
- name: Install packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - vim
    - git
    - curl
```

#### Error Handling
```yaml
- name: Task that might fail
  command: /bin/false
  ignore_errors: yes
  register: result

- name: Handle failure
  debug:
    msg: "Task failed but continuing"
  when: result.failed
```

## 3. Real-world Playbook Examples

### LAMP Stack Deployment
```yaml
---
- name: Deploy LAMP Stack
  hosts: webservers
  become: yes
  vars:
    mysql_root_password: "{{ vault_mysql_password }}"
    
  tasks:
    - name: Install LAMP packages
      apt:
        name:
          - apache2
          - mysql-server
          - php
          - php-mysql
          - libapache2-mod-php
        state: present
        update_cache: yes
        
    - name: Start services
      service:
        name: "{{ item }}"
        state: started
        enabled: yes
      loop:
        - apache2
        - mysql
        
    - name: Create PHP info page
      copy:
        content: "<?php phpinfo(); ?>"
        dest: /var/www/html/info.php
```

### Multi-tier Application
```yaml
---
# Database tier
- name: Database Setup
  hosts: databases
  become: yes
  tasks:
    - name: Install MySQL
      apt:
        name: mysql-server
        state: present
    
    - name: Create database
      mysql_db:
        name: webapp_db
        state: present

# Web tier
- name: Web Server Setup
  hosts: webservers
  become: yes
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Deploy application
      copy:
        src: webapp/
        dest: /var/www/html/
```

## 4. Handlers

### What are Handlers?
Special tasks that run only when notified by other tasks, typically for service restarts.

### Basic Handler Example
```yaml
---
- name: Web Server Configuration
  hosts: webservers
  become: yes
  
  tasks:
    - name: Copy nginx config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: restart nginx
      
    - name: Copy SSL cert
      copy:
        src: server.crt
        dest: /etc/ssl/certs/
      notify: restart nginx
      
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

### Handler Features
- Run only when notified
- Execute once per play (even if notified multiple times)
- Run at the end of the play
- Can be chained together

### Multiple Handlers with Listen
```yaml
tasks:
  - name: Update application
    copy:
      src: app.tar.gz
      dest: /tmp/
    notify: "restart web services"
    
handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
    listen: "restart web services"
    
  - name: restart php-fpm
    service:
      name: php-fpm
      state: restarted
    listen: "restart web services"
```

## 5. Environment Variables

### Setting Environment Variables
```yaml
---
- name: Environment Variables Example
  hosts: webservers
  tasks:
    - name: Run command with environment
      shell: echo "Database: $DATABASE_URL"
      environment:
        DATABASE_URL: "postgresql://user:pass@localhost/db"
        API_KEY: "{{ vault_api_key }}"
        DEBUG: "false"
        
    - name: Use host environment variables
      debug:
        msg: "Home directory: {{ ansible_env.HOME }}"
```

### Global Environment
```yaml
---
- name: Global Environment
  hosts: all
  environment:
    PATH: "{{ ansible_env.PATH }}:/usr/local/bin"
    PYTHONPATH: "/opt/myapp"
    
  tasks:
    - name: Task inherits global environment
      command: which python3
```

### Environment File Template
```yaml
- name: Create .env file
  template:
    src: app.env.j2
    dest: /opt/myapp/.env
    mode: '0600'
```

## 6. Variables, Facts, and Prompts

### Variable Precedence (High to Low)
1. Command line (`-e`)
2. Task vars
3. Block vars
4. Role vars
5. Play vars
6. Host vars
7. Group vars
8. Role defaults

### Variable Examples
```yaml
---
- name: Variable Usage
  hosts: webservers
  vars:
    app_name: "myapp"
    database:
      host: "db.example.com"
      port: 3306
      
  tasks:
    - name: Display variables
      debug:
        msg: "App: {{ app_name }}, DB: {{ database.host }}:{{ database.port }}"
        
    - name: Register command output
      shell: date
      register: current_date
      
    - name: Use registered variable
      debug:
        msg: "Date: {{ current_date.stdout }}"
```

### Facts
System information automatically gathered by Ansible:

```yaml
- name: Display system facts
  debug:
    msg: |
      Hostname: {{ ansible_hostname }}
      OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
      IP: {{ ansible_default_ipv4.address }}
      Memory: {{ ansible_memtotal_mb }}MB
```

### Common Facts
- `ansible_hostname` - System hostname
- `ansible_os_family` - OS family (Debian, RedHat, etc.)
- `ansible_distribution` - OS distribution
- `ansible_default_ipv4.address` - Primary IP address
- `ansible_memtotal_mb` - Total memory in MB
- `ansible_processor_cores` - CPU cores

### Prompts
Interactive input during playbook execution:

```yaml
---
- name: Interactive Deployment
  hosts: webservers
  vars_prompt:
    - name: app_version
      prompt: "Which version to deploy?"
      default: "latest"
      private: no
      
    - name: database_password
      prompt: "Enter database password"
      private: yes
      
  tasks:
    - name: Deploy version
      debug:
        msg: "Deploying {{ app_version }}"
```

## 7. Tags and Blocks

### Tags
Label tasks for selective execution:

```yaml
---
- name: Web Server Setup
  hosts: webservers
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
        
    - name: Install monitoring
      apt:
        name: htop
        state: present
      tags:
        - monitoring
```

#### Running with tags
```bash
# Run only install tasks
ansible-playbook site.yml --tags "install"

# Skip monitoring tasks
ansible-playbook site.yml --skip-tags "monitoring"

# List available tags
ansible-playbook site.yml --list-tags
```

### Blocks
Group tasks for error handling:

```yaml
---
- name: Database Setup with Error Handling
  hosts: databases
  become: yes
  
  tasks:
    - name: Database operations
      block:
        - name: Install MySQL
          apt:
            name: mysql-server
            state: present
            
        - name: Start MySQL
          service:
            name: mysql
            state: started
            
      rescue:
        - name: Handle errors
          debug:
            msg: "Database setup failed, cleaning up"
            
        - name: Stop MySQL
          service:
            name: mysql
            state: stopped
          ignore_errors: yes
          
      always:
        - name: Log completion
          debug:
            msg: "Database setup process completed"
```

## 8. Ansible with AWS for Application Deployment

### Prerequisites
```bash
# Install AWS tools
pip install boto3 botocore awscli
ansible-galaxy collection install amazon.aws

# Configure credentials
aws configure
# OR set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-west-2"
```

### AWS Infrastructure Playbook
```yaml
---
- name: Create AWS Infrastructure
  hosts: localhost
  gather_facts: no
  vars:
    aws_region: us-west-2
    
  tasks:
    - name: Create VPC
      amazon.aws.ec2_vpc_net:
        name: "ansible-vpc"
        cidr_block: "10.0.0.0/16"
        region: "{{ aws_region }}"
        state: present
      register: vpc
      
    - name: Create subnet
      amazon.aws.ec2_vpc_subnet:
        vpc_id: "{{ vpc.vpc.id }}"
        cidr: "10.0.1.0/24"
        region: "{{ aws_region }}"
        state: present
      register: subnet
      
    - name: Create security group
      amazon.aws.ec2_security_group:
        name: "web-sg"
        description: "Web server security group"
        vpc_id: "{{ vpc.vpc.id }}"
        region: "{{ aws_region }}"
        rules:
          - proto: tcp
            ports: [80, 443, 22]
            cidr_ip: "0.0.0.0/0"
      register: sg
```

### Launch EC2 Instances
```yaml
- name: Launch EC2 Instances
  hosts: localhost
  tasks:
    - name: Launch web servers
      amazon.aws.ec2_instance:
        name: "web-{{ item }}"
        image_id: "ami-0c2d3e23ef31cb4be"  # Ubuntu 20.04
        instance_type: "t3.micro"
        key_name: "my-key"
        vpc_subnet_id: "{{ subnet.subnet.id }}"
        security_groups: ["{{ sg.group_id }}"]
        region: "{{ aws_region }}"
        state: present
        wait: true
      loop: [1, 2]
      register: instances
      
    - name: Add to inventory
      add_host:
        hostname: "{{ item.instances[0].public_ip_address }}"
        groupname: aws_webservers
        ansible_user: ubuntu
        ansible_ssh_private_key_file: "~/.ssh/my-key.pem"
      loop: "{{ instances.results }}"
```

### Deploy Application to AWS
```yaml
- name: Configure AWS Web Servers
  hosts: aws_webservers
  become: yes
  tasks:
    - name: Wait for SSH
      wait_for_connection:
        delay: 30
        timeout: 300
        
    - name: Install packages
      apt:
        name: [nginx, python3]
        state: present
        update_cache: yes
        
    - name: Deploy web app
      copy:
        content: |
          <!DOCTYPE html>
          <html>
          <head><title>Deployed with Ansible</title></head>
          <body>
            <h1>Hello from {{ inventory_hostname }}</h1>
            <p>Deployed on {{ ansible_date_time.date }}</p>
          </body>
          </html>
        dest: /var/www/html/index.html
        
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

### Application Load Balancer
```yaml
- name: Create Load Balancer
  hosts: localhost
  tasks:
    - name: Create target group
      amazon.aws.elb_target_group:
        name: "web-targets"
        protocol: HTTP
        port: 80
        vpc_id: "{{ vpc.vpc.id }}"
        region: "{{ aws_region }}"
        state: present
      register: tg
      
    - name: Create ALB
      amazon.aws.elb_application_lb:
        name: "web-alb"
        security_groups: ["{{ sg.group_id }}"]
        subnets: ["{{ subnet.subnet.id }}"]
        listeners:
          - Protocol: HTTP
            Port: 80
            DefaultActions:
              - Type: forward
                TargetGroupArn: "{{ tg.target_group_arn }}"
        region: "{{ aws_region }}"
        state: present
```

## 9. Best Practices Summary

### Playbook Organization
- Use roles for reusable components
- Separate variables by environment
- Keep playbooks focused and simple
- Use meaningful names for tasks

### Security
- Use Ansible Vault for sensitive data
- Limit privilege escalation
- Use SSH keys instead of passwords
- Regularly update Ansible

### Performance
- Use strategy plugins (free, linear)
- Optimize SSH settings
- Use async for long-running tasks
- Minimize fact gathering when not needed

### Error Handling
- Use blocks for complex error handling
- Implement proper validation
- Use check mode for testing
- Add meaningful error messages

---

## Summary

Unit VI covered advanced Ansible features:
- ✅ **Roles**: Reusable automation components
- ✅ **Playbooks**: Complex automation workflows
- ✅ **Handlers**: Event-driven task execution
- ✅ **Variables & Facts**: Dynamic configuration
- ✅ **Tags & Blocks**: Selective execution and error handling
- ✅ **Environment Variables**: Application configuration
- ✅ **AWS Integration**: Cloud infrastructure automation

**Key Skills Gained**: Writing production-ready playbooks, organizing code with roles, handling errors gracefully, and deploying to cloud platforms.