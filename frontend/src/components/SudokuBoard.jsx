import React from 'react';

const SudokuBoard = ({ board, onCellChange, highlightedCell, lockedCells, errors }) => {
  const handleCellClick = (row, col) => {
    if (!lockedCells[row][col]) {
      onCellChange(row, col, null);
    }
  };

  const handleKeyPress = (e, row, col) => {
    if (lockedCells[row][col]) return;

    const key = e.key;
    if (key >= '1' && key <= '9') {
      onCellChange(row, col, parseInt(key));
    } else if (key === 'Backspace' || key === 'Delete' || key === '0') {
      onCellChange(row, col, 0);
    }
  };

  const getCellClass = (row, col) => {
    let classes = ['cell'];
    
    if (lockedCells[row][col]) {
      classes.push('locked');
    }
    
    if (highlightedCell && highlightedCell.row === row && highlightedCell.col === col) {
      classes.push('highlighted');
    }
    
    if (errors && errors.some(e => e.row === row && e.col === col)) {
      classes.push('error');
    }
    
    // Box borders
    if (col % 3 === 2 && col !== 8) classes.push('right-border');
    if (row % 3 === 2 && row !== 8) classes.push('bottom-border');
    
    return classes.join(' ');
  };

  return (
    <div className="sudoku-board">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, colIndex) => (
            <input
              key={`${rowIndex}-${colIndex}`}
              type="text"
              className={getCellClass(rowIndex, colIndex)}
              value={cell === 0 ? '' : cell}
              onClick={() => handleCellClick(rowIndex, colIndex)}
              onKeyDown={(e) => handleKeyPress(e, rowIndex, colIndex)}
              readOnly={lockedCells[rowIndex][colIndex]}
              maxLength="1"
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default SudokuBoard;
