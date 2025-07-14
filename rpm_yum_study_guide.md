# RPM and YUM Package Management Study Guide

## Prerequisites
- Docker Desktop installed on your system
- Basic command line knowledge

## What You'll Learn
- Understanding RPM (Red Hat Package Manager)
- Working with YUM (Yellowdog Updater Modified)
- Practical package installation and management

---

## Section 1: Understanding Package Management

### What is a Package?
A package is a pre-compiled software bundle that contains:
- Executable files
- Configuration files
- Documentation
- Dependency information

### RPM vs YUM
- **RPM**: Low-level package manager (handles individual .rpm files)
- **YUM**: High-level package manager (resolves dependencies automatically)

---

## Section 2: Setting Up Practice Environment

### Step 1: Start a CentOS Container
```bash
# Pull and run a CentOS container
docker run -it --name rpm-yum-practice centos:7 /bin/bash
```

**What this does:**
- Downloads CentOS 7 image
- Creates a container named "rpm-yum-practice"
- Gives you interactive terminal access

### Step 2: Update the System
```bash
# Inside the container, update package lists
yum update -y
```

---

## Section 3: Working with YUM (Recommended for Beginners)

### Basic YUM Commands

#### 1. Search for Packages
```bash
# Search for a package
yum search wget

# Search with description
yum search all wget
```

#### 2. Get Package Information
```bash
# Show detailed information about a package
yum info wget

# List all available packages
yum list available | head -20
```

#### 3. Install Packages
```bash
# Install a single package
yum install wget -y

# Install multiple packages
yum install curl vim -y

# Install a specific version (if available)
yum install wget-1.14-18.el7_6.1
```

#### 4. Remove Packages
```bash
# Remove a package
yum remove wget -y

# Remove package and its dependencies (be careful!)
yum autoremove wget -y
```

#### 5. Update Packages
```bash
# Update a specific package
yum update wget -y

# Update all packages
yum update -y
```

#### 6. List Installed Packages
```bash
# List all installed packages
yum list installed | head -20

# Check if specific package is installed
yum list installed | grep wget
```

### Practice Exercise 1: YUM Basics
```bash
# Try these commands in sequence:
yum search httpd
yum info httpd
yum install httpd -y
yum list installed | grep httpd
systemctl start httpd  # Start the service
systemctl status httpd # Check status
yum remove httpd -y
```

---

## Section 4: Working with RPM (Advanced)

### Understanding RPM Files
RPM files have naming convention: `name-version-release.architecture.rpm`
Example: `wget-1.14-18.el7_6.1.x86_64.rpm`

### Basic RPM Commands

#### 1. Query Operations
```bash
# List all installed packages
rpm -qa | head -20

# Find which package owns a file
rpm -qf /bin/bash

# Show package information
rpm -qi bash

# List files in a package
rpm -ql bash | head -10
```

#### 2. Install RPM Package
```bash
# Download an RPM package first
yum install wget -y  # Install wget to download files

# Download an RPM package
wget https://download.fedoraproject.org/pub/epel/7/x86_64/Packages/h/htop-2.2.0-3.el7.x86_64.rpm

# Install RPM package
rpm -ivh htop-2.2.0-3.el7.x86_64.rpm

# Force install (if needed)
rpm -ivh --force htop-2.2.0-3.el7.x86_64.rpm
```

#### 3. Upgrade RPM Package
```bash
# Upgrade a package
rpm -Uvh package-name.rpm

# Freshen (upgrade only if already installed)
rpm -Fvh package-name.rpm
```

#### 4. Remove RPM Package
```bash
# Remove a package
rpm -e htop

# Remove without dependency check (dangerous!)
rpm -e --nodeps package-name
```

#### 5. Verify Packages
```bash
# Verify all installed packages
rpm -Va | head -10

# Verify specific package
rpm -V bash
```

### Practice Exercise 2: RPM Basics
```bash
# Try these commands:
rpm -qa | grep kernel
rpm -qi kernel
rpm -ql filesystem | head -10
rpm -qf /etc/passwd
```

---

## Section 5: Practical Examples

### Example 1: Installing Development Tools
```bash
# Using YUM (easy way)
yum groupinstall "Development Tools" -y

# Check what was installed
yum grouplist installed
```

### Example 2: Installing from EPEL Repository
```bash
# Install EPEL repository
yum install epel-release -y

# Install a package from EPEL
yum install htop -y

# Use the installed package
htop
```

### Example 3: Handling Dependencies
```bash
# Install a package that has dependencies
yum install httpd -y

# See what dependencies were installed
yum deplist httpd
```

---

## Section 6: Troubleshooting Common Issues

### Problem 1: Package Not Found
```bash
# Solution: Update package lists
yum clean all
yum update -y
```

### Problem 2: Dependency Issues with RPM
```bash
# Solution: Use YUM instead
yum install package-name -y
```

### Problem 3: Lock File Issues
```bash
# Solution: Remove lock file
rm -f /var/lib/rpm/.rpm.lock
```

---

## Section 7: Best Practices

### Do's:
- Always use `yum` for package management when possible
- Keep your system updated: `yum update -y`
- Use `-y` flag for automated installations
- Check package information before installing: `yum info package-name`

### Don'ts:
- Don't mix RPM and YUM commands carelessly
- Don't use `--force` or `--nodeps` unless absolutely necessary
- Don't install packages from untrusted sources

---

## Section 8: Quick Reference

### YUM Command Cheat Sheet
```bash
yum search <package>      # Search for package
yum info <package>        # Show package details
yum install <package>     # Install package
yum remove <package>      # Remove package
yum update <package>      # Update package
yum list installed       # List installed packages
yum clean all            # Clear cache
```

### RPM Command Cheat Sheet
```bash
rpm -qa                  # List all installed packages
rpm -qi <package>        # Show package info
rpm -ql <package>        # List package files
rpm -qf <file>          # Find package that owns file
rpm -ivh <package.rpm>  # Install RPM package
rpm -e <package>        # Remove package
rpm -V <package>        # Verify package
```

---

## Section 9: Hands-On Lab

### Complete this lab in your Docker container:

1. **Search and Install**
   ```bash
   yum search nano
   yum install nano -y
   ```

2. **Verify Installation**
   ```bash
   rpm -qa | grep nano
   which nano
   ```

3. **Use and Remove**
   ```bash
   nano /tmp/test.txt  # Create a test file
   yum remove nano -y
   ```

4. **Work with Groups**
   ```bash
   yum grouplist
   yum groupinfo "Base"
   ```

---

## Section 10: Clean Up

### Exit and Remove Container
```bash
# Exit the container
exit

# Remove the container (from host system)
docker rm rpm-yum-practice

# Remove the image (optional)
docker rmi centos:7
```

---

## Summary

You've learned:
- ✅ Difference between RPM and YUM
- ✅ Basic package management operations
- ✅ How to search, install, and remove packages
- ✅ Troubleshooting common issues
- ✅ Best practices for package management

### Next Steps:
- Practice with different packages
- Learn about repository management
- Explore advanced RPM queries
- Study package creation basics

---

## Additional Resources

- Red Hat Documentation: Package Management
- CentOS Wiki: Package Management
- RPM Official Documentation
- YUM Configuration Guide

---

*Remember: Practice makes perfect! Try these commands in your Docker environment safely.*