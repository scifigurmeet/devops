# Quick Next.js Deployment Assignment with Tailwind CSS
**Duration: 1 hour**
**Objective:** Deploy a Next.js project using Vercel UI and create a custom homepage with Tailwind CSS.

## Part 1: Project Setup (15 minutes)
1. Go to [Vercel](https://vercel.com)
2. Sign in with GitHub
3. Click "Add New Project"
4. Select "Create Next.js App" from the templates
5. Configure your project:
   - Name your project
   - Select latest Next.js version
   - Make sure Tailwind CSS is enabled
   - Click "Deploy"

## Part 2: Update Homepage (30 minutes)
1. Once deployed, go to your project dashboard
2. Click "Git" in sidebar
3. Click on your repository link (Vercel created this automatically)
4. Navigate to `app/page.tsx`
5. Edit the file directly in GitHub with this code:

```tsx
export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-800 mb-4 animate-fade-in">
            Welcome to My Next.js Site
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            A simple homepage built with Next.js and Tailwind CSS
          </p>
          
          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            {/* Card 1 */}
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="text-indigo-500 text-2xl mb-4">🚀</div>
              <h2 className="text-xl font-semibold mb-2 text-gray-800">
                Fast Deployment
              </h2>
              <p className="text-gray-600">
                Deploy quickly with Vercel&#39;s seamless platform
              </p>
            </div>

            {/* Card 2 */}
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="text-indigo-500 text-2xl mb-4">🎨</div>
              <h2 className="text-xl font-semibold mb-2 text-gray-800">
                Tailwind CSS
              </h2>
              <p className="text-gray-600">
                Beautiful, responsive design made simple
              </p>
            </div>

            {/* Card 3 */}
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="text-indigo-500 text-2xl mb-4">⚡</div>
              <h2 className="text-xl font-semibold mb-2 text-gray-800">
                Auto Updates
              </h2>
              <p className="text-gray-600">
                Changes deploy automatically via CI/CD
              </p>
            </div>
          </div>

          {/* Call to Action */}
          <div className="mt-16">
            <button className="bg-indigo-600 text-white px-8 py-3 rounded-full font-semibold hover:bg-indigo-700 transition-colors duration-300">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
```

## Part 3: Test Auto-Deployment (10 minutes)
1. Commit your changes in GitHub
2. Go back to your Vercel dashboard
3. Watch the automatic deployment progress
4. Visit your site URL to see the changes

## Part 4: Make Another Change (5 minutes)
1. Go back to `page.tsx` in GitHub
2. Change the heading text
3. Commit and watch another deployment happen

## Part 5: Test Rollback (5 minutes)
1. In your Vercel dashboard, go to "Deployments"
2. Find your previous deployment
3. Click the three dots (⋯)
4. Select "Promote to Production"
5. Verify your site reverted to the previous version

## Deliverables
- Vercel deployment URL
- Screenshot of your deployment history
- Brief explanation of what you learned about auto-deployment

## Common Issues & Solutions
- If you don't see your changes, hard refresh your browser (Ctrl/Cmd + Shift + R)
- If deployment fails, check the Vercel deployment logs
- Make sure you committed your changes in GitHub

## Bonus (if time permits)
- Add a dark mode toggle
- Add more interactive elements using Tailwind's hover states
- Add a custom animation using Tailwind's animation classes
