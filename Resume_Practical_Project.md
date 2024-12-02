# Complete Guide: Create and Deploy Your HTML Resume

This beginner-friendly guide will help you create a professional HTML resume and deploy it online using GitHub and Vercel.

## Table of Contents
1. [Creating Your HTML Resume](#creating-your-html-resume)
2. [Setting Up Your Development Environment](#setting-up-your-development-environment)
3. [GitHub Setup](#github-setup)
4. [Deploying with Vercel](#deploying-with-vercel)
5. [Making Updates](#making-updates)
6. [Troubleshooting](#troubleshooting)

## Creating Your HTML Resume

### Step 1: Set Up Your Project Structure

Create a new folder on your computer called `my-resume` and create the following files inside it:

```
my-resume/
├── index.html
├── styles.css
└── assets/
    └── profile-picture.jpg (optional)
```

### Step 2: HTML Resume Template

Copy this sample HTML code into your `index.html` file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Name - Resume</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>Your Full Name</h1>
            <div class="contact-info">
                <p>📧 your.email@example.com</p>
                <p>📱 (123) 456-7890</p>
                <p>📍 City, State</p>
                <p>💼 <a href="https://linkedin.com/in/yourprofile">LinkedIn</a></p>
                <p>💻 <a href="https://github.com/yourusername">GitHub</a></p>
            </div>
        </header>

        <section class="summary">
            <h2>Professional Summary</h2>
            <p>Enthusiastic and detail-oriented professional seeking opportunities in [Your Field]. 
               Skilled in [Skill 1], [Skill 2], and [Skill 3] with a passion for [Industry/Field].</p>
        </section>

        <section class="education">
            <h2>Education</h2>
            <div class="entry">
                <h3>University Name</h3>
                <p class="date">Expected Graduation: Month Year</p>
                <p>Degree Name (e.g., Bachelor of Science in Computer Science)</p>
                <p>GPA: X.XX</p>
                <ul>
                    <li>Relevant Coursework: Course 1, Course 2, Course 3</li>
                    <li>Academic Achievement or Honor</li>
                </ul>
            </div>
        </section>

        <section class="experience">
            <h2>Experience</h2>
            <div class="entry">
                <h3>Company Name</h3>
                <p class="date">Month Year - Present</p>
                <p class="title">Job Title</p>
                <ul>
                    <li>Accomplished [X] by implementing [Y] which led to [Z]</li>
                    <li>Developed and maintained [Project/System] using [Technologies]</li>
                    <li>Collaborated with team members to deliver [Result]</li>
                </ul>
            </div>
        </section>

        <section class="projects">
            <h2>Projects</h2>
            <div class="entry">
                <h3>Project Name</h3>
                <p class="date">Month Year</p>
                <ul>
                    <li>Built [Project] using [Technologies]</li>
                    <li>Implemented [Feature] which achieved [Result]</li>
                    <li>GitHub: <a href="https://github.com/yourusername/project">Project Link</a></li>
                </ul>
            </div>
        </section>

        <section class="skills">
            <h2>Skills</h2>
            <div class="skills-grid">
                <div class="skill-category">
                    <h3>Programming Languages</h3>
                    <p>Language 1, Language 2, Language 3</p>
                </div>
                <div class="skill-category">
                    <h3>Technologies & Tools</h3>
                    <p>Tool 1, Tool 2, Tool 3</p>
                </div>
                <div class="skill-category">
                    <h3>Soft Skills</h3>
                    <p>Skill 1, Skill 2, Skill 3</p>
                </div>
            </div>
        </section>
    </div>
</body>
</html>
```

### Step 3: CSS Styling

Copy this CSS code into your `styles.css` file:

```css
/* Reset default styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Global styles */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

.container {
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

/* Header styles */
header {
    text-align: center;
    margin-bottom: 30px;
}

h1 {
    font-size: 2.5em;
    color: #2c3e50;
    margin-bottom: 15px;
}

.contact-info {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 10px;
}

.contact-info p {
    margin: 5px;
}

/* Section styles */
section {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #eee;
}

h2 {
    color: #2c3e50;
    font-size: 1.5em;
    margin-bottom: 15px;
    padding-bottom: 5px;
    border-bottom: 2px solid #3498db;
}

.entry {
    margin-bottom: 20px;
}

h3 {
    color: #34495e;
    font-size: 1.2em;
    margin-bottom: 5px;
}

.date {
    color: #7f8c8d;
    font-style: italic;
    margin-bottom: 5px;
}

.title {
    font-weight: bold;
    margin-bottom: 5px;
}

/* List styles */
ul {
    list-style-position: inside;
    margin-left: 20px;
}

li {
    margin-bottom: 5px;
}

/* Skills section */
.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.skill-category {
    margin-bottom: 15px;
}

.skill-category h3 {
    font-size: 1.1em;
    color: #2c3e50;
    margin-bottom: 5px;
}

/* Link styles */
a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Responsive design */
@media (max-width: 600px) {
    .container {
        margin: 20px;
        padding: 15px;
    }

    h1 {
        font-size: 2em;
    }

    .contact-info {
        flex-direction: column;
        gap: 10px;
    }

    .skills-grid {
        grid-template-columns: 1fr;
    }
}
```

## Setting Up Your Development Environment

### Step 1: Install Required Software

1. **Install Visual Studio Code**
   - Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)
   - Download and install the version for your operating system

2. **Install Git**
   - Go to [https://git-scm.com/downloads](https://git-scm.com/downloads)
   - Download and install the version for your operating system
   - For Windows users: Choose "Git Bash" during installation

### Step 2: Basic Configuration

1. **Open Visual Studio Code**
2. **Open your project folder**
   - Go to File → Open Folder
   - Navigate to your `my-resume` folder
   - Click "Select Folder"

3. **Configure Git (one-time setup)**
   - Open Terminal in VS Code (View → Terminal)
   - Set your Git username:
     ```bash
     git config --global user.name "Your Name"
     ```
   - Set your Git email:
     ```bash
     git config --global user.email "your.email@example.com"
     ```

## GitHub Setup

### Step 1: Create GitHub Account

1. Go to [https://github.com/](https://github.com/)
2. Click "Sign up"
3. Follow the registration process
4. Verify your email address

### Step 2: Create New Repository

1. Click the "+" icon in the top right corner
2. Select "New repository"
3. Fill in the details:
   - Repository name: `my-resume`
   - Description: "My professional resume website"
   - Make it Public
   - Don't initialize with README
4. Click "Create repository"

### Step 3: Push Your Code to GitHub

Open Terminal in VS Code and run these commands one by one:

```bash
# Initialize Git repository
git init

# Add all files to Git
git add .

# Commit your files
git commit -m "Initial commit: Add resume files"

# Add GitHub repository as remote
# Replace YOUR-USERNAME with your GitHub username
git remote add origin https://github.com/YOUR-USERNAME/my-resume.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

## Deploying with Vercel

### Step 1: Create Vercel Account

1. Go to [https://vercel.com/](https://vercel.com/)
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub

### Step 2: Deploy Your Resume

1. Once logged in to Vercel, click "New Project"
2. Under "Import Git Repository", find and select `my-resume`
3. Keep all default settings:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: None
   - Output Directory: ./
4. Click "Deploy"

### Step 3: Access Your Deployed Resume

1. Wait for deployment to complete (usually takes less than a minute)
2. Click "Visit" to view your live resume
3. Your resume is now live at: `https://my-resume-yourusername.vercel.app`

## Making Updates

To update your resume:

1. Make changes to your files in VS Code
2. Open Terminal in VS Code
3. Run these commands:
   ```bash
   git add .
   git commit -m "Update resume content"
   git push
   ```
4. Vercel will automatically deploy your changes

## Troubleshooting

### Common Issues and Solutions

1. **Git push fails**
   - Check if you're connected to the internet
   - Verify your GitHub credentials
   - Try: `git push --force origin main`

2. **Vercel deployment fails**
   - Ensure your HTML file is named exactly `index.html`
   - Check that all file paths are correct
   - Verify all files are committed to GitHub

3. **Styling issues**
   - Confirm `styles.css` is in the same folder as `index.html`
   - Check file paths in your HTML
   - Clear your browser cache

4. **Changes not appearing**
   - Wait a few minutes for Vercel to complete deployment
   - Check Vercel dashboard for deployment status
   - Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)

### Getting Help

1. Check error messages in:
   - VS Code terminal
   - GitHub website
   - Vercel dashboard

2. Common resources:
   - [GitHub Help](https://help.github.com)
   - [Vercel Documentation](https://vercel.com/docs)
   - Stack Overflow

## Next Steps

1. **Customize Your Resume**
   - Replace placeholder text with your information
   - Add your profile picture (optional)
   - Modify colors in CSS
   - Add additional sections as needed

2. **Add Professional Links**
   - LinkedIn profile
   - GitHub profile
   - Portfolio website
   - Professional blog

3. **Optimize for Search Engines**
   - Add relevant meta tags
   - Include a clear title
   - Use semantic HTML

4. **Test Thoroughly**
   - Check all links
   - Verify mobile responsiveness
   - Test in different browsers

Remember: Your resume is a living document. Keep it updated with your latest achievements and experiences!
