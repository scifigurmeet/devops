# Unit 6: Introduction to DevOps Tools & Technologies
## A Comprehensive Guide for B.Tech 2nd Year Students

## Table of Contents
1. [Git & GitHub (Source Code Management)](#1-git--github-source-code-management)
2. [Docker (Containerization)](#2-docker-containerization)
3. [Jenkins (CI/CD Pipelines)](#3-jenkins-cicd-pipelines)
4. [Terraform (Infrastructure as Code)](#4-terraform-infrastructure-as-code)
5. [Maven (Build & Release Management)](#5-maven-build--release-management)
6. [Ansible (Configuration Management)](#6-ansible-configuration-management)
7. [Selenium (Test Automation)](#7-selenium-test-automation)
8. [AWS (Cloud Computing)](#8-aws-cloud-computing)
9. [SonarQube (Code Quality)](#9-sonarqube-code-quality)
10. [Prometheus/Nagios (Monitoring)](#10-prometheusinagios-monitoring)

---

## 1. Git & GitHub (Source Code Management)

### Overview
Git is a distributed version control system that tracks changes in source code during software development. GitHub is a web-based hosting service for Git repositories.

### Key Concepts
- Repository (Repo)
- Commit
- Branch
- Pull Request (PR)
- Merge

### Practical Example
```bash
# Initialize a new repository
git init

# Add files to staging
git add index.html

# Create a commit
git commit -m "Add homepage"

# Create and switch to a new branch
git checkout -b feature/login-page

# Push changes to GitHub
git push origin feature/login-page
```

### Best Practices
- Write clear commit messages
- Use feature branches
- Regular commits
- Pull before push
- Review code before merging

---

## 2. Docker (Containerization)

### Overview
Docker is a platform that enables developers to package applications into containers—standardized executable components that combine application source code with all its dependencies.

### Key Concepts
- Container
- Image
- Dockerfile
- Docker Compose
- Registry

### Practical Example
```dockerfile
# Simple Node.js application Dockerfile
FROM node:14-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose Example
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "3000:3000"
  db:
    image: mongodb:latest
    volumes:
      - db-data:/data/db

volumes:
  db-data:
```

---

## 3. Jenkins (CI/CD Pipelines)

### Overview
Jenkins is an open-source automation server that enables developers to build, test, and deploy their applications automatically.

### Key Concepts
- Pipeline
- Stage
- Step
- Agent
- Jenkinsfile

### Practical Example
```groovy
// Jenkinsfile example
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
        
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker build -t myapp .'
                sh 'docker push myapp:latest'
            }
        }
    }
}
```

---

## 4. Terraform (Infrastructure as Code)

### Overview
Terraform is an infrastructure as code (IaC) tool that allows you to build, change, and version infrastructure safely and efficiently.

### Key Concepts
- Provider
- Resource
- State
- Module
- Variables

### Practical Example
```hcl
# AWS EC2 instance creation
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
    Environment = "Development"
  }
}
```

---

## 5. Maven (Build & Release Management)

### Overview
Maven is a build automation tool used primarily for Java projects, handling project dependencies and the build process.

### Key Concepts
- POM (Project Object Model)
- Dependencies
- Plugins
- Lifecycle
- Goals

### Practical Example
```xml
<!-- pom.xml example -->
<project>
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0-SNAPSHOT</version>
    
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

---

## 6. Ansible (Configuration Management)

### Overview
Ansible is an open-source automation tool that automates software provisioning, configuration management, and application deployment.

### Key Concepts
- Playbooks
- Inventory
- Roles
- Tasks
- Handlers

### Practical Example
```yaml
# Simple playbook example
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Start nginx service
      service:
        name: nginx
        state: started
```

---

## 7. Selenium (Test Automation)

### Overview
Selenium is a portable framework for testing web applications that provides a playback tool for authoring functional tests.

### Key Concepts
- WebDriver
- Element Location
- Actions
- Wait Strategies
- Test Suites

### Practical Example
```java
// Java with Selenium WebDriver
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class SimpleTest {
    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        
        driver.get("https://www.example.com");
        
        driver.findElement(By.id("username"))
              .sendKeys("testuser");
              
        driver.findElement(By.id("password"))
              .sendKeys("password123");
              
        driver.findElement(By.id("login-button"))
              .click();
              
        driver.quit();
    }
}
```

---

## 8. AWS (Cloud Computing)

### Overview
Amazon Web Services (AWS) is a comprehensive cloud platform offering over 200 services from data centers globally.

### Key Services
- EC2 (Virtual Servers)
- S3 (Storage)
- RDS (Managed Databases)
- Lambda (Serverless)
- IAM (Security)

### Practical Example
```python
# AWS SDK (Boto3) example
import boto3

# Create EC2 client
ec2 = boto3.client('ec2')

# Launch EC2 instance
response = ec2.run_instances(
    ImageId='ami-0c55b159cbfafe1f0',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'DevOpsDemo'
                }
            ]
        }
    ]
)
```

---

## 9. SonarQube (Code Quality)

### Overview
SonarQube is an open-source platform for continuous inspection of code quality to perform automatic reviews with static analysis of code to detect bugs and code smells.

### Key Concepts
- Quality Gates
- Issues
- Technical Debt
- Code Coverage
- Duplications

### Practical Example
```properties
# sonar-project.properties
sonar.projectKey=my:project
sonar.projectName=My Project
sonar.projectVersion=1.0
sonar.sources=src
sonar.java.binaries=target/classes
sonar.language=java
sonar.sourceEncoding=UTF-8
```

---

## 10. Prometheus/Nagios (Monitoring)

### Overview
Both tools are used for monitoring systems and services, with Prometheus being more modern and focused on metrics, while Nagios is traditional and focused on alerts.

### Prometheus Key Concepts
- Metrics
- Labels
- PromQL
- Alerting Rules
- Grafana Integration

### Practical Example (Prometheus)
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'spring_app'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['localhost:8080']
```

### Nagios Key Concepts
- Hosts
- Services
- Checks
- Notifications
- Plugins

### Study Tips
1. Practice each tool hands-on
2. Create small projects using multiple tools
3. Follow official documentation
4. Join DevOps communities
5. Set up a home lab for practice

### Additional Resources
- Official Documentation links for each tool
- Online learning platforms
- Community forums
- GitHub repositories with example projects
- DevOps blogs and YouTube channels

---

Remember: DevOps is about culture as much as it is about tools. Understanding the philosophy behind these tools is as important as knowing how to use them.
