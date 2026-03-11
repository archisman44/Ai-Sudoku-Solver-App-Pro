"""
Backtracking Sudoku Solver with optimizations
Uses recursive backtracking with constraint checking
"""

class BacktrackingSolver:
    def __init__(self):
        self.steps = []
        self.recursive_calls = 0
        
    def solve(self, board, visualize=False):
        """Solve sudoku using backtracking algorithm"""
        self.steps = []
        self.recursive_calls = 0
        self.visualize = visualize
        
        if self._solve_helper(board):
            return True, board, self.steps, self.recursive_calls
        return False, board, self.steps, self.recursive_calls
    
    def _solve_helper(self, board):
        self.recursive_calls += 1
        
        # Find empty cell
        empty = self._find_empty(board)
        if not empty:
            return True  # Solved
        
        row, col = empty
        
        # Try digits 1-9
        for num in range(1, 10):
            if self._is_valid(board, num, row, col):
                board[row][col] = num
                
                if self.visualize:
                    self.steps.append({
                        'row': row,
                        'col': col,
                        'value': num,
                        'action': 'place'
                    })
                
                if self._solve_helper(board):
                    return True
                
                # Backtrack
                board[row][col] = 0
                if self.visualize:
                    self.steps.append({
                        'row': row,
                        'col': col,
                        'value': 0,
                        'action': 'backtrack'
                    })
        
        return False
    
    def _find_empty(self, board):
        """Find empty cell with minimum remaining values (MRV heuristic)"""
        min_options = 10
        best_cell = None
        
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    options = sum(1 for num in range(1, 10) if self._is_valid(board, num, i, j))
                    if options < min_options:
                        min_options = options
                        best_cell = (i, j)
                        if options == 1:  # Best case
                            return best_cell
        
        return best_cell
    
    def _is_valid(self, board, num, row, col):
        """Check if number is valid in position"""
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
