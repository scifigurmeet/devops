# CSV 204 - Build & Release Management Lab
## Unit 5: Containerization and Automated Container Image Publishing

### Introduction

Containerization has revolutionized the way we deploy and manage applications. Docker, one of the most popular containerization platforms, allows developers to package applications with all their dependencies into standardized units called containers. These containers can run consistently across different environments, from development to production.

GitHub Actions, on the other hand, is a powerful CI/CD (Continuous Integration/Continuous Deployment) tool that allows you to automate your software workflow. In this lab, we'll use GitHub Actions to automatically build and publish our Docker images.

### Objectives

By the end of this lab, you will be able to:
1. Create a Dockerfile for a Node.js application
2. Build and run Docker containers locally
3. Set up a GitHub repository with GitHub Actions
4. Create a workflow to automatically build and publish Docker images

### Prerequisites

- Basic knowledge of Node.js and npm
- Git and GitHub account
- Docker installed on your local machine
- A Docker Hub account (for publishing images)

### Part 1: Creating a Dockerfile for a Node.js Application

1. Create a new directory for your project and navigate into it:
   ```bash
   mkdir nodejs-docker-demo
   cd nodejs-docker-demo
   ```

2. Initialize a new Node.js project and install Express:
   ```bash
   npm init -y
   npm install express
   ```

3. Create a simple `app.js` file:
   ```javascript
   const express = require('express');
   const app = express();
   const port = 3000;

   app.get('/', (req, res) => {
     res.send('Hello from a containerized Node.js app!');
   });

   app.listen(port, () => {
     console.log(`App listening at http://localhost:${port}`);
   });
   ```

4. Create a `Dockerfile` in the root of your project:
   ```dockerfile
   FROM node:14

   WORKDIR /usr/src/app

   COPY package*.json ./

   RUN npm install

   COPY . .

   EXPOSE 3000

   CMD [ "node", "app.js" ]
   ```

5. Create a `.dockerignore` file to exclude unnecessary files:
   ```
   node_modules
   npm-debug.log
   ```

### Part 2: Building and Running Docker Containers Locally

1. Build your Docker image:
   ```bash
   docker build -t nodejs-docker-demo .
   ```

2. Run your Docker container:
   ```bash
   docker run -p 3000:3000 nodejs-docker-demo
   ```

3. Open a web browser and navigate to `http://localhost:3000` to see your app running.

4. Stop the container by pressing `Ctrl+C` in the terminal where it's running.

### Part 3: Setting Up a GitHub Repository with GitHub Actions

1. Create a new repository on GitHub.

2. Initialize Git in your local project directory and push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/nodejs-docker-demo.git
   git push -u origin main
   ```

3. In your GitHub repository, go to "Settings" > "Secrets" and add the following secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

### Part 4: Creating a GitHub Actions Workflow

1. In your local project, create a directory structure for GitHub Actions:
   ```bash
   mkdir -p .github/workflows
   ```

2. Create a file named `docker-publish.yml` in the `.github/workflows` directory:
   ```yaml
   name: Docker Publish

   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]

   jobs:
     build-and-push:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v2
       
       - name: Log in to Docker Hub
         uses: docker/login-action@v1
         with:
           username: ${{ secrets.DOCKERHUB_USERNAME }}
           password: ${{ secrets.DOCKERHUB_TOKEN }}
       
       - name: Build and push Docker image
         uses: docker/build-push-action@v2
         with:
           context: .
           push: true
           tags: ${{ secrets.DOCKERHUB_USERNAME }}/nodejs-docker-demo:latest
   ```

3. Commit and push these changes to GitHub:
   ```bash
   git add .
   git commit -m "Add GitHub Actions workflow"
   git push
   ```

4. Go to your GitHub repository and click on the "Actions" tab to see your workflow running.

### Part 5: Verifying the Automated Build and Publish Process

1. Make a small change to your `app.js` file, for example:
   ```javascript
   app.get('/', (req, res) => {
     res.send('Hello from an updated containerized Node.js app!');
   });
   ```

2. Commit and push this change:
   ```bash
   git add app.js
   git commit -m "Update app message"
   git push
   ```

3. Go to your GitHub repository's "Actions" tab and watch the workflow run.

4. Once the workflow is complete, go to your Docker Hub repository to verify that a new image has been pushed.

### Exercises

1. Modify the GitHub Actions workflow to only trigger on tagged releases instead of every push to main.
2. Add a step in the workflow to scan the Docker image for vulnerabilities before pushing it to Docker Hub.
3. Create a development Dockerfile that includes development dependencies and uses `nodemon` for hot reloading.
4. Modify the `app.js` to read a message from an environment variable, and update the Dockerfile and GitHub Actions workflow to pass this variable.

### Conclusion

In this lab, you've learned how to containerize a Node.js application using Docker and how to automate the build and publish process using GitHub Actions. These skills are crucial for modern DevOps practices, allowing for consistent deployment across different environments and streamlining the delivery pipeline.

Remember to always follow best practices for Dockerfile creation and to keep your GitHub Action workflows secure by using secrets for sensitive information.
