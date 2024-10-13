# Unit 4: Build Tools and Development Environment
## Webpack for Bundling and Optimization, VS Code for npm Scripts and Debugging

**Instructions:**
- This practical is designed for Windows PC users, but most commands are OS-independent.
- Use Visual Studio Code (VS Code) as your code editor.
- Ensure you have Node.js and npm (Node Package Manager) installed on your system.

---

1. What is the command to create a new Node.js project and generate a `package.json` file?

   **Answer:**
   ```
   npm init -y
   ```
   This command creates a new `package.json` file with default values. The `-y` flag automatically answers "yes" to all prompts.

2. How do you install Webpack and its CLI as dev dependencies in your project?

   **Answer:**
   ```
   npm install webpack webpack-cli --save-dev
   ```
   This command installs Webpack and the Webpack CLI as development dependencies and adds them to your `package.json` file.

3. Create a basic Webpack configuration file (`webpack.config.js`) that specifies an entry point of `./src/index.js` and an output file of `./dist/bundle.js`. Write the content of this file.

   **Answer:**
   Create a file named `webpack.config.js` in your project root with the following content:
   ```javascript
   const path = require('path');

   module.exports = {
     entry: './src/index.js',
     output: {
       filename: 'bundle.js',
       path: path.resolve(__dirname, 'dist'),
     },
   };
   ```

4. How do you run Webpack using npm scripts? Add a build script to your `package.json` and show the updated script section.

   **Answer:**
   Edit your `package.json` file and add the following to the "scripts" section:
   ```json
   "scripts": {
     "build": "webpack --mode production"
   }
   ```
   You can now run Webpack by using the command `npm run build`.

