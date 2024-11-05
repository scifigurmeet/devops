# Setting Up a NextJS Project with Bun, Git and Vercel Deployment

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setting Up Git](#setting-up-git)
3. [Creating a NextJS Project](#creating-a-nextjs-project)
4. [Git Repository Setup](#git-repository-setup)
5. [Vercel Deployment](#vercel-deployment)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting, ensure you have the following installed:
- Bun (instead of Node.js)
- Git
- A GitHub account
- A Vercel account (can be created using GitHub)

Install Bun (if not already installed):
```bash
# For macOS and Linux
curl -fsSL https://bun.sh/install | bash

# For Windows (using WSL)
# First install WSL if you haven't already
wsl --install
# Then install Bun inside WSL
curl -fsSL https://bun.sh/install | bash
```

Verify installations:
```bash
bun --version
git --version
```

## Setting Up Git

1. **Configure Git globally** (if not done before):
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

2. **Generate SSH Key** (recommended for GitHub):
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

3. **Add SSH Key to GitHub**:
- Copy the SSH key:
  ```bash
  cat ~/.ssh/id_ed25519.pub
  ```
- Go to GitHub → Settings → SSH and GPG keys → New SSH key
- Paste your key and save

## Creating a NextJS Project

1. **Create a new Next.js project using Bun**:
```bash
bun create next-app my-nextjs-app
```

2. **During setup, you'll be prompted with questions**:
```plaintext
Would you like to use TypeScript? › Yes
Would you like to use ESLint? › Yes
Would you like to use Tailwind CSS? › Yes
Would you like to use `src/` directory? › Yes
Would you like to use App Router? › Yes
Would you like to customize the default import alias? › No
```

3. **Navigate to project directory**:
```bash
cd my-nextjs-app
```

4. **Key differences when using Bun**:
- `bun install` instead of `npm install`
- `bunx` instead of `npx`
- Much faster installation and execution times
- Built-in `.env` support
- Native TypeScript support without additional setup

5. **Test the development server**:
```bash
bun dev
```
Visit `http://localhost:3000` to see your app.

6. **Using Bun's package manager**:
```bash
# Add a dependency
bun add package-name

# Add a dev dependency
bun add -d package-name

# Remove a dependency
bun remove package-name
```

## Git Repository Setup

1. **Initialize Git repository** (if not already initialized):
```bash
git init
```

2. **Create .gitignore file** (should be created automatically by create-next-app):
```plaintext
# .gitignore
node_modules/
.next/
.env*.local
bun.lockb
```

Note: Bun uses `bun.lockb` instead of `package-lock.json`

3. **Create a new repository on GitHub**:
- Go to GitHub.com
- Click "New repository"
- Name it "my-nextjs-app"
- Don't initialize with README (we'll push our existing code)

4. **Link and push to remote repository**:
```bash
git add .
git commit -m "Initial commit: NextJS project setup with Bun"
git branch -M main
git remote add origin git@github.com:username/my-nextjs-app.git
git push -u origin main
```

## Vercel Deployment

1. **Prepare for deployment**:
- Ensure your code is pushed to GitHub
- Create a Vercel account at vercel.com (sign up with GitHub)

2. **Configure for Bun deployment**:
- Create a `vercel.json` file in your project root:
```json
{
  "buildCommand": "bun run build",
  "devCommand": "bun run dev",
  "installCommand": "bun install"
}
```

3. **Deploy to Vercel**:
- Go to vercel.com/dashboard
- Click "New Project"
- Import your GitHub repository
- Select "my-nextjs-app"
- Configure project:
  - Framework Preset: Next.js
  - Root Directory: ./
  - Build Command: `bun run build`
  - Output Directory: .next

4. **Environment Variables** (if needed):
- Add them in Vercel's project settings
- Format: KEY=value
- Bun automatically loads `.env` files

5. **Deploy**:
- Click "Deploy"
- Wait for build and deployment
- Your app will be live at: `https://my-nextjs-app-username.vercel.app`

## Best Practices

1. **Using Bun Scripts**:
Define scripts in `package.json`:
```json
{
  "scripts": {
    "dev": "bun run next dev",
    "build": "bun run next build",
    "start": "bun run next start",
    "lint": "bun run next lint"
  }
}
```

2. **Branch Management**:
```bash
# Create feature branch
git checkout -b feature/new-feature

# After changes
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

3. **Bun-specific Optimizations**:
- Use Bun's built-in test runner:
```bash
bun test
```
- Use Bun's built-in package manager:
```bash
bun install
bun add package-name
```
- Leverage Bun's TypeScript support:
```bash
bun run index.ts
```

## Troubleshooting

### Common Issues and Solutions

1. **Bun-specific Issues**:
```bash
# Clear Bun's cache
bun clean

# Reinstall dependencies
rm -rf node_modules bun.lockb
bun install
```

2. **Next.js Build Errors**:
- Check console for error messages
- Verify all dependencies are installed
- Clear `.next` cache:
```bash
rm -rf .next
bun run build
```

3. **Vercel Deployment Fails**:
- Check build logs in Vercel dashboard
- Verify environment variables
- Ensure `vercel.json` is properly configured
- Verify Bun compatibility

### Getting Help
- Bun Documentation: https://bun.sh/docs
- Next.js Documentation: https://nextjs.org/docs
- Vercel Documentation: https://vercel.com/docs
- GitHub Documentation: https://docs.github.com/en

---

Remember to:
- Take advantage of Bun's speed and built-in features
- Keep dependencies updated with `bun update`
- Use `bun.lockb` for version locking
- Regularly test with `bun test`
- Keep sensitive data in environment variables

This guide should help you get started with NextJS using Bun, Git, and Vercel. The main advantages of using Bun include:
- Faster installation and execution times
- Built-in TypeScript support
- Native testing capabilities
- Improved package management
- Better development experience

If you encounter any issues, refer to the official documentation or seek help in the respective communities.
