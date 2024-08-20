# Basic Monitoring Stack Setup Guide

## Introduction

In this practical guide, we'll set up a basic monitoring stack using Docker on a Windows 11 PC. We'll cover the following tools:

1. Prometheus
2. Grafana
3. Node Exporter
4. Nagios

Each of these tools plays a crucial role in monitoring and visualizing the health and performance of your infrastructure.

## Tool Overview

### Prometheus

Prometheus is an open-source monitoring and alerting toolkit. It collects and stores time-series data as metrics, making it ideal for monitoring system and application performance.

**Key Features:**
- Powerful query language (PromQL)
- Multi-dimensional data model
- No reliance on distributed storage
- Pull model for collecting metrics

### Grafana

Grafana is an open-source platform for monitoring and observability. It allows you to visualize, alert on, and understand your metrics no matter where they are stored.

**Key Features:**
- Beautiful, customizable dashboards
- Support for multiple data sources
- Alerting capabilities
- Plugin ecosystem

### Node Exporter

Node Exporter is a Prometheus exporter for hardware and OS metrics. It provides detailed information about the system it's running on, exposing a wide variety of hardware and kernel-related metrics.

**Key Features:**
- Exposes system metrics (CPU, memory, disk, network)
- Easy to deploy and integrate with Prometheus
- Extensible through textfile collector

### Nagios

Nagios is an open-source monitoring system that watches hosts and services, alerting you when things go wrong and again when they get better. It's particularly powerful for infrastructure monitoring.

**Key Features:**
- Monitor network services (SMTP, POP3, HTTP, NNTP, etc.)
- Monitor host resources (processor load, disk usage, etc.)
- Simple plugin design that allows users to easily develop their own service checks
- Parallelized service checks

## Practical Guide

### Step 1: Set up Docker Compose

Create a new directory for your project and create a `docker-compose.yml` file with the following content:

```yaml
version: '3'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"

  nagios:
    image: jasonrivers/nagios
    ports:
      - "8080:80"
    environment:
      - NAGIOSADMIN_PASS=nagios
    volumes:
      - ./custom_nagios.cfg:/opt/nagios/etc/objects/custom_nagios.cfg
```

### Step 2: Configure Prometheus

Create a `prometheus.yml` file in the same directory with the following content:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

### Step 3: Start the Services

Open a command prompt in your project directory and run:

```
docker-compose up -d
```

This will start all the services defined in your `docker-compose.yml` file.

### Step 4: Access the Tools

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (username: admin, password: admin)
- Node Exporter metrics: http://localhost:9100/metrics
- Nagios: http://localhost:8080/nagios (username: nagiosadmin, password: nagios)

### Step 5: Configure Grafana

