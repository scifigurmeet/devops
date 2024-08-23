# Swagger API Documentation Tutorial for Beginners

This tutorial will guide you through creating a simple API endpoint using Node.js and Express, and then documenting it using Swagger. We'll create an API that returns a "Hello, World!" message.

## Prerequisites

- Node.js installed on your computer
- Basic understanding of JavaScript
- A text editor (e.g., Visual Studio Code, Sublime Text)

## Step 1: Set up the project

1. Create a new directory for your project:
   ```
   mkdir swagger-api-tutorial
   cd swagger-api-tutorial
   ```

2. Initialize a new Node.js project:
   ```
   npm init -y
   ```

3. Install the required dependencies:
   ```
   npm install express swagger-jsdoc swagger-ui-express
   ```

## Step 2: Create the API

1. Create a new file called `app.js` in your project directory and add the following code:

```javascript
const express = require('express');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const app = express();
const port = 3000;

/**
 * @swagger
 * /hello:
 *   get:
 *     summary: Returns a hello world message
 *     description: A simple endpoint that returns a greeting message
 *     responses:
 *       200:
 *         description: A successful response
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 message:
 *                   type: string
 *                   example: Hello, World!
 */
app.get('/hello', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

// Swagger configuration
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Hello World API',
      version: '1.0.0',
      description: 'A simple Express API',
    },
  },
  apis: ['./app.js'], // files containing annotations as above
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
  console.log(`Swagger documentation is available on http://localhost:${port}/api-docs`);
});
```

## Step 3: Run the API

1. Start the server by running:
   ```
   node app.js
   ```

2. You should see output similar to:
   ```
   Server is running on http://localhost:3000
   Swagger documentation is available on http://localhost:3000/api-docs
   ```

## Step 4: Test the API

1. Open a web browser and go to `http://localhost:3000/hello`. You should see a JSON response:
   ```json
   {"message":"Hello, World!"}
   ```

2. To view the Swagger documentation, go to `http://localhost:3000/api-docs`. You'll see the Swagger UI with your API documentation.

## Understanding the Code

- We use Express to create a simple web server and define our `/hello` endpoint.
- The `@swagger` comments above the endpoint are used to generate the Swagger documentation.
- We configure Swagger using `swaggerOptions` and generate the Swagger specification using `swaggerJsdoc`.
- Finally, we serve the Swagger UI using `swagger-ui-express`.

## Conclusion

You've now created a simple API endpoint and documented it using Swagger. This approach makes it easy for others to understand and interact with your API. As you build more complex APIs, you can add more endpoints and expand your Swagger documentation accordingly.

