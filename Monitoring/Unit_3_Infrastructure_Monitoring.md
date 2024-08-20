# Unit 3: Infrastructure Monitoring

## Overview of Infrastructure Monitoring
Infrastructure monitoring involves tracking the performance, health, and availability of the various components that make up an organization's IT infrastructure. This includes servers, networks, databases, and applications. The goal is to ensure optimal operation and to identify and resolve issues before they impact end users.

## Monitoring Components and Metrics
### Key Components
1. **Servers:** Physical or virtual machines hosting applications and services.
2. **Networks:** Routers, switches, firewalls, and other networking equipment.
3. **Databases:** SQL and NoSQL databases storing application data.
4. **Applications:** Software applications providing services to users.
5. **Storage:** Disk drives, SSDs, and storage arrays.

### Important Metrics
1. **CPU Usage:** Percentage of CPU capacity being used.
2. **Memory Usage:** Amount of RAM being utilized.
3. **Disk I/O:** Read and write operations on storage devices.
4. **Network Latency:** Time taken for data to travel across the network.
5. **Uptime:** Duration that a component is operational and available.
6. **Error Rates:** Frequency of errors occurring in the system.

## Agent vs Agentless Monitoring
### Agent Monitoring
- **Definition:** Uses software agents installed on monitored systems to collect data.
- **Pros:** Provides detailed, granular data; can monitor specific applications and processes.
- **Cons:** Requires installation and maintenance of agents on each monitored system; potential performance impact on the host.

### Agentless Monitoring
- **Definition:** Collects data without installing software agents on the monitored systems, often using standard protocols (e.g., SNMP, WMI).
- **Pros:** Easier to set up and maintain; no performance impact on the host.
- **Cons:** May provide less detailed data compared to agent-based monitoring; limited to the metrics exposed by standard protocols.

## Reactive Monitoring vs Proactive Monitoring
### Reactive Monitoring
- **Definition:** Responds to issues and alerts as they occur.
- **Pros:** Simple to implement; provides immediate responses to issues.
- **Cons:** Often results in downtime or degraded performance before issues are resolved; not ideal for preventing issues.

### Proactive Monitoring
- **Definition:** Continuously monitors systems to identify and address potential issues before they cause problems.
- **Pros:** Helps prevent downtime and performance degradation; improves overall system reliability.
- **Cons:** More complex to implement; requires thorough planning and continuous monitoring.

## Cloud vs On-Premise Monitoring
### Cloud Monitoring
- **Definition:** Monitoring of cloud-based infrastructure and services.
- **Pros:** Scalable; typically includes built-in monitoring tools; less maintenance overhead.
- **Cons:** Dependency on cloud provider; potential data security concerns.

### On-Premise Monitoring
- **Definition:** Monitoring of infrastructure hosted within an organization's own data centers.
- **Pros:** Full control over monitoring setup and data; customizable to specific needs.
- **Cons:** Requires significant resources to set up and maintain; scalability can be challenging.

## Network and Security Monitoring
### Network Monitoring
- **Purpose:** Ensure the health and performance of network components.
- **Metrics:** Bandwidth usage, latency, packet loss, error rates.
- **Tools:** SolarWinds, PRTG Network Monitor, Wireshark.

### Security Monitoring
- **Purpose:** Detect and respond to security threats and vulnerabilities.
- **Metrics:** Intrusion attempts, malware detection, unauthorized access attempts.
- **Tools:** Splunk, OSSEC, Snort.

## Infrastructure Monitoring Challenges
1. **Complexity:** Modern IT environments can be highly complex, with many interconnected components.
2. **Scalability:** Ensuring that the monitoring solution can scale with the infrastructure.
3. **Data Overload:** Managing and making sense of large volumes of monitoring data.
4. **Integration:** Integrating monitoring tools with existing systems and workflows.
5. **Security:** Ensuring that monitoring tools and data are secure from unauthorized access.

## Tools Overview
### Comprehensive Monitoring Tools
1. **Prometheus:** Open-source monitoring and alerting toolkit, ideal for infrastructure monitoring.
2. **Nagios:** Popular open-source monitoring tool for servers, networks, and applications.
3. **Zabbix:** Open-source monitoring solution for performance and availability.

### Cloud-Specific Monitoring Tools
1. **AWS CloudWatch:** Monitoring and observability service for AWS cloud resources.
2. **Azure Monitor:** Comprehensive monitoring tool for Azure cloud services.
3. **Google Cloud Operations (formerly Stackdriver):** Monitoring and logging service for Google Cloud Platform.

### Network Monitoring Tools
1. **SolarWinds Network Performance Monitor:** Comprehensive network monitoring solution.
2. **PRTG Network Monitor:** Network monitoring tool that covers a wide range of metrics.
3. **Wireshark:** Network protocol analyzer for in-depth network traffic analysis.

### Security Monitoring Tools
1. **Splunk:** Security Information and Event Management (SIEM) tool for security monitoring.
2. **OSSEC:** Open-source host-based intrusion detection system.
3. **Snort:** Open-source network intrusion detection system.
