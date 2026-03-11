@echo off
echo ========================================
echo AI Sudoku Solver Pro - Setup Script
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo [2/4] Setting up Frontend...
cd frontend
echo Installing Node dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Node dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo [3/4] Checking Tesseract OCR...
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Tesseract OCR not found!
    echo Please install from: https://github.com/UB-Mannheim/tesseract/wiki
    echo Add to PATH: C:\Program Files\Tesseract-OCR
) else (
    echo Tesseract OCR found!
)

echo.
echo [4/4] Setup Complete!
echo.
echo ========================================
echo To run the application:
echo ========================================
echo 1. Backend:  cd backend ^&^& python app.py
echo 2. Frontend: cd frontend ^&^& npm start
echo.
echo Or use run.bat to start both automatically
echo ========================================
pause
