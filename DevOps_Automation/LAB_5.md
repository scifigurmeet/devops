# DevOps Automation Lab
## Unit 5: Scheduling and Time-based Tasks

### Overview
In this lab, you'll learn about scheduling tasks and managing time-based operations in a DevOps environment. We'll focus on two key areas:
1. Working with Cron
2. Managing time in Nagios

By the end of this lab, you'll be able to schedule automated tasks and monitor time-sensitive operations in a Linux environment using Docker containers.

### Prerequisites
- Windows PC with Docker Desktop installed
- Basic understanding of Linux commands
- Familiarity with Docker concepts

### Part 1: Working with Cron

#### 1.1 Setting up the Ubuntu Container

First, let's set up an Ubuntu container where we'll work with Cron:

```bash
docker run -it --name ubuntu-cron ubuntu:latest
```

Once inside the container, update the package list and install Cron:

```bash
apt-get update
apt-get install -y cron
```

#### 1.2 Understanding Cron Syntax

Cron uses a specific syntax to schedule tasks. The basic format is:

```
* * * * * command_to_execute
```

Each asterisk represents:
- Minute (0-59)
- Hour (0-23)
- Day of the month (1-31)
- Month (1-12)
- Day of the week (0-7, where 0 and 7 are Sunday)

#### 1.3 Creating a Cron Job

Let's create a simple Cron job that writes the current date and time to a file every minute:

1. Open the crontab file:
   ```bash
   crontab -e
   ```
   (Choose your preferred editor if prompted)

2. Add the following line:
   ```
   * * * * * date >> /root/cron_log.txt
   ```

3. Save and exit the editor.

#### 1.4 Verifying the Cron Job

To verify that your Cron job is working:

1. Wait for a minute or two.
2. Check the contents of the log file:
   ```bash
   cat /root/cron_log.txt
   ```

You should see multiple entries with timestamps.

#### 1.5 Exercise

Create a Cron job that runs a script every day at 3 AM. The script should:
- Create a backup of a specified directory
- Delete files older than 7 days in a specified directory

Hint: You'll need to write a bash script and schedule it with Cron.

### Part 2: Managing Time in Nagios

For this part, we'll use a pre-configured Nagios Docker image to explore time management in Nagios.

#### 2.1 Setting up Nagios Container

Pull and run the Nagios container:

```bash
docker run --name nagios4 -p 0.0.0.0:8080:80 jasonrivers/nagios:latest
```

Access Nagios web interface at `http://localhost:8080/nagios`
- Username: `nagiosadmin`
- Password: `nagios`

#### 2.2 Understanding Time-Related Concepts in Nagios

In Nagios, several time-related concepts are crucial:

1. **Check Interval**: How often Nagios checks the status of a host or service.
2. **Retry Interval**: How often Nagios rechecks a host or service in a non-OK state.
3. **Notification Interval**: How often Nagios sends notifications about a problem.
4. **Time Periods**: Defined time ranges when checks or notifications are active.

#### 2.3 Configuring Time-Related Settings

Let's modify the check interval for a host:

1. In the Nagios container, navigate to the configuration directory:
   ```bash
   cd /opt/nagios/etc/objects
   ```

2. Edit the `localhost.cfg` file:
   ```bash
   vi localhost.cfg
   ```

3. Find the host definition and modify the `check_interval`:
   ```
   define host {
       use                     linux-server
       host_name               localhost
       alias                   localhost
       address                 127.0.0.1
       check_interval          5  ; Check every 5 minutes
   }
   ```

4. Save the file and exit.

5. Restart Nagios to apply changes:
   ```bash
   /etc/init.d/nagios restart
   ```

#### 2.4 Creating a Custom Time Period

Let's create a time period for business hours:

1. Edit the `timeperiods.cfg` file:
   ```bash
   vi /opt/nagios/etc/objects/timeperiods.cfg
   ```

2. Add the following definition:
   ```
   define timeperiod {
       timeperiod_name business_hours
       alias           Normal Business Hours
       monday          09:00-17:00
       tuesday         09:00-17:00
       wednesday       09:00-17:00
       thursday        09:00-17:00
       friday          09:00-17:00
   }
   ```

3. Save the file and restart Nagios.

#### 2.5 Exercise

Create a new service check that:
- Runs every 10 minutes
- Only during business hours
- Has a different retry interval for non-OK states

Hint: You'll need to define a new service in a configuration file and use the time period we created.

### Conclusion

In this lab, you've learned how to work with Cron for task scheduling and manage time-related settings in Nagios. These skills are crucial for automating and monitoring time-sensitive operations in a DevOps environment.

### Additional Resources
- Cron documentation: https://man7.org/linux/man-pages/man5/crontab.5.html
- Nagios time management: https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/timeperiods.html

Remember to stop and remove your Docker containers when you're done with the lab:
```bash
docker stop ubuntu-cron nagios4
docker rm ubuntu-cron nagios4
```
