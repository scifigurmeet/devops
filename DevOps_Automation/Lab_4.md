# CSV 206 – DevOps Automation Lab
## Unit 4: System Administration and Security

### Introduction

In this lab, we'll focus on two critical aspects of system administration and security:
1. Blocking the execution of forbidden commands
2. Monitoring disk usage and alerting when it exceeds a specified threshold

These practices are essential for maintaining system security and stability in a DevOps environment.

### Objectives

By the end of this lab, you will be able to:
1. Implement a script to block forbidden commands
2. Create a disk usage monitoring script with alert functionality
3. Understand basic system administration and security concepts

### Prerequisites

- A Linux-based system (Ubuntu 20.04 LTS recommended)
- Basic knowledge of Bash scripting
- sudo privileges on your system

### Part 1: Blocking Forbidden Commands

In this section, we'll create a script that prevents the execution of specified commands.

1. Create a new file called `block_commands.sh`:

   ```bash
   nano block_commands.sh
   ```

2. Add the following content to the file:

   ```bash
   #!/bin/bash

   # List of forbidden commands
   FORBIDDEN_COMMANDS=("rm -rf /" "mkfs" "dd" "format")

   # Function to check if a command is forbidden
   is_forbidden() {
       local cmd="$1"
       for forbidden in "${FORBIDDEN_COMMANDS[@]}"; do
           if [[ "$cmd" == *"$forbidden"* ]]; then
               return 0
           fi
       done
       return 1
   }

   # Main script
   while true; do
       read -p "Enter a command: " user_command
       if is_forbidden "$user_command"; then
           echo "Error: This command is forbidden and cannot be executed."
       else
           echo "Executing: $user_command"
           eval "$user_command"
       fi
   done
   ```

3. Save the file and exit the editor.

4. Make the script executable:

   ```bash
   chmod +x block_commands.sh
   ```

5. Run the script:

   ```bash
   ./block_commands.sh
   ```

6. Test the script by entering both allowed and forbidden commands.

### Part 2: Monitoring Disk Usage with Alerts

In this section, we'll create a script that monitors disk usage and sends an alert when it exceeds a specified threshold.

1. Create a new file called `monitor_disk_usage.sh`:

   ```bash
   nano monitor_disk_usage.sh
   ```

2. Add the following content to the file:

   ```bash
   #!/bin/bash

   # Configuration
   THRESHOLD=80  # Disk usage threshold (%)
   CHECK_INTERVAL=300  # Check every 5 minutes (300 seconds)
   ALERT_EMAIL="admin@example.com"  # Change this to your email

   # Function to get disk usage for root partition
   get_disk_usage() {
       df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
   }

   # Function to send email alert
   send_alert() {
       local usage=$1
       echo "Disk usage alert: ${usage}% of disk space used." | mail -s "High Disk Usage Alert" "$ALERT_EMAIL"
   }

   # Main monitoring loop
   while true; do
       usage=$(get_disk_usage)
       if [ "$usage" -gt "$THRESHOLD" ]; then
           echo "Warning: Disk usage is at ${usage}%"
           send_alert "$usage"
       else
           echo "Disk usage is at ${usage}%"
       fi
       sleep "$CHECK_INTERVAL"
   done
   ```

3. Save the file and exit the editor.

4. Make the script executable:

   ```bash
   chmod +x monitor_disk_usage.sh
   ```

5. Install the `mailutils` package to enable email functionality:

   ```bash
   sudo apt-get update
   sudo apt-get install mailutils
   ```

6. Run the script:

   ```bash
   ./monitor_disk_usage.sh
   ```

   Note: Keep the script running in a separate terminal or run it in the background for continuous monitoring.

### Exercises

1. Modify the `block_commands.sh` script to log attempted executions of forbidden commands to a file.

2. Update the `monitor_disk_usage.sh` script to monitor multiple partitions instead of just the root partition.

3. Implement a feature in the `monitor_disk_usage.sh` script to automatically delete old log files when disk usage is high.

4. Create a new script that combines both functionalities: blocking forbidden commands and monitoring disk usage.

5. Implement a simple web interface using Python Flask to display the current disk usage and recent command execution attempts.

### Best Practices

1. Regularly update your list of forbidden commands based on your organization's security policies.
2. Use more sophisticated methods like SELinux or AppArmor for comprehensive system hardening in production environments.
3. Implement proper logging and alerting mechanisms for all critical system events.
4. Regularly review and test your monitoring scripts to ensure they're functioning correctly.
5. Use secure methods to store and transmit sensitive information like email addresses and system alerts.

### Conclusion

In this lab, you've learned how to implement basic system administration and security measures using Bash scripts. You've created a script to block forbidden commands and another to monitor disk usage with alerts. These scripts form a foundation for more comprehensive system monitoring and security practices in a DevOps environment.

Remember that while these scripts are useful for learning purposes, production environments often require more robust, scalable solutions. Always follow your organization's security policies and best practices when implementing system administration and security measures.
