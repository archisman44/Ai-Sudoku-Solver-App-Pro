# 🚀 Quick Start Guide

## For Windows (VS Code)

### Step 1: Install Prerequisites

1. **Python 3.10+**
   - Download: https://www.python.org/downloads/
   - Check: `python --version`

2. **Node.js 18+**
   - Download: https://nodejs.org/
   - Check: `node --version`

3. **Tesseract OCR**
   - Download: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to: `C:\Program Files\Tesseract-OCR`
   - Add to PATH

### Step 2: Automated Setup

Run the setup script:
```bash
setup.bat
```

This will:
- Install Python dependencies
- Install Node dependencies
- Verify Tesseract installation

### Step 3: Run Application

**Option A: Automated (Recommended)**
```bash
run.bat
```

**Option B: Manual**

Terminal 1 (Backend):
```bash
cd backend
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm start
```

### Step 4: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## First Time Usage

1. **Generate a puzzle**: Select difficulty and click "Generate Puzzle"
2. **Solve it**: Choose algorithm and click "Solve Puzzle"
3. **Try visualization**: Enable "Visualize Steps" before solving
4. **Upload image**: Click "Upload Sudoku Image" to scan a puzzle

## Testing Solvers

Run test suite:
```bash
cd backend
python test_solvers.py
```

## Troubleshooting

### Tesseract Not Found
```bash
# Add to PATH
set PATH=%PATH%;C:\Program Files\Tesseract-OCR
```

### Port Already in Use
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Module Not Found
```bash
cd backend
pip install -r requirements.txt
```

## VS Code Setup

1. Open `sudoku-solver.code-workspace`
2. Install recommended extensions
3. Use integrated terminal for both servers

## Next Steps

- Read full README.md for detailed documentation
- Explore API endpoints
- Try different algorithms
- Upload your own Sudoku images

---

**Need help?** Check README.md or open an issue.
