@echo off
title Push to GitHub - Mumbai Local Development Dashboard
cd /d "%~dp0"
echo ========================================================
echo  Publishing to GitHub Repository:
echo  https://github.com/fulwariyalokesh7-create/mumbai-local-development-dashboard.git
echo ========================================================
echo.

git init
git add .
git commit -m "Initial commit: Mumbai Local Development Dashboard"
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/fulwariyalokesh7-create/mumbai-local-development-dashboard.git
echo.
echo Pushing code to GitHub...
git push -u origin main

echo.
echo ========================================================
echo  Completed! Refresh your GitHub page to see your project!
echo ========================================================
pause
