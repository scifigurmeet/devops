# DevOps Automation - Unit 3: Automating the Linux Tasks

## Table of Contents
1. [Introduction](#introduction)
2. [Understanding Cron and Crontab](#understanding-cron-and-crontab)
3. [Crontab Syntax](#crontab-syntax)
4. [Practical Exercises](#practical-exercises)
5. [Best Practices and Tips](#best-practices-and-tips)
6. [Conclusion](#conclusion)

## 1. Introduction

Welcome to Unit 3 of the DevOps Automation course. In this unit, we'll dive deep into automating Linux tasks using cron and crontab. These powerful tools are essential for any DevOps engineer, allowing for the scheduling and automation of various system tasks and scripts.

## 2. Understanding Cron and Crontab

### What is Cron?

Cron is a time-based job scheduler in Unix-like operating systems. It enables users to schedule jobs (commands or shell scripts) to run periodically at fixed times, dates, or intervals.

🔑 **Key Points:**
- Cron runs as a daemon process in the background.
- It reads configuration files called "crontabs" to execute scheduled tasks.

### What is Crontab?

Crontab (Cron Table) is a file containing the schedule of cron entries to be run at specified times. 

📌 **Facts:**
- Each user can have their own crontab file.
- The system also has a global crontab file, typically located at `/etc/crontab`.

### Scope of Crontab

Crontab has a wide scope in system administration and DevOps:

1. **System Maintenance**: Scheduling cleanup tasks, log rotations, backups.
2. **Monitoring**: Regular checking of system health, resource usage.
3. **Updates**: Scheduling software updates and patches.
4. **Data Processing**: Running periodic data analysis or reporting scripts.
5. **Notifications**: Sending regular status updates or reports.

### Use Cases of Crontab

Some common use cases include:

- Daily database backups at midnight.
- Sending weekly report emails every Monday at 8 AM.
- Checking system load every 5 minutes.
- Clearing temporary files every hour.

## 3. Crontab Syntax

Understanding crontab syntax is crucial for effectively scheduling tasks.

### Basic Syntax

A crontab entry typically has six fields:

```
* * * * * command_to_execute
│ │ │ │ │
│ │ │ │ └─── Day of the week (0 - 7) (Sunday = 0 or 7)
│ │ │ └────── Month (1 - 12)
│ │ └─────────── Day of the month (1 - 31)
│ └──────────────── Hour (0 - 23)
└───────────────────── Minute (0 - 59)
```

### Special Characters

- `*`: Matches any value
- `,`: Specifies a list of values
- `-`: Specifies a range of values
- `/`: Specifies steps

### Examples

1. Run every minute:
   ```
   * * * * * /path/to/script.sh
   ```

2. Run at 3:30 AM daily:
   ```
   30 3 * * * /path/to/script.sh
   ```

3. Run every Monday at 9 AM:
   ```
   0 9 * * 1 /path/to/script.sh
   ```

4. Run every 15 minutes:
   ```
   */15 * * * * /path/to/script.sh
   ```

## 4. Practical Exercises

Let's dive into some practical exercises to reinforce your understanding of crontab.

### Exercise 1: Creating Your First Cron Job

**Objective**: Create a cron job that logs the current date and time every 5 minutes.

**Steps**:

1. Open the terminal and edit your crontab:
   ```
   crontab -e
   ```

2. Add the following line to the crontab:
   ```
   */5 * * * * date >> /home/yourusername/time_log.txt
   ```

3. Save and exit the editor.

**Explanation**: This cron job will append the current date and time to the `time_log.txt` file every 5 minutes.

### Exercise 2: Scheduling System Updates

**Objective**: Schedule a system update to run every Sunday at 1 AM.

**Steps**:

1. Create a script named `update_system.sh`:
   ```bash
   #!/bin/bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Make the script executable:
   ```
   chmod +x update_system.sh
   ```

3. Edit your crontab:
   ```
   crontab -e
   ```

4. Add the following line:
   ```
   0 1 * * 0 /path/to/update_system.sh >> /home/yourusername/update_log.txt 2>&1
   ```

**Explanation**: This cron job will run the system update script every Sunday at 1 AM and log the output.

### Exercise 3: Rotating Log Files

**Objective**: Set up a cron job to rotate log files daily.

**Steps**:

1. Create a script named `rotate_logs.sh`:
   ```bash
   #!/bin/bash
   
   LOG_DIR="/var/log/myapp"
   TIMESTAMP=$(date +"%Y%m%d")
   
   for log in $LOG_DIR/*.log; do
       mv $log $log.$TIMESTAMP
       gzip $log.$TIMESTAMP
   done
   ```

2. Make the script executable:
   ```
   chmod +x rotate_logs.sh
   ```

3. Edit your crontab:
   ```
   crontab -e
   ```

4. Add the following line:
   ```
   0 0 * * * /path/to/rotate_logs.sh
   ```

**Explanation**: This cron job will run the log rotation script daily at midnight, renaming current log files with a timestamp and compressing them.

## 5. Best Practices and Tips

1. **Use Absolute Paths**: Always use full paths in cron jobs to avoid issues with working directories.

2. **Redirect Output**: Redirect stdout and stderr to a log file for easier troubleshooting:
   ```
   * * * * * /path/to/script.sh >> /path/to/logfile.log 2>&1
   ```

3. **Set a PATH**: If your scripts rely on commands in various locations, set the PATH at the beginning of your crontab:
   ```
   PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
   ```

4. **Use Comments**: Add comments to your crontab entries for better maintainability:
   ```
   # Daily backup at 2 AM
   0 2 * * * /path/to/backup_script.sh
   ```

5. **Test Your Scripts**: Always test your scripts manually before adding them to crontab.

6. **Use Cron Wrappers**: For more complex scheduling needs, consider using cron wrappers like `anacron` or `fcron`.

## 6. Conclusion

In this unit, we've explored the power of cron and crontab for automating Linux tasks. We've covered the basics of cron, crontab syntax, and worked through practical exercises to reinforce your understanding.

🔑 **Key Takeaways**:
- Cron is a powerful tool for scheduling recurring tasks in Linux systems.
- Understanding crontab syntax is crucial for effective task scheduling.
- Proper logging and error handling are important for maintaining cron jobs.
- Regular review and maintenance of cron jobs is essential for system health.

As you continue your DevOps journey, remember that mastering cron and crontab is just the beginning. These tools will serve as a foundation for more advanced automation techniques you'll encounter in your career.

