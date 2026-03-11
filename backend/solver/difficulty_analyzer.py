"""
Difficulty Analyzer
Analyzes Sudoku puzzle complexity and assigns difficulty rating
"""

class DifficultyAnalyzer:
    def analyze(self, board):
        """Analyze puzzle difficulty"""
        
        # Count clues
        clues = sum(1 for i in range(9) for j in range(9) if board[i][j] != 0)
        
        # Calculate branching factor
        branching = self._calculate_branching(board)
        
        # Determine required techniques
        techniques = self._required_techniques(board)
        
        # Calculate difficulty score
        score = self._calculate_score(clues, branching, techniques)
        
        # Classify difficulty
        difficulty = self._classify(score, clues)
        
        return {
            'difficulty': difficulty,
            'score': score,
            'clues': clues,
            'branching_factor': branching,
            'techniques': techniques
        }
    
    def _calculate_branching(self, board):
        """Calculate average branching factor"""
        candidates = self._get_candidates(board)
        
        empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
        
        if not empty_cells:
            return 0
        
        total_candidates = sum(len(candidates[i][j]) for i, j in empty_cells)
        return total_candidates / len(empty_cells)
    
    def _get_candidates(self, board):
        """Get possible candidates for each cell"""
        candidates = [[set(range(1, 10)) if board[i][j] == 0 else set() 
                      for j in range(9)] for i in range(9)]
        
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    num = board[i][j]
                    # Eliminate from row
                    for k in range(9):
                        candidates[i][k].discard(num)
                    # Eliminate from column
                    for k in range(9):
                        candidates[k][j].discard(num)
                    # Eliminate from box
                    box_row, box_col = 3 * (i // 3), 3 * (j // 3)
                    for x in range(box_row, box_row + 3):
                        for y in range(box_col, box_col + 3):
                            candidates[x][y].discard(num)
        
        return candidates
    
    def _required_techniques(self, board):
        """Determine which solving techniques are required"""
        techniques = []
        
        candidates = self._get_candidates(board)
        
        # Check for naked singles
        if any(len(candidates[i][j]) == 1 for i in range(9) for j in range(9) if board[i][j] == 0):
            techniques.append('naked_singles')
        
        # Check for hidden singles
        if self._has_hidden_singles(board, candidates):
            techniques.append('hidden_singles')
        
        # Check if needs advanced techniques
        if self._needs_advanced(board, candidates):
            techniques.append('advanced_techniques')
        
        # Check if needs guessing
        if not techniques or self._needs_guessing(board):
            techniques.append('backtracking')
        
        return techniques
    
    def _has_hidden_singles(self, board, candidates):
        """Check if puzzle has hidden singles"""
        # Check rows
        for i in range(9):
            for num in range(1, 10):
                count = sum(1 for j in range(9) if num in candidates[i][j])
                if count == 1:
                    return True
        return False
    
    def _needs_advanced(self, board, candidates):
        """Check if advanced techniques are needed"""
        # Simple heuristic: if average candidates > 4
        empty = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
        if not empty:
            return False
        
        avg = sum(len(candidates[i][j]) for i, j in empty) / len(empty)
        return avg > 4
    
    def _needs_guessing(self, board):
        """Check if puzzle needs guessing/backtracking"""
        # Puzzles with very few clues typically need guessing
        clues = sum(1 for i in range(9) for j in range(9) if board[i][j] != 0)
        return clues < 25
    
    def _calculate_score(self, clues, branching, techniques):
        """Calculate difficulty score"""
        score = 0
        
        # Clue-based scoring (fewer clues = harder)
        if clues >= 40:
            score += 10
        elif clues >= 32:
            score += 30
        elif clues >= 27:
            score += 50
        elif clues >= 22:
            score += 70
        else:
            score += 90
        
        # Branching factor scoring
        score += int(branching * 5)
        
        # Technique-based scoring
        if 'naked_singles' in techniques:
            score += 5
        if 'hidden_singles' in techniques:
            score += 15
        if 'advanced_techniques' in techniques:
            score += 30
        if 'backtracking' in techniques:
            score += 25
        
        return min(score, 100)
    
    def _classify(self, score, clues):
        """Classify difficulty based on score"""
        if score < 20:
            return 'Easy'
        elif score < 40:
            return 'Medium'
        elif score < 60:
            return 'Hard'
        elif score < 80:
            return 'Expert'
        else:
            return 'Extreme'
