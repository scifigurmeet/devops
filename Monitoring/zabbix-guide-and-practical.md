# Zabbix Guide and Basic Practical Exercise

## Introduction to Zabbix

Zabbix is an open-source monitoring solution for various IT components, including networks, servers, virtual machines, and cloud services. It provides:

- Real-time monitoring of metrics
- Flexible notification mechanisms
- Visualization through graphs, screens, and maps
- Auto-discovery of servers and devices
- Distributed monitoring with centralized web administration

## Basic Practical Exercise: Setting up Zabbix with Docker Compose

In this exercise, we'll set up a basic Zabbix environment using Docker Compose. This setup will include the Zabbix server, web interface, and a MySQL database.

### Prerequisites

- Docker Desktop installed on Windows 11 PC
- Basic understanding of Docker and Docker Compose
- Text editor (e.g., Notepad++, Visual Studio Code)

### Step 1: Create Docker Compose File

1. Create a new directory for your Zabbix project.
2. Inside this directory, create a file named `docker-compose.yml`.
3. Open the file in your text editor and add the following content:

```yaml
version: '3'
services:
  zabbix-server:
    image: zabbix/zabbix-server-mysql:ubuntu-6.0-latest
    ports:
      - "10051:10051"
    environment:
      - DB_SERVER_HOST=mysql-server
      - MYSQL_DATABASE=zabbix
      - MYSQL_USER=zabbix
      - MYSQL_PASSWORD=zabbix_pwd
    depends_on:
      - mysql-server

  zabbix-web:
    image: zabbix/zabbix-web-nginx-mysql:ubuntu-6.0-latest
    ports:
      - "80:8080"
    environment:
      - DB_SERVER_HOST=mysql-server
      - MYSQL_DATABASE=zabbix
      - MYSQL_USER=zabbix
      - MYSQL_PASSWORD=zabbix_pwd
      - ZBX_SERVER_HOST=zabbix-server
    depends_on:
      - mysql-server
      - zabbix-server

  mysql-server:
    image: mysql:8.0
    command: --default-authentication-plugin=mysql_native_password
    environment:
      - MYSQL_DATABASE=zabbix
      - MYSQL_USER=zabbix
      - MYSQL_PASSWORD=zabbix_pwd
      - MYSQL_ROOT_PASSWORD=root_pwd
```

### Step 2: Start the Zabbix Environment

1. Open a command prompt or PowerShell window.
2. Navigate to the directory containing your `docker-compose.yml` file.
3. Run the following command to start the Zabbix environment:

```
docker-compose up -d
```

This command will download the necessary Docker images and start the containers in detached mode.

### Step 3: Access Zabbix Web Interface

1. Open a web browser and navigate to `http://localhost`.
2. You should see the Zabbix login page.
3. Log in with the default credentials:
   - Username: Admin
   - Password: zabbix

### Step 4: Basic Configuration

1. After logging in, go to Configuration > Hosts.
2. Click on "Create host" to add a new host for monitoring.
3. Enter a name for the host (e.g., "Local Machine").
4. In the "Interfaces" section, add a new interface:
   - Type: Agent
   - IP address: 172.17.0.1 (This is typically the Docker host's IP address)
   - Port: 10050
5. Click "Add" to create the host.

### Step 5: View Monitoring Data

1. Go to Monitoring > Latest data.
2. Select your newly created host from the filter and click "Apply".
3. You should start seeing some basic metrics for the host.

## Conclusion

This basic setup demonstrates how to quickly deploy a Zabbix monitoring environment using Docker Compose. In a real-world scenario, you would configure more detailed monitoring, set up alerts, and add more hosts to monitor your infrastructure effectively.

## Next Steps

- Explore Zabbix documentation to learn about advanced features.
- Configure email notifications for alerts.
- Set up additional monitoring templates for different types of systems.
- Implement Zabbix agents on actual servers or network devices for more comprehensive monitoring.
