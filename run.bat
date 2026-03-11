@echo off
echo ========================================
echo AI Sudoku Solver Pro - Starting...
echo ========================================
echo.

echo Starting Backend Server...
start "Backend - Flask" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend - React" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Both servers are starting...
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to stop all servers...
pause >nul

taskkill /FI "WindowTitle eq Backend - Flask*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Frontend - React*" /T /F >nul 2>&1

echo Servers stopped.
