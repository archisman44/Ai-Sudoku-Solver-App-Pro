"""
Dancing Links (Algorithm X) Solver
Implements Knuth's Algorithm X with Dancing Links for exact cover
"""

class DancingLinksSolver:
    def __init__(self):
        self.steps = []
        self.recursive_calls = 0
        self.solution = []
        
    def solve(self, board, visualize=False):
        """Solve using Dancing Links Algorithm X"""
        self.steps = []
        self.recursive_calls = 0
        self.visualize = visualize
        self.solution = []
        
        # Convert to exact cover problem
        cover_matrix = self._build_cover_matrix(board)
        
        # Solve using Algorithm X
        if self._algorithm_x(cover_matrix):
            self._apply_solution(board)
            return True, board, self.steps, self.recursive_calls
        
        return False, board, self.steps, self.recursive_calls
    
    def _build_cover_matrix(self, board):
        """Build exact cover matrix for Sudoku"""
        # 324 constraints: 81 cells + 81 rows + 81 cols + 81 boxes
        matrix = []
        
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    # Fixed cell
                    num = board[row][col]
                    matrix.append(self._make_constraint_row(row, col, num))
                else:
                    # Try all numbers
                    for num in range(1, 10):
                        matrix.append(self._make_constraint_row(row, col, num))
        
        return matrix
    
    def _make_constraint_row(self, row, col, num):
        """Create constraint row for position and number"""
        constraint = [0] * 324
        
        # Cell constraint
        constraint[row * 9 + col] = 1
        
        # Row constraint
        constraint[81 + row * 9 + (num - 1)] = 1
        
        # Column constraint
        constraint[162 + col * 9 + (num - 1)] = 1
        
        # Box constraint
        box = (row // 3) * 3 + (col // 3)
        constraint[243 + box * 9 + (num - 1)] = 1
        
        return {
            'row': row,
            'col': col,
            'num': num,
            'constraints': constraint
        }
    
    def _algorithm_x(self, matrix, solution=[]):
        """Recursive Algorithm X implementation"""
        self.recursive_calls += 1
        
        if not matrix:
            self.solution = solution[:]
            return True
        
        # Choose column with minimum options
        col_counts = [sum(row['constraints'][i] for row in matrix) for i in range(324)]
        
        # Find uncovered column with minimum count
        min_col = -1
        min_count = float('inf')
        for i in range(324):
            if col_counts[i] > 0 and col_counts[i] < min_count:
                min_count = col_counts[i]
                min_col = i
        
        if min_col == -1:
            return False
        
        # Try each row that covers this column
        for row in matrix[:]:
            if row['constraints'][min_col] == 1:
                # Select this row
                solution.append(row)
                
                if self.visualize:
                    self.steps.append({
                        'row': row['row'],
                        'col': row['col'],
                        'value': row['num'],
                        'action': 'place'
                    })
                
                # Remove covered columns
                new_matrix = self._cover(matrix, row)
                
                if self._algorithm_x(new_matrix, solution):
                    return True
                
                # Backtrack
                solution.pop()
        
        return False
    
    def _cover(self, matrix, selected_row):
        """Remove rows that conflict with selected row"""
        new_matrix = []
        
        for row in matrix:
            # Skip if any constraint overlaps
            conflict = False
            for i in range(324):
                if selected_row['constraints'][i] == 1 and row['constraints'][i] == 1:
                    conflict = True
                    break
            
            if not conflict:
                new_matrix.append(row)
        
        return new_matrix
    
    def _apply_solution(self, board):
        """Apply solution to board"""
        for row_data in self.solution:
            board[row_data['row']][row_data['col']] = row_data['num']