1. Log in to Grafana
2. Add Prometheus as a data source:
   - Go to Configuration > Data Sources
   - Click "Add data source"
   - Choose Prometheus
   - Set URL to `http://prometheus:9090` (or http://host.docker.internal:9090)
   - Click "Save & Test"

3. Create a new dashboard:
   - Click "+" > "Create Dashboard"
   - Add a new panel
   - In the query editor, you can now use PromQL to query metrics

### Step 6: Example Grafana Dashboard

Here's a simple PromQL query to get you started:

```
node_cpu_seconds_total{mode="system"}
```

This query will show the total CPU time spent in system mode.

## Nagios: In-Depth Look and Infrastructure Monitoring

Nagios is a powerful tool for infrastructure monitoring, providing real-time awareness of your IT infrastructure's state and alerting you to problems before they impact your users or business operations.

### How Nagios Works for Infrastructure Monitoring

1. **Checks**: Nagios performs regular checks on hosts and services.
2. **States**: Each check results in a state: OK, WARNING, CRITICAL, or UNKNOWN.
3. **Notifications**: Based on the state and configuration, Nagios sends notifications.
4. **Escalations**: Problems can be escalated to different support groups over time.
5. **Reporting**: Nagios provides availability reports and performance graphs.

### Key Infrastructure Metrics Monitored by Nagios

1. **Server Health**
   - CPU usage
   - Memory usage
   - Disk usage
   - System load
   - Uptime

2. **Network Performance**
   - Bandwidth usage
   - Packet loss
   - Network latency

3. **Service Availability**
   - Web server status
   - Database server status
   - Mail server status

4. **Application Performance**
   - Response time
   - Error rates
   - Queue lengths

5. **Security Metrics**
   - Failed login attempts
   - Firewall status
   - Intrusion detection alerts

### Use Cases for Nagios in Infrastructure Monitoring

1. **Data Center Monitoring**
   - Monitor temperature and humidity in server rooms
   - Track power consumption and UPS status
   - Monitor HVAC systems

2. **Network Infrastructure Monitoring**
   - Monitor router and switch performance
   - Track bandwidth usage across network links
   - Monitor VPN tunnels and firewall status

3. **Web Application Stack Monitoring**
   - Monitor web server performance (Apache, Nginx)
   - Track database server health (MySQL, PostgreSQL)
   - Monitor application server status (Tomcat, Node.js)

4. **Cloud Infrastructure Monitoring**
   - Monitor EC2 instances in AWS
   - Track Azure virtual machine performance
   - Monitor Google Cloud Platform services

5. **Compliance Monitoring**
   - Monitor file integrity for PCI DSS compliance
   - Track access attempts for HIPAA compliance
   - Monitor backup processes for data protection regulations

### Practical Exercise: Monitoring Multiple Aspects of Infrastructure

Let's set up a more comprehensive monitoring scenario using Nagios. We'll monitor CPU load, disk usage, and a web service.

#### Step 1: Create New Check Commands

Open your `custom_nagios.cfg` file and add the following command definitions:

```
define command {
    command_name check_docker_host_load
    command_line $USER1$/check_load -w 70,80,90 -c 80,90,100
}

define command {
    command_name check_docker_host_disk
    command_line $USER1$/check_disk -w 80% -c 90% -p /
}

define command {
    command_name check_grafana_http
    command_line $USER1$/check_http -H grafana -p 3000 -u /login
}
```

#### Step 2: Add New Service Checks

Add the following service definitions to your `custom_nagios.cfg` file:

```
define host {
    use                     linux-server
    host_name               docker-host
    alias                   Docker Host
    address                 localhost
    max_check_attempts      5
    check_period            24x7
    notification_interval   30
    notification_period     24x7
}

define service {
    use                     generic-service
    host_name               docker-host
    service_description     CPU Load
    check_command           check_docker_host_load
    notifications_enabled   1
}

define service {
    use                     generic-service
    host_name               docker-host
    service_description     Disk Usage
    check_command           check_docker_host_disk
    notifications_enabled   1
}

define service {
    use                     generic-service
    host_name               docker-host
    service_description     Grafana Web Interface
    check_command           check_grafana_http
    notifications_enabled   1
}
```

#### Step 3: Restart Nagios

Restart your Docker containers to apply the changes:

```
docker-compose down
docker-compose up -d
```

#### Step 4: View and Interpret the New Checks

1. Go to the Nagios web interface and log in.
2. Click on "Services" in the left menu.
3. You should now see three new service checks under the host "docker-host":
   - CPU Load
   - Disk Usage
   - Grafana Web Interface

Each check will show a status (OK, WARNING, or CRITICAL) and provide specific metrics:

- CPU Load: Shows 1-minute, 5-minute, and 15-minute load averages
- Disk Usage: Shows percentage of disk space used
- Grafana Web Interface: Shows HTTP response time and status code

This setup demonstrates how Nagios can monitor various aspects of your infrastructure, from system resources (CPU and disk) to service availability (Grafana web interface).

### Conclusion

This basic setup provides a foundation for monitoring your infrastructure using a combination of Prometheus, Grafana, Node Exporter, and Nagios. Each tool plays a unique role:

- Prometheus collects and stores metrics
- Node Exporter exposes system metrics to Prometheus
- Grafana visualizes the metrics collected by Prometheus
- Nagios provides real-time monitoring and alerting for various infrastructure components

As you become more familiar with these tools, you can expand your monitoring capabilities by adding more checks, creating custom plugins, setting up detailed alerting rules, and designing comprehensive dashboards to suit your specific infrastructure needs.

Remember to replace default passwords with strong, unique passwords in a production environment, and to regularly update and maintain your monitoring tools for optimal performance and security.