5. Create a simple `index.js` file in the `src` directory that logs a message to the console. Then, create an `index.html` file in the `dist` directory that includes the bundled script. Show the content of both files.

   **Answer:**
   `src/index.js`:
   ```javascript
   console.log('Hello from Webpack!');
   ```

   `dist/index.html`:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Webpack Demo</title>
   </head>
   <body>
       <h1>Webpack Demo</h1>
       <script src="bundle.js"></script>
   </body>
   </html>
   ```

6. How do you install and configure the `html-webpack-plugin` to automatically generate the `index.html` file? Show the installation command and the updated `webpack.config.js`.

   **Answer:**
   Install the plugin:
   ```
   npm install html-webpack-plugin --save-dev
   ```

   Update `webpack.config.js`:
   ```javascript
   const path = require('path');
   const HtmlWebpackPlugin = require('html-webpack-plugin');

   module.exports = {
     entry: './src/index.js',
     output: {
       filename: 'bundle.js',
       path: path.resolve(__dirname, 'dist'),
     },
     plugins: [
       new HtmlWebpackPlugin({
         title: 'Webpack Demo',
       }),
     ],
   };
   ```

7. How do you set up Webpack Dev Server for a development environment with hot reloading? Show the installation command and the necessary configuration changes.

   **Answer:**
   Install Webpack Dev Server:
   ```
   npm install webpack-dev-server --save-dev
   ```

   Update `webpack.config.js`:
   ```javascript
   const path = require('path');
   const HtmlWebpackPlugin = require('html-webpack-plugin');

   module.exports = {
     entry: './src/index.js',
     output: {
       filename: 'bundle.js',
       path: path.resolve(__dirname, 'dist'),
     },
     plugins: [
       new HtmlWebpackPlugin({
         title: 'Webpack Demo',
       }),
     ],
     devServer: {
       contentBase: './dist',
       hot: true,
     },
   };
   ```

   Add a new script to `package.json`:
   ```json
   "scripts": {
     "build": "webpack --mode production",
     "start": "webpack serve --mode development"
   }
   ```

8. How do you configure Webpack to use Babel for transpiling modern JavaScript? Show the installation commands and the necessary configuration changes.

   **Answer:**
   Install Babel and related packages:
   ```
   npm install @babel/core @babel/preset-env babel-loader --save-dev
   ```

   Update `webpack.config.js`:
   ```javascript
   const path = require('path');
   const HtmlWebpackPlugin = require('html-webpack-plugin');

   module.exports = {
     entry: './src/index.js',
     output: {
       filename: 'bundle.js',
       path: path.resolve(__dirname, 'dist'),
     },
     module: {
       rules: [
         {
           test: /\.js$/,
           exclude: /node_modules/,
           use: {
             loader: 'babel-loader',
             options: {
               presets: ['@babel/preset-env']
             }
           }
         }
       ]
     },
     plugins: [
       new HtmlWebpackPlugin({
         title: 'Webpack Demo',
       }),
     ],
     devServer: {
       contentBase: './dist',
       hot: true,
     },
   };
   ```

9. How do you configure VS Code to run npm scripts from the editor? Show the steps to add a npm script to the VS Code task runner.

   **Answer:**
   1. Open the Command Palette (Ctrl+Shift+P)
   2. Type "Tasks: Configure Task" and select it
   3. Choose "npm: run script"
   4. Select the script you want to run (e.g., "build" or "start")

   This will create a `.vscode/tasks.json` file. To run the task, use the Command Palette and select "Tasks: Run Task", then choose the npm script you want to run.

10. How do you set up a launch configuration in VS Code to debug your Webpack-bundled JavaScript? Show the content of the `launch.json` file.

    **Answer:**
    Create a file named `launch.json` in the `.vscode` directory with the following content:
    ```json
    {
      "version": "0.2.0",
      "configurations": [
        {
          "type": "chrome",
          "request": "launch",
          "name": "Debug Webpack App",
          "url": "http://localhost:8080",
          "webRoot": "${workspaceFolder}/dist",
          "sourceMaps": true,
          "sourceMapPathOverrides": {
            "webpack:///./src/*": "${webRoot}/*"
          }
        }
      ]
    }
    ```
    This configuration allows you to debug your application in Chrome. Make sure your Webpack Dev Server is running before starting the debug session.

11. How do you optimize your Webpack bundle for production? Show the necessary configuration changes and explain their purpose.

    **Answer:**
    Update `webpack.config.js`:
    ```javascript
    const path = require('path');
    const HtmlWebpackPlugin = require('html-webpack-plugin');
    const TerserPlugin = require('terser-webpack-plugin');

    module.exports = {
      entry: './src/index.js',
      output: {
        filename: 'bundle.[contenthash].js',
        path: path.resolve(__dirname, 'dist'),
        clean: true,
      },
      optimization: {
        minimize: true,
        minimizer: [new TerserPlugin()],
        splitChunks: {
          chunks: 'all',
        },
      },
      plugins: [
        new HtmlWebpackPlugin({
          title: 'Webpack Demo',
        }),
      ],
    };
    ```
    This configuration:
    - Uses content hashing for cache busting
    - Cleans the output directory before each build
    - Minimizes the bundle using TerserPlugin
    - Splits the code into chunks for better caching

12. How do you analyze the size of your Webpack bundle? Show the installation command and configuration for the Webpack Bundle Analyzer plugin.

    **Answer:**
    Install the plugin:
    ```
    npm install webpack-bundle-analyzer --save-dev
    ```

    Update `webpack.config.js`:
    ```javascript
    const path = require('path');
    const HtmlWebpackPlugin = require('html-webpack-plugin');
    const TerserPlugin = require('terser-webpack-plugin');
    const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

    module.exports = {
      // ... other configurations ...
      plugins: [
        new HtmlWebpackPlugin({
          title: 'Webpack Demo',
        }),
        new BundleAnalyzerPlugin(),
      ],
    };
    ```
    Run your build command, and it will generate an interactive treemap visualization of your bundle.

---

This practical guide covers the basics of setting up Webpack for bundling and optimization, as well as using VS Code for running npm scripts and debugging. Remember to practice these concepts regularly to become proficient in using these tools in your development workflow.
