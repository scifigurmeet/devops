# Complete Nagios Monitoring Study Guide for Beginners

## Table of Contents
1. [Continuous Monitoring Concepts](#continuous-monitoring-concepts)
2. [Introduction to Nagios](#introduction-to-nagios)
3. [Installation of Nagios using Docker](#installation-of-nagios-using-docker)
4. [Nagios Configuration](#nagios-configuration)
5. [Monitoring Web Servers](#monitoring-web-servers)
6. [Using Nagios Web Interface](#using-nagios-web-interface)
7. [Deploying a Simple Web Application](#deploying-a-simple-web-application)
8. [Practical Exercises](#practical-exercises)
9. [Troubleshooting Guide](#troubleshooting-guide)

---

## 1. Continuous Monitoring Concepts

### Definition
Continuous monitoring is the practice of constantly observing and analyzing the performance, availability, and health of IT infrastructure, applications, and services in real-time. It involves automated collection, analysis, and reporting of system metrics to ensure optimal performance and quick problem resolution.

### Importance
- **Proactive Issue Detection**: Identify problems before they impact users
- **Reduced Downtime**: Minimize service interruptions through early warning systems
- **Performance Optimization**: Continuously track system performance metrics
- **Compliance**: Meet regulatory requirements for system monitoring
- **Business Continuity**: Ensure critical services remain operational
- **Cost Reduction**: Prevent expensive outages and optimize resource usage

### Benefits
- **Real-time Visibility**: Complete view of infrastructure health
- **Automated Alerting**: Immediate notifications for critical issues
- **Historical Analysis**: Trend analysis and capacity planning
- **Improved Response Time**: Faster incident resolution
- **Resource Optimization**: Better utilization of system resources
- **Enhanced Security**: Detection of security anomalies and breaches

---

## 2. Introduction to Nagios

### What is Nagios?
Nagios is an open-source monitoring system that watches hosts and services, alerting users when things go wrong and when they get better. It's designed to run on Linux but can monitor Windows, Linux, Unix, and network devices.

### Key Features
- **Comprehensive Monitoring**: Monitors network services, host resources, and server components
- **Plugin Architecture**: Extensible through plugins for custom monitoring
- **Alerting System**: Email, SMS, and custom notification methods
- **Web Interface**: User-friendly web-based dashboard
- **Event Handlers**: Automated response to system events
- **Reporting**: Historical data and trend analysis
- **Distributed Monitoring**: Support for multiple monitoring servers

### Nagios Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Nagios Core Architecture                  │
├─────────────────────────────────────────────────────────────┤
│  Web Interface (CGI)  │  Configuration Files  │  Log Files  │
├─────────────────────────────────────────────────────────────┤
│                    Nagios Core Engine                       │
├─────────────────────────────────────────────────────────────┤
│     Scheduler    │    Event Handler    │    Notifications   │
├─────────────────────────────────────────────────────────────┤
│                      Plugin Interface                       │
├─────────────────────────────────────────────────────────────┤
│  Standard Plugins  │  Custom Plugins  │  Third-party Plugins│
├─────────────────────────────────────────────────────────────┤
│              Monitored Hosts and Services                   │
└─────────────────────────────────────────────────────────────┘
```

### Components Breakdown

1. **Nagios Core Engine**: The main program that schedules monitoring tasks
2. **Plugins**: External programs that perform actual monitoring checks
3. **Configuration Files**: Define what to monitor and how
4. **Web Interface**: CGI-based web interface for viewing status
5. **Notifications**: Alert mechanisms for problems

### Plugins
Nagios plugins are standalone programs that return specific exit codes:
- **Exit Code 0**: OK - Service is working normally
- **Exit Code 1**: WARNING - Service is in warning state
- **Exit Code 2**: CRITICAL - Service is in critical state
- **Exit Code 3**: UNKNOWN - Service status cannot be determined

### Common Plugin Types
- **check_http**: Monitor web services
- **check_ping**: Check host reachability
- **check_ssh**: Monitor SSH services
- **check_disk**: Monitor disk usage
- **check_load**: Monitor system load
- **check_procs**: Monitor running processes

### Soft and Hard States

#### Soft States
- **Definition**: Temporary state that hasn't been confirmed by multiple checks
- **Characteristics**:
  - Occurs when a service check returns a non-OK state for the first time
  - Nagios will retry the check before considering it a "hard" state
  - No notifications are sent during soft states
  - Used to reduce false alarms

#### Hard States
- **Definition**: Confirmed state after multiple consecutive checks
- **Characteristics**:
  - Occurs when a service has been rechecked and confirmed to be in a non-OK state
  - Notifications are sent for hard states
  - Event handlers are executed
  - State is logged and appears in reports

#### State Transition Example
```
Service OK → Service WARNING (Soft State 1/3)
             ↓ (recheck)
Service WARNING (Soft State 2/3)
             ↓ (recheck)
Service WARNING (Hard State) → Notification Sent
```

---

## 3. Installation of Nagios using Docker

Since you're using Windows 10 with Docker Desktop, we'll use Docker containers for a clean, isolated Nagios installation.

### Prerequisites Check
Before starting, ensure you have:
- Docker Desktop installed and running
- At least 2GB RAM available
- Basic understanding of command line operations

### Step 1: Create Project Directory

**For Windows Command Prompt:**
```cmd
# Create project directory
mkdir nagios-monitoring
cd nagios-monitoring
```

**For Windows PowerShell (Recommended):**
```powershell
# Create project directory
New-Item -ItemType Directory -Name nagios-monitoring
Set-Location nagios-monitoring
```

### Step 2: Create Docker Compose File
Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  nagios:
    image: jasonrivers/nagios:latest
    container_name: nagios
    ports:
      - "8080:80"
    environment:
      - NAGIOSADMIN_USER=nagiosadmin
      - NAGIOSADMIN_PASS=password123
    volumes:
      - ./nagios/etc:/opt/nagios/etc
      - ./nagios/var:/opt/nagios/var
      - ./custom-plugins:/opt/Custom-Nagios-Plugins
    restart: unless-stopped
    
  web-server:
    image: nginx:alpine
    container_name: test-web-server
    ports:
      - "8081:80"
    volumes:
      - ./web-content:/usr/share/nginx/html
    restart: unless-stopped
```

### Step 3: Create Directory Structure

**For Windows Command Prompt:**
```cmd
# Create necessary directories
mkdir nagios\etc
mkdir nagios\var
mkdir custom-plugins
mkdir web-content

# Create a simple web page for testing
echo ^<h1^>Test Web Server^</h1^>^<p^>This is a test web server for Nagios monitoring.^</p^> > web-content\index.html
```

**For Windows PowerShell (Recommended):**
```powershell
# Create necessary directories
New-Item -ItemType Directory -Force -Path nagios\etc
New-Item -ItemType Directory -Force -Path nagios\var
New-Item -ItemType Directory -Force -Path custom-plugins
New-Item -ItemType Directory -Force -Path web-content

# Create a simple web page for testing
'<h1>Test Web Server</h1><p>This is a test web server for Nagios monitoring.</p>' | Out-File -FilePath web-content\index.html
```

### Step 4: Start Nagios Container

**For Windows Command Prompt or PowerShell:**
```cmd
# Start the containers
docker-compose up -d

# Check if containers are running
docker-compose ps
```

### Step 5: Access Nagios Web Interface
1. Open your web browser
2. Navigate to `http://localhost:8080/nagios`
3. Login with:
   - Username: `nagiosadmin`
   - Password: `password123`

### Step 6: Verify Installation

**For Windows Command Prompt or PowerShell:**
```cmd
# Check Nagios logs
docker-compose logs nagios

# Access Nagios container shell
docker exec -it nagios /bin/bash

# Check Nagios configuration (run this inside the container)
/opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg
```

---

## 4. Nagios Configuration

### Configuration File Structure
Nagios uses several configuration files:

```
/opt/nagios/etc/
├── nagios.cfg          # Main configuration file
├── cgi.cfg             # CGI configuration
├── resource.cfg        # Resource definitions
├── objects/
│   ├── commands.cfg    # Command definitions
│   ├── contacts.cfg    # Contact definitions
│   ├── hosts.cfg       # Host definitions
│   ├── services.cfg    # Service definitions
│   └── timeperiods.cfg # Time period definitions
```

### Basic Configuration Objects

#### 1. Host Definition
```bash
# Create host configuration
cat > nagios/etc/objects/hosts.cfg << 'EOF'
define host {
    host_name               test-web-server
    alias                   Test Web Server
    address                 web-server
    check_command           check-host-alive
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    d,u,r
    contact_groups          admins
}

define host {
    host_name               localhost
    alias                   Localhost
    address                 127.0.0.1
    check_command           check-host-alive
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    d,u,r
    contact_groups          admins
}
EOF
```

#### 2. Service Definition
```bash
# Create service configuration
cat > nagios/etc/objects/services.cfg << 'EOF'
define service {
    host_name               test-web-server
    service_description     HTTP
    check_command           check_http
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}

define service {
    host_name               localhost
    service_description     PING
    check_command           check_ping!100.0,20%!500.0,60%
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}
EOF
```

#### 3. Contact Definition
```bash
# Create contact configuration
cat > nagios/etc/objects/contacts.cfg << 'EOF'
define contact {
    contact_name                    nagiosadmin
    use                             generic-contact
    alias                           Nagios Admin
    email                           admin@localhost
}

define contactgroup {
    contactgroup_name       admins
    alias                   Nagios Administrators
    members                 nagiosadmin
}
EOF
```

#### 4. Command Definition
```bash
# Create custom commands
cat > nagios/etc/objects/commands.cfg << 'EOF'
define command {
    command_name    check_http
    command_line    /opt/nagios/libexec/check_http -H $HOSTADDRESS$ -p $ARG1$
}

define command {
    command_name    check_ping
    command_line    /opt/nagios/libexec/check_ping -H $HOSTADDRESS$ -w $ARG1$ -c $ARG2$
}

define command {
    command_name    check-host-alive
    command_line    /opt/nagios/libexec/check_ping -H $HOSTADDRESS$ -w 3000.0,80% -c 5000.0,100%
}
EOF
```

### Configuration Validation
```bash
# Restart Nagios to apply changes
docker-compose restart nagios

# Validate configuration
docker exec nagios /opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg
```

---

## 5. Monitoring Web Servers

### Setting Up Web Server Monitoring

#### 1. HTTP Service Check
```bash
# Add HTTP service check for our test web server
cat >> nagios/etc/objects/services.cfg << 'EOF'

define service {
    host_name               test-web-server
    service_description     HTTP Port 80
    check_command           check_http_port!80
    check_interval          2
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}
EOF
```

#### 2. Advanced HTTP Checks
```bash
# Add more sophisticated HTTP checks
cat >> nagios/etc/objects/services.cfg << 'EOF'

define service {
    host_name               test-web-server
    service_description     HTTP Response Time
    check_command           check_http_response_time!80!2!5
    check_interval          2
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}

define service {
    host_name               test-web-server
    service_description     HTTP Content Check
    check_command           check_http_content!80!Test Web Server
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}
EOF
```

#### 3. Custom Commands for Web Monitoring
```bash
# Add custom commands for web monitoring
cat >> nagios/etc/objects/commands.cfg << 'EOF'

define command {
    command_name    check_http_port
    command_line    /opt/nagios/libexec/check_http -H $HOSTADDRESS$ -p $ARG1$
}

define command {
    command_name    check_http_response_time
    command_line    /opt/nagios/libexec/check_http -H $HOSTADDRESS$ -p $ARG1$ -w $ARG2$ -c $ARG3$
}

define command {
    command_name    check_http_content
    command_line    /opt/nagios/libexec/check_http -H $HOSTADDRESS$ -p $ARG1$ -s "$ARG2$"
}
EOF
```

### Testing Web Server Monitoring
```bash
# Restart Nagios
docker-compose restart nagios

# Test the web server
curl http://localhost:8081

# Check if monitoring is working
docker exec nagios /opt/nagios/libexec/check_http -H web-server -p 80
```

---

## 6. Using Nagios Web Interface

### Accessing the Interface
1. Open browser and go to `http://localhost:8080/nagios`
2. Login with nagiosadmin/password123

### Main Interface Components

#### 1. Tactical Overview
- **Hosts**: Shows total hosts (UP/DOWN/UNREACHABLE)
- **Services**: Shows service status (OK/WARNING/CRITICAL/UNKNOWN)
- **Monitoring Features**: Shows what monitoring features are active

#### 2. Host Management

**Viewing Hosts:**
1. Click "Hosts" in the left menu
2. Select "Hosts" to see all monitored hosts
3. Click on a host name to see detailed information

**Managing Host States:**
- **Schedule Downtime**: Temporarily disable notifications
- **Disable Notifications**: Stop alerts for maintenance
- **Add Comments**: Document changes or issues

#### 3. Service Management

**Viewing Services:**
1. Click "Services" in the left menu
2. Select "Services" to see all monitored services
3. Filter by host or service status

**Service Actions:**
- **Re-schedule Next Check**: Force immediate check
- **Submit Passive Check Result**: Manually set service status
- **Disable/Enable Notifications**: Control alerting

#### 4. Scheduling Downtime

**For Hosts:**
```
1. Navigate to Host Detail page
2. Click "Schedule downtime for this host"
3. Set start/end times
4. Add comment explaining the maintenance
5. Choose if services should also be scheduled for downtime
```

**For Services:**
```
1. Navigate to Service Detail page
2. Click "Schedule downtime for this service"
3. Set duration and reason
4. Submit the downtime
```

#### 5. Adding Comments

**Host Comments:**
```
1. Go to Host Detail page
2. Click "Add a new comment"
3. Enter comment text
4. Choose if comment should be persistent
5. Submit comment
```

**Service Comments:**
```
1. Go to Service Detail page
2. Click "Add a new comment"
3. Provide descriptive comment
4. Submit
```

### Navigation Tips
- Use the left sidebar for quick navigation
- Status maps provide visual representation
- Reports section shows historical data
- Configuration section shows current settings

---

## 7. Deploying a Simple Web Application

### Creating a Multi-Service Web Application

#### 1. Update Docker Compose
```yaml
# Update docker-compose.yml
version: '3.8'

services:
  nagios:
    image: jasonrivers/nagios:latest
    container_name: nagios
    ports:
      - "8080:80"
    environment:
      - NAGIOSADMIN_USER=nagiosadmin
      - NAGIOSADMIN_PASS=password123
    volumes:
      - ./nagios/etc:/opt/nagios/etc
      - ./nagios/var:/opt/nagios/var
      - ./custom-plugins:/opt/Custom-Nagios-Plugins
    restart: unless-stopped
    depends_on:
      - web-app
      - database
    
  web-app:
    image: nginx:alpine
    container_name: web-app
    ports:
      - "8081:80"
    volumes:
      - ./web-app:/usr/share/nginx/html
    restart: unless-stopped
    
  database:
    image: mysql:8.0
    container_name: database
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=webapp
      - MYSQL_USER=appuser
      - MYSQL_PASSWORD=apppassword
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
    restart: unless-stopped
    
  api-server:
    image: python:3.9-slim
    container_name: api-server
    ports:
      - "5000:5000"
    volumes:
      - ./api-server:/app
    working_dir: /app
    command: python -m http.server 5000
    restart: unless-stopped

volumes:
  db_data:
```

#### 2. Create Web Application Content
```bash
# Create web application directory
mkdir -p web-app

# Create a simple HTML application
cat > web-app/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Sample Web Application</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .ok { background-color: #d4edda; color: #155724; }
        .warning { background-color: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <h1>Sample Web Application</h1>
    <p>This is a sample web application for Nagios monitoring demonstration.</p>
    
    <div class="status ok">
        <h3>Application Status: Running</h3>
        <p>All services are operational.</p>
    </div>
    
    <div class="status warning">
        <h3>Database Connection</h3>
        <p>Connected to MySQL database.</p>
    </div>
    
    <h3>Service Links:</h3>
    <ul>
        <li><a href="http://localhost:5000">API Server</a></li>
        <li><a href="http://localhost:8080/nagios">Nagios Monitoring</a></li>
    </ul>
</body>
</html>
EOF
```

#### 3. Create API Server
```bash
# Create API server directory
mkdir -p api-server

# Create a simple Python API
cat > api-server/app.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = {
                'status': 'ok',
                'message': 'API server is running',
                'services': {
                    'database': 'connected',
                    'web_server': 'running'
                }
            }
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 5000), APIHandler)
    print("API Server running on port 5000")
    server.serve_forever()
EOF
```

#### 4. Configure Nagios for Multi-Service Monitoring
```bash
# Update hosts configuration
cat > nagios/etc/objects/hosts.cfg << 'EOF'
define host {
    host_name               web-app
    alias                   Web Application Server
    address                 web-app
    check_command           check-host-alive
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    d,u,r
    contact_groups          admins
}

define host {
    host_name               database
    alias                   Database Server
    address                 database
    check_command           check-host-alive
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    d,u,r
    contact_groups          admins
}

define host {
    host_name               api-server
    alias                   API Server
    address                 api-server
    check_command           check-host-alive
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    d,u,r
    contact_groups          admins
}
EOF
```

#### 5. Configure Services for Each Component
```bash
# Update services configuration
cat > nagios/etc/objects/services.cfg << 'EOF'
# Web Application Services
define service {
    host_name               web-app
    service_description     HTTP
    check_command           check_http
    check_interval          2
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}

# Database Services
define service {
    host_name               database
    service_description     MySQL
    check_command           check_mysql
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}

# API Server Services
define service {
    host_name               api-server
    service_description     API Endpoint
    check_command           check_api_status
    check_interval          2
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}
EOF
```

#### 6. Add Custom Commands
```bash
# Add commands for new services
cat >> nagios/etc/objects/commands.cfg << 'EOF'

define command {
    command_name    check_mysql
    command_line    /opt/nagios/libexec/check_tcp -H $HOSTADDRESS$ -p 3306
}

define command {
    command_name    check_api_status
    command_line    /opt/nagios/libexec/check_http -H $HOSTADDRESS$ -p 5000 -u /status
}
EOF
```

---

## 8. Practical Exercises

### Exercise 1: Basic Monitoring Setup
**Objective**: Set up basic host and service monitoring

**Tasks**:
1. Start the Docker environment
2. Access Nagios web interface
3. Verify all hosts are being monitored
4. Check service status for all components

**Commands**:
```bash
# Start environment
docker-compose up -d

# Check status
docker-compose ps

# Access Nagios
# Navigate to http://localhost:8080/nagios
```

### Exercise 2: Service Testing
**Objective**: Test monitoring by simulating service failures

**Tasks**:
1. Stop the web application container
2. Observe status changes in Nagios
3. Add comments documenting the issue
4. Restart the service
5. Verify recovery in Nagios

**Commands**:
```bash
# Stop web application
docker-compose stop web-app

# Check Nagios interface for status changes
# Add comment through web interface

# Restart service
docker-compose start web-app
```

### Exercise 3: Scheduled Downtime
**Objective**: Practice scheduling maintenance windows

**Tasks**:
1. Schedule downtime for database server
2. Perform simulated maintenance
3. Verify notifications are suppressed
4. End downtime early if needed

**Steps**:
1. Navigate to database host in Nagios
2. Click "Schedule downtime for this host"
3. Set 30-minute downtime window
4. Add comment about maintenance
5. Submit downtime request

### Exercise 4: Custom Plugin Development
**Objective**: Create a custom monitoring plugin

**Tasks**:
1. Create a custom plugin script
2. Configure Nagios to use the plugin
3. Test the plugin functionality

**Custom Plugin Example**:
```bash
# Create custom plugin directory
mkdir -p custom-plugins

# Create a simple disk usage plugin
cat > custom-plugins/check_disk_usage.sh << 'EOF'
#!/bin/bash

# Simple disk usage check plugin
# Returns OK if disk usage < 80%, WARNING if 80-90%, CRITICAL if > 90%

USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ $USAGE -lt 80 ]; then
    echo "OK - Disk usage is ${USAGE}%"
    exit 0
elif [ $USAGE -lt 90 ]; then
    echo "WARNING - Disk usage is ${USAGE}%"
    exit 1
else
    echo "CRITICAL - Disk usage is ${USAGE}%"
    exit 2
fi
EOF

# Make it executable
chmod +x custom-plugins/check_disk_usage.sh
```

### Exercise 5: Monitoring External Services
**Objective**: Monitor external websites and services

**Tasks**:
1. Add external website monitoring
2. Configure SSL certificate checks
3. Set up response time monitoring

**Configuration**:
```bash
# Add external host
cat >> nagios/etc/objects/hosts.cfg << 'EOF'

define host {
    host_name               google
    alias                   Google Search
    address                 google.com
    check_command           check-host-alive
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    d,u,r
    contact_groups          admins
}
EOF

# Add external service
cat >> nagios/etc/objects/services.cfg << 'EOF'

define service {
    host_name               google
    service_description     HTTPS
    check_command           check_https
    check_interval          5
    retry_interval          1
    max_check_attempts      3
    check_period            24x7
    notification_interval   30
    notification_period     24x7
    notification_options    w,u,c,r
    contact_groups          admins
}
EOF
```

---

## 9. Troubleshooting Guide

### Common Issues and Solutions

#### Issue 1: Nagios Configuration Errors
**Symptoms**: Configuration validation fails

**Solution**:
```bash
# Check configuration syntax
docker exec nagios /opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg

# Check specific file syntax
docker exec nagios /opt/nagios/bin/nagios -v /opt/nagios/etc/objects/hosts.cfg
```

#### Issue 2: Plugin Execution Problems
**Symptoms**: Services show UNKNOWN status

**Solution**:
```bash
# Test plugin manually
docker exec nagios /opt/nagios/libexec/check_http -H web-app -p 80

# Check plugin permissions
docker exec nagios ls -la /opt/nagios/libexec/check_http

# Verify plugin exists
docker exec nagios ls -la /opt/nagios/libexec/
```

#### Issue 3: Web Interface Access Problems
**Symptoms**: Cannot access Nagios web interface

**Solution**:
```bash
# Check if container is running
docker-compose ps

# Check port mapping
docker port nagios

# Check logs
docker-compose logs nagios

# Restart container
docker-compose restart nagios
```

#### Issue 4: Service Check Failures
**Symptoms**: Services showing CRITICAL when they should be OK

**Solution**:
```bash
# Check network connectivity
docker exec nagios ping web-app

# Test service manually
docker exec nagios /opt/nagios/libexec/check_http -H web-app

# Check service configuration
docker exec nagios cat /opt/nagios/etc/objects/services.cfg
```

### Performance Optimization

#### 1. Adjust Check Intervals
```bash
# Reduce check frequency for stable services
check_interval          10    # Instead of 5
retry_interval          2     # Instead of 1
```

#### 2. Optimize Plugin Timeouts
```bash
# Set appropriate timeouts for plugins
command_line    /opt/nagios/libexec/check_http -H $HOSTADDRESS$ -t 30
```

#### 3. Use Service Dependencies
```bash
# Define service dependencies to reduce unnecessary checks
define servicedependency {
    host_name                   web-app
    service_description         HTTP
    dependent_host_name         web-app
    dependent_service_description   Database Connection
    execution_failure_criteria n
    notification_failure_criteria w,u,c
}
```

### Log Analysis

#### Nagios Log Files
```bash
# Main Nagios log
docker exec nagios tail -f /opt/nagios/var/nagios.log

# Archive logs
docker exec nagios ls -la /opt/nagios/var/archives/

# Check for errors
docker exec nagios grep ERROR /opt/nagios/var/nagios.log
```

### Backup and Recovery

#### Configuration Backup
```bash
# Backup configuration
docker exec nagios tar -czf /tmp/nagios-config-backup.tar.gz /opt/nagios/etc/

# Copy backup to host
docker cp nagios:/tmp/nagios-config-backup.tar.gz ./backup/
```

#### Recovery Process
```bash
# Restore configuration
docker cp ./backup/nagios-config-backup.tar.gz nagios:/tmp/

# Extract backup
docker exec nagios tar -xzf /tmp/nagios-config-
