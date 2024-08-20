# CSV 204 - Build & Release Management Lab
## Unit 1: Node.js and npm Fundamentals

### 🎯 Objectives
By the end of this practical, you will be able to:
- Set up Node.js and npm
- Understand the structure of package.json
- Create a project using npm
- Understand package-lock.json files
- Use private npm registries (e.g., Verdaccio) in npm configuration

### 📚 Prerequisites
- Windows 11 PC with Node.js installed

### 1. Setting up Node.js and npm

Node.js should already be installed on your system. Let's verify the installation and ensure npm is set up correctly.

1. Open Command Prompt or PowerShell
2. Run the following commands:

```bash
node --version
npm --version
```

You should see version numbers for both Node.js and npm. If not, please seek assistance to install Node.js properly.

### 2. Understanding package.json structure

The `package.json` file is crucial in Node.js projects. Let's create one and examine its structure.

1. Create a new directory for your project:

```bash
mkdir my-node-project
cd my-node-project
```

2. Initialize a new Node.js project:

```bash
npm init -y
```

3. Open the created `package.json` file in a text editor. It should look similar to this:

```json
{
  "name": "my-node-project",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

📝 Note: Each field in `package.json` has a specific purpose:
- `name`: The name of your project
- `version`: The current version of your project
- `description`: A brief description of your project
- `main`: The entry point of your application
- `scripts`: Custom scripts that can be run with `npm run`
- `keywords`: Array of keywords to describe your project
- `author`: The author of the project
- `license`: The license under which the project is distributed

### 3. Creating a project using npm

Let's create a simple Node.js project and add a dependency.

1. Create a new file named `index.js` in your project directory:

```javascript
console.log("Hello, Node.js!");
```

2. Install a popular package, like `lodash`:

```bash
npm install lodash
```

3. Modify `index.js` to use lodash:

```javascript
const _ = require('lodash');

const numbers = [1, 2, 3, 4, 5];
console.log(_.sum(numbers));
```

4. Run your project:

```bash
node index.js
```

You should see the sum of the numbers printed.

### 4. Understanding package-lock.json files

After installing a package, you'll notice a `package-lock.json` file in your project directory.

📝 Note: `package-lock.json` ensures that the same dependencies are installed across different environments. It locks the versions of installed packages and their dependencies.

Open `package-lock.json` and observe its structure. You'll see detailed information about each installed package and its dependencies.

### 5. Using private npm registries (e.g., Verdaccio) in npm configuration

For this part, we'll simulate using a private registry with Verdaccio.

1. Install Verdaccio globally:

```bash
npm install -g verdaccio
```

2. Start Verdaccio:

```bash
verdaccio
```

3. In a new terminal, configure npm to use Verdaccio as a registry:

```bash
npm set registry http://localhost:4873/
```

4. Create a new user on Verdaccio:

```bash
npm adduser --registry http://localhost:4873/
```

Follow the prompts to create a username and password.

5. Publish your package to Verdaccio:

```bash
npm publish --registry http://localhost:4873/
```

6. To reset npm to use the default registry:

```bash
npm config delete registry
```

🎉 Congratulations! You've completed Unit 1 of the Build & Release Management Lab. You've set up Node.js and npm, created a project, understood package.json and package-lock.json, and worked with a private npm registry.

### 📌 Key Takeaways
- `package.json` is the heart of a Node.js project, containing metadata and dependencies.
- `npm init` initializes a new Node.js project.
- `npm install` adds dependencies to your project.
- `package-lock.json` ensures consistency in installed packages across environments.
- Private npm registries like Verdaccio can be used for organization-specific packages.

In the next unit, we'll dive deeper into package management and dependencies.
