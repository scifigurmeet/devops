# Practical Assignment: Dependency Management in Node.js

## Objective
Create a simple Node.js project and manage its dependencies using npm.

## Time
15-20 minutes

## Steps

1. Initialize a new Node.js project:
   - Open your terminal
   - Create a new directory for your project and navigate into it
   - Run `npm init -y` to create a default `package.json` file

2. Install dependencies:
   - Install Express as a production dependency: `npm install express`
   - Install Jest as a development dependency: `npm install --save-dev jest`

3. Create a simple Express server:
   - Create a file named `app.js`
   - Write a basic Express server that responds with "Hello, World!" on the root route

4. Create a simple test:
   - Create a file named `app.test.js`
   - Write a basic test for your Express server using Jest

5. Update `package.json`:
   - Add a "start" script to run your server
   - Add a "test" script to run Jest

6. Examine dependencies:
   - Look at your `package.json` file
   - Identify direct dependencies vs transitive dependencies
   - Run `npm list` to see the full dependency tree

7. (Optional) If time permits:
   - Try updating one of your dependencies to a newer version
   - Observe how this affects your dependency tree

## Submission
Provide screenshots of:
1. Your final `package.json` file
2. The output of `npm list`
3. Your `app.js` and `app.test.js` files

Include a brief explanation (2-3 sentences) of what you learned about dependency management from this exercise.
