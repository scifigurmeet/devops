# Practical Guide: Cloud Computing and Provisioning

## Introduction

This practical guide is designed to help you understand the concepts of cloud computing, provisioning, and related topics through hands-on exercises. You'll be using your Windows 11 PC with Docker installed to simulate cloud environments and practice various concepts.

## Prerequisites

- Windows 11 PC
- Docker Desktop installed and running
- Internet connection

## Exercise 1: Understanding Cloud Providers and Deployment Models

### Intention
To simulate different cloud deployment models using Docker, helping you visualize how private, public, and hybrid clouds operate.

### Objective
Simulate different cloud deployment models using Docker containers.

### Steps

1. Open PowerShell and run the following commands to create three different "cloud" environments:

```powershell
# Create a "private cloud" network
docker network create private-cloud

# Create a "public cloud" network
docker network create public-cloud

# Create a "hybrid cloud" setup
docker network create hybrid-cloud
```

2. Now, let's create containers in these networks:

```powershell
# Private cloud container
docker run -d --name private-app --network private-cloud nginx

# Public cloud container
docker run -d --name public-app --network public-cloud -p 8080:80 nginx

# Hybrid cloud containers
docker run -d --name hybrid-app1 --network hybrid-cloud nginx
docker run -d --name hybrid-app2 --network hybrid-cloud nginx
docker network connect public-cloud hybrid-app2
```

3. Verify the setup:

```powershell
docker network ls
docker container ls
```

### Interpretation
- The private network represents a private cloud, where resources are used exclusively by one organization.
- The public network with exposed ports represents a public cloud, accessible to anyone on the internet.
- The hybrid setup shows how organizations can use both private and public resources together.

By creating these different networks, you can see how various cloud models isolate or expose resources, mirroring real-world cloud environments.

### Discussion
- How does this setup represent different cloud deployment models?
- What are the advantages and disadvantages of each model?

## Exercise 2: Exploring Service Models (IaaS, PaaS, SaaS)

### Intention
To demonstrate the different levels of control and management in IaaS, PaaS, and SaaS using Docker containers.

### Objective
Understand different service models using Docker containers.

### Steps

1. IaaS Simulation:

```powershell
# Run a basic Ubuntu container (simulating IaaS)
docker run -it --name iaas-example ubuntu /bin/bash

# Inside the container, you can install and configure as needed
apt update
apt install -y nginx
exit
```

2. PaaS Simulation:

```powershell
# Run a Node.js container (simulating PaaS)
docker run -it --name paas-example -p 3000:3000 node:14 /bin/bash

# Inside the container
npm init -y
npm install express
echo "const express = require('express'); const app = express(); app.get('/', (req, res) => res.send('Hello from PaaS!')); app.listen(3000, () => console.log('PaaS app listening on port 3000!'));" > index.js
node index.js
```

3. SaaS Simulation:

```powershell
# Run a WordPress container (simulating SaaS)
docker run -d --name saas-example -p 8080:80 wordpress
```

### Interpretation
- The Ubuntu container (IaaS) gives you full control over the environment, similar to having a virtual machine in the cloud.
- The Node.js container (PaaS) provides a pre-configured platform, letting you focus on application development.
- The WordPress container (SaaS) offers a complete application, ready to use with minimal configuration.

These simulations help you understand the different levels of abstraction and management responsibilities in cloud service models.

### Discussion
- How do these examples represent different service models?
- What level of control and responsibility does the user have in each model?

## Exercise 3: Automated Provisioning and Cloud Automation

### Intention
To showcase how complex environments can be defined and deployed with a single command, demonstrating the power of automation in cloud provisioning.

### Objective
Use Docker Compose to demonstrate automated provisioning and cloud automation.

### Steps

1. Create a file named `docker-compose.yml` with the following content:

```yaml
version: '3'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: example
  cache:
    image: redis
```

2. Run the following command to provision the entire stack:

```powershell
docker-compose up -d
```

3. Verify the setup:

```powershell
docker-compose ps
```

### Interpretation
This exercise demonstrates how multiple services (web server, database, cache) can be defined in a single file and deployed together. In cloud environments, this approach allows for consistent, repeatable deployments and easy scaling of complex applications.

### Discussion
- How does this demonstrate automated provisioning?
- What are the benefits of using such automation in cloud environments?

## Exercise 4: Code Quality Checks with SonarQube

### Intention
To introduce automated code quality checks, an essential practice in cloud-native development for maintaining high-quality, secure code.

### Objective
Set up SonarQube and perform code quality checks on a sample project.

### Steps

1. Run SonarQube using Docker:

```powershell
docker run -d --name sonarqube -p 9000:9000 sonarqube
```

2. Access SonarQube at `http://localhost:9000` in your web browser. The default login is admin/admin.

3. Create a new project in SonarQube and note down the project key and token.

4. Create a sample Python file named `sample.py` with the following content:

```python
def greet(name):
    print "Hello, " + name + "!"

greet("World")
```

5. Install SonarScanner for Python:

```powershell
pip install sonar-scanner
```

6. Run the scanner:

```powershell
sonar-scanner -D sonar.projectKey=my-project -D sonar.sources=. -D sonar.host.url=http://localhost:9000 -D sonar.login=your-token
```

7. View the results in the SonarQube web interface.

### Interpretation
This exercise shows how automated tools can help maintain code quality in cloud environments. SonarQube analyzes code for bugs, vulnerabilities, and code smells, which is crucial for developing robust and secure cloud applications.

### Discussion
- What code quality issues did SonarQube identify?
- How can tools like SonarQube improve the development process in cloud environments?

## Conclusion

These exercises have provided hands-on experience with various cloud computing concepts. Reflect on how these principles apply to real-world cloud environments and consider the scalability and flexibility that cloud computing offers.

Remember to clean up your Docker environment after completing the exercises:

```powershell
docker-compose down
docker container prune
docker network prune
```

For further exploration, consider signing up for free tiers of major cloud providers like AWS, Azure, or Google Cloud to experience real cloud environments.
