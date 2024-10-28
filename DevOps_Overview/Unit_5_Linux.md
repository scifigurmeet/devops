# Linux Basics and Administration Guide
## For B.Tech DevOps Students (2nd Year)

## Table of Contents
1. [Introduction to Linux](#1-introduction-to-linux)
2. [Linux in DevOps](#2-linux-in-devops)
3. [Basic Command Utilities](#3-basic-command-utilities)
4. [Linux Administration](#4-linux-administration)
5. [Environment Variables](#5-environment-variables)
6. [Networking](#6-networking)
7. [Package Management](#7-package-management)

## 1. Introduction to Linux

### What is Linux?
Linux is a free, open-source operating system kernel first created by Linus Torvalds in 1991. It's the foundation for many operating systems (distributions or "distros") like Ubuntu, which you'll be using in this course.

### Key Features
- Multi-user and multi-tasking capabilities
- Secure and stable
- Open-source and community-driven
- Highly customizable
- Excellent for servers and development

### Linux File System Hierarchy
```
/           # Root directory
├── bin     # Essential user binaries
├── boot    # Boot loader files
├── dev     # Device files
├── etc     # System configuration
├── home    # User home directories
├── lib     # System libraries
├── media   # Mount point for removable media
├── mnt     # Mount point for temporary filesystems
├── opt     # Optional application software
├── proc    # Virtual filesystem for process info
├── root    # Root user home directory
├── sbin    # System binaries
├── tmp     # Temporary files
├── usr     # User programs
└── var     # Variable files (logs, etc.)
```

## 2. Linux in DevOps

### Importance in DevOps Pipeline
- **Automation**: Scripting and task automation
- **Containerization**: Docker runs natively on Linux
- **CI/CD**: Most CI/CD tools are Linux-based
- **Configuration Management**: Easy system configuration
- **Monitoring**: Rich set of monitoring tools

### Practical Example: Creating a Simple DevOps Script
```bash
#!/bin/bash
# Simple deployment script

echo "Starting deployment..."

# Update system
sudo apt update
echo "System updated"

# Check disk space
df -h
echo "Disk space checked"

# Check system memory
free -h
echo "Memory status checked"

# Check running processes
ps aux | grep nginx
echo "Process status checked"

echo "Deployment checks completed"
```

## 3. Basic Command Utilities

### File and Directory Operations
```bash
# Directory navigation
pwd                     # Print working directory
cd /path/to/directory   # Change directory
ls -la                  # List all files with details

# File operations
touch file.txt          # Create empty file
mkdir directory         # Create directory
cp source dest          # Copy files
mv source dest          # Move/rename files
rm file                 # Remove file
rm -r directory        # Remove directory recursively

# File viewing
cat file.txt           # View entire file
less file.txt          # View file page by page
head -n 5 file.txt     # View first 5 lines
tail -n 5 file.txt     # View last 5 lines
```

### Practical Exercise: File Management
```bash
# Create a project directory structure
mkdir -p ~/devops-project/{src,docs,tests}
cd ~/devops-project
touch src/app.py docs/README.md tests/test_app.py

# List the structure
tree ~/devops-project

# Create a backup
tar -czf devops-project-backup.tar.gz ~/devops-project
```

## 4. Linux Administration

### User Management
```bash
# Create new user
sudo useradd -m username

# Set password
sudo passwd username

# Add user to sudo group
sudo usermod -aG sudo username

# Delete user
sudo userdel -r username

# View user information
id username
```

### Permission Management
```bash
# Change file permissions
chmod 755 script.sh    # rwxr-xr-x
chmod u+x script.sh    # Add execute permission for user

# Change ownership
chown user:group file.txt

# View permissions
ls -l file.txt
```

### Process Management
```bash
# View processes
ps aux                 # All processes
top                    # Interactive process viewer

# Process control
kill -9 PID           # Force kill process
killall processname    # Kill all instances

# Background processes
command &             # Run in background
nohup command &       # Run immune to hangups
```

## 5. Environment Variables

### Working with Environment Variables
```bash
# View all environment variables
env

# Set temporary variable
export MY_VAR="value"

# View specific variable
echo $MY_VAR

# Add permanent variable (add to ~/.bashrc)
echo 'export MY_VAR="value"' >> ~/.bashrc
source ~/.bashrc
```

### Practical Exercise: Environment Setup
```bash
# Create development environment variables
cat << EOF >> ~/.bashrc
export DEV_ENV="development"
export APP_PORT="3000"
export DB_HOST="localhost"
export DB_PORT="5432"
EOF

source ~/.bashrc

# Test variables
echo "Development Environment: $DEV_ENV"
echo "Application Port: $APP_PORT"
```

## 6. Networking

### Network Configuration
```bash
# View network interfaces
ip addr show
ifconfig

# Test connectivity
ping google.com
curl http://example.com

# View open ports
sudo netstat -tulpn
sudo ss -tulpn

# DNS lookup
nslookup google.com
dig google.com
```

### Firewall Management (UFW)
```bash
# Enable firewall
sudo ufw enable

# Allow specific port
sudo ufw allow 22
sudo ufw allow 80/tcp

# Check status
sudo ufw status
```

### SSH Operations
```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096

# Copy key to server
ssh-copy-id username@remote_host

# Connect to remote server
ssh username@remote_host

# SCP file transfer
scp file.txt username@remote_host:/path/
```

## 7. Package Management

### APT (Advanced Package Tool)
```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade

# Install package
sudo apt install package-name

# Remove package
sudo apt remove package-name

# Search for package
apt search keyword
```

### Practical Exercise: LAMP Stack Installation
```bash
# Install Apache, MySQL, PHP
sudo apt update
sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql

# Start services
sudo systemctl start apache2
sudo systemctl start mysql

# Enable services on boot
sudo systemctl enable apache2
sudo systemctl enable mysql

# Check status
sudo systemctl status apache2
sudo systemctl status mysql
```

## Practice Exercises

1. **System Exploration**
```bash
# Create a script that shows:
# - System uptime
# - Disk usage
# - Memory usage
# - CPU information

#!/bin/bash
echo "System Information Report"
echo "========================"
echo "Uptime:"
uptime
echo -e "\nDisk Usage:"
df -h
echo -e "\nMemory Usage:"
free -h
echo -e "\nCPU Information:"
lscpu
```

2. **Log Analysis**
```bash
# Create a script to analyze Apache access logs
#!/bin/bash
echo "Top 10 IP addresses:"
cat /var/log/apache2/access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 10

echo -e "\nTop 10 requested pages:"
cat /var/log/apache2/access.log | awk '{print $7}' | sort | uniq -c | sort -nr | head -n 10
```

## Additional Resources
- Linux Documentation Project: https://tldp.org/
- Ubuntu Documentation: https://help.ubuntu.com/
- DevOps Roadmap: https://roadmap.sh/devops

## Note to Students
- Always practice commands in a safe environment
- Create backups before making system changes
- Use `man` command or `--help` flag for detailed information
- Keep security in mind when working with permissions and networking
- Document your learning and create your own command reference

Remember: The best way to learn Linux is through hands-on practice. Try to use these commands regularly and experiment in your EC2 environment.
