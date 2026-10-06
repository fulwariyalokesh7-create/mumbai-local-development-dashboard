@echo off
title Mumbai Local Development Dashboard
cd /d "%~dp0"
echo ========================================================
echo  Checking and installing Python dependencies...
echo ========================================================
pip install Flask pandas numpy
echo.
echo ========================================================
echo  Starting Mumbai Local Development Dashboard...
echo  👉 Web Link: http://127.0.0.1:5000
echo ========================================================
echo.
python app.py
pause
