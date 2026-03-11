"""
Heuristic Solver using human-like strategies
Implements various Sudoku solving techniques
"""

class HeuristicSolver:
    def __init__(self):
        self.steps = []
        self.recursive_calls = 0
        
    def solve(self, board, visualize=False):
        """Solve using human-like heuristics"""
        self.steps = []
        self.recursive_calls = 0
        self.visualize = visualize
        
        candidates = self._init_candidates(board)
        
        max_iterations = 100
        for _ in range(max_iterations):
            progress = False
            
            # Apply techniques in order of complexity
            if self._naked_singles(board, candidates):
                progress = True
            
            if self._hidden_singles(board, candidates):
                progress = True
            
            if self._naked_pairs(board, candidates):
                progress = True
            
            if self._pointing_pairs(board, candidates):
                progress = True
            
            if self._is_solved(board):
                return True, board, self.steps, self.recursive_calls
            
            if not progress:
                # Fall back to guessing
                return self._guess_and_check(board, candidates)
        
        return False, board, self.steps, self.recursive_calls
    
    def _init_candidates(self, board):
        """Initialize candidates for each cell"""
        candidates = [[set(range(1, 10)) if board[i][j] == 0 else set() 
                      for j in range(9)] for i in range(9)]
        
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self._eliminate_from_peers(candidates, i, j, board[i][j])
        
        return candidates
    
    def _eliminate_from_peers(self, candidates, row, col, num):
        """Remove number from all peers"""
        for j in range(9):
            candidates[row][j].discard(num)
        for i in range(9):
            candidates[i][col].discard(num)
        
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                candidates[i][j].discard(num)
    
    def _naked_singles(self, board, candidates):
        """Find cells with only one candidate"""
        found = False
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and len(candidates[i][j]) == 1:
                    num = list(candidates[i][j])[0]
                    board[i][j] = num
                    self._eliminate_from_peers(candidates, i, j, num)
                    found = True
                    
                    if self.visualize:
                        self.steps.append({
                            'row': i, 'col': j, 'value': num,
                            'action': 'naked_single',
                            'reason': 'Only one possible value'
                        })
        return found
    
    def _hidden_singles(self, board, candidates):
        """Find numbers that can only go in one place"""
        found = False
        
        # Rows
        for i in range(9):
            for num in range(1, 10):
                positions = [j for j in range(9) if num in candidates[i][j]]
                if len(positions) == 1:
                    j = positions[0]
                    if board[i][j] == 0:
                        board[i][j] = num
                        candidates[i][j] = set()
                        self._eliminate_from_peers(candidates, i, j, num)
                        found = True
                        
                        if self.visualize:
                            self.steps.append({
                                'row': i, 'col': j, 'value': num,
                                'action': 'hidden_single',
                                'reason': f'Only place for {num} in row {i+1}'
                            })
        
        # Columns
        for j in range(9):
            for num in range(1, 10):
                positions = [i for i in range(9) if num in candidates[i][j]]
                if len(positions) == 1:
                    i = positions[0]
                    if board[i][j] == 0:
                        board[i][j] = num
                        candidates[i][j] = set()
                        self._eliminate_from_peers(candidates, i, j, num)
                        found = True
                        
                        if self.visualize:
                            self.steps.append({
                                'row': i, 'col': j, 'value': num,
                                'action': 'hidden_single',
                                'reason': f'Only place for {num} in column {j+1}'
                            })
        
        # Boxes
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
                            candidates[i][j] = set()
                            self._eliminate_from_peers(candidates, i, j, num)
                            found = True
                            
                            if self.visualize:
                                self.steps.append({
                                    'row': i, 'col': j, 'value': num,
                                    'action': 'hidden_single',
                                    'reason': f'Only place for {num} in box'
                                })
        
        return found
    
    def _naked_pairs(self, board, candidates):
        """Find and eliminate naked pairs"""
        found = False
        
        # Check rows
        for i in range(9):
            cells = [(j, candidates[i][j]) for j in range(9) if len(candidates[i][j]) == 2]
            for idx1 in range(len(cells)):
                for idx2 in range(idx1 + 1, len(cells)):
                    if cells[idx1][1] == cells[idx2][1]:
                        pair = cells[idx1][1]
                        for j in range(9):
                            if j != cells[idx1][0] and j != cells[idx2][0]:
                                before = len(candidates[i][j])
                                candidates[i][j] -= pair
                                if len(candidates[i][j]) < before:
                                    found = True
        
        return found
    
    def _pointing_pairs(self, board, candidates):
        """Find pointing pairs/triples"""
        found = False
        
        for box_i in range(3):
            for box_j in range(3):
                for num in range(1, 10):
                    positions = []
                    for i in range(box_i * 3, box_i * 3 + 3):
                        for j in range(box_j * 3, box_j * 3 + 3):
                            if num in candidates[i][j]:
                                positions.append((i, j))
                    
                    if len(positions) in [2, 3]:
                        # Check if all in same row
                        if len(set(p[0] for p in positions)) == 1:
                            row = positions[0][0]
                            for j in range(9):
                                if (row, j) not in positions:
                                    if num in candidates[row][j]:
                                        candidates[row][j].discard(num)
                                        found = True
                        
                        # Check if all in same column
                        if len(set(p[1] for p in positions)) == 1:
                            col = positions[0][1]
                            for i in range(9):
                                if (i, col) not in positions:
                                    if num in candidates[i][col]:
                                        candidates[i][col].discard(num)
                                        found = True
        
        return found
    
    def _guess_and_check(self, board, candidates):
        """Fallback to guessing with backtracking"""
        self.recursive_calls += 1
        
        if self._is_solved(board):
            return True, board, self.steps, self.recursive_calls
        
        # Find cell with minimum candidates
        min_len = 10
        best_cell = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and 0 < len(candidates[i][j]) < min_len:
                    min_len = len(candidates[i][j])
                    best_cell = (i, j)
        
        if not best_cell:
            return False, board, self.steps, self.recursive_calls
        
        i, j = best_cell
        
        for num in list(candidates[i][j]):
            board_copy = [row[:] for row in board]
            cand_copy = [[cell.copy() for cell in row] for row in candidates]
            
            board[i][j] = num
            candidates[i][j] = set()
            self._eliminate_from_peers(candidates, i, j, num)
            
            if self.visualize:
                self.steps.append({
                    'row': i, 'col': j, 'value': num,
                    'action': 'guess',
                    'reason': 'Trying possible value'
                })
            
            result = self._guess_and_check(board, candidates)
            if result[0]:
                return result
            
            # Restore
            for x in range(9):
                for y in range(9):
                    board[x][y] = board_copy[x][y]
                    candidates[x][y] = cand_copy[x][y]
        
        return False, board, self.steps, self.recursive_calls
    
    def _is_solved(self, board):
        """Check if puzzle is solved"""
        return all(board[i][j] != 0 for i in range(9) for j in range(9))
