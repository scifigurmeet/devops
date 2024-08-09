# Practical Guide: On-Premise Provisioning

## Introduction
This guide will help you understand on-premise provisioning concepts through hands-on exercises using Docker on your Windows laptop. We'll simulate a small on-premise infrastructure, explore server templating, and demonstrate both server-side and client-side operations.

## Prerequisites
- Windows 10 or 11 laptop
- Docker Desktop installed and running
- Basic familiarity with command line operations

## Part 1: Understanding On-Premise and Provisioning Infrastructure

### Exercise 1: Setting Up a Simple "On-Premise" Environment

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

### Exercise 2: Provisioning Multiple Servers

1. Run two more instances of your server:
   ```
   docker run -d -p 3001:3000 --name server2 my-onprem-server
   docker run -d -p 3002:3000 --name server3 my-onprem-server
   ```

2. Visit `http://localhost:3001` and `http://localhost:3002` in your browser. Notice how each server has a unique hostname.

## Part 2: Server Templating

### Exercise 3: Creating a Server Template

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

## Part 3: Connectivity with Servers

### Exercise 4: Setting Up a Client

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

## Part 4: Server-Side vs Client-Side Templating

### Exercise 5: Server-Side Templating

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

### Exercise 6: Client-Side Templating

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

## Conclusion

This guide has provided hands-on experience with:
- Setting up a simulated on-premise environment
- Provisioning multiple servers
- Server templating
- Connectivity between clients and servers
- Server-side templating
- Client-side templating

By comparing the server-side and client-side templating examples, you can observe the differences in how and where the content is generated, helping you understand the advantages and challenges of each approach.
