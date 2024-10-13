# 🚀 Git and GitHub Desktop: Building Your First Website

### 📚 Introduction
Welcome, future DevOps engineers! This guide will take you through the basics of version control using Git and GitHub Desktop. You'll build a simple website while learning these essential tools.

### 🛠️ Prerequisites
- A Windows PC
- Git installed (Download from: https://git-scm.com/download/win)
- GitHub Desktop installed (Download from: https://desktop.github.com/)
- Visual Studio Code (or your preferred text editor)

### 🌟 Part 1: Understanding Version Control and Git (20 minutes)

#### 1.1 What is Version Control?
Version control is like a time machine for your code. It allows you to:
- Track changes over time
- Collaborate with others
- Experiment without fear

#### 1.2 What is Git?
Git is a distributed version control system, invented by Linus Torvalds (the creator of Linux) in 2005.

> 💡 **Fun Fact:** Git was named by Linus Torvalds as a play on the British slang "git," which means an unpleasant person. Torvalds said, "I'm an egotistical bastard, and I name all my projects after myself. First 'Linux', now 'Git'."

#### 1.3 Key Concepts
- **Repository**: Your project's home, containing all files and history.
- **Commit**: A snapshot of your project at a specific point in time.
- **Branch**: A parallel version of your repository for feature development.
- **Merge**: The process of combining different branches.

### 🏗️ Part 2: Setting Up Git on Windows (15 minutes)

#### 2.1 Configuring Git
Open Command Prompt and run:

```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 2.2 Verifying the Configuration
Check your setup:

```
git config --list
```

> 💡 **Pro Tip:** Use `git config --global core.autocrlf true` on Windows to handle line endings automatically.

### 🖥️ Part 3: Building Your First Website with Git (45 minutes)

#### 3.1 Creating a New Repository
1. Open Command Prompt
2. Navigate to your desired location:
   ```
   cd C:\Users\YourUsername\Documents
   ```
3. Create and enter a new directory:
   ```
   mkdir my-first-website
   cd my-first-website
   ```
4. Initialize the repository:
   ```
   git init
   ```

#### 3.2 Creating Your First HTML Page
1. Open Visual Studio Code
2. Create a new file named `index.html`
3. Add the following content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My First Git Website</title>
</head>
<body>
    <h1>Welcome to My First Git Website!</h1>
    <p>I'm learning Git and it's awesome!</p>
</body>
</html>
```

#### 3.3 Tracking Changes with Git
1. Check the status of your repository:
   ```
   git status
   ```
2. Add your new file to the staging area:
   ```
   git add index.html
   ```
3. Commit your changes:
   ```
   git commit -m "Add initial HTML page"
   ```

> 💡 **Fun Fact:** The first commit in a Git repository is often called the "root commit" or "initial commit".

#### 3.4 Making Changes and Creating New Commits
1. Add a CSS file named `styles.css`:

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
}
h1 {
    color: #0366d6;
}
```

2. Update `index.html` to link the CSS file:

```html
<head>
    <!-- ... other head content ... -->
    <link rel="stylesheet" href="styles.css">
</head>
```

3. Stage and commit your changes:
   ```
   git add styles.css index.html
   git commit -m "Add CSS styling"
   ```

### 🌿 Part 4: Branching and Merging (30 minutes)

1. Create a new branch for adding a navigation menu:
   ```
   git branch add-nav-menu
   git checkout add-nav-menu
   ```

2. Update `index.html` to add a navigation menu:

```html
<body>
    <nav>
        <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
    <!-- ... existing content ... -->
</body>
```

3. Commit your changes:
   ```
   git add index.html
   git commit -m "Add navigation menu"
   ```

4. Switch back to the main branch and merge:
   ```
   git checkout main
   git merge add-nav-menu
   ```

### 🖱️ Part 5: Using GitHub Desktop (30 minutes)

1. Open GitHub Desktop
2. Add your existing repository:
   - File > Add Local Repository
   - Choose your `my-first-website` folder

3. Commit changes:
   - Make a small change to your HTML file
   - Fill in the commit message
   - Click "Commit to main"

4. Creating branches:
   - Click on "Current Branch"
   - Choose "New Branch"
   - Name it "add-footer"

5. Publishing to GitHub:
   - Click "Publish repository"
   - Choose a name and description
   - Click "Publish Repository"

> 💡 **Pro Tip:** GitHub Desktop automatically creates a .gitignore file for you when publishing a repository!

### 🎨 Part 6: Enhancing Your Website (20 minutes)

1. Add an `images` folder and include a logo image
2. Update your HTML to include the image and a footer
3. Modify your CSS to style the new elements
4. Use GitHub Desktop to commit and push your changes

### 🏁 Conclusion

Congratulations! You've built your first website using Git and GitHub Desktop. You've learned:
- Basic Git commands
- Branching and merging
- Using GitHub Desktop
- Building and versioning a simple website

Continue practicing and exploring Git's features. Remember, version control is a crucial skill for any DevOps engineer!

### 📚 Additional Resources
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Desktop Documentation](https://docs.github.com/en/desktop)
- [Interactive Git Learning](https://learngitbranching.js.org/)
