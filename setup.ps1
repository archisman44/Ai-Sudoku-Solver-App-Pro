# AI Sudoku Solver Pro - Setup Script (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Sudoku Solver Pro - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Setting up Backend..." -ForegroundColor Yellow
Set-Location backend
Write-Host "Installing Python dependencies..." -ForegroundColor Gray
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install Python dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Set-Location ..

Write-Host ""
Write-Host "[2/4] Setting up Frontend..." -ForegroundColor Yellow
Set-Location frontend
Write-Host "Installing Node dependencies..." -ForegroundColor Gray
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install Node dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Set-Location ..

Write-Host ""
Write-Host "[3/4] Checking Tesseract OCR..." -ForegroundColor Yellow
$tesseract = Get-Command tesseract -ErrorAction SilentlyContinue
if ($null -eq $tesseract) {
    Write-Host "WARNING: Tesseract OCR not found!" -ForegroundColor Red
    Write-Host "Please install from: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
    Write-Host "Add to PATH: C:\Program Files\Tesseract-OCR" -ForegroundColor Yellow
} else {
    Write-Host "Tesseract OCR found!" -ForegroundColor Green
}

Write-Host ""
Write-Host "[4/4] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Backend:  cd backend; python app.py" -ForegroundColor White
Write-Host "2. Frontend: cd frontend; npm start" -ForegroundColor White
Write-Host ""
Write-Host "Or use: .\run.ps1 to start both automatically" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
