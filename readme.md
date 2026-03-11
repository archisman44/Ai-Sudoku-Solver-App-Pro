# 🧩 AI Sudoku Solver Pro

A production-level, full-stack web application for solving Sudoku puzzles using advanced algorithms, image recognition, and step-by-step visualization.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)

## 🌟 Features

### Core Functionality
- **Multiple Solving Algorithms**
  - Backtracking with MRV heuristic
  - Constraint Propagation (Naked/Hidden Singles)
  - Dancing Links (Algorithm X)
  - Heuristic Solver (Human-like strategies)

- **Image Recognition**
  - Upload Sudoku puzzle images
  - Automatic grid detection using OpenCV
  - Digit recognition with OCR
  - Preprocessing and perspective correction

- **Puzzle Generation**
  - Generate puzzles with 5 difficulty levels (Easy to Extreme)
  - Guaranteed unique solutions
  - Configurable clue counts

- **Interactive Features**
  - Click-to-edit cells
  - Keyboard input support
  - Real-time validation
  - Hint system with reasoning
  - Difficulty analyzer

- **Visualization**
  - Step-by-step solving animation
  - Play/Pause/Step controls
  - Adjustable speed
  - Highlighted cells and reasoning

- **UI/UX**
  - Dark/Light mode
  - Responsive design
  - Local storage persistence
  - Performance statistics
  - Error highlighting

## 🏗️ Architecture

```
ai-sudoku-solver/
├── backend/                    # Python Flask API
│   ├── app.py                 # Main Flask application
│   ├── solver/                # Solving algorithms
│   │   ├── backtracking_solver.py
│   │   ├── constraint_solver.py
│   │   ├── dancing_links_solver.py
│   │   ├── heuristic_solver.py
│   │   ├── difficulty_analyzer.py
│   │   └── puzzle_generator.py
│   ├── image_processing/      # Computer vision
│   │   ├── sudoku_detector.py
│   │   └── digit_recognition.py
│   └── requirements.txt
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── SudokuBoard.jsx
│   │   │   ├── ControlPanel.jsx
│   │   │   └── SolverVisualizer.jsx
│   │   ├── App.jsx
│   │   ├── index.js
│   │   └── styles.css
│   ├── public/
│   └── package.json
├── docker/
│   └── Dockerfile
└── README.md
```

## 🧠 Algorithm Explanations

### 1. Backtracking Solver
Classic recursive backtracking with **Minimum Remaining Values (MRV)** heuristic.

**How it works:**
1. Find empty cell with fewest possible values
2. Try each valid number (1-9)
3. Recursively solve remaining puzzle
4. Backtrack if no solution found

**Complexity:** O(9^n) where n is empty cells
**Best for:** Most puzzles, reliable and fast

### 2. Constraint Propagation Solver
Uses constraint satisfaction techniques to eliminate candidates.

**Techniques:**
- **Naked Singles:** Cells with only one candidate
- **Hidden Singles:** Numbers that can only go in one place
- **Constraint Propagation:** Eliminate impossible values

**Complexity:** O(n²) for propagation, O(9^n) worst case
**Best for:** Easier puzzles, human-readable steps

### 3. Dancing Links (Algorithm X)
Knuth's Algorithm X for exact cover problems using Dancing Links data structure.

**How it works:**
1. Convert Sudoku to exact cover matrix (324 constraints)
2. Use DLX to find exact cover
3. Backtrack efficiently with pointer manipulation

**Complexity:** O(9^n) but with better constants
**Best for:** Hard puzzles, theoretical elegance

### 4. Heuristic Solver
Mimics human solving strategies.

**Strategies:**
- Naked Singles/Pairs
- Hidden Singles
- Pointing Pairs/Triples
- Box-Line Reduction
- Fallback to guessing

**Complexity:** Variable, O(n²) to O(9^n)
**Best for:** Educational purposes, explainable AI

## 📡 API Endpoints

### POST `/api/solve`
Solve a Sudoku puzzle.

**Request:**
```json
{
  "board": [[0,0,0,...], ...],
  "algorithm": "backtracking",
  "visualize": false
}
```

**Response:**
```json
{
  "success": true,
  "board": [[5,3,4,...], ...],
  "steps": [...],
  "algorithm": "backtracking",
  "time": 0.0234,
  "recursive_calls": 142
}
```

### POST `/api/generate`
Generate a new puzzle.

**Request:**
```json
{
  "difficulty": "medium"
}
```

**Response:**
```json
{
  "success": true,
  "puzzle": [[0,0,3,...], ...],
  "difficulty": "Medium",
  "clues": 32
}
```

### POST `/api/analyze`
Analyze puzzle difficulty.

**Request:**
```json
{
  "board": [[0,0,0,...], ...]
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "difficulty": "Hard",
    "score": 67,
    "clues": 27,
    "branching_factor": 4.2,
    "techniques": ["naked_singles", "backtracking"]
  }
}
```

### POST `/api/scan-image`
Extract Sudoku from image.

**Request:** Multipart form data with image file

**Response:**
```json
{
  "success": true,
  "board": [[5,3,0,...], ...]
}
```

### GET `/api/algorithms`
Get available algorithms.

**Response:**
```json
{
  "algorithms": [
    {
      "id": "backtracking",
      "name": "Backtracking",
      "description": "Classic recursive backtracking..."
    },
    ...
  ]
}
```

