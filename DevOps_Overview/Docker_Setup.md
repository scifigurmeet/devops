# Ubuntu DevOps Environment Setup Guide
A comprehensive guide for setting up and using a Docker-based Ubuntu environment for DevOps learning.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Usage Guide](#usage-guide)
4. [Included Tools](#included-tools)
5. [Common Tasks](#common-tasks)
6. [Troubleshooting](#troubleshooting)

## Prerequisites
Before starting, ensure you have the following installed on your host machine:
- Docker Engine (latest version)
- Git (for version control)
- Text editor of your choice (VSCode recommended)

## Environment Setup

### Step 1: Create Dockerfile
Create a new directory for your project and save the following content in a file named `Dockerfile`:

```dockerfile
# Use Ubuntu as the base image
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install essential packages
RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    wget \
    vim \
    git \
    tree \
    net-tools \
    iputils-ping \
    dnsutils \
    apache2 \
    mysql-server \
    php \
    libapache2-mod-php \
    php-mysql \
    ssh \
    ufw \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with sudo privileges
RUN useradd -m -s /bin/bash devops && \
    echo "devops:devops" | chpasswd && \
    adduser devops sudo && \
    echo "devops ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set up working directory
WORKDIR /home/devops

# Create project directory structure from the guide
RUN mkdir -p ~/devops-project/{src,docs,tests}

# Create the startup script properly
RUN echo '#!/bin/bash' > /usr/local/bin/startup.sh && \
    echo 'service ssh start' >> /usr/local/bin/startup.sh && \
    echo 'service apache2 start' >> /usr/local/bin/startup.sh && \
    echo 'service mysql start' >> /usr/local/bin/startup.sh && \
    echo 'tail -f /dev/null' >> /usr/local/bin/startup.sh && \
    chmod +x /usr/local/bin/startup.sh

# Switch to non-root user
USER devops

# Set up some example environment variables
RUN echo 'export DEV_ENV="development"' >> ~/.bashrc && \
    echo 'export APP_PORT="3000"' >> ~/.bashrc && \
    echo 'export DB_HOST="localhost"' >> ~/.bashrc && \
    echo 'export DB_PORT="5432"' >> ~/.bashrc

# Switch back to root for startup
USER root

# Expose common ports
EXPOSE 22 80 443 3000 5432

# Run the startup script
CMD ["/usr/local/bin/startup.sh"]
```

### Step 2: Build the Docker Image
Open a terminal in the directory containing your Dockerfile and run:
```bash
docker build -t ubuntu-devops .
```

### Step 3: Run the Container
After successful build, start the container:
```bash
docker run -d -p 80:80 -p 22:22 -p 3000:3000 -p 5432:5432 --name devops-lab ubuntu-devops
```

## Usage Guide

### Accessing the Container
To access the container's shell:
```bash
docker exec -it devops-lab bash
```

### User Credentials
- Username: `devops`
- Password: `devops`
- The user has sudo privileges without password requirement

### Directory Structure
```
/home/devops/
└── devops-project/
    ├── src/
    ├── docs/
    └── tests/
```

## Included Tools

### System Utilities
- sudo (privilege escalation)
- vim (text editor)
- git (version control)
- tree (directory visualization)
- curl & wget (file download)

### Network Tools
- net-tools (networking utilities)
- iputils-ping (ping command)
- dnsutils (DNS utilities)
- ssh (secure shell)
- ufw (uncomplicated firewall)

### Web Stack
- Apache2 (web server)
- MySQL (database)
- PHP (programming language)
- libapache2-mod-php (Apache PHP module)
- php-mysql (PHP MySQL connector)

## Common Tasks

### Check Services Status
```bash
# Apache status
sudo systemctl status apache2

# MySQL status
sudo systemctl status mysql

# SSH status
sudo systemctl status ssh
```

### Web Development
1. Apache web root is at `/var/www/html/`
2. MySQL can be accessed with:
```bash
sudo mysql
```

### Network Configuration
1. Check IP configuration:
```bash
ip addr show
```

2. Test connectivity:
```bash
ping google.com
```

### Environment Variables
View configured environment variables:
```bash
env | grep DEV
```

## Troubleshooting

### Container Won't Start
1. Check Docker logs:
```bash
docker logs devops-lab
```

2. Ensure no services are using required ports:
```bash
sudo netstat -tulpn | grep -E '80|22|3000|5432'
```

### Services Not Starting
Inside the container:
```bash
# Check service status
sudo service apache2 status
sudo service mysql status

# Manually start services
sudo service apache2 start
sudo service mysql start
```

### Permission Issues
1. Ensure you're using the correct user:
```bash
whoami
```

2. Switch to root if needed:
```bash
sudo su
```

## Best Practices
1. Always use the `devops` user for regular operations
2. Use `sudo` only when necessary
3. Keep the container updated:
```bash
sudo apt update && sudo apt upgrade
```
4. Regularly commit your work when making changes
5. Document any additional configurations you make

## Additional Notes
- The container automatically starts Apache, MySQL, and SSH services
- All exposed ports (22, 80, 443, 3000, 5432) are mapped to the host
- The environment is configured for development purposes and shouldn't be used in production
- Regular backups of your work are recommended

For any additional help or information, refer to:
- Docker Documentation: https://docs.docker.com
- Ubuntu Documentation: https://help.ubuntu.com
- Apache Documentation: https://httpd.apache.org/docs/
- MySQL Documentation: https://dev.mysql.com/doc/

Remember to always check the official documentation for the most up-to-date information about specific tools and commands.
