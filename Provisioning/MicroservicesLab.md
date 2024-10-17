# DevOps Microservices Project Lab Guide for Beginners

## Introduction
Welcome to this hands-on lab guide on microservices and Docker! This guide is designed for B.Tech final year students who are new to microservices architecture and containerization. By the end of this 2-3 hour laboratory session, you'll have created a small but functional e-commerce application using microservices, all running in Docker containers.

### What are Microservices?
Microservices is an architectural style that structures an application as a collection of small, loosely coupled services. Each service is focused on doing one thing well, runs in its own process, and communicates with other services through well-defined APIs. This approach contrasts with monolithic architectures where all functionality exists in a single, tightly-coupled application.

### Why Docker?
Docker is a platform for developing, shipping, and running applications in containers. Containers are lightweight, standalone, executable packages that include everything needed to run a piece of software, including the code, runtime, system tools, libraries, and settings. Docker makes it easy to create, deploy, and run applications in a consistent environment, which is crucial when working with microservices.

## Prerequisites
- Docker Desktop installed on your Windows PC
- Basic knowledge of Python and Flask
- Familiarity with RESTful APIs
- Text editor (e.g., Visual Studio Code)

## Project Overview
Our e-commerce application will consist of the following microservices:
1. Product Service: Manages product information
2. Order Service: Handles order processing
3. Frontend Service: Serves the user interface and integrates the other services

Each service will run in its own Docker container, demonstrating the isolation and independence of microservices.

## Step 1: Set Up Project Structure (15 minutes)
Create the following directory structure for your project:

```
ecommerce-microservices/
├── product-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── order-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
│       └── index.html
└── docker-compose.yml
```

This structure separates each microservice into its own directory, promoting modularity and independence. The `docker-compose.yml` file at the root will orchestrate all services.

## Step 2: Implement Product Service (30 minutes)

### Understanding the Product Service
The Product Service is responsible for managing product information. In a real-world scenario, this service would interact with a database to store and retrieve product data. For simplicity, we'll use an in-memory list to store products.

1. In `product-service/app.py`, create a Flask app with a simple in-memory product database:

```python
from flask import Flask, jsonify
app = Flask(__name__)

# In-memory product database
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99},
    {"id": 3, "name": "Headphones", "price": 99.99}
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Explanation:
- We create a Flask application and define a list of products.
- The `@app.route('/products', methods=['GET'])` decorator creates an endpoint that responds to GET requests at the '/products' URL.
- The `get_products()` function returns the list of products as a JSON response.
- We run the app on host `0.0.0.0` to make it accessible outside the container, and on port 5000.

2. Create `product-service/requirements.txt`:
```
Flask==2.0.1
```
This file lists the Python packages required for the service.

3. Create `product-service/Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Explanation of the Dockerfile:
- `FROM python:3.9-slim`: Use the official Python 3.9 slim image as the base.
- `WORKDIR /app`: Set the working directory in the container.
- `COPY requirements.txt .`: Copy the requirements file into the container.
- `RUN pip install -r requirements.txt`: Install the required Python packages.
- `COPY . .`: Copy all files from the current directory to the container.
- `CMD ["python", "app.py"]`: Specify the command to run when the container starts.

## Step 3: Implement Order Service (30 minutes)

### Understanding the Order Service
The Order Service handles order processing. It will allow creating new orders and retrieving all orders. Like the Product Service, we'll use an in-memory list to store orders for simplicity.

1. In `order-service/app.py`, create a Flask app with a simple in-memory order database:

```python
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# In-memory order database
orders = []

@app.route('/orders', methods=['POST'])
def create_order():
    order = request.json
    order['id'] = str(uuid.uuid4())  # Generate a unique ID for the order
    orders.append(order)
    return jsonify(order), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

Explanation:
- We create two endpoints: one for creating orders (POST) and one for retrieving all orders (GET).
- The `create_order()` function receives order data as JSON, generates a unique ID, and adds it to the orders list.
- The `get_orders()` function returns all orders as a JSON response.

2. Create `order-service/requirements.txt`:
```
Flask==2.0.1
```

3. Create `order-service/Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

This Dockerfile is similar to the one for the Product Service.

## Step 4: Implement Frontend Service (40 minutes)

### Understanding the Frontend Service
The Frontend Service serves as the user interface and integrates the Product and Order services. It will display products, allow adding them to a cart, and place orders.

1. In `frontend-service/app.py`, create a Flask app that interacts with both the product and order services:

```python
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

PRODUCT_SERVICE_URL = 'http://product-service:5000'
ORDER_SERVICE_URL = 'http://order-service:5001'

@app.route('/')
def index():
    products = requests.get(f'{PRODUCT_SERVICE_URL}/products').json()
    return render_template('index.html', products=products)

@app.route('/place-order', methods=['POST'])
def place_order():
    order = request.json
    response = requests.post(f'{ORDER_SERVICE_URL}/orders', json=order)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
```

