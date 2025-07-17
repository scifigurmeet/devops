# Ansible HTML File Operations - Practical Guide

## Overview
This guide demonstrates two common Ansible operations:
1. Copy a local HTML file to remote servers
2. Fetch web content and save it on remote servers

## Prerequisites
- Ansible control node setup (from Unit V)
- Docker environment running with managed nodes
- Basic `ansible.cfg` and `inventory.ini` configured

## Task 1: Copy Local HTML File

### Step 1: Create Local HTML File
```bash
# Create a sample index.html file
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My Ansible Deployed Website</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #4CAF50; color: white; padding: 20px; text-align: center; }
        .content { margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome to My Website</h1>
        <p>Deployed using Ansible</p>
    </div>
    <div class="content">
        <h2>About This Page</h2>
        <p>This HTML file was copied from the Ansible control node to remote servers.</p>
        <p><strong>Deployment Date:</strong> $(date)</p>
    </div>
</body>
</html>
EOF
```

### Step 2: Create Playbook to Copy File
```bash
cat > copy_html_file.yml << 'EOF'
---
- name: Copy local index.html to remote hosts
  hosts: managed_nodes
  become: false
  
  tasks:
    - name: Copy index.html to remote machine
      copy:
        src: ./index.html
        dest: /home/{{ ansible_user }}/index.html
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        mode: '0644'
      
    - name: Verify file was copied
      stat:
        path: /home/{{ ansible_user }}/index.html
      register: html_file
      
    - name: Display file information
      debug:
        msg: |
          File copied successfully!
          Path: /home/{{ ansible_user }}/index.html
          Size: {{ html_file.stat.size }} bytes
          Owner: {{ html_file.stat.pw_name }}
EOF
```

### Step 3: Run the Playbook
```bash
ansible-playbook copy_html_file.yml
```

## Task 2: Fetch Web Content

### Step 1: Create Playbook to Fetch LPU Website
```bash
cat > fetch_web_content.yml << 'EOF'
---
- name: Fetch website content and save to remote hosts
  hosts: managed_nodes
  become: false
  
  tasks:
    - name: Fetch HTML content from https://www.lpu.in
      uri:
        url: https://www.lpu.in
        return_content: yes
        timeout: 30
      register: website_content
      delegate_to: localhost
      run_once: true
      
    - name: Save website content to remote file
      copy:
        content: "{{ website_content.content }}"
        dest: /home/{{ ansible_user }}/lpu_website.html
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        mode: '0644'
        
    - name: Create metadata file
      copy:
        content: |
          Website Fetch Information
          ========================
          URL: https://www.lpu.in
          Fetch Date: {{ ansible_date_time.iso8601 }}
          Content Length: {{ website_content.content | length }} characters
          Status Code: {{ website_content.status }}
          Remote Host: {{ inventory_hostname }}
        dest: /home/{{ ansible_user }}/lpu_fetch_info.txt
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        mode: '0644'
        
    - name: Display fetch results
      debug:
        msg: |
          Website content fetched successfully!
          Status: {{ website_content.status }}
          Content size: {{ website_content.content | length }} characters
          Saved to: /home/{{ ansible_user }}/lpu_website.html
EOF
```

### Step 2: Run the Playbook
```bash
ansible-playbook fetch_web_content.yml
```

## Verification Commands

### Check Files on Remote Hosts
```bash
# List created files
ansible managed_nodes -m shell -a "ls -la /home/ansible/*.html /home/ansible/*.txt"

# Check file contents (first few lines)
ansible managed_nodes -m shell -a "head -10 /home/ansible/index.html"

# Check file sizes
ansible managed_nodes -m shell -a "wc -c /home/ansible/*.html"
```

### Verify Web Content
```bash
# Check if LPU content was fetched successfully
ansible managed_nodes -m shell -a "grep -i 'LPU' /home/ansible/lpu_website.html | head -5"

# View fetch metadata
ansible managed_nodes -m shell -a "cat /home/ansible/lpu_fetch_info.txt"
```

## Combined Playbook (Optional)

For running both tasks together:

```bash
cat > html_operations.yml << 'EOF'
---
- name: HTML File Operations - Copy and Fetch
  hosts: managed_nodes
  become: false
  
  tasks:
    # Task 1: Copy local file
    - name: Copy local index.html
      copy:
        src: ./index.html
        dest: /home/{{ ansible_user }}/local_index.html
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        mode: '0644'
        
    # Task 2: Fetch web content
    - name: Fetch LPU website content
      uri:
        url: https://www.lpu.in
        return_content: yes
        timeout: 30
      register: lpu_content
      delegate_to: localhost
      run_once: true
      
    - name: Save LPU content
      copy:
        content: "{{ lpu_content.content }}"
        dest: /home/{{ ansible_user }}/lpu_website.html
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        mode: '0644'
        
    # Verification
    - name: List all HTML files
      find:
        paths: /home/{{ ansible_user }}
        patterns: "*.html"
      register: html_files
      
    - name: Display results
      debug:
        msg: |
          HTML files created on {{ inventory_hostname }}:
          {% for file in html_files.files %}
          - {{ file.path }} ({{ file.size }} bytes)
          {% endfor %}
EOF
```

### Run Combined Playbook
```bash
ansible-playbook html_operations.yml
```

## Expected Output

After running the playbooks, you should see files created on remote hosts:

```
/home/ansible/index.html          # Copied local file
/home/ansible/lpu_website.html    # Fetched web content
/home/ansible/lpu_fetch_info.txt  # Metadata about fetch operation
```

## Troubleshooting

### Common Issues and Solutions

1. **File not found error**: Ensure `index.html` exists in the same directory as playbook
2. **Permission denied**: Check file permissions and ownership settings
3. **Network timeout**: Increase timeout value in `uri` module or check internet connectivity
4. **SSL certificate issues**: Add `validate_certs: no` to `uri` module (for testing only)

### Debug Commands
```bash
# Check if files exist locally
ls -la index.html

# Test web connectivity from control node
curl -I https://www.lpu.in

# Verify remote file permissions
ansible managed_nodes -m shell -a "ls -la /home/ansible/*.html"
```

## Summary

This guide demonstrated:
- ✅ Copying local files to remote hosts using `copy` module
- ✅ Fetching web content using `uri` module  
- ✅ File operations with proper ownership and permissions
- ✅ Verification and troubleshooting techniques
- ✅ Creating metadata and documentation files

These are fundamental operations for web deployment and content management with Ansible.