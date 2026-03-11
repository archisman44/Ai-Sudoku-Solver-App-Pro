"""
Sudoku Puzzle Generator
Generates valid Sudoku puzzles with unique solutions
"""
import random
from .backtracking_solver import BacktrackingSolver

class PuzzleGenerator:
    def __init__(self):
        self.solver = BacktrackingSolver()
    
    def generate(self, difficulty='medium'):
        """Generate a puzzle of specified difficulty"""
        
        # Generate complete solved board
        board = self._generate_complete_board()
        
        # Remove numbers based on difficulty
        clues = self._get_clues_for_difficulty(difficulty)
        puzzle = self._remove_numbers(board, clues)
        
        return puzzle
    
    def _generate_complete_board(self):
        """Generate a complete valid Sudoku board"""
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill diagonal 3x3 boxes first (they're independent)
        for box in range(0, 9, 3):
            self._fill_box(board, box, box)
        
        # Solve the rest
        self.solver.solve(board)
        
        return board
    
    def _fill_box(self, board, row, col):
        """Fill a 3x3 box with random numbers"""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        idx = 0
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = numbers[idx]
                idx += 1
    
    def _get_clues_for_difficulty(self, difficulty):
        """Get number of clues based on difficulty"""
        clues_map = {
            'easy': random.randint(36, 40),
            'medium': random.randint(30, 35),
            'hard': random.randint(25, 29),
            'expert': random.randint(22, 24),
            'extreme': random.randint(17, 21)
        }
        return clues_map.get(difficulty.lower(), 30)
    
    def _remove_numbers(self, board, target_clues):
        """Remove numbers while maintaining unique solution"""
        puzzle = [row[:] for row in board]
        
        # Get all positions
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        removed = 0
        max_removals = 81 - target_clues
        
        for row, col in positions:
            if removed >= max_removals:
                break
            
            # Save value
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            
            # Check if still has unique solution
            if self._has_unique_solution(puzzle):
                removed += 1
            else:
                # Restore
                puzzle[row][col] = backup
        
        return puzzle
    
    def _has_unique_solution(self, board):
        """Check if puzzle has exactly one solution"""
        solutions = []
        self._count_solutions([row[:] for row in board], solutions, max_solutions=2)
        return len(solutions) == 1
    
    def _count_solutions(self, board, solutions, max_solutions=2):
        """Count number of solutions (up to max)"""
        if len(solutions) >= max_solutions:
            return
        
        # Find empty cell
        empty = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    empty = (i, j)
                    break
            if empty:
                break
        
        if not empty:
            # Found a solution
            solutions.append([row[:] for row in board])
            return
        
        row, col = empty
        
        for num in range(1, 10):
            if self._is_valid(board, num, row, col):
                board[row][col] = num
                self._count_solutions(board, solutions, max_solutions)
                board[row][col] = 0
    
    def _is_valid(self, board, num, row, col):
        """Check if number is valid in position"""
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        
        # Check box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
