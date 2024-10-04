# Detailed Guide: Deploying a React Application to EC2 using GitLab CI/CD

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setting Up the AWS EC2 Instance](#setting-up-the-aws-ec2-instance)
3. [Preparing the GitLab Repository](#preparing-the-gitlab-repository)
4. [Configuring the React Application](#configuring-the-react-application)
5. [Setting Up the Web Server (Nginx)](#setting-up-the-web-server-nginx)
6. [Creating the GitLab CI/CD Pipeline](#creating-the-gitlab-cicd-pipeline)
7. [Testing the Deployment](#testing-the-deployment)
8. [Optional Enhancements](#optional-enhancements)
9. [Troubleshooting](#troubleshooting)
10. [Conclusion](#conclusion)

## 1. Prerequisites

Before starting the implementation, ensure you have the following:

- An AWS account with permissions to create and manage EC2 instances
- A GitLab account
- Basic knowledge of React, Node.js, and Linux commands
- SSH client installed on your local machine

## 2. Setting Up the AWS EC2 Instance

### 2.1 Launch an EC2 Instance

1. Log in to your AWS Management Console.
2. Navigate to EC2 and click "Launch Instance."
3. Choose "Ubuntu Server 22.04 LTS" as the Amazon Machine Image (AMI).
4. Select t2.micro instance type (or any suitable for your needs).
5. Configure instance details as needed.
6. Add storage (default is usually sufficient).
7. Add tags if desired (e.g., Key: Name, Value: React-App-Server).
8. Configure Security Group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
9. Review and launch the instance.
10. Create a new key pair or use an existing one, and download the .pem file.

### 2.2 Connect to Your EC2 Instance

```bash
chmod 400 your-key-pair.pem
ssh -i your-key-pair.pem ubuntu@your-instance-public-dns
```

### 2.3 Install Required Software

Update the system and install the latest Node.js, npm, and Nginx:

```bash
sudo apt update
sudo apt upgrade -y

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Install Nginx
sudo apt install nginx -y
```

Verify the installations:

```bash
node --version
npm --version
nginx -v
```

## 3. Preparing the GitLab Repository

### 3.1 Create a New GitLab Repository

1. Log in to GitLab and create a new project.
2. Choose a project name (e.g., "react-ec2-deployment").
3. Set the visibility level as needed.
4. Initialize with a README file.

### 3.2 Configure GitLab CI/CD Variables

1. In your GitLab project, go to "Settings" > "CI/CD" > "Variables."
2. Add the following variables:
   - `EC2_HOST`: Your EC2 instance's public DNS
   - `EC2_USER`: ubuntu
   - `SSH_PRIVATE_KEY`: The content of your EC2 instance's private key file

Make sure to mask the `SSH_PRIVATE_KEY` for security.

## 4. Configuring the React Application

### 4.1 Clone the GitLab Repository Locally

```bash
git clone https://gitlab.com/your-username/react-ec2-deployment.git
cd react-ec2-deployment
```

### 4.2 Add the Provided React Application Code

Copy the provided React application code into your local repository. Ensure you have the following structure:

```
react-ec2-deployment/
├── public/
├── src/
├── package.json
├── README.md
└── .gitignore
```

### 4.3 Update .gitignore

Ensure your .gitignore file includes:

```
node_modules/
build/
.env
```

### 4.4 Commit and Push the React Application

```bash
git add .
git commit -m "Add React application code"
git push origin main
```

## 5. Setting Up the Web Server (Nginx)

### 5.1 Configure Nginx

SSH into your EC2 instance and create an Nginx server block:

```bash
sudo nano /etc/nginx/sites-available/react-app
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name your_ec2_public_dns;

    root /var/www/react-app;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

Create a symbolic link to enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/react-app /etc/nginx/sites-enabled/
```

Test the Nginx configuration and restart the service:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

## 6. Creating the GitLab CI/CD Pipeline

### 6.1 Create .gitlab-ci.yml File

In your local repository, create a `.gitlab-ci.yml` file:

```bash
nano .gitlab-ci.yml
```

Add the following content:

```yaml
stages:
  - build
  - deploy

build:
  stage: build
  image: node:latest
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - build/

deploy:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
  script:
    - scp -r -o StrictHostKeyChecking=no build/* ${EC2_USER}@${EC2_HOST}:/var/www/react-app
    - ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "sudo systemctl restart nginx"
  only:
    - main
```

### 6.2 Commit and Push the CI/CD Configuration

```bash
git add .gitlab-ci.yml
git commit -m "Add GitLab CI/CD configuration"
git push origin main
```

## 7. Testing the Deployment

### 7.1 Monitor the Pipeline

1. In GitLab, go to your project's "CI/CD" > "Pipelines" section.
2. You should see a pipeline running. Wait for it to complete.

### 7.2 Access Your Deployed Application

Open a web browser and navigate to your EC2 instance's public DNS or IP address. You should see your React application running.

## 8. Optional Enhancements

### 8.1 Implement CI/CD Notifications

To receive email notifications for pipeline events:

1. In GitLab, go to your project's "Settings" > "Integrations" > "Email on pipeline events."
2. Configure the email address and select the events you want to be notified about.
3. Test the integration to ensure it's working correctly.

## 9. Troubleshooting

- If the deployment fails, check the GitLab CI/CD logs for error messages.
- Verify that all GitLab variables are set correctly.
- Ensure the EC2 instance's security group allows inbound traffic on ports 22 and 80.
- Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`

## 10. Conclusion

This guide has walked you through the process of setting up a CI/CD pipeline to deploy a React application to an EC2 instance using GitLab CI/CD. You've learned how to:

- Set up an EC2 instance and configure it for hosting a web application
- Prepare a GitLab repository with a React application
- Configure Nginx as a web server
- Create a GitLab CI/CD pipeline for automated building and deployment
- Implement optional enhancements like email notifications

These skills demonstrate your proficiency in DevOps practices, cloud deployment, and automating software delivery processes. Good luck with your interview!
