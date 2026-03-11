"""
Constraint Propagation Solver
Uses naked singles, hidden singles, and constraint propagation
"""

class ConstraintSolver:
    def __init__(self):
        self.steps = []
        self.recursive_calls = 0
        
    def solve(self, board, visualize=False):
        """Solve using constraint propagation"""
        self.steps = []
        self.recursive_calls = 0
        self.visualize = visualize
        
        # Initialize candidates
        candidates = self._init_candidates(board)
        
        # Propagate constraints
        if not self._propagate(board, candidates):
            return False, board, self.steps, self.recursive_calls
        
        # Check if solved
        if self._is_solved(board):
            return True, board, self.steps, self.recursive_calls
        
        # Use backtracking with propagation
        if self._search(board, candidates):
            return True, board, self.steps, self.recursive_calls
        
        return False, board, self.steps, self.recursive_calls
    
    def _init_candidates(self, board):
        """Initialize candidate sets for each cell"""
        candidates = [[set(range(1, 10)) if board[i][j] == 0 else set() 
                      for j in range(9)] for i in range(9)]
        
        # Remove candidates based on initial values
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self._eliminate(candidates, i, j, board[i][j])
        
        return candidates
    
    def _eliminate(self, candidates, row, col, num):
        """Eliminate number from peers"""
        # Row
        for j in range(9):
            candidates[row][j].discard(num)
        
        # Column
        for i in range(9):
            candidates[i][col].discard(num)
        
        # Box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                candidates[i][j].discard(num)
    
    def _propagate(self, board, candidates):
        """Propagate constraints until no more changes"""
        changed = True
        while changed:
            changed = False
            
            # Naked singles
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0 and len(candidates[i][j]) == 1:
                        num = list(candidates[i][j])[0]
                        board[i][j] = num
                        self._eliminate(candidates, i, j, num)
                        changed = True
                        
                        if self.visualize:
                            self.steps.append({
                                'row': i, 'col': j, 'value': num,
                                'action': 'naked_single'
                            })
                    
                    elif board[i][j] == 0 and len(candidates[i][j]) == 0:
                        return False  # Invalid state
            
            # Hidden singles
            if self._find_hidden_singles(board, candidates):
                changed = True
        
        return True
    
    def _find_hidden_singles(self, board, candidates):
        """Find hidden singles in rows, columns, and boxes"""
        found = False
        
        # Check rows
        for i in range(9):
            for num in range(1, 10):
                positions = [j for j in range(9) if num in candidates[i][j]]
                if len(positions) == 1:
                    j = positions[0]
                    if board[i][j] == 0:
                        board[i][j] = num
                        self._eliminate(candidates, i, j, num)
                        found = True
                        
                        if self.visualize:
                            self.steps.append({
                                'row': i, 'col': j, 'value': num,
                                'action': 'hidden_single_row'
                            })
        
        # Check columns
        for j in range(9):
            for num in range(1, 10):
                positions = [i for i in range(9) if num in candidates[i][j]]
                if len(positions) == 1:
                    i = positions[0]
                    if board[i][j] == 0:
                        board[i][j] = num
                        self._eliminate(candidates, i, j, num)
                        found = True
                        
                        if self.visualize:
                            self.steps.append({
                                'row': i, 'col': j, 'value': num,
                                'action': 'hidden_single_col'
                            })
        
        # Check boxes
        for box_i in range(3):
            for box_j in range(3):
                for num in range(1, 10):
                    positions = []
                    for i in range(box_i * 3, box_i * 3 + 3):
                        for j in range(box_j * 3, box_j * 3 + 3):
                            if num in candidates[i][j]:
                                positions.append((i, j))
                    
                    if len(positions) == 1:
                        i, j = positions[0]
                        if board[i][j] == 0:
                            board[i][j] = num
                            self._eliminate(candidates, i, j, num)
                            found = True
                            
                            if self.visualize:
                                self.steps.append({
                                    'row': i, 'col': j, 'value': num,
                                    'action': 'hidden_single_box'
                                })
        
        return found
    
    def _search(self, board, candidates):
        """Backtracking search with constraint propagation"""
        self.recursive_calls += 1
        
        if self._is_solved(board):
            return True
        
        # Find cell with minimum candidates
        min_len = 10
        best_cell = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and len(candidates[i][j]) < min_len:
                    min_len = len(candidates[i][j])
                    best_cell = (i, j)
        
        if not best_cell:
            return False
        
        i, j = best_cell
        
        for num in list(candidates[i][j]):
            # Save state
            board_copy = [row[:] for row in board]
            cand_copy = [[cell.copy() for cell in row] for row in candidates]
            
            # Try number
            board[i][j] = num
            self._eliminate(candidates, i, j, num)
            
            if self.visualize:
                self.steps.append({
                    'row': i, 'col': j, 'value': num,
                    'action': 'search'
                })
            
            if self._propagate(board, candidates) and self._search(board, candidates):
                return True
            
            # Restore state
            for x in range(9):
                for y in range(9):
                    board[x][y] = board_copy[x][y]
                    candidates[x][y] = cand_copy[x][y]
        
        return False
    
    def _is_solved(self, board):
        """Check if board is completely filled"""
        return all(board[i][j] != 0 for i in range(9) for j in range(9))
