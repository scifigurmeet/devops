# 🚀 Zabbix Lab Guide: Introduction to Infrastructure Monitoring

## 📚 Table of Contents

1. [Introduction to Zabbix](#introduction-to-zabbix)
2. [Setting Up Your Zabbix Environment](#setting-up-your-zabbix-environment)
3. [Exploring the Zabbix Web Interface](#exploring-the-zabbix-web-interface)
4. [Implementing a Basic Monitoring Use Case](#implementing-a-basic-monitoring-use-case)
5. [Conclusion and Further Learning](#conclusion-and-further-learning)

## 1. Introduction to Zabbix

Zabbix is an open-source monitoring solution for IT infrastructure. Key features include:

- 🔍 Real-time monitoring of servers, virtual machines, and network devices
- 📊 Customizable dashboards and visualizations
- 🚨 Flexible alerting mechanisms
- 🤖 Automation through APIs

> 💡 **Fun Fact:** Zabbix can monitor millions of metrics from thousands of devices, making it suitable for both small businesses and large enterprises!

## 2. Setting Up Your Zabbix Environment

### Prerequisites

- Windows PC with Docker Desktop installed
- Basic understanding of Docker and YAML

### Step-by-step Setup

1. Create a new directory for your Zabbix project:
   ```
   mkdir zabbix-lab
   cd zabbix-lab
   ```

2. Create a file named `docker-compose.yml` with the following content:

   ```yaml
   version: '3'
   services:
     zabbix-server:
       image: zabbix/zabbix-server-pgsql:alpine-latest
       environment:
         - DB_SERVER_HOST=postgres
         - POSTGRES_USER=zabbix
         - POSTGRES_PASSWORD=zabbix_pwd
         - POSTGRES_DB=zabbix
       ports:
         - "10051:10051"
       depends_on:
         - postgres
       restart: always
     zabbix-web:
       image: zabbix/zabbix-web-nginx-pgsql:alpine-latest
       environment:
         - ZBX_SERVER_HOST=zabbix-server
         - DB_SERVER_HOST=postgres
         - POSTGRES_USER=zabbix
         - POSTGRES_PASSWORD=zabbix_pwd
         - POSTGRES_DB=zabbix
         - PHP_TZ=UTC
       ports:
         - "80:8080"
       depends_on:
         - zabbix-server
         - postgres
       restart: always
     postgres:
       image: postgres:13-alpine
       environment:
         - POSTGRES_USER=zabbix
         - POSTGRES_PASSWORD=zabbix_pwd
         - POSTGRES_DB=zabbix
       volumes:
         - postgres-data:/var/lib/postgresql/data
       restart: always
     monitored-host:
       image: zabbix/zabbix-agent:alpine-latest
       environment:
         - ZBX_HOSTNAME=alpine-host
         - ZBX_SERVER_HOST=zabbix-server
       restart: always
   volumes:
     postgres-data:
   ```

3. Open a terminal in the `zabbix-lab` directory and run:
   ```
   docker-compose up -d
   ```

4. After running `docker-compose up -d`, wait for a few minutes to allow all services to initialize.

5. Run the following command to get the IP address of your monitored host:
   ```
   docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' zabbix-lab-monitored-host-1
   ```
   Note down this IP address; you'll need it in the next section.

> 💡 **Tip:** Check the status of your containers by running `docker-compose ps`.

## 3. Exploring the Zabbix Web Interface

1. Open your web browser and navigate to `http://localhost`

2. Log in with the default credentials:
   - Username: Admin
   - Password: zabbix

3. 🔒 Immediately change your password:
   - Click on your username in the top right corner
   - Select "User settings"
   - Go to the "Password" tab
   - Enter and confirm your new password

4. Explore the main sections of the Zabbix interface:
   - Dashboard
   - Problems
   - Monitoring
   - Inventory
   - Reports
   - Configuration

> 💡 **Fun Fact:** You can create custom dashboards in Zabbix to monitor different aspects of your infrastructure at a glance!

## 4. Implementing a Basic Monitoring Use Case

Let's set up monitoring for our Alpine Linux container using the Zabbix agent.

1. In the Zabbix web interface, go to Configuration > Hosts

2. Click "Create host"

3. Set the following:
   - Host name: alpine-host
   - Groups: Linux servers
   - Interfaces: 
     - Add Agent interface
     - IP address: [Enter the IP address you noted in step 5 of the setup]
     - Port: 10050

4. Go to the "Templates" tab and link the "Template OS Linux by Zabbix agent" template

5. Click "Add" to create the host

6. Wait a few minutes, then go to Monitoring > Latest data. Filter by your host name "alpine-host" to see the metrics being collected.

> 💡 **Tip:** If you don't see any data after a few minutes, check the host's availability in Configuration > Hosts. The "ZBX" column should be green.

### Troubleshooting

If you're not seeing data:

1. Go to Configuration > Hosts
2. Click on "alpine-host"
3. In the "Agent" interface, ensure the IP address is correct
4. Click the "Check now" button next to the interface to test the connection

> 💡 **Fun Fact:** Zabbix can automatically detect and start monitoring network devices using discovery rules!

## 5. Conclusion and Further Learning

Congratulations! You've set up a basic Zabbix monitoring environment and implemented a simple use case. This is just the beginning of your journey with Zabbix and infrastructure monitoring.

To continue your learning:
- Explore the [official Zabbix documentation](https://www.zabbix.com/documentation/current/)
- Join the [Zabbix community forums](https://www.zabbix.com/forum/)
- Experiment with monitoring different types of systems and applications

> 💡 **Fun Fact:** Zabbix can send alerts through various channels, including email, SMS, and chat applications like Slack or Microsoft Teams!

Remember, effective monitoring is crucial in DevOps for ensuring system reliability and performance. Keep exploring and learning!
