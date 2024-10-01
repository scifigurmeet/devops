# Unit 4: Distributed Tracing and Application Performance Monitoring - Beginner's Practical Lab

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Setting Up Your Work Environment](#setting-up-your-work-environment)
4. [Part 1: Distributed Tracing with Jaeger](#part-1-distributed-tracing-with-jaeger)
5. [Part 2: Application Performance Monitoring with New Relic](#part-2-application-performance-monitoring-with-new-relic)
6. [Conclusion](#conclusion)

## 1. Introduction

Welcome to this beginner-friendly practical lab on Distributed Tracing and Application Performance Monitoring! In this lab, you'll learn how to use two important tools in the world of DevOps: Jaeger for distributed tracing and New Relic for application performance monitoring.

Don't worry if these terms sound complicated - we'll explain everything step by step. By the end of this lab, you'll have hands-on experience with these tools and understand their importance in managing modern applications.

## 2. Prerequisites

Before we start, make sure you have the following installed on your Windows computer:

- Docker Desktop: This will allow us to run our applications in containers.
- Git: We'll use this to download some code.
- A text editor: Visual Studio Code is recommended, but any text editor will do.

If you haven't installed these yet, please do so before continuing.

## 3. Setting Up Your Work Environment

Let's start by setting up our work environment:

1. Open the Command Prompt on your Windows computer. You can do this by pressing the Windows key, typing "cmd", and pressing Enter.

2. Create a new folder for our project and navigate into it:
   ```
   mkdir distributed-tracing-lab
   cd distributed-tracing-lab
   ```

3. Open this folder in your text editor. If you're using Visual Studio Code, you can do this by typing:
   ```
   code .
   ```

Now you're ready to start the lab!

## 4. Part 1: Distributed Tracing with Jaeger

### What is Distributed Tracing?

Distributed tracing is a method used to track requests as they flow through distributed systems. It helps developers understand the path of a request as it travels through various services, making it easier to identify bottlenecks and troubleshoot issues.

### What is Jaeger?

Jaeger is an open-source distributed tracing system. It helps collect and visualize data about request flows in a distributed system.

### 4.1 Setting up Jaeger

1. In your text editor, create a new file named `docker-compose.yml` in the `distributed-tracing-lab` folder.

2. Copy and paste the following content into `docker-compose.yml`:
   ```yaml
   version: '3'
   services:
     jaeger:
       image: jaegertracing/all-in-one:latest
       ports:
         - "16686:16686"
         - "6831:6831/udp"
   ```

   This file tells Docker how to run Jaeger for us.

3. Save the file.

4. In your Command Prompt, make sure you're in the `distributed-tracing-lab` folder, then run:
   ```
   docker-compose up -d
   ```

   This command starts Jaeger in the background.

### 4.2 Creating a Sample Microservices Application

We'll create two simple Python services: an API gateway and a backend service. These will demonstrate how distributed tracing works across multiple services.

1. In your text editor, create a new file named `api_gateway.py` in the `distributed-tracing-lab` folder.

2. Copy and paste the following code into `api_gateway.py`:
   ```python
   from flask import Flask, jsonify
   import requests
   from jaeger_client import Config
   from flask_opentracing import FlaskTracing
   
   app = Flask(__name__)
   
   def init_tracer():
       config = Config(
           config={
               'sampler': {'type': 'const', 'param': 1},
               'local_agent': {'reporting_host': 'jaeger'},
           },
           service_name='api_gateway'
       )
       return config.initialize_tracer()
   
   tracer = init_tracer()
   tracing = FlaskTracing(tracer, True, app)
   
   @app.route('/api/user/<username>')
   def get_user(username):
       with tracer.start_span('get-user') as span:
           response = requests.get(f'http://backend:5000/user/{username}')
           span.set_tag('http.status_code', response.status_code)
           return jsonify(response.json())
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8080)
   ```

   This code creates a simple API gateway that forwards requests to our backend service.

3. Create another new file named `backend_service.py` in the same folder.

4. Copy and paste the following code into `backend_service.py`:
   ```python
   from flask import Flask, jsonify
   from jaeger_client import Config
   from flask_opentracing import FlaskTracing
   
   app = Flask(__name__)
   
   def init_tracer():
       config = Config(
           config={
               'sampler': {'type': 'const', 'param': 1},
               'local_agent': {'reporting_host': 'jaeger'},
           },
           service_name='backend_service'
       )
       return config.initialize_tracer()
   
   tracer = init_tracer()
   tracing = FlaskTracing(tracer, True, app)
   
   @app.route('/user/<username>')
   def get_user(username):
       with tracer.start_span('fetch-user-data') as span:
           # Simulate database query
           user_data = {'username': username, 'email': f'{username}@example.com'}
           span.set_tag('user.username', username)
           return jsonify(user_data)
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

   This code creates a simple backend service that returns user data.

5. Save both files.

### 4.3 Setting Up Docker for Our Services

1. Create a new file named `Dockerfile.api` in the `distributed-tracing-lab` folder.

2. Copy and paste the following content into `Dockerfile.api`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY api_gateway.py .
   CMD ["python", "api_gateway.py"]
   ```

3. Create another new file named `Dockerfile.backend` in the same folder.

4. Copy and paste the following content into `Dockerfile.backend`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY backend_service.py .
   CMD ["python", "backend_service.py"]
   ```

5. Create a new file named `requirements.txt` in the same folder.

6. Copy and paste the following content into `requirements.txt`:
   ```
   flask
   requests
   jaeger-client
   flask-opentracing
   ```

7. Now, update your `docker-compose.yml` file to include our new services. Replace the entire content of `docker-compose.yml` with:
   ```yaml
   version: '3'
   services:
     jaeger:
       image: jaegertracing/all-in-one:latest
       ports:
         - "16686:16686"
         - "6831:6831/udp"
     
     api_gateway:
       build:
         context: .
         dockerfile: Dockerfile.api
       ports:
         - "8080:8080"
       depends_on:
         - jaeger
         - backend
     
     backend:
       build:
         context: .
         dockerfile: Dockerfile.backend
       depends_on:
         - jaeger
   ```

8. Save all files.

### 4.4 Running and Testing the Application

1. In your Command Prompt, make sure you're in the `distributed-tracing-lab` folder, then run:
   ```
   docker-compose up --build
   ```

   This command builds and starts all our services.

2. Once everything is running, open a web browser and visit `http://localhost:8080/api/user/testuser`

   You should see some JSON data about a user.

### 4.5 Analyzing Traces in Jaeger UI

1. Open another tab in your web browser and visit `http://localhost:16686`

   This opens the Jaeger UI.

2. In the left sidebar, select "api_gateway" from the "Service" dropdown.

3. Click "Find Traces" to see the traces generated by your requests.

4. Click on a trace to see detailed information about how the request moved through your services.

Congratulations! You've just set up and used distributed tracing with Jaeger!

## 5. Part 2: Application Performance Monitoring with New Relic

### What is Application Performance Monitoring (APM)?

APM tools help you monitor and manage the performance and availability of your software applications. They provide insights into how your application is performing and help identify issues.

### What is New Relic?

New Relic is a popular APM tool that provides detailed performance metrics for your applications.

### 5.1 Setting up New Relic

1. Sign up for a free New Relic account at https://newrelic.com/signup

2. After signing up, you'll receive a license key. We'll need this for the next steps.

### 5.2 Instrumenting the Application with New Relic

1. Update `api_gateway.py`. Replace its entire content with:
   ```python
   from flask import Flask, jsonify
   import requests
   import newrelic.agent
   
   newrelic.agent.initialize('newrelic.ini')
   
   app = Flask(__name__)
   
   @app.route('/api/user/<username>')
   @newrelic.agent.flask_application()
   def get_user(username):
       response = requests.get(f'http://backend:5000/user/{username}')
       return jsonify(response.json())
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8080)
   ```

2. Update `backend_service.py`. Replace its entire content with:
   ```python
   from flask import Flask, jsonify
   import newrelic.agent
   
   newrelic.agent.initialize('newrelic.ini')
   
   app = Flask(__name__)
   
   @app.route('/user/<username>')
   @newrelic.agent.flask_application()
   def get_user(username):
       # Simulate database query
       user_data = {'username': username, 'email': f'{username}@example.com'}
       return jsonify(user_data)
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

3. Create a new file named `newrelic.ini` in the `distributed-tracing-lab` folder.

4. Copy and paste the following into `newrelic.ini`, replacing `your_license_key_here` with your actual New Relic license key:
   ```ini
   [newrelic]
   license_key = your_license_key_here
   app_name = Python Application
   monitor_mode = true
   log_level = info
   ssl = true
   high_security = false
   transaction_tracer.enabled = true
   transaction_tracer.transaction_threshold = apdex_f
   transaction_tracer.record_sql = obfuscated
   transaction_tracer.stack_trace_threshold = 0.5
   transaction_tracer.explain_enabled = true
   transaction_tracer.explain_threshold = 0.5
   transaction_tracer.function_trace =
   error_collector.enabled = true
   error_collector.ignore_errors =
   browser_monitoring.auto_instrument = true
   thread_profiler.enabled = true
   distributed_tracing.enabled = true
   ```

5. Update `requirements.txt`. Add a new line at the end of the file:
   ```
   newrelic
   ```

6. Update both `Dockerfile.api` and `Dockerfile.backend`. Add this line just before the `CMD` line in both files:
   ```dockerfile
   COPY newrelic.ini .
   ```

7. Save all files.

### 5.3 Running and Testing the Application

1. In your Command Prompt, make sure you're in the `distributed-tracing-lab` folder, then run:
   ```
   docker-compose up --build
   ```

   This rebuilds and starts all our services with New Relic instrumentation.

2. Generate some traffic by making multiple requests to `http://localhost:8080/api/user/testuser` in your web browser.

### 5.4 Analyzing Performance in New Relic Dashboard

1. Log in to your New Relic account at https://one.newrelic.com

2. In the left sidebar, click on "APM" (Application Performance Monitoring).

3. You should see your application listed. Click on it to view detailed performance metrics.

4. Explore different sections of the New Relic dashboard:
   - Overview: General application performance
   - Transactions: Detailed breakdown of API endpoints
   - Errors: Any exceptions or errors in your application

Congratulations! You've now set up application performance monitoring with New Relic!

## 6. Conclusion

In this lab, you've successfully:
1. Implemented distributed tracing using Jaeger
2. Set up application performance monitoring using New Relic
3. Created a simple microservices application and instrumented it with both tools
4. Analyzed traces and performance metrics

These skills are crucial for monitoring and troubleshooting modern, distributed applications. As you work on more complex systems, you'll find these tools invaluable for maintaining performance and quickly identifying issues.

Remember, practice makes perfect. Try modifying the application or adding more services to see how it affects the traces and performance metrics. Happy learning!