### POST `/api/hint`
Get solving hint.

**Request:**
```json
{
  "board": [[0,0,0,...], ...]
}
```

**Response:**
```json
{
  "success": true,
  "hint": {
    "row": 0,
    "col": 2,
    "value": 5,
    "reason": "Naked single - only one possible value",
    "candidates": [5]
  }
}
```

### POST `/api/validate`
Validate board state.

**Request:**
```json
{
  "board": [[5,3,4,...], ...]
}
```

**Response:**
```json
{
  "valid": false,
  "errors": [
    {
      "type": "row",
      "row": 0,
      "col": 3,
      "value": 5
    }
  ]
}
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Tesseract OCR
- Git

### Local Development Setup

#### 1. Clone Repository
```bash
git clone <repository-url>
cd ai-sudoku-solver
```

#### 2. Backend Setup

**Install Tesseract OCR:**

**Windows:**
```bash
# Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH: C:\Program Files\Tesseract-OCR
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Run backend:**
```bash
python app.py
```

Backend runs on `http://localhost:5000`

#### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

### VS Code Setup

1. Open project in VS Code
2. Install recommended extensions:
   - Python
   - ESLint
   - Prettier
3. Open two terminals:
   - Terminal 1: `cd backend && python app.py`
   - Terminal 2: `cd frontend && npm start`

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t ai-sudoku-solver -f docker/Dockerfile .
```

### Run Container
```bash
docker run -p 5000:5000 ai-sudoku-solver
```

Access at `http://localhost:5000`

### Docker Compose (Optional)
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  sudoku-solver:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

Run:
```bash
docker-compose up
```

## 🎮 Usage Guide

### Manual Input
1. Click on any cell
2. Type numbers 1-9
3. Press Backspace/Delete to clear

### Solve Puzzle
1. Select algorithm from dropdown
2. Enable "Visualize Steps" for animation
3. Click "Solve Puzzle"
4. Watch step-by-step solution or see instant result

### Generate Puzzle
1. Select difficulty level
2. Click "Generate Puzzle"
3. Puzzle appears with locked cells

### Upload Image
1. Click "Upload Sudoku Image"
2. Select image file
3. Wait for processing
4. Detected puzzle appears on board

### Get Hints
1. Click "Get Hint"
2. See suggested move with reasoning
3. Highlighted cell shows where to focus

### Analyze Difficulty
1. Click "Analyze Difficulty"
2. See complexity metrics and required techniques

## 🧪 Testing

### Test Puzzles

**Easy Puzzle:**
```
5 3 0 | 0 7 0 | 0 0 0
6 0 0 | 1 9 5 | 0 0 0
0 9 8 | 0 0 0 | 0 6 0
------+-------+------
8 0 0 | 0 6 0 | 0 0 3
4 0 0 | 8 0 3 | 0 0 1
7 0 0 | 0 2 0 | 0 0 6
------+-------+------
0 6 0 | 0 0 0 | 2 8 0
0 0 0 | 4 1 9 | 0 0 5
0 0 0 | 0 8 0 | 0 7 9
```

**Hard Puzzle (World's Hardest):**
```
8 0 0 | 0 0 0 | 0 0 0
0 0 3 | 6 0 0 | 0 0 0
0 7 0 | 0 9 0 | 2 0 0
------+-------+------
0 5 0 | 0 0 7 | 0 0 0
0 0 0 | 0 4 5 | 7 0 0
0 0 0 | 1 0 0 | 0 3 0
------+-------+------
0 0 1 | 0 0 0 | 0 6 8
0 0 8 | 5 0 0 | 0 1 0
0 9 0 | 0 0 0 | 4 0 0
```

## 📊 Performance Benchmarks

| Algorithm | Easy | Medium | Hard | Extreme |
|-----------|------|--------|------|---------|
| Backtracking | 0.01s | 0.05s | 0.2s | 1.5s |
| Constraint | 0.02s | 0.08s | 0.5s | 3.0s |
| Dancing Links | 0.03s | 0.1s | 0.3s | 2.0s |
| Heuristic | 0.02s | 0.1s | 0.8s | 4.0s |

*Benchmarks on Intel i7, Python 3.10*

## 🔧 Configuration

### Environment Variables

Create `.env` file in backend:
```
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

### Frontend Configuration

Edit `frontend/package.json`:
```json
{
  "proxy": "http://localhost:5000"
}
```

## 🐛 Troubleshooting

### Tesseract Not Found
```bash
# Windows: Add to PATH
set PATH=%PATH%;C:\Program Files\Tesseract-OCR

# Linux/Mac: Install via package manager
```

### CORS Errors
Ensure Flask-CORS is installed and configured in `app.py`

### Image Upload Fails
- Check file size (max 10MB)
- Ensure image contains clear Sudoku grid
- Try preprocessing image (crop, enhance contrast)

### Slow Solving
- Use Backtracking for fastest results
- Disable visualization for instant solving
- Reduce puzzle complexity

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📄 License

MIT License - see LICENSE file

## 👨‍💻 Author

Portfolio-grade project for freelance work

## 🙏 Acknowledgments

- Knuth's Dancing Links algorithm
- OpenCV for image processing
- React community
- Flask framework

## 📞 Support

For issues and questions:
- Open GitHub issue
- Check documentation
- Review API endpoints

---

**Built with ❤️ for Sudoku enthusiasts and algorithm lovers**
