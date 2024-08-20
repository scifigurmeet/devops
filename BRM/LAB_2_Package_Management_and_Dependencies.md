# CSV 204 - Build & Release Management Lab
## Unit 2: Package Management and Dependencies

### 🎯 Objectives
By the end of this practical, you will be able to:
- Understand Artifactory requirements in package.json
- Work with environment variables and secrets management
- Deploy npm packages to Artifactory
- Use npm scopes for organization-level packages

### 📚 Prerequisites
- Completion of Unit 1
- Access to an Artifactory instance (we'll use JFrog Artifactory for this lab)

### 1. Artifactory requirements in package.json

JFrog Artifactory is a universal repository manager supporting all major packaging formats. Let's set up our project to work with Artifactory.

1. Modify your `package.json` to include Artifactory-specific fields:

```json
{
  "name": "my-node-project",
  "version": "1.0.0",
  "description": "A project demonstrating Artifactory integration",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": ["artifactory", "npm"],
  "author": "Your Name",
  "license": "ISC",
  "publishConfig": {
    "registry": "https://your-artifactory-url/api/npm/npm-local/"
  },
  "repository": {
    "type": "git",
    "url": "https://your-git-repo-url.git"
  }
}
```

📝 Note: Replace `https://your-artifactory-url/api/npm/npm-local/` with your actual Artifactory npm repository URL.

### 2. Working with environment variables and secrets management

It's crucial to keep sensitive information like API keys and passwords out of your source code. Let's use environment variables to manage secrets.

1. Install the `dotenv` package:

```bash
npm install dotenv
```

2. Create a `.env` file in your project root:

```
ARTIFACTORY_API_KEY=your-api-key-here
ARTIFACTORY_EMAIL=your-email@example.com
```

3. Create a `.gitignore` file to prevent committing sensitive information:

```
node_modules
.env
```

4. Modify your `index.js` to use environment variables:

```javascript
require('dotenv').config();
const _ = require('lodash');

console.log("Artifactory Email:", process.env.ARTIFACTORY_EMAIL);

const numbers = [1, 2, 3, 4, 5];
console.log("Sum:", _.sum(numbers));
```

🔒 Security Tip: Never commit your `.env` file to version control. Always use `.gitignore` to exclude it.

### 3. Deploying npm packages to Artifactory

Now, let's deploy our package to Artifactory.

1. Set up your Artifactory credentials:

```bash
npm config set @your-scope:registry https://your-artifactory-url/api/npm/npm-local/
npm login --registry=https://your-artifactory-url/api/npm/npm-local/
```

Replace `@your-scope` with your organization's npm scope and use the Artifactory URL provided to you.

2. Modify your `package.json` to include the scope:

```json
{
  "name": "@your-scope/my-node-project",
  ...
}
```

3. Publish your package:

```bash
npm publish
```

📝 Note: Ensure you have the necessary permissions in Artifactory to publish packages.

### 4. Using npm scopes for organization-level packages

npm scopes allow you to group related packages together and control access to them.

1. Create a new scoped package:

```bash
mkdir @your-scope/util
cd @your-scope/util
npm init -y
```

2. Modify the `package.json`:

```json
{
  "name": "@your-scope/util",
  "version": "1.0.0",
  "description": "Utility functions for our organization",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "publishConfig": {
    "registry": "https://your-artifactory-url/api/npm/npm-local/"
  }
}
```

3. Create an `index.js` file with some utility functions:

```javascript
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

module.exports = { add, subtract };
```

4. Publish the scoped package:

```bash
npm publish
```

5. Use the scoped package in your main project:

```bash
cd ../..
npm install @your-scope/util
```

6. Modify your main `index.js` to use the scoped package:

```javascript
require('dotenv').config();
const _ = require('lodash');
const util = require('@your-scope/util');

console.log("Artifactory Email:", process.env.ARTIFACTORY_EMAIL);

const numbers = [1, 2, 3, 4, 5];
console.log("Sum:", _.sum(numbers));

console.log("Add:", util.add(5, 3));
console.log("Subtract:", util.subtract(10, 4));
```

🎉 Congratulations! You've completed Unit 2 of the Build & Release Management Lab. You've worked with Artifactory, managed secrets using environment variables, deployed packages to Artifactory, and used npm scopes for organization-level packages.

### 📌 Key Takeaways
- Use `publishConfig` in `package.json` to specify the Artifactory registry.
- Environment variables and `.env` files help manage secrets securely.
- npm scopes (`@your-scope`) organize and control access to packages.
- Artifactory acts as a private npm registry for your organization's packages.

In the next unit, we'll focus on testing and code quality using Jest, ESLint, and Prettier.
