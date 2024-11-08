# Practical Guide: Managing Docker Nodes with Ansible on Windows using WSL

## Prerequisites
- Windows 10 or 11
- Docker Desktop for Windows
- WSL2 with Ubuntu installed

## Setup Instructions

### 1. Setting up WSL Ubuntu
```bash
# Install WSL Ubuntu if not already installed
wsl --install -d Ubuntu
```

### 2. Project Structure
Create a new directory for your Ansible project in WSL Ubuntu:
```bash
mkdir ~/ansible
cd ~/ansible
```

### 3. Create Docker Configuration Files (On Windows in a New Folder)
1. Create `Dockerfile`:
```bash
cat << 'EOF' > Dockerfile
FROM ubuntu:20.04

# Install Python and other required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    apache2 \
    && rm -rf /var/lib/apt/lists/*

# Keep container running
CMD ["tail", "-f", "/dev/null"]
EOF
```

2. Create `docker-compose.yml`:
```bash
cat << 'EOF' > docker-compose.yml
version: '3.8'
services:
  node1:
    build: .
    container_name: ansible-node1
    networks:
      - ansible-network
    volumes:
      - ansible_tmp:/root/.ansible/tmp
    environment:
      - ANSIBLE_HOST_KEY_CHECKING=False
    command: tail -f /dev/null
    restart: always
  node2:
    build: .
    container_name: ansible-node2
    networks:
      - ansible-network
    volumes:
      - ansible_tmp:/root/.ansible/tmp
    environment:
      - ANSIBLE_HOST_KEY_CHECKING=False
    command: tail -f /dev/null
    restart: always
networks:
  ansible-network:
    driver: bridge
volumes:
  ansible_tmp:
    driver: local
EOF
```

### 4. Configure Ansible
1. Create `inventory.ini`:
```bash
cat << 'EOF' > inventory.ini
[webservers]
node1 ansible_host=ansible-node1 ansible_connection=docker
node2 ansible_host=ansible-node2 ansible_connection=docker
EOF
```

2. Create `ansible.cfg`:
```bash
cat << 'EOF' > ansible.cfg
[defaults]
inventory = inventory.ini
host_key_checking = False
EOF
```

3. Create the Apache playbook (`setup_apache.yml`):
```bash
cat << 'EOF' > setup_apache.yml
---
- name: Setup Apache Servers
  hosts: webservers
  become: yes
  tasks:
    - name: Ensure Apache is running
      service:
        name: apache2
        state: started
        enabled: yes

    - name: Create custom index.html for each node
      copy:
        content: "Welcome to {{ inventory_hostname }}\n"
        dest: /var/www/html/index.html
EOF
```

## Running the Environment

### 1. Start Docker Containers
```bash
# Build and start the containers
docker-compose up -d --build
```

### 2. Install Ansible in WSL Ubuntu
```bash
# Update package list
sudo apt update

# Install Ansible
sudo apt install -y ansible
```

### 3. Verify Connection
```bash
# Test connection to nodes
ansible webservers -m ping
```

### 4. Run the Apache Playbook
```bash
# Execute the playbook
ansible-playbook setup_apache.yml
```

### 5. Testing the Setup
After running the playbook, you can verify the web servers are working:
```bash
# Test node1
curl http://ansible-node1

# Test node2
curl http://ansible-node2
```

## Troubleshooting Tips
1. If containers aren't accessible, ensure Docker Desktop is running and WSL integration is enabled
2. If Ansible connection fails, verify the containers are running:
   ```bash
   docker ps
   ```
3. To restart the environment:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Cleanup
To remove the environment when done:
```bash
docker-compose down -v
```

## Additional Notes
- The containers will automatically restart if Docker Desktop is restarted
- All Ansible commands should be run from the WSL Ubuntu terminal
- The `ansible_connection=docker` in the inventory file allows Ansible to communicate directly with the Docker containers

This setup provides a safe, isolated environment for practicing Ansible automation without affecting your host system.
