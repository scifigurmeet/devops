# Git and GitHub Desktop Class Test (with Answers)

**Time Allowed: 1 Hour**
**Total Questions: 20**

**Instructions:**
- This is a practical test. You will need access to a computer with Git and GitHub Desktop installed.
- Read each question carefully and follow the instructions.
- Write your answers, including any necessary Git commands or steps, in a text file or document.
- For questions requiring practical actions, perform the tasks and note down the steps you took.

---

1. Initialize a new Git repository named "devops_test" in your documents folder. Write the commands you used to do this.

   **Answer:**
   ```
   cd C:\Users\YourUsername\Documents
   mkdir devops_test
   cd devops_test
   git init
   ```

2. Create a new file named "index.html" in the "devops_test" repository with the following content:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>DevOps Test</title>
   </head>
   <body>
       <h1>Welcome to DevOps</h1>
   </body>
   </html>
   ```
   Stage and commit this file. Write the Git commands you used.

   **Answer:**
   ```
   echo "<!DOCTYPE html><html><head><title>DevOps Test</title></head><body><h1>Welcome to DevOps</h1></body></html>" > index.html
   git add index.html
   git commit -m "Add initial index.html file"
   ```

3. Check the status of your repository and write down what Git reports.

   **Answer:**
   ```
   git status
   ```
   The output should be similar to:
   ```
   On branch main
   nothing to commit, working tree clean
   ```

4. Create a new branch named "feature-navbar". Switch to this branch and add a navigation bar to your HTML file. Commit your changes. Write down all the commands you used and the HTML code you added.

   **Answer:**
   ```
   git branch feature-navbar
   git checkout feature-navbar
   ```
   Edit index.html to add:
   ```html
   <nav>
       <ul>
           <li><a href="#home">Home</a></li>
           <li><a href="#about">About</a></li>
           <li><a href="#contact">Contact</a></li>
       </ul>
   </nav>
   ```
   Then:
   ```
   git add index.html
   git commit -m "Add navigation bar"
   ```

5. Switch back to the main branch. Create a new file named "styles.css" and add some basic styling for your HTML. Commit this change. Write the commands you used and the CSS code you wrote.

   **Answer:**
   ```
   git checkout main
   echo "body { font-family: Arial, sans-serif; } nav { background-color: #333; }" > styles.css
   git add styles.css
   git commit -m "Add basic CSS styles"
   ```

6. Merge the "feature-navbar" branch into the main branch. If there are any conflicts, resolve them. Describe the steps you took and any conflicts you encountered.

   **Answer:**
   ```
   git merge feature-navbar
   ```
   There should be no conflicts as the changes were made to different files or different parts of the same file.

7. Use GitHub Desktop to publish your "devops_test" repository to GitHub. Describe the steps you took in GitHub Desktop to do this.

   **Answer:**
   1. Open GitHub Desktop
   2. Click on "File" > "Add Local Repository"
   3. Browse and select the "devops_test" folder
   4. Click "Publish repository" in the top right
   5. Set repository name, description, and choose to keep it private or public
   6. Click "Publish Repository"

8. Clone your GitHub repository to a different location on your computer using the command line. Write the command you used.

   **Answer:**
   ```
   git clone https://github.com/YourUsername/devops_test.git C:\Users\YourUsername\Desktop\devops_test_clone
   ```

9. In GitHub Desktop, create a new branch named "add-footer". Add a footer to your HTML file and commit this change. Push this branch to GitHub. Describe the steps you took in GitHub Desktop.

   **Answer:**
   1. In GitHub Desktop, click on "Current Branch"
   2. Click "New Branch" and name it "add-footer"
   3. Edit index.html to add a footer
   4. In GitHub Desktop, write a commit message and click "Commit to add-footer"
   5. Click "Publish branch" to push to GitHub

10. Using the command line, pull the latest changes from the remote repository. Write the command you used.

    **Answer:**
    ```
    git pull origin main
    ```

11. Create a new file named "script.js" in your repository. Add a simple JavaScript function that changes the text color of the h1 element when clicked. Stage and commit this file using Git commands. Write the commands you used and the JavaScript code you wrote.

    **Answer:**
    ```
    echo "document.querySelector('h1').addEventListener('click', function() { this.style.color = 'blue'; });" > script.js
    git add script.js
    git commit -m "Add JavaScript to change h1 color on click"
    ```

12. Use Git to view the commit history of your repository. Write the command you used and the output you see.

    **Answer:**
    ```
    git log
    ```
    The output will show a list of commits with their hash, author, date, and message.

13. In GitHub Desktop, create a pull request to merge the "add-footer" branch into the main branch. Describe the steps you took to do this.

    **Answer:**
    1. In GitHub Desktop, ensure you're on the "add-footer" branch
    2. Click "Create Pull Request"
    3. GitHub website opens. Fill in the pull request title and description
    4. Click "Create pull request"

14. Using the command line, create a new branch named "update-readme". Create a README.md file with a brief description of your project. Commit this change and push the branch to GitHub. Write all the commands you used.

    **Answer:**
    ```
    git checkout -b update-readme
    echo "# DevOps Test Project" > README.md
    echo "This is a sample project for learning Git and GitHub." >> README.md
    git add README.md
    git commit -m "Add README file"
    git push -u origin update-readme
    ```

15. In GitHub Desktop, fetch the latest changes from GitHub. Then, checkout the "update-readme" branch. Describe the steps you took in GitHub Desktop.

    **Answer:**
    1. In GitHub Desktop, click "Fetch origin" to get the latest changes
    2. Click on "Current Branch"
    3. In the list of branches, select "update-readme"
    4. Click "Checkout"

16. Using Git commands, add a .gitignore file to your repository that ignores all .log files and the "node_modules" directory. Write the commands you used and the content of your .gitignore file.

    **Answer:**
    ```
    echo "*.log" > .gitignore
    echo "node_modules/" >> .gitignore
    git add .gitignore
    git commit -m "Add .gitignore file"
    ```

17. Simulate a merge conflict: In the main branch, modify the h1 text in index.html. In the "update-readme" branch, also modify the h1 text differently. Try to merge "update-readme" into main. Resolve the conflict. Describe all steps and commands you used, including how you resolved the conflict.

    **Answer:**
    ```
    git checkout main
    # Edit index.html, change h1 to "Welcome to Main DevOps"
    git commit -am "Update h1 in main"
    
    git checkout update-readme
    # Edit index.html, change h1 to "Welcome to DevOps README"
    git commit -am "Update h1 in readme branch"
    
    git checkout main
    git merge update-readme
    ```
    Git will report a conflict. Edit index.html to resolve the conflict, then:
    ```
    git add index.html
    git commit -m "Resolve merge conflict in h1"
    ```

18. Use Git to discard all uncommitted changes in your working directory. Write the command you used.

    **Answer:**
    ```
    git reset --hard
    ```

19. Tag your latest commit in the main branch as "v1.0". Push this tag to GitHub. Write the Git commands you used.

    **Answer:**
    ```
    git checkout main
    git tag v1.0
    git push origin v1.0
    ```

20. Use GitHub Desktop to clone a public repository of your choice from GitHub. Describe the steps you took in GitHub Desktop.

    **Answer:**
    1. Open GitHub Desktop
    2. Click on "File" > "Clone Repository"
    3. Go to the "URL" tab
    4. Paste the URL of the public repository you want to clone
    5. Choose the local path where you want to clone the repository
    6. Click "Clone"

---

**Submission:**
- Save your answers, including all commands used and code written, in a text file named "GitTest_YourName.txt".
- Push this file to a new branch named "test-submission" in your "devops_test" repository.
- Create a pull request for this branch on GitHub.

Good luck!
