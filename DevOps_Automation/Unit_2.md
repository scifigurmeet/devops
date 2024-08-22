# DevOps Automation - Unit 2: Advantages of Automation

## Table of Contents
1. [Introduction](#introduction)
2. [Advantages of Automation](#advantages-of-automation)
3. [Automation Scenarios](#automation-scenarios)
4. [Practical Exercises](#practical-exercises)
5. [Conclusion](#conclusion)

## 1. Introduction

Welcome to Unit 2 of the DevOps Automation course. In this unit, we'll explore the advantages of automation and dive into various automation scenarios that are common in DevOps practices. By the end of this unit, you'll have a solid understanding of why automation is crucial in DevOps and how to implement it in various scenarios.

## 2. Advantages of Automation

Automation in DevOps offers numerous benefits that contribute to improved efficiency, reliability, and scalability of software development and operations processes.

🚀 **Key Advantages:**

1. **Consistency**: Automated processes ensure tasks are performed identically each time, reducing human errors.
2. **Speed**: Automation significantly reduces the time required to perform repetitive tasks.
3. **Scalability**: Automated processes can easily handle increased workloads without proportional increases in time or resources.
4. **Cost-effectiveness**: While initial setup may require investment, automation reduces long-term operational costs.
5. **Improved quality**: Automated testing and deployment processes lead to more reliable and stable software releases.
6. **Enhanced collaboration**: Automation tools provide a common platform for developers and operations teams to work together.
7. **Increased productivity**: By automating routine tasks, team members can focus on more valuable, creative work.
8. **Better compliance and security**: Automated processes can enforce security policies and maintain audit trails consistently.

## 3. Automation Scenarios

Let's explore some common automation scenarios in DevOps:

### 3.1 Archiving Logs

Automating log archival ensures that important system and application logs are regularly backed up and organized.

### 3.2 Auto-Discard Old Archives

Automatically removing old archives helps manage storage space and keeps the system clean.

### 3.3 MySQL (RDBMS) Backups

Regular automated backups of databases are crucial for data protection and disaster recovery.

### 3.4 Email Web Server Summary

Sending automated reports about web server status helps in proactive monitoring and quick issue resolution.

### 3.5 Ensure Web Server is Running

Automated checks and restarts of web servers ensure high availability of web applications.

### 3.6 User Command Validation

Automating the validation of user commands enhances system security and prevents accidental misuse.

### 3.7 Disk Usage Alarm

Automated alerts for high disk usage help prevent system failures due to lack of storage space.

### 3.8 Sending Files to Recycle Bin

Automating the process of moving files to a recycle bin instead of permanent deletion aids in data recovery if needed.

### 3.9 Restoring Files from Recycle Bin

Automated restoration processes can help quickly recover accidentally deleted files.

### 3.10 Logging Delete Actions

Keeping automated logs of file deletions aids in auditing and tracking system changes.

### 3.11 File Formatter

Automating file formatting ensures consistency across all documents and code files in a project.

### 3.12 Decrypting Files

Automated decryption processes can streamline access to encrypted data when needed.

### 3.13 Bulk File Downloader

Automating the download of multiple files saves time and reduces manual effort.

### 3.14 System Information

Automated collection and reporting of system information aids in monitoring and troubleshooting.

### 3.15 Install LAMP Stack

Automating the installation of common software stacks like LAMP (Linux, Apache, MySQL, PHP) ensures consistent development environments.

### 3.16 Get NIC's IP

Automated retrieval of network interface IP addresses aids in network configuration and troubleshooting.

## 4. Practical Exercises

Let's dive into some practical exercises to implement automation for some of the scenarios we discussed.

### Exercise 1: Automating Log Archival

In this exercise, we'll create a bash script to automatically archive log files.

```bash
#!/bin/bash

# Set variables
LOG_DIR="/var/log"
ARCHIVE_DIR="/var/log/archives"
DATE=$(date +%Y%m%d)

# Create archive directory if it doesn't exist
mkdir -p $ARCHIVE_DIR

# Archive logs older than 7 days
find $LOG_DIR -name "*.log" -type f -mtime +7 -exec gzip -c {} \; | tar -cvf $ARCHIVE_DIR/logs_$DATE.tar.gz -T -

# Remove original log files older than 7 days
find $LOG_DIR -name "*.log" -type f -mtime +7 -delete

echo "Log archival completed on $DATE"
```

**Instructions:**
1. Save this script as `archive_logs.sh` in a suitable location (e.g., `/usr/local/bin/`).
2. Make the script executable: `chmod +x /usr/local/bin/archive_logs.sh`
3. Set up a cron job to run this script daily:
   ```
   0 1 * * * /usr/local/bin/archive_logs.sh >> /var/log/archive_logs.log 2>&1
   ```

**Intention:** This script automates the process of archiving log files older than 7 days, compressing them, and removing the original files to save space.

**Interpretation:** By running this script daily via cron, you ensure that your log files are regularly archived and your system doesn't run out of disk space due to ever-growing log files.

### Exercise 2: Automated MySQL Backup

Let's create a script to automate MySQL database backups.

```bash
#!/bin/bash

# Set variables
BACKUP_DIR="/var/backups/mysql"
DATE=$(date +%Y%m%d)
MYSQL_USER="backup_user"
MYSQL_PASSWORD="your_password"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Get list of databases
databases=$(mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SHOW DATABASES;" | grep -Ev "(Database|information_schema|performance_schema)")

# Backup each database
for db in $databases; do
    mysqldump -u $MYSQL_USER -p$MYSQL_PASSWORD --databases $db | gzip > "$BACKUP_DIR/$db-$DATE.sql.gz"
done

# Remove backups older than 30 days
find $BACKUP_DIR -type f -name "*.sql.gz" -mtime +30 -delete

echo "MySQL backup completed on $DATE"
```

**Instructions:**
1. Save this script as `mysql_backup.sh` in a suitable location (e.g., `/usr/local/bin/`).
2. Make the script executable: `chmod +x /usr/local/bin/mysql_backup.sh`
3. Create a MySQL user with appropriate permissions for backups.
4. Set up a cron job to run this script daily:
   ```
   0 2 * * * /usr/local/bin/mysql_backup.sh >> /var/log/mysql_backup.log 2>&1
   ```

**Intention:** This script automates the process of backing up all MySQL databases individually, compressing the backups, and removing old backups to manage storage.

**Interpretation:** By running this script daily, you ensure that you have recent backups of all your MySQL databases, which is crucial for data protection and disaster recovery.

### Exercise 3: Automated Web Server Status Check

Let's create a script to check if the Apache web server is running and restart it if it's down.

```bash
#!/bin/bash

# Check if Apache is running
if ! pgrep apache2 > /dev/null
then
    echo "Apache is not running. Attempting to start..."
    systemctl start apache2
    sleep 5
    
    # Check if Apache started successfully
    if pgrep apache2 > /dev/null
    then
        echo "Apache started successfully."
        # Send email notification
        echo "Apache was down and has been restarted successfully." | mail -s "Apache Restarted" admin@example.com
    else
        echo "Failed to start Apache. Manual intervention required."
        # Send email notification
        echo "Failed to start Apache. Manual intervention required." | mail -s "Apache Start Failure" admin@example.com
    fi
else
    echo "Apache is running."
fi
```

**Instructions:**
1. Save this script as `check_apache.sh` in a suitable location (e.g., `/usr/local/bin/`).
2. Make the script executable: `chmod +x /usr/local/bin/check_apache.sh`
3. Set up a cron job to run this script every 5 minutes:
   ```
   */5 * * * * /usr/local/bin/check_apache.sh >> /var/log/apache_check.log 2>&1
   ```

**Intention:** This script automates the process of checking if the Apache web server is running, attempts to restart it if it's down, and sends email notifications about the status.

**Interpretation:** By running this script regularly, you ensure high availability of your web server. If Apache goes down, it will be automatically restarted, and you'll be notified of the event.

## 5. Conclusion

In this unit, we've explored the numerous advantages of automation in DevOps and looked at various automation scenarios. Through practical exercises, we've implemented automation for log archival, database backups, and web server monitoring.

🔑 **Key Takeaways:**
- Automation improves consistency, speed, and reliability of DevOps processes.
- Proper implementation of automation can significantly reduce operational costs and human errors.
- Regular backups, monitoring, and proactive maintenance can be effectively managed through automation.
- Bash scripting and cron jobs are powerful tools for implementing automation in Linux environments.

As you continue your DevOps journey, always look for opportunities to automate repetitive tasks. Remember, the goal of automation is not just to save time, but to improve the overall quality and reliability of your systems and processes.

