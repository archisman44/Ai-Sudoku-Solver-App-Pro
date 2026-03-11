import React, { useState } from 'react';

const ControlPanel = ({ 
  onSolve, 
  onGenerate, 
  onClear, 
  onUploadImage,
  onAnalyze,
  onGetHint,
  algorithms,
  isLoading 
}) => {
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('backtracking');
  const [selectedDifficulty, setSelectedDifficulty] = useState('medium');
  const [visualize, setVisualize] = useState(false);

  const handleSolve = () => {
    onSolve(selectedAlgorithm, visualize);
  };

  const handleGenerate = () => {
    onGenerate(selectedDifficulty);
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUploadImage(file);
    }
  };

  return (
    <div className="control-panel">
      <div className="control-section">
        <h3>Solver</h3>
        <div className="control-group">
          <label>Algorithm:</label>
          <select 
            value={selectedAlgorithm} 
            onChange={(e) => setSelectedAlgorithm(e.target.value)}
            disabled={isLoading}
          >
            {algorithms.map(algo => (
              <option key={algo.id} value={algo.id}>
                {algo.name}
              </option>
            ))}
          </select>
        </div>
        
        <div className="control-group checkbox">
          <label>
            <input 
              type="checkbox" 
              checked={visualize}
              onChange={(e) => setVisualize(e.target.checked)}
              disabled={isLoading}
            />
            Visualize Steps
          </label>
        </div>
        
        <button 
          className="btn btn-primary" 
          onClick={handleSolve}
          disabled={isLoading}
        >
          {isLoading ? 'Solving...' : 'Solve Puzzle'}
        </button>
      </div>

      <div className="control-section">
        <h3>Generator</h3>
        <div className="control-group">
          <label>Difficulty:</label>
          <select 
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            disabled={isLoading}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
            <option value="expert">Expert</option>
            <option value="extreme">Extreme</option>
          </select>
        </div>
        
        <button 
          className="btn btn-secondary" 
          onClick={handleGenerate}
          disabled={isLoading}
        >
          Generate Puzzle
        </button>
      </div>

      <div className="control-section">
        <h3>Tools</h3>
        <button 
          className="btn btn-info" 
          onClick={onGetHint}
          disabled={isLoading}
        >
          Get Hint
        </button>
        
        <button 
          className="btn btn-info" 
          onClick={onAnalyze}
          disabled={isLoading}
        >
          Analyze Difficulty
        </button>
        
        <button 
          className="btn btn-warning" 
          onClick={onClear}
          disabled={isLoading}
        >
          Clear Board
        </button>
      </div>

      <div className="control-section">
        <h3>Image Upload</h3>
        <input 
          type="file" 
          accept="image/*"
          onChange={handleImageUpload}
          disabled={isLoading}
          id="image-upload"
          style={{ display: 'none' }}
        />
        <label htmlFor="image-upload" className="btn btn-upload">
          {isLoading ? 'Processing...' : 'Upload Sudoku Image'}
        </label>
      </div>
    </div>
  );
};

export default ControlPanel;
