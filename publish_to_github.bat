@echo off
title Publish Mumbai Local Development Dashboard to GitHub
cd /d "%~dp0"
echo ========================================================
echo   Preparing Git Repository for GitHub...
echo ========================================================
git init
git add .
git commit -m "Initial commit: Mumbai Local Development Dashboard"
git branch -M main
echo.
echo ========================================================
echo  All files committed to local Git!
echo.
echo  To push to your GitHub account:
echo  1. Create a new empty repository at: https://github.com/new
echo  2. Copy its URL and run:
echo     git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo     git push -u origin main
echo ========================================================
pause
