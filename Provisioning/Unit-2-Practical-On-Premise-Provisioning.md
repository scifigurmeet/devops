# Practical Guide: On-Premise Provisioning for Beginners

## Introduction
This guide will help you understand on-premise provisioning concepts through hands-on exercises using Docker on your Windows laptop. We'll simulate a small on-premise infrastructure, explore server templating, and demonstrate both server-side and client-side operations. Each exercise includes an explanation of its purpose and how it relates to real-world scenarios.

## Prerequisites
- Windows 10 or 11 laptop
- Docker Desktop installed and running
- Basic familiarity with command line operations

## Part 1: Understanding On-Premise and Provisioning Infrastructure

### What is On-Premise?
"On-premise" refers to hosting and maintaining hardware and software on your own physical infrastructure, typically within your organization's facilities. This is in contrast to cloud-based solutions where resources are hosted by third-party providers.

### Exercise 1: Setting Up a Simple "On-Premise" Environment

**Intention:** This exercise simulates setting up a basic on-premise server. In a real-world scenario, this would involve installing an operating system and necessary software on a physical server in your organization's data center.

**Steps:**

1. Open PowerShell as Administrator
2. Create a new directory for our project:
   ```
   mkdir on-premise-lab
   cd on-premise-lab
   ```
3. Create a simple web server using Node.js. Create a file named `app.js`:
   ```javascript
   const http = require('http');
   const os = require('os');

   const server = http.createServer((req, res) => {
     res.statusCode = 200;
     res.setHeader('Content-Type', 'text/plain');
     res.end(`Hello from ${os.hostname()}`);
   });

   server.listen(3000, () => {
     console.log('Server running on http://localhost:3000/');
   });
   ```

4. Create a Dockerfile:
   ```dockerfile
   FROM node:14
   WORKDIR /app
   COPY app.js .
   EXPOSE 3000
   CMD ["node", "app.js"]
   ```

5. Build and run the Docker image:
   ```
   docker build -t my-onprem-server .
   docker run -d -p 3000:3000 --name server1 my-onprem-server
   ```

6. Open a web browser and navigate to `http://localhost:3000`. You should see a message from your "on-premise" server.

**Interpretation:** By creating this Docker container, we've simulated setting up a single on-premise server. The Dockerfile represents the server configuration, and running the container is analogous to powering on a physical server in your data center.

### Exercise 2: Provisioning Multiple Servers

**Intention:** This exercise demonstrates the concept of provisioning multiple servers, which is common in on-premise environments to handle increased load or separate different applications.

**Steps:**

1. Run two more instances of your server:
   ```
   docker run -d -p 3001:3000 --name server2 my-onprem-server
   docker run -d -p 3002:3000 --name server3 my-onprem-server
   ```

2. Visit `http://localhost:3001` and `http://localhost:3002` in your browser. Notice how each server has a unique hostname.

**Interpretation:** Each Docker container represents a separate server in your on-premise infrastructure. In a real-world scenario, this would be equivalent to setting up multiple physical or virtual servers in your data center. The unique hostnames demonstrate that these are distinct server instances.

## Part 2: Server Templating

### What is Server Templating?
Server templating is the practice of creating a standardized server configuration that can be easily replicated. This ensures consistency across multiple servers and simplifies the provisioning process.

### Exercise 3: Creating a Server Template

**Intention:** This exercise introduces the concept of server templating, allowing you to create servers with different roles based on a single template.

**Steps:**

1. Create a new file named `server-template.js`:
   ```javascript
   const http = require('http');
   const os = require('os');

   const server = http.createServer((req, res) => {
     res.statusCode = 200;
     res.setHeader('Content-Type', 'text/plain');
     res.end(`Hello from ${os.hostname()}\nServer Role: {{SERVER_ROLE}}`);
   });

   server.listen(3000, () => {
     console.log('Server running on http://localhost:3000/');
   });
   ```

2. Update your Dockerfile:
   ```dockerfile
   FROM node:14
   WORKDIR /app
   COPY server-template.js .
   EXPOSE 3000
   CMD sed -i 's/{{SERVER_ROLE}}/'$SERVER_ROLE'/' server-template.js && node server-template.js
   ```

3. Build the new image:
   ```
   docker build -t templated-server .
   ```

4. Run instances with different roles:
   ```
   docker run -d -p 3003:3000 -e SERVER_ROLE=webserver --name web-server templated-server
   docker run -d -p 3004:3000 -e SERVER_ROLE=database --name db-server templated-server
   ```

5. Visit `http://localhost:3003` and `http://localhost:3004` to see the different server roles.

**Interpretation:** The `server-template.js` file represents a server template. By using environment variables (SERVER_ROLE), we can create different server instances from the same template. This is similar to how organizations might use a single base image to create various types of servers (web servers, database servers, etc.) in their on-premise infrastructure.

## Part 3: Connectivity with Servers

### Exercise 4: Setting Up a Client

**Intention:** This exercise demonstrates how clients interact with servers in an on-premise environment. It shows how applications might communicate with different servers for various purposes.

