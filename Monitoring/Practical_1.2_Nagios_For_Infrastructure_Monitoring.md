# Comprehensive Beginner's Guide to Nagios with Docker

## Introduction
Nagios is an open-source monitoring system that helps you keep track of your IT infrastructure. It can monitor various aspects of your network, servers, and services, alerting you when issues arise. This guide will help you set up Nagios using Docker on your Windows PC and understand the basics of what you're monitoring.

## Prerequisites
- Docker Desktop installed on your Windows PC
- Basic understanding of command-line interfaces
- Basic knowledge of networks (IP addresses, ports)

## What Nagios Monitors
Nagios can monitor a wide range of IT infrastructure components, including:
1. Physical devices (servers, workstations, network switches, routers)
2. Services (web servers, email servers, databases)
3. Operating system metrics (CPU usage, disk space, memory usage)
4. Network protocols and services (HTTP, SMTP, DNS)

## Steps to Set Up Nagios

### 1. Create a Docker network
```
docker network create nagios-net
```
Explanation: This creates a virtual network within Docker where Nagios and potentially other related containers can communicate.

### 2. Set up Nagios Core
```
docker run --name nagios4 \
  --network nagios-net \
  -p 8080:80 \
  -d jasonrivers/nagios:latest
```
Explanation: This command downloads and runs the Nagios container. It connects to the network we created and maps port 8080 on your PC to port 80 in the container, allowing you to access the Nagios web interface.

### 3. Access Nagios Web Interface
- Open a web browser and go to `http://localhost:8080/nagios`
- Login with:
  - Username: `nagiosadmin`
  - Password: `nagios`

Explanation: This is where you'll see all your monitoring results. The web interface provides an overview of all monitored devices and services, their current status, and any alerts or problems.

### 4. Add a host to monitor
Create a file named `custom_host.cfg` on your PC with the following content:
```
define host {
    use                     linux-server
    host_name               example-host
    alias                   Example Host
    address                 192.168.1.100
    max_check_attempts      5
    check_period            24x7
    notification_interval   30
    notification_period     24x7
}
```

Explanation:
- `host_name`: A unique name for this host in Nagios.
- `alias`: A human-readable name for the host.
- `address`: The IP address of the host you're monitoring. 
  - We use 192.168.1.100 as an example of a local network IP. You should replace this with the actual IP of the device you want to monitor.
  - If you're monitoring a device on your home network, it might have an IP like 192.168.0.X or 10.0.0.X.
  - For a public website, you would use its public IP address.
- `max_check_attempts`: How many times Nagios will check if it gets an error before alerting.
- `check_period` and `notification_period`: When Nagios should check and send alerts (24x7 means always).
- `notification_interval`: How often Nagios should resend alerts for ongoing problems.

### 5. Add the configuration to Nagios
```
docker cp custom_host.cfg nagios4:/opt/nagios/etc/objects/
```
Explanation: This copies your configuration file into the Nagios container.

### 6. Update Nagios configuration
```
docker exec -it nagios4 /bin/bash
nano /opt/nagios/etc/nagios.cfg
```
Add this line at the end of the file:
```
cfg_file=/opt/nagios/etc/objects/custom_host.cfg
```
Explanation: This tells Nagios to include your new host configuration.

### 7. Restart Nagios
```
docker exec -it nagios4 /opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg
docker restart nagios4
```
Explanation: This checks your configuration for errors and then restarts Nagios to apply the changes.

## Viewing Monitoring Results

1. Go to `http://localhost:8080/nagios` in your web browser.
2. Log in using the credentials provided earlier.
3. Click on "Hosts" in the left sidebar to see a list of all monitored hosts.
4. Click on a host name to see detailed information about its status.
5. Use the "Services" menu to see specific services being monitored on each host.
6. The "Map" view provides a visual representation of your monitored infrastructure.

## What You're Monitoring (Example)

In this basic setup, you're monitoring:
1. Host Availability: Nagios will check if the host at 192.168.1.100 is reachable.
2. Basic Services: By default, Nagios may check things like SSH availability on this host.

To monitor more aspects:
1. Add service definitions to check specific ports or services.
2. Install Nagios plugins on the monitored host to check internal metrics like CPU, memory, and disk usage.

## Next Steps
1. Add more hosts: Create additional .cfg files for other devices or servers you want to monitor.
2. Configure services: Define specific services to monitor on each host (e.g., web server, database).
3. Set up notifications: Configure Nagios to send emails or other alerts when issues are detected.
4. Learn about Nagios plugins: These extend Nagios' capabilities to monitor more specific or complex aspects of your systems.

Remember, monitoring is an ongoing process. Start with basic checks and gradually expand your monitoring as you become more comfortable with Nagios and identify what's most important for your infrastructure.
