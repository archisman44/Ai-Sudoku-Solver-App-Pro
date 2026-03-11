import React, { useState, useEffect } from 'react';

const SolverVisualizer = ({ steps, onStepChange, isPlaying, onPlayPause }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [speed, setSpeed] = useState(100);

  useEffect(() => {
    if (isPlaying && currentStep < steps.length) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => prev + 1);
        onStepChange(currentStep + 1);
      }, speed);
      return () => clearTimeout(timer);
    } else if (currentStep >= steps.length && isPlaying) {
      onPlayPause(false);
    }
  }, [isPlaying, currentStep, steps.length, speed, onStepChange, onPlayPause]);

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(prev => prev + 1);
      onStepChange(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
      onStepChange(currentStep - 1);
    }
  };

  const handleReset = () => {
    setCurrentStep(0);
    onStepChange(0);
    onPlayPause(false);
  };

  if (!steps || steps.length === 0) {
    return null;
  }

  const currentStepData = steps[currentStep] || {};

  return (
    <div className="visualizer">
      <h3>Solving Visualization</h3>
      
      <div className="visualizer-info">
        <div className="step-info">
          <strong>Step:</strong> {currentStep + 1} / {steps.length}
        </div>
        {currentStepData.action && (
          <div className="action-info">
            <strong>Action:</strong> {currentStepData.action.replace(/_/g, ' ')}
          </div>
        )}
        {currentStepData.reason && (
          <div className="reason-info">
            <strong>Reason:</strong> {currentStepData.reason}
          </div>
        )}
        {currentStepData.row !== undefined && (
          <div className="position-info">
            <strong>Position:</strong> Row {currentStepData.row + 1}, Col {currentStepData.col + 1}
            {currentStepData.value > 0 && ` → Value: ${currentStepData.value}`}
          </div>
        )}
      </div>

      <div className="visualizer-controls">
        <button 
          className="btn btn-small" 
          onClick={handleReset}
          disabled={currentStep === 0}
        >
          ⏮ Reset
        </button>
        
        <button 
          className="btn btn-small" 
          onClick={handlePrev}
          disabled={currentStep === 0}
        >
          ⏪ Prev
        </button>
        
        <button 
          className="btn btn-small btn-primary" 
          onClick={() => onPlayPause(!isPlaying)}
        >
          {isPlaying ? '⏸ Pause' : '▶ Play'}
        </button>
        
        <button 
          className="btn btn-small" 
          onClick={handleNext}
          disabled={currentStep >= steps.length}
        >
          Next ⏩
        </button>
      </div>

      <div className="speed-control">
        <label>Speed:</label>
        <input 
          type="range" 
          min="10" 
          max="1000" 
          value={speed}
          onChange={(e) => setSpeed(parseInt(e.target.value))}
        />
        <span>{speed}ms</span>
      </div>
    </div>
  );
};

export default SolverVisualizer;
