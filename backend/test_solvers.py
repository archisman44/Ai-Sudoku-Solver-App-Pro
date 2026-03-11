"""
Test script to verify all solvers work correctly
"""
import sys
sys.path.append('.')

from solver.backtracking_solver import BacktrackingSolver
from solver.constraint_solver import ConstraintSolver
from solver.dancing_links_solver import DancingLinksSolver
from solver.heuristic_solver import HeuristicSolver
from solver.difficulty_analyzer import DifficultyAnalyzer
from solver.puzzle_generator import PuzzleGenerator

# Test puzzle (easy)
test_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Hard puzzle
hard_puzzle = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

def print_board(board):
    """Print board in readable format"""
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        row_str = ""
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(cell) + " "
        print(row_str)

def test_solver(name, solver, puzzle):
    """Test a solver"""
    print(f"\n{'='*50}")
    print(f"Testing {name}")
    print('='*50)
    
    board = [row[:] for row in puzzle]
    
    try:
        success, solved, steps, calls = solver.solve(board, visualize=False)
        
        if success:
            print(f"✓ {name} PASSED")
            print(f"  Recursive calls: {calls}")
            print(f"  Steps: {len(steps)}")
            print("\nSolved board:")
            print_board(solved)
        else:
            print(f"✗ {name} FAILED - No solution found")
    except Exception as e:
        print(f"✗ {name} ERROR: {str(e)}")

def test_generator():
    """Test puzzle generator"""
    print(f"\n{'='*50}")
    print("Testing Puzzle Generator")
    print('='*50)
    
    generator = PuzzleGenerator()
    
    for difficulty in ['easy', 'medium', 'hard', 'expert', 'extreme']:
        try:
            puzzle = generator.generate(difficulty)
            clues = sum(1 for row in puzzle for cell in row if cell != 0)
            print(f"✓ Generated {difficulty} puzzle with {clues} clues")
        except Exception as e:
            print(f"✗ Failed to generate {difficulty}: {str(e)}")

def test_analyzer():
    """Test difficulty analyzer"""
    print(f"\n{'='*50}")
    print("Testing Difficulty Analyzer")
    print('='*50)
    
    analyzer = DifficultyAnalyzer()
    
    try:
        analysis = analyzer.analyze(test_puzzle)
        print(f"✓ Easy puzzle analysis:")
        print(f"  Difficulty: {analysis['difficulty']}")
        print(f"  Score: {analysis['score']}")
        print(f"  Clues: {analysis['clues']}")
        print(f"  Techniques: {', '.join(analysis['techniques'])}")
        
        analysis = analyzer.analyze(hard_puzzle)
        print(f"\n✓ Hard puzzle analysis:")
        print(f"  Difficulty: {analysis['difficulty']}")
        print(f"  Score: {analysis['score']}")
        print(f"  Clues: {analysis['clues']}")
        print(f"  Techniques: {', '.join(analysis['techniques'])}")
    except Exception as e:
        print(f"✗ Analyzer ERROR: {str(e)}")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("AI SUDOKU SOLVER PRO - TEST SUITE")
    print("="*50)
    
    print("\nOriginal puzzle:")
    print_board(test_puzzle)
    
    # Test all solvers
    test_solver("Backtracking Solver", BacktrackingSolver(), test_puzzle)
    test_solver("Constraint Solver", ConstraintSolver(), test_puzzle)
    test_solver("Dancing Links Solver", DancingLinksSolver(), test_puzzle)
    test_solver("Heuristic Solver", HeuristicSolver(), test_puzzle)
    
    # Test hard puzzle with backtracking
    print("\n\nTesting with HARD puzzle:")
    print_board(hard_puzzle)
    test_solver("Backtracking Solver (Hard)", BacktrackingSolver(), hard_puzzle)
    
    # Test generator
    test_generator()
    
    # Test analyzer
    test_analyzer()
    
    print("\n" + "="*50)
    print("TEST SUITE COMPLETE")
    print("="*50 + "\n")
