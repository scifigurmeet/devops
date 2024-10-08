# CSV 204 - Build & Release Management Lab
## Unit 4: Build Tools and Development Environment

### Introduction to Webpack

#### What is Webpack?

Webpack is a powerful and popular module bundler for JavaScript applications. It takes your project's assets (JavaScript files, CSS, images, etc.) and their dependencies, then processes and bundles them into a smaller set of files that can be efficiently served to the browser.

Key features of Webpack include:

1. **Module Bundling**: Combines many JavaScript files into a single file.
2. **Code Splitting**: Splits your code into various bundles which can be loaded on demand.
3. **Loaders**: Transforms files as they're imported, allowing you to preprocess files.
4. **Plugins**: Performs a wider range of tasks like bundle optimization, asset management, and injection of environment variables.

#### Why use Webpack?

In modern web development, we often work with many JavaScript files and dependencies. Without a tool like Webpack:

1. We'd have to manually manage the order of script tags in HTML.
2. We'd face potential naming conflicts in the global scope.
3. We'd have to manually handle dependencies between files.
4. Our page load times might be slower due to many HTTP requests for each script.

Webpack solves these problems by bundling all our files together in a smart way, while also providing an environment where we can use modern JavaScript features, optimize our code, and much more.

#### Webpack Example

Let's look at a simple example to illustrate how Webpack works:

Suppose we have two JavaScript files:

`greet.js`:
```javascript
export function greet(name) {
    return `Hello, ${name}!`;
}
```

`index.js`:
```javascript
import { greet } from './greet';

console.log(greet('Webpack'));
```

Without Webpack, we'd need to include both these files in our HTML, ensuring `greet.js` comes before `index.js`. We'd also need to use a module system supported by the browser.

With Webpack, we can bundle these files together. Here's a basic `webpack.config.js`:

```javascript
const path = require('path');

module.exports = {
  entry: './index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
};
```

After running Webpack, it will create a `bundle.js` file in a `dist` directory. This file will contain all the necessary code from both `index.js` and `greet.js`, properly bundled and ready to use in the browser with a single script tag.

Now that we understand the basics of Webpack, let's dive into our practical lab exercises.

### Objective
In this lab, you will learn how to use Webpack for bundling and optimizing JavaScript applications, and how to leverage Visual Studio Code (VS Code) for running npm scripts and debugging Node.js applications.

### Prerequisites
- Node.js and npm installed on your system
- Visual Studio Code installed
- Basic knowledge of JavaScript and Node.js

### Part 1: Setting up a Webpack Project

1. Create a new directory for your project and navigate to it:
   ```
   mkdir webpack-demo
   cd webpack-demo
   ```

2. Initialize a new Node.js project:
   ```
   npm init -y
   ```

3. Install Webpack and Webpack CLI as dev dependencies:
   ```
   npm install webpack webpack-cli --save-dev
   ```

4. Create a `src` directory and add an `index.js` file:
   ```
   mkdir src
   echo "console.log('Hello, Webpack!');" > src/index.js
   ```

5. Create a `webpack.config.js` file in the root of your project:
   ```javascript
   const path = require('path');

   module.exports = {
     entry: './src/index.js',
     output: {
       filename: 'main.js',
       path: path.resolve(__dirname, 'dist'),
     },
   };
   ```

6. Add a build script to your `package.json`:
   ```json
   "scripts": {
     "build": "webpack --mode production"
   }
   ```

7. Run the build script:
   ```
   npm run build
   ```

8. Verify that Webpack has created a `dist` directory with a `main.js` file.

### Part 2: Optimizing with Webpack

1. Install `lodash` as a dependency:
   ```
   npm install lodash
   ```

2. Update `src/index.js` to use `lodash`:
   ```javascript
   import _ from 'lodash';

   function component() {
     const element = document.createElement('div');
     element.innerHTML = _.join(['Hello', 'Webpack'], ' ');
     return element;
   }

   document.body.appendChild(component());
   ```

3. Create an `index.html` file in the `dist` directory:
   ```html
   <!DOCTYPE html>
   <html>
     <head>
       <title>Webpack Demo</title>
     </head>
     <body>
       <script src="main.js"></script>
     </body>
   </html>
   ```

4. Install `html-webpack-plugin`:
   ```
   npm install html-webpack-plugin --save-dev
   ```

5. Update `webpack.config.js`:
   ```javascript
   const path = require('path');
   const HtmlWebpackPlugin = require('html-webpack-plugin');

   module.exports = {
     entry: './src/index.js',
     output: {
       filename: '[name].[contenthash].js',
       path: path.resolve(__dirname, 'dist'),
       clean: true,
     },
     plugins: [
       new HtmlWebpackPlugin({
         title: 'Webpack Demo',
       }),
     ],
     optimization: {
       moduleIds: 'deterministic',
       runtimeChunk: 'single',
       splitChunks: {
         cacheGroups: {
           vendor: {
             test: /[\\/]node_modules[\\/]/,
             name: 'vendors',
             chunks: 'all',
           },
         },
       },
     },
   };
   ```

6. Run the build script again and observe the optimized output in the `dist` directory.

### Part 3: Using VS Code for npm Scripts and Debugging

1. Open your project in VS Code:
   ```
   code .
   ```

2. Create a `.vscode` directory in your project root and add a `launch.json` file:
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "type": "node",
         "request": "launch",
         "name": "Debug Webpack Build",
         "program": "${workspaceFolder}/node_modules/webpack/bin/webpack.js",
         "args": ["--mode", "development"],
         "cwd": "${workspaceFolder}",
         "console": "integratedTerminal"
       }
     ]
   }
   ```

3. To run npm scripts, open the VS Code Command Palette (Ctrl+Shift+P or Cmd+Shift+P) and type "Tasks: Run Task". Select "npm: build" to run your Webpack build script.

4. To debug your Webpack build, set a breakpoint in your `src/index.js` file and press F5 or use the Run and Debug view to start debugging.

### Exercises

1. Add a CSS loader to your Webpack configuration and create a simple stylesheet for your application.
2. Implement code splitting in your application by creating multiple entry points.
3. Use the VS Code debugger to step through your Webpack build process and understand how it works.
4. Create a development server using `webpack-dev-server` and configure it in VS Code for easy debugging.

### Conclusion

In this lab, you've learned about Webpack, its importance in modern web development, and how to set up a Webpack project. You've also learned how to optimize it for production and use VS Code for running npm scripts and debugging. These skills are essential for modern JavaScript development and will be valuable in your DevOps career.

Remember to experiment with different Webpack plugins and loaders to further optimize your builds and improve your development workflow.
