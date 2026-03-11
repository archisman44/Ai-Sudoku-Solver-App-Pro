import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SudokuBoard from './components/SudokuBoard';
import ControlPanel from './components/ControlPanel';
import SolverVisualizer from './components/SolverVisualizer';
import './styles.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [board, setBoard] = useState(Array(9).fill(null).map(() => Array(9).fill(0)));
  const [lockedCells, setLockedCells] = useState(Array(9).fill(null).map(() => Array(9).fill(false)));
  const [highlightedCell, setHighlightedCell] = useState(null);
  const [errors, setErrors] = useState([]);
  const [algorithms, setAlgorithms] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [steps, setSteps] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [stats, setStats] = useState(null);
  const [message, setMessage] = useState('');
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    fetchAlgorithms();
    loadFromLocalStorage();
  }, []);

  useEffect(() => {
    localStorage.setItem('sudoku_board', JSON.stringify(board));
    localStorage.setItem('sudoku_locked', JSON.stringify(lockedCells));
  }, [board, lockedCells]);

  useEffect(() => {
    document.body.className = darkMode ? 'dark-mode' : '';
  }, [darkMode]);

  const fetchAlgorithms = async () => {
    try {
      const response = await axios.get(`${API_URL}/algorithms`);
      setAlgorithms(response.data.algorithms);
    } catch (error) {
      console.error('Error fetching algorithms:', error);
      setAlgorithms([
        { id: 'backtracking', name: 'Backtracking', description: 'Classic backtracking' },
        { id: 'constraint', name: 'Constraint Propagation', description: 'Constraint-based' },
        { id: 'dancing_links', name: 'Dancing Links', description: 'Algorithm X' },
        { id: 'heuristic', name: 'Heuristic', description: 'Human-like strategies' }
      ]);
    }
  };



  const loadFromLocalStorage = () => {
    const savedBoard = localStorage.getItem('sudoku_board');
    const savedLocked = localStorage.getItem('sudoku_locked');
    
    if (savedBoard) {
      setBoard(JSON.parse(savedBoard));
    }
    if (savedLocked) {
      setLockedCells(JSON.parse(savedLocked));
    }
  };

  const handleCellChange = (row, col, value) => {
    if (lockedCells[row][col]) return;

    const newBoard = board.map(r => [...r]);
    newBoard[row][col] = value === null ? board[row][col] : value;
    setBoard(newBoard);
    setHighlightedCell({ row, col });
    validateBoard(newBoard);
  };

  const validateBoard = async (currentBoard) => {
    try {
      const response = await axios.post(`${API_URL}/validate`, { board: currentBoard });
      setErrors(response.data.errors || []);
    } catch (error) {
      console.error('Validation error:', error);
    }
  };

  const handleSolve = async (algorithm, visualize) => {
    setIsLoading(true);
    setMessage('');
    setSteps([]);
    
    try {
      const response = await axios.post(`${API_URL}/solve`, {
        board: board,
        algorithm: algorithm,
        visualize: visualize
      });

      if (response.data.success) {
        if (visualize && response.data.steps.length > 0) {
          setSteps(response.data.steps);
          setMessage(`Solution found using ${algorithm}!`);
        } else {
          setBoard(response.data.board);
          setMessage(`Solved in ${response.data.time}s using ${algorithm}`);
        }
        
        setStats({
          algorithm: response.data.algorithm,
          time: response.data.time,
          recursiveCalls: response.data.recursive_calls
        });
      } else {
        setMessage('No solution found for this puzzle');
      }
    } catch (error) {
      setMessage('Error solving puzzle: ' + (error.response?.data?.error || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerate = async (difficulty) => {
    setIsLoading(true);
    setMessage('');
    setSteps([]);
    setStats(null);
    
    try {
      const response = await axios.post(`${API_URL}/generate`, {
        difficulty: difficulty
      });

      if (response.data.success) {
        const newBoard = response.data.puzzle;
        setBoard(newBoard);
        
        // Lock filled cells
        const locked = newBoard.map(row => row.map(cell => cell !== 0));
        setLockedCells(locked);
        
        setMessage(`Generated ${response.data.difficulty} puzzle with ${response.data.clues} clues`);
      }
    } catch (error) {
      setMessage('Error generating puzzle: ' + (error.response?.data?.error || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setBoard(Array(9).fill(null).map(() => Array(9).fill(0)));
    setLockedCells(Array(9).fill(null).map(() => Array(9).fill(false)));
    setErrors([]);
    setSteps([]);
    setStats(null);
    setMessage('');
    setHighlightedCell(null);
  };

  const handleUploadImage = async (file) => {
    setIsLoading(true);
    setMessage('Processing image...');
    
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axios.post(`${API_URL}/scan-image`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        const detectedBoard = response.data.board;
        setBoard(detectedBoard);
        
        // Lock detected cells
        const locked = detectedBoard.map(row => row.map(cell => cell !== 0));
        setLockedCells(locked);
        
        setMessage('Sudoku detected from image successfully!');
      }
    } catch (error) {
      setMessage('Error processing image: ' + (error.response?.data?.error || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    
    try {
      const response = await axios.post(`${API_URL}/analyze`, { board: board });
      
      if (response.data.success) {
        const analysis = response.data.analysis;
        setMessage(
          `Difficulty: ${analysis.difficulty} | ` +
          `Clues: ${analysis.clues} | ` +
          `Score: ${analysis.score} | ` +
          `Techniques: ${analysis.techniques.join(', ')}`
        );
      }
    } catch (error) {
      setMessage('Error analyzing puzzle: ' + (error.response?.data?.error || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetHint = async () => {
    setIsLoading(true);
    
    try {
      const response = await axios.post(`${API_URL}/hint`, { board: board });
      
      if (response.data.success) {
        const hint = response.data.hint;
        setHighlightedCell({ row: hint.row, col: hint.col });
        
        if (hint.value) {
          setMessage(`Hint: Place ${hint.value} at row ${hint.row + 1}, col ${hint.col + 1}. ${hint.reason}`);
        } else {
          setMessage(`Hint: ${hint.reason}. Candidates: ${hint.candidates.join(', ')}`);
        }
      }
    } catch (error) {
      setMessage('No hints available');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStepChange = (stepIndex) => {
    
    if (stepIndex === 0) {
      return;
    }

    // Apply steps up to current index
    const newBoard = board.map(r => [...r]);
    for (let i = 0; i < stepIndex && i < steps.length; i++) {
      const step = steps[i];
      if (step.action !== 'backtrack') {
        newBoard[step.row][step.col] = step.value;
      } else {
        newBoard[step.row][step.col] = 0;
      }
    }
    
    setBoard(newBoard);
    
    if (steps[stepIndex - 1]) {
      setHighlightedCell({ 
        row: steps[stepIndex - 1].row, 
        col: steps[stepIndex - 1].col 
      });
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧩 AI Sudoku Solver Pro</h1>
        <button 
          className="theme-toggle"
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </header>

      <div className="app-content">
        <div className="left-panel">
          <SudokuBoard 
            board={board}
            onCellChange={handleCellChange}
            highlightedCell={highlightedCell}
            lockedCells={lockedCells}
            errors={errors}
          />
          
          {message && (
            <div className="message-box">
              {message}
            </div>
          )}
          
          {stats && (
            <div className="stats-box">
              <h4>Performance Stats</h4>
              <p><strong>Algorithm:</strong> {stats.algorithm}</p>
              <p><strong>Time:</strong> {stats.time}s</p>
              <p><strong>Recursive Calls:</strong> {stats.recursiveCalls}</p>
            </div>
          )}
        </div>

        <div className="right-panel">
          <ControlPanel 
            onSolve={handleSolve}
            onGenerate={handleGenerate}
            onClear={handleClear}
            onUploadImage={handleUploadImage}
            onAnalyze={handleAnalyze}
            onGetHint={handleGetHint}
            algorithms={algorithms}
            isLoading={isLoading}
          />
          
          {steps.length > 0 && (
            <SolverVisualizer 
              steps={steps}
              onStepChange={handleStepChange}
              isPlaying={isPlaying}
              onPlayPause={setIsPlaying}
            />
          )}
        </div>
      </div>

      <footer className="app-footer">
        <p>AI Sudoku Solver Pro - Advanced Sudoku solving with multiple algorithms</p>
      </footer>
    </div>
  );
}

export default App;
