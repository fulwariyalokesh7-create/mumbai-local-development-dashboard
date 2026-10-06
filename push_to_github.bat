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
git commit -m "Add Streamlit Cloud dashboard support (streamlit_app.py)"
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/fulwariyalokesh7-create/mumbai-local-development-dashboard.git
echo.
echo Pushing code to GitHub...
git push -u origin main

echo.
echo ========================================================
echo  Completed! Refresh your GitHub and Streamlit Cloud!
echo ========================================================
pause
