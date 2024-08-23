# Practical Assignment: Automating the Software Delivery Pipeline

## Objective
Create a simple automated pipeline for a web application that demonstrates continuous integration and deployment, along with some basic system automation tasks.

## Time
15-20 minutes

## Prerequisites
- GitHub account
- Basic knowledge of Git
- Basic understanding of JavaScript/Node.js

## Steps

1. Create a simple Express.js application:
   - Initialize a new Node.js project
   - Install Express: `npm install express`
   - Create an `app.js` file with a basic Express server
   - Add a simple test using Jest

2. Set up a GitHub repository:
   - Create a new repository on GitHub
   - Push your local project to the repository

3. Create a GitHub Actions workflow:
   - In your repository, create a `.github/workflows` directory
   - Create a file named `ci-cd.yml` in this directory

4. Define the CI/CD pipeline in `ci-cd.yml`:
   ```yaml
   name: CI/CD Pipeline

   on: [push]

   jobs:
     build-test-deploy:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v2
       - name: Use Node.js
         uses: actions/setup-node@v2
         with:
           node-version: '14'
       - run: npm ci
       - run: npm test
       - name: Deploy to Heroku
         if: success()
         uses: akhileshns/heroku-deploy@v3.12.12
         with:
           heroku_api_key: ${{secrets.HEROKU_API_KEY}}
           heroku_app_name: "your-app-name"
           heroku_email: "your-email@example.com"
   ```

5. Add some automation scripts:
   - Create a `scripts` directory in your project
   - Add a script for archiving logs:
     ```javascript
     // archive-logs.js
     const fs = require('fs');
     const path = require('path');

     const logsDir = path.join(__dirname, 'logs');
     const archiveDir = path.join(__dirname, 'archives');

     if (!fs.existsSync(archiveDir)) {
       fs.mkdirSync(archiveDir);
     }

     fs.readdirSync(logsDir).forEach(file => {
       const oldPath = path.join(logsDir, file);
       const newPath = path.join(archiveDir, file);
       fs.renameSync(oldPath, newPath);
     });

     console.log('Logs archived successfully');
     ```

   - Add a script for checking disk usage:
     ```javascript
     // check-disk-usage.js
     const disk = require('diskusage');

     disk.check('/', function(err, info) {
       if (err) {
         console.log(err);
       } else {
         const usedPercentage = (info.total - info.free) / info.total * 100;
         console.log(`Disk usage: ${usedPercentage.toFixed(2)}%`);
         if (usedPercentage > 90) {
           console.log('Warning: Disk usage is above 90%!');
         }
       }
     });
     ```

6. Update `package.json` to include these scripts:
   ```json
   "scripts": {
     "start": "node app.js",
     "test": "jest",
     "archive-logs": "node scripts/archive-logs.js",
     "check-disk": "node scripts/check-disk-usage.js"
   }
   ```

7. Commit and push your changes to GitHub

## Submission
Provide:
1. The link to your GitHub repository
2. A screenshot of your GitHub Actions workflow runs
3. The content of your `ci-cd.yml` file
4. The content of your automation scripts

Include a brief explanation (3-4 sentences) of how this pipeline demonstrates the concepts of Continuous Integration, Continuous Deployment, and the benefits of automation in the software delivery process.
