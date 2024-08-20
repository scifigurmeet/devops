# CSV 203 - Build & Release Management
## Unit 1: Beginner's Practical Guide

### Introduction

Welcome to the practical guide for Unit 1 of CSV 203 - Build & Release Management. This guide is designed for absolute beginners in DevOps. We'll cover the basics of modern build and release management through simple, hands-on exercises. Each exercise includes detailed steps and explanations to help you understand the concepts.

### Prerequisites

- A Windows 11 PC with Docker Desktop installed
- A GitHub account (free)
- Visual Studio Code (or any text editor you're comfortable with)

### Exercise 1: Introduction to Version Control with Git and GitHub

**Objective:** Understand the basics of version control and set up a GitHub repository.

**Steps:**

1. **Create a GitHub Account**
   - Go to [GitHub](https://github.com) and sign up for a free account if you haven't already.

2. **Install Git**
   - Download Git from [https://git-scm.com/downloads](https://git-scm.com/downloads)
   - Install Git, accepting the default options during installation.

3. **Configure Git**
   - Open Command Prompt and run these commands, replacing with your information:
     ```
     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
     ```

4. **Create a New Repository on GitHub**
   - Log in to GitHub
   - Click the '+' icon in the top-right corner and select "New repository"
   - Name your repository "hello-devops"
   - Choose "Public" and initialize with a README
   - Click "Create repository"

5. **Clone the Repository**
   - On your repository page, click the "Code" button and copy the HTTPS URL
   - Open Command Prompt, navigate to where you want to store your project, and run:
     ```
     git clone https://github.com/your-username/hello-devops.git
     ```
   - Navigate into the cloned repository:
     ```
     cd hello-devops
     ```

6. **Make Changes and Commit**
   - Open the README.md file in a text editor and add a line: "My first DevOps project"
   - Save the file
   - In Command Prompt, run:
     ```
     git add README.md
     git commit -m "Update README with project description"
     git push origin main
     ```

7. **View Changes on GitHub**
   - Refresh your repository page on GitHub to see the updated README.

**Explanation:** This exercise introduces you to version control, which is fundamental in modern software development and DevOps practices. Git allows you to track changes in your code, while GitHub provides a platform for storing and collaborating on your projects.

### Exercise 2: Creating a Simple Web Application

**Objective:** Create a basic web application that we'll use in subsequent exercises.

**Steps:**

1. **Set Up the Project**
   - In your "hello-devops" directory, create a new file named `app.py`
   - Open `app.py` in your text editor

2. **Write a Simple Flask Application**
   - Paste the following code into `app.py`:
     ```python
     from flask import Flask

     app = Flask(__name__)

     @app.route('/')
     def hello():
         return "Hello, DevOps!"

     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=5000)
     ```

3. **Create Requirements File**
   - Create a new file named `requirements.txt`
   - Add the following line to `requirements.txt`:
     ```
     Flask==2.0.1
     ```

4. **Commit and Push Changes**
   - In Command Prompt, run:
     ```
     git add app.py requirements.txt
     git commit -m "Add simple Flask application"
     git push origin main
     ```

**Explanation:** This exercise creates a very simple web application using Flask, a lightweight web framework for Python. This application will serve as the basis for our future exercises in build and deployment processes.

### Exercise 3: Introduction to Containerization with Docker

**Objective:** Learn the basics of containerization by dockerizing our Flask application.

**Steps:**

1. **Create a Dockerfile**
   - In your project directory, create a new file named `Dockerfile` (no extension)
   - Add the following content to the `Dockerfile`:
     ```dockerfile
     FROM python:3.9-slim

     WORKDIR /app

     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt

     COPY app.py .

     CMD ["python", "app.py"]
     ```

2. **Build the Docker Image**
   - Open Command Prompt in your project directory
   - Run the following command:
     ```
     docker build -t hello-devops .
     ```

3. **Run the Docker Container**
   - After the build completes, run:
     ```
     docker run -p 5000:5000 hello-devops
     ```
   - Open a web browser and go to `http://localhost:5000`. You should see "Hello, DevOps!"

4. **Stop the Container**
   - Press Ctrl+C in the Command Prompt to stop the container

5. **Commit and Push Changes**
   - Add the Dockerfile to Git:
     ```
     git add Dockerfile
     git commit -m "Add Dockerfile for containerization"
     git push origin main
     ```

**Explanation:** This exercise introduces containerization, a key concept in modern DevOps. Containers package an application with all its dependencies, ensuring it runs consistently across different environments. Docker is a popular platform for creating and managing containers.

### Exercise 4: Introduction to CI/CD with GitHub Actions

**Objective:** Set up a basic Continuous Integration pipeline using GitHub Actions.

**Steps:**

1. **Create GitHub Actions Workflow File**
   - In your local repository, create a new directory structure: `.github/workflows`
   - Inside the `workflows` directory, create a file named `ci.yml`

2. **Define the Workflow**
   - Add the following content to `ci.yml`:
     ```yaml
     name: CI

     on:
       push:
         branches: [ main ]
       pull_request:
         branches: [ main ]

     jobs:
       build:
         runs-on: ubuntu-latest
         
         steps:
         - uses: actions/checkout@v2
         
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: 3.9
         
         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
         
         - name: Run tests
           run: |
             python -m unittest discover tests
     ```

3. **Add a Simple Test**
   - Create a new directory named `tests`
   - Inside `tests`, create a file named `test_app.py`
   - Add the following content to `test_app.py`:
     ```python
     import unittest
     from app import app

     class TestApp(unittest.TestCase):
         def setUp(self):
             self.client = app.test_client()

         def test_hello(self):
             response = self.client.get('/')
             self.assertEqual(response.data.decode(), 'Hello, DevOps!')

     if __name__ == '__main__':
         unittest.main()
     ```

4. **Commit and Push Changes**
   - Add the new files to Git:
     ```
     git add .github/workflows/ci.yml tests/test_app.py
     git commit -m "Add GitHub Actions workflow and tests"
     git push origin main
     ```

5. **View the Workflow Run**
   - Go to your GitHub repository page
   - Click on the "Actions" tab to see your workflow running

**Explanation:** This exercise introduces Continuous Integration (CI), an essential DevOps practice. GitHub Actions automates the process of testing your code every time you push changes to the repository, helping catch errors early.

### Exercise 5: Basic Release Management

**Objective:** Understand the basics of release management by creating a release on GitHub.

**Steps:**

1. **Create a New Branch**
   - In your local repository, create and switch to a new branch:
     ```
     git checkout -b v1.0.0
     ```

2. **Update the Application**
   - Modify `app.py` to include a version number:
     ```python
     from flask import Flask

     app = Flask(__name__)

     @app.route('/')
     def hello():
         return "Hello, DevOps! Version 1.0.0"

     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=5000)
     ```

3. **Commit and Push Changes**
   ```
   git add app.py
   git commit -m "Bump version to 1.0.0"
   git push origin v1.0.0
   ```

4. **Create a Pull Request**
   - Go to your GitHub repository page
   - Click "Pull requests" > "New pull request"
   - Set "base: main" and "compare: v1.0.0"
   - Click "Create pull request"
   - Add a description and click "Create pull request"

5. **Merge the Pull Request**
   - Review the changes and click "Merge pull request"

6. **Create a Release**
   - On your repository page, click "Releases" > "Create a new release"
   - Set the tag version to "v1.0.0"
   - Set the release title to "Version 1.0.0"
   - Add a description of the changes
   - Click "Publish release"

**Explanation:** This exercise introduces basic release management. By creating branches, pull requests, and releases, you're following a simplified version of GitFlow, a popular branching model in DevOps. This process helps manage different versions of your software and provides a clear history of changes.

### Conclusion

Congratulations! You've completed the beginner's practical guide for Unit 1 of Build and Release Management. These exercises have introduced you to:

1. Version control with Git and GitHub
2. Creating a simple web application
3. Containerization with Docker
4. Continuous Integration with GitHub Actions
5. Basic release management

These foundational concepts are crucial in modern DevOps practices. As you progress, you'll build upon these basics to create more complex and robust build and release management processes.
