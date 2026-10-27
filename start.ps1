Write-Host "===================================================" -ForegroundColor Magenta
Write-Host "  SafeStay Smart Women Hostel Management System" -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "[1/3] Checking dependencies..." -ForegroundColor Cyan
python -m pip install -r requirements.txt --quiet
Write-Host "[2/3] Initializing SQLite database..." -ForegroundColor Cyan
python database.py
Write-Host "[3/3] Starting backend server on http://127.0.0.1:5000 ..." -ForegroundColor Green
Start-Process "http://127.0.0.1:5000"
python app.py