Explanation:
- We define URLs for the Product and Order services. Note that we use the service names defined in Docker Compose (explained later) as hostnames.
- The `index()` function retrieves products from the Product Service and renders them in the HTML template.
- The `place_order()` function receives order data from the frontend and sends it to the Order Service.

2. Create `frontend-service/templates/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-commerce Microservices Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.js"></script>
</head>
<body>
    <div id="app">
        <h1>Product List</h1>
        <ul>
            <li v-for="product in products" :key="product.id">
                {{ product.name }} - ${{ product.price }}
                <button @click="addToCart(product)">Add to Cart</button>
            </li>
        </ul>
        <h2>Cart</h2>
        <ul>
            <li v-for="item in cart" :key="item.id">
                {{ item.name }} - ${{ item.price }}
            </li>
        </ul>
        <button @click="placeOrder" :disabled="cart.length === 0">Place Order</button>
        <div v-if="orderPlaced">Order placed successfully!</div>
    </div>
    <script>
        new Vue({
            el: '#app',
            data: {
                products: {{ products|tojson|safe }},
                cart: [],
                orderPlaced: false
            },
            methods: {
                addToCart(product) {
                    this.cart.push(product);
                },
                placeOrder() {
                    fetch('/place-order', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            items: this.cart
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        this.orderPlaced = true;
                        this.cart = [];
                    });
                }
            }
        });
    </script>
</body>
</html>
```

This HTML file uses Vue.js for dynamic content and interactivity. It displays products, allows adding them to a cart, and placing orders.

3. Create `frontend-service/requirements.txt`:
```
Flask==2.0.1
requests==2.26.0
```

4. Create `frontend-service/Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Step 5: Create Docker Compose File (20 minutes)

### Understanding Docker Compose
Docker Compose is a tool for defining and running multi-container Docker applications. It uses a YAML file to configure the application's services, networks, and volumes.

Create a `docker-compose.yml` file in the root directory:

```yaml
version: '3'
services:
  product-service:
    build: ./product-service
    ports:
      - "5000:5000"

  order-service:
    build: ./order-service
    ports:
      - "5001:5001"

  frontend-service:
    build: ./frontend-service
    ports:
      - "5002:5002"
    depends_on:
      - product-service
      - order-service
```

Explanation:
- We define three services: product-service, order-service, and frontend-service.
- For each service, we specify the build context (the directory containing the Dockerfile) and the ports to expose.
- The `depends_on` field for the frontend-service ensures that it starts after the other services.

## Step 6: Build and Run the Application (15 minutes)
1. Open a terminal in the root directory of your project.
2. Run the following command to build and start the containers:
   ```
   docker-compose up --build
   ```
3. Wait for the containers to start. You should see output from all three services.

This command does the following:
- Builds Docker images for each service based on their Dockerfiles.
- Creates a Docker network for the services to communicate.
- Starts containers for each service, mapping the specified ports to the host.

## Step 7: Test the Application (20 minutes)
1. Open a web browser and navigate to `http://localhost:5002`.
2. You should see a list of products. Add some products to the cart and place an order.
3. To verify the order was created, you can use curl or a tool like Postman to send a GET request to `http://localhost:5001/orders`.

Example using curl:
```
curl http://localhost:5001/orders
```

This should return a JSON array of orders.

## Conclusion and Further Exploration (20 minutes)
Congratulations! You've created a basic microservices application using Docker. Let's recap what we've learned:

1. Microservices Architecture: We built three separate services, each with its own responsibility.
2. Docker Containers: Each service runs in its own container, providing isolation and portability.
3. Docker Compose: We used Docker Compose to orchestrate our multi-container application.
4. Inter-service Communication: Our services communicate with each other over HTTP.

Here are some ideas for further exploration:

1. Persistent Storage: Add databases (e.g., MySQL, MongoDB) to store products and orders persistently.
2. Service Discovery: Implement service discovery using tools like Consul or etcd.
3. API Gateway: Add an API gateway to route requests to the appropriate services and handle cross-cutting concerns like authentication.
4. Authentication and Authorization: Implement user accounts and secure the services.
5. Container Orchestration: Explore using Docker Swarm or Kubernetes for managing your containerized services at scale.
6. Monitoring and Logging: Add centralized logging and monitoring to your microservices.

Remember to stop your containers when you're done:
```
docker-compose down
```

This lab has introduced you to key concepts in microservices architecture and containerization. Continue exploring these technologies to deepen your understanding of DevOps practices. Don't hesitate to experiment with the code, add new features, or try different configurations!
