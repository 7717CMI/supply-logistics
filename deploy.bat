@echo off
echo 🚀 NextLoad Dashboard - Render Deployment Setup
echo.

echo 📁 Current directory: %CD%
echo.

echo 🔧 Initializing Git repository...
git init
echo.

echo 📦 Adding all files...
git add .
echo.

echo 💾 Creating initial commit...
git commit -m "NextLoad Dashboard - Ready for Render deployment"
echo.

echo ✅ Git repository ready!
echo.
echo 📋 Next steps:
echo 1. Create a new repository on GitHub (make it PUBLIC)
echo 2. Copy the repository URL
echo 3. Run: git remote add origin YOUR_REPO_URL
echo 4. Run: git push -u origin main
echo 5. Go to render.com and deploy from GitHub
echo.
echo 🎉 Your dashboard is ready for deployment!
pause
