# Infrastructure Monitoring: A Practical Guide
## Table of Contents
1. [Understanding Monitoring](#understanding-monitoring)
2. [Nagios Core](#nagios-core)
3. [Practical: Setting Up Nagios with Docker](#practical-nagios)
4. [Advanced Nagios Configuration](#advanced-nagios)
5. [Modern Monitoring with Prometheus & Grafana](#prometheus-grafana)
6. [Practical: Implementing Prometheus & Grafana](#practical-prometheus)

## Understanding Monitoring {#understanding-monitoring}

### Why Monitoring Matters
- **Proactive Problem Detection**: Identify issues before they affect users
- **Performance Optimization**: Track system metrics to optimize resource usage
- **Capacity Planning**: Use historical data to plan infrastructure scaling
- **Incident Response**: Quick detection and resolution of issues
- **Compliance**: Meet regulatory requirements for system monitoring

## Nagios Core {#nagios-core}

### What is Nagios?
Nagios Core is an open-source monitoring system that:
- Monitors infrastructure components (servers, switches, applications)
- Sends alerts when things go wrong
- Provides historical data and reports
- Supports plugin architecture for extensibility

### Key Concepts
1. **Hosts**: Physical/virtual servers or network devices
2. **Services**: Specific checks running on hosts (CPU, memory, disk)
3. **Checks**: Scripts that test host/service status
4. **Notifications**: Alerts sent when problems occur
5. **Event Handlers**: Automated actions triggered by state changes

### Components
- **Core Program**: Main monitoring engine
- **Web Interface**: HTML interface for viewing status
- **Plugins**: External programs for checks
- **Configuration Files**: Define what to monitor

## Practical: Setting Up Nagios with Docker {#practical-nagios}

### Prerequisites
- Docker Desktop installed on Windows
- Basic understanding of Docker commands
- Text editor (VS Code recommended)

### Step 1: Create Docker Environment

Create a new directory for your project:
```bash
mkdir nagios-monitor
cd nagios-monitor
```

Create a `docker-compose.yml` file:
```yaml
version: '3'
services:
  nagios:
    image: jasonrivers/nagios:latest
    ports:
      - "8080:80"
    volumes:
      - ./nagios/etc:/opt/nagios/etc
      - ./nagios/var:/opt/nagios/var
      - ./custom-plugins:/opt/Custom-Nagios-Plugins
    environment:
      - NAGIOSADMIN_PASSWORD=nagios
```

### Step 2: Initialize Configuration
Create necessary directories:
```bash
mkdir -p nagios/etc nagios/var custom-plugins
```

### Step 3: Start Nagios
```bash
docker-compose up -d
```

Access Nagios at http://localhost:8080/nagios
- Username: nagiosadmin
- Password: nagios

### Step 4: Basic Configuration
Create a host definition (`nagios/etc/objects/localhost.cfg`):
```cfg
define host {
    use                     linux-server
    host_name               localhost
    alias                   localhost
    address                 127.0.0.1
    max_check_attempts      5
    check_period            24x7
    notification_interval   30
    notification_period     24x7
}

define service {
    use                     generic-service
    host_name               localhost
    service_description     CPU Usage
    check_command           check_nrpe!check_cpu
    notifications_enabled   1
}
```

## Advanced Nagios Configuration {#advanced-nagios}

### Notification Configuration
```cfg
define contact {
    contact_name            nagiosadmin
    use                     generic-contact
    alias                   Nagios Admin
    email                   your-email@domain.com
    service_notification_commands   notify-service-by-email
    host_notification_commands      notify-host-by-email
}
```

### Event Handlers
```cfg
define command {
    command_name    restart_apache
    command_line    /usr/local/nagios/libexec/eventhandlers/restart_apache.sh
}

define service {
    use                     generic-service
    host_name               webserver
    service_description     HTTP
    check_command           check_http
    event_handler           restart_apache
}
```

### SNMP Monitoring
Install SNMP utilities in your container:
```bash
docker exec -it nagios-monitor_nagios_1 apt-get update
docker exec -it nagios-monitor_nagios_1 apt-get install snmp snmpd
```

SNMP service definition:
```cfg
define command {
    command_name    check_snmp_load
    command_line    $USER1$/check_snmp -H $HOSTADDRESS$ -C public -o .1.3.6.1.4.1.2021.10.1.3.1
}
```

## Modern Monitoring with Prometheus & Grafana {#prometheus-grafana}

### Prometheus Overview
- Time-series database for metrics
- Pull-based architecture
- Powerful query language (PromQL)
- Service discovery capabilities

### Grafana Features
- Rich visualization options
- Dashboard templates
- Alert management
- Data source integration

## Practical: Implementing Prometheus & Grafana {#practical-prometheus}

### Step 1: Create Docker Compose Configuration
Create a new `docker-compose.yml`:
```yaml
version: '3'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus:/etc/prometheus
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

volumes:
  prometheus_data:
  grafana_data:
```

### Step 2: Configure Prometheus
Create `prometheus/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

### Step 3: Start the Stack
```bash
docker-compose up -d
```

Access:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

### Step 4: Configure Grafana
1. Add Prometheus data source:
   - URL: http://prometheus:9090
   - Access: Browser

2. Import a dashboard:
   - Dashboard ID: 1860 (Node Exporter Full)
   - Select Prometheus data source

### Practical Exercises

1. **Basic Monitoring Setup**
   - Set up Nagios to monitor local system
   - Configure email notifications
   - Add custom service checks

2. **SNMP Integration**
   - Configure SNMP on a test device
   - Add SNMP monitoring to Nagios
   - Create SNMP-based alerts

3. **Prometheus & Grafana**
   - Create custom PromQL queries
   - Build a custom dashboard
   - Set up alerting rules

### Troubleshooting Tips

1. **Nagios Issues**
   - Check Docker logs: `docker logs nagios-container`
   - Verify configuration: `docker exec nagios-container nagios -v /opt/nagios/etc/nagios.cfg`
   - Check permissions on mounted volumes

2. **Prometheus Issues**
   - Verify targets in Prometheus UI
   - Check prometheus.yml syntax
   - Review container logs

3. **Grafana Issues**
   - Confirm data source connection
   - Check Grafana logs
   - Verify dashboard permissions

### Best Practices

1. **Configuration Management**
   - Use version control for configurations
   - Document all custom checks and alerts
   - Maintain backup of configurations

2. **Monitoring Strategy**
   - Start with essential metrics
   - Avoid alert fatigue
   - Use appropriate check intervals
   - Implement escalation procedures

3. **Security**
   - Change default passwords
   - Use HTTPS where possible
   - Implement access controls
   - Regular security updates

### Additional Resources

1. **Documentation**
   - [Nagios Core Documentation](https://www.nagios.org/documentation/)
   - [Prometheus Documentation](https://prometheus.io/docs/)
   - [Grafana Documentation](https://grafana.com/docs/)

2. **Community Resources**
   - Nagios Exchange (plugins and addons)
   - Grafana dashboard repository
   - Prometheus operator documentation

3. **Learning Materials**
   - Video tutorials
   - Online courses
   - Community forums