**Steps:**

1. Create a new file named `client.js`:
   ```javascript
   const http = require('http');

   function makeRequest(port) {
     return new Promise((resolve, reject) => {
       http.get(`http://host.docker.internal:${port}`, (res) => {
         let data = '';
         res.on('data', (chunk) => data += chunk);
         res.on('end', () => resolve(data));
       }).on('error', reject);
     });
   }

   async function main() {
     try {
       const response1 = await makeRequest(3003);
       console.log('Response from server 1:', response1);
       const response2 = await makeRequest(3004);
       console.log('Response from server 2:', response2);
     } catch (error) {
       console.error('Error:', error.message);
     }
   }

   main();
   ```

2. Run the client:
   ```
   docker run --rm -v ${PWD}:/app -w /app node:14 node client.js
   ```

**Interpretation:** This client script represents an application in your on-premise environment that needs to communicate with multiple servers. In a real-world scenario, this could be a backend service that needs to interact with both a web server and a database server.

## Part 4: Server-Side vs Client-Side Templating

### What is Templating?
Templating is a technique used to generate dynamic content by combining a template (a pre-designed layout) with data. It can be done on either the server-side or the client-side.

### Exercise 5: Server-Side Templating

**Intention:** This exercise demonstrates server-side templating, where the server generates the final HTML content before sending it to the client.

**Steps:**

1. Install EJS templating engine:
   ```
   npm init -y
   npm install ejs
   ```

2. Create a new file named `server-side-template.js`:
   ```javascript
   const http = require('http');
   const ejs = require('ejs');

   const template = `
   <!DOCTYPE html>
   <html>
   <head><title>Server-Side Templating</title></head>
   <body>
     <h1>Hello, <%= name %>!</h1>
     <p>The current time is: <%= currentTime %></p>
   </body>
   </html>
   `;

   const server = http.createServer((req, res) => {
     const renderedHtml = ejs.render(template, {
       name: 'Student',
       currentTime: new Date().toLocaleTimeString()
     });

     res.statusCode = 200;
     res.setHeader('Content-Type', 'text/html');
     res.end(renderedHtml);
   });

   server.listen(3000, () => {
     console.log('Server running on http://localhost:3000/');
   });
   ```

3. Update your Dockerfile:
   ```dockerfile
   FROM node:14
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY server-side-template.js .
   EXPOSE 3000
   CMD ["node", "server-side-template.js"]
   ```

4. Build and run the server-side templating example:
   ```
   docker build -t server-side-template .
   docker run -d -p 3005:3000 --name server-side server-side-template
   ```

5. Visit `http://localhost:3005` in your browser and refresh a few times to see the time update.

**Interpretation:** In this example, the server generates the complete HTML content, including the dynamic time, before sending it to the client. This approach is common in traditional web applications and can be beneficial for SEO and initial page load times.

### Exercise 6: Client-Side Templating

**Intention:** This exercise showcases client-side templating, where the browser receives a template and data separately, then combines them to generate the final content.

**Steps:**

1. Create a new file named `client-side-template.html`:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <title>Client-Side Templating</title>
     <script src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.7.7/handlebars.min.js"></script>
   </head>
   <body>
     <div id="content"></div>

     <script id="template" type="text/x-handlebars-template">
       <h1>Hello, {{name}}!</h1>
       <p>The current time is: {{currentTime}}</p>
     </script>

     <script>
       const source = document.getElementById('template').innerHTML;
       const template = Handlebars.compile(source);
       
       function updateTime() {
         const context = {
           name: 'Student',
           currentTime: new Date().toLocaleTimeString()
         };
         const html = template(context);
         document.getElementById('content').innerHTML = html;
       }

       setInterval(updateTime, 1000);
       updateTime();
     </script>
   </body>
   </html>
   ```

2. Serve this file using a simple HTTP server:
   ```
   docker run -d -p 3006:80 -v ${PWD}:/usr/share/nginx/html:ro --name client-side nginx
   ```

3. Visit `http://localhost:3006/client-side-template.html` in your browser to see the client-side templating in action.

**Interpretation:** In this example, the browser receives the template and the JavaScript code. The final content is generated in the browser, allowing for dynamic updates without server requests. This approach is common in modern single-page applications (SPAs) and can provide a more responsive user experience for dynamic content.

## Conclusion and Reflection

This guide has provided hands-on experience with key concepts in on-premise provisioning:

1. Setting up a simulated on-premise environment
2. Provisioning multiple servers
3. Server templating
4. Connectivity between clients and servers
5. Server-side templating
6. Client-side templating

**Reflection Questions:**

1. How does server templating simplify the process of setting up multiple servers with different roles?
2. What are the main differences you observed between server-side and client-side templating?
3. Can you think of scenarios where server-side templating might be preferable to client-side templating, and vice versa?
4. How might the challenges of managing an on-premise infrastructure differ from using cloud services?

By working through these exercises and considering these questions, you should now have a practical understanding of the basics of on-premise provisioning and the related concepts of server templating and connectivity.
