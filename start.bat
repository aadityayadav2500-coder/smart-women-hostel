@echo off
title SafeStay Smart Women Hostel Backend Server
echo ===================================================
echo   SafeStay Smart Women Hostel Management System
echo ===================================================
echo.
echo [1/3] Checking dependencies...
python -m pip install -r requirements.txt --quiet
echo.
echo [2/3] Initializing SQLite database...
python database.py
echo.
echo [3/3] Starting backend server on http://127.0.0.1:5000 ...
echo.
start http://127.0.0.1:5000
python app.py
pause
