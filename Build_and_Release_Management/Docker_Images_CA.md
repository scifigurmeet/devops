# Unit 5: Containerization
## Creating Docker images for Node.js applications

**Instructions:**
- This practical is designed for Windows PC users, but most commands are OS-independent.
- Ensure you have Docker Desktop installed on your system.
- You should have Node.js and npm (Node Package Manager) installed.

---

1. What is the command to check if Docker is installed correctly on your system?

   **Answer:**
   ```
   docker --version
   ```
   This command will display the installed Docker version if it's correctly set up.

2. Create a simple Node.js application that responds with "Hello, Docker!" when accessed. Show the content of the `app.js` file.

   **Answer:**
   Create a file named `app.js` with the following content:
   ```javascript
   const express = require('express');
   const app = express();
   const PORT = process.env.PORT || 3000;

   app.get('/', (req, res) => {
     res.send('Hello, Docker!');
   });

   app.listen(PORT, () => {
     console.log(`Server is running on port ${PORT}`);
   });
   ```

3. Create a `package.json` file for your Node.js application. What command do you use, and what should be the content of the file?

   **Answer:**
   Use the following command to create a `package.json` file:
   ```
   npm init -y
   ```
   Then, modify the `package.json` file to look like this:
   ```json
   {
     "name": "docker-nodejs-app",
     "version": "1.0.0",
     "description": "A simple Node.js app for Docker",
     "main": "app.js",
     "scripts": {
       "start": "node app.js"
     },
     "dependencies": {
       "express": "^4.17.1"
     }
   }
   ```

4. What command do you use to install the required dependencies for your Node.js application?

   **Answer:**
   ```
   npm install
   ```
   This command will install all dependencies listed in the `package.json` file, in this case, Express.js.

5. Create a Dockerfile for your Node.js application. What should be the content of this file?

   **Answer:**
   Create a file named `Dockerfile` (no extension) with the following content:
   ```dockerfile
   # Use an official Node.js runtime as the base image
   FROM node:14

   # Set the working directory in the container
   WORKDIR /usr/src/app

   # Copy package.json and package-lock.json to the working directory
   COPY package*.json ./

   # Install the application dependencies
   RUN npm install

   # Copy the application code to the working directory
   COPY . .

   # Expose the port that the app runs on
   EXPOSE 3000

   # Define the command to run the application
   CMD [ "npm", "start" ]
   ```

6. What command do you use to build a Docker image from your Dockerfile? Assume you want to tag the image as "my-nodejs-app:1.0".

   **Answer:**
   ```
   docker build -t my-nodejs-app:1.0 .
   ```
   This command builds a Docker image using the Dockerfile in the current directory (`.`) and tags it as "my-nodejs-app" with version "1.0".

7. How do you list all Docker images on your system?

   **Answer:**
   ```
   docker images
   ```
   This command lists all Docker images currently stored on your system.

8. What command do you use to run a container from your newly created image, mapping port 3000 of the container to port 8080 on your host machine?

   **Answer:**
   ```
   docker run -p 8080:3000 my-nodejs-app:1.0
   ```
   This command runs a container from the "my-nodejs-app:1.0" image, mapping port 3000 in the container to port 8080 on your host machine.

9. How do you check if your container is running? Provide the command and explain its output.

   **Answer:**
   ```
   docker ps
   ```
   This command lists all running containers. The output will show details like the Container ID, Image, Command, Created time, Status, Ports, and Name of each running container.

10. What command do you use to stop a running container? Assume the container ID is "abc123".

    **Answer:**
    ```
    docker stop abc123
    ```
    This command stops the container with the ID "abc123". You can also use the container name instead of the ID if you prefer.

11. How do you remove a Docker image from your system? Provide the command to remove the "my-nodejs-app:1.0" image.

    **Answer:**
    ```
    docker rmi my-nodejs-app:1.0
    ```
    This command removes the Docker image tagged as "my-nodejs-app:1.0" from your system.

12. Create a `.dockerignore` file for your Node.js application. What should be its content and why?

    **Answer:**
    Create a file named `.dockerignore` with the following content:
    ```
    node_modules
    npm-debug.log
    ```
    This file tells Docker to ignore the `node_modules` directory and any npm debug logs when building the image. We ignore `node_modules` because we want to install fresh dependencies in the container, and debug logs are not needed in the image.

13. How can you view the logs of a running container? Assume the container name is "myapp-container".

    **Answer:**
    ```
    docker logs myapp-container
    ```
    This command displays the logs output by the container named "myapp-container".

14. What command would you use to execute an interactive bash shell in a running container named "myapp-container"?

    **Answer:**
    ```
    docker exec -it myapp-container /bin/bash
    ```
    This command starts an interactive bash shell inside the running container, allowing you to explore its file system and run commands.

15. How do you create a volume and mount it to a container when running it? Provide a command that creates a volume named "myapp-data" and mounts it to "/usr/src/app/data" in the container.

    **Answer:**
    First, create the volume:
    ```
    docker volume create myapp-data
    ```
    Then, run the container with the volume mounted:
    ```
    docker run -p 8080:3000 -v myapp-data:/usr/src/app/data my-nodejs-app:1.0
    ```
    This command runs the container, mapping ports as before, and mounts the "myapp-data" volume to "/usr/src/app/data" in the container.

---

This practical guide covers the basics of creating Docker images for Node.js applications. It includes creating a simple Node.js app, writing a Dockerfile, building and running Docker images, and basic Docker commands for managing containers and images. Remember to practice these concepts regularly to become proficient in using Docker for your Node.js applications.
