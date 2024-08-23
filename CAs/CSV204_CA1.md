# Practical Assignment: Advanced npm and Private Registries

## Objective
Set up a Node.js project using a private npm registry, create and publish a scoped package, and use environment variables for configuration.

## Time
15-20 minutes

## Prerequisites
- Node.js and npm installed
- Access to a private npm registry (e.g., Verdaccio running locally or a provided Artifactory instance)

## Steps

1. Set up the private registry:
   - If using Verdaccio locally, install and start it:
     ```
     npm install -g verdaccio
     verdaccio
     ```
   - If using a provided Artifactory instance, ensure you have the access URL and credentials

2. Configure npm to use the private registry:
   - Create a `.npmrc` file in your home directory or project root
   - Add the registry URL:
     ```
     registry=http://localhost:4873  # For local Verdaccio
     # OR
     registry=http://your-artifactory-url  # For Artifactory
     ```

3. Create a new Node.js project:
   - Create a new directory and navigate into it
   - Run `npm init -y` to create a `package.json` file

4. Modify the `package.json`:
   - Add a scope to your package name (e.g., "@myorg/my-package")
   - Add a simple script that uses an environment variable:
     ```json
     "scripts": {
       "start": "node index.js"
     }
     ```

5. Create an `index.js` file:
   ```javascript
   console.log(`Hello from ${process.env.PROJECT_NAME || 'unnamed project'}!`);
   ```

6. Create a simple module to publish:
   - Create a file named `greeting.js`:
     ```javascript
     module.exports = (name) => `Hello, ${name}!`;
     ```

7. Update `package.json` to include only the `greeting.js` file:
   ```json
   "files": ["greeting.js"]
   ```

8. Publish your package to the private registry:
   - If required, add user to the registry: `npm adduser --registry=http://localhost:4873`
   - Publish: `npm publish --registry=http://localhost:4873`

9. In a new directory, create a project that uses your published package:
   - Initialize a new project: `npm init -y`
   - Install your package: `npm install @myorg/my-package`
   - Create an `index.js` that uses your package

10. Run your new project with an environment variable:
    ```
    PROJECT_NAME="Awesome Project" npm start
    ```

## Submission
Provide:
1. Your `.npmrc` file content (exclude any sensitive information)
2. The `package.json` of your published package
3. The `package.json` of the project that uses your published package
4. A screenshot of the output when running the project with the environment variable

Include a brief explanation (3-4 sentences) of what you learned about private registries, scoped packages, and environment variables in npm projects.
