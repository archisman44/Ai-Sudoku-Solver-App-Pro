"""
Flask Backend API for AI Sudoku Solver Pro
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
import base64
from io import BytesIO
from PIL import Image

from solver.backtracking_solver import BacktrackingSolver
from solver.constraint_solver import ConstraintSolver
from solver.dancing_links_solver import DancingLinksSolver
from solver.heuristic_solver import HeuristicSolver
from solver.difficulty_analyzer import DifficultyAnalyzer
from solver.puzzle_generator import PuzzleGenerator
from image_processing.sudoku_detector import SudokuDetector
from image_processing.digit_recognition import DigitRecognizer

app = Flask(__name__)
CORS(app)

# Initialize solvers
solvers = {
    'backtracking': BacktrackingSolver(),
    'constraint': ConstraintSolver(),
    'dancing_links': DancingLinksSolver(),
    'heuristic': HeuristicSolver()
}

analyzer = DifficultyAnalyzer()
generator = PuzzleGenerator()
detector = SudokuDetector()
recognizer = DigitRecognizer()

@app.route('/api/solve', methods=['POST'])
def solve():
    """Solve Sudoku puzzle"""
    try:
        data = request.json
        board = data.get('board')
        algorithm = data.get('algorithm', 'backtracking')
        visualize = data.get('visualize', False)
        
        if not board or len(board) != 9 or any(len(row) != 9 for row in board):
            return jsonify({'error': 'Invalid board format'}), 400
        
        # Get solver
        solver = solvers.get(algorithm)
        if not solver:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        # Solve
        start_time = time.time()
        success, solved_board, steps, recursive_calls = solver.solve(
            [row[:] for row in board], visualize
        )
        solve_time = time.time() - start_time
        
        if success:
            return jsonify({
                'success': True,
                'board': solved_board,
                'steps': steps if visualize else [],
                'algorithm': algorithm,
                'time': round(solve_time, 4),
                'recursive_calls': recursive_calls
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No solution found'
            }), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate Sudoku puzzle"""
    try:
        data = request.json
        difficulty = data.get('difficulty', 'medium')
        
        puzzle = generator.generate(difficulty)
        
        # Analyze difficulty
        analysis = analyzer.analyze(puzzle)
        
        return jsonify({
            'success': True,
            'puzzle': puzzle,
            'difficulty': analysis['difficulty'],
            'clues': analysis['clues']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze puzzle difficulty"""
    try:
        data = request.json
        board = data.get('board')
        
        if not board or len(board) != 9 or any(len(row) != 9 for row in board):
            return jsonify({'error': 'Invalid board format'}), 400
        
        analysis = analyzer.analyze(board)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scan-image', methods=['POST'])
def scan_image():
    """Scan Sudoku from image"""
    try:
        # Get image from request
        if 'image' not in request.files:
            # Try base64
            data = request.json
            if 'image' in data:
                # Decode base64
                image_data = base64.b64decode(data['image'].split(',')[1])
                image = Image.open(BytesIO(image_data))
                
                # Save temporarily
                temp_path = 'temp_sudoku.png'
                image.save(temp_path)
            else:
                return jsonify({'error': 'No image provided'}), 400
        else:
            file = request.files['image']
            temp_path = 'temp_sudoku.png'
            file.save(temp_path)
        
        # Detect grid
        grid, cells = detector.detect_grid(temp_path)
        
        if grid is None or cells is None:
            return jsonify({'error': 'Could not detect Sudoku grid'}), 400
        
        # Recognize digits
        board = recognizer.recognize_cells(cells)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'board': board
        })
    
    except Exception as e:
        # Clean up
        if os.path.exists('temp_sudoku.png'):
            os.remove('temp_sudoku.png')
        return jsonify({'error': str(e)}), 500

@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """Get available algorithms"""
    return jsonify({
        'algorithms': [
            {
                'id': 'backtracking',
                'name': 'Backtracking',
                'description': 'Classic recursive backtracking with MRV heuristic'
            },
            {
                'id': 'constraint',
                'name': 'Constraint Propagation',
                'description': 'Uses constraint propagation with naked and hidden singles'
            },
            {
                'id': 'dancing_links',
                'name': 'Dancing Links (Algorithm X)',
                'description': 'Knuth\'s Algorithm X with Dancing Links for exact cover'
            },
            {
                'id': 'heuristic',
                'name': 'Heuristic Solver',
                'description': 'Human-like solving strategies with multiple techniques'
            }
        ]
    })

@app.route('/api/hint', methods=['POST'])
def get_hint():
    """Get hint for next move"""
    try:
        data = request.json
        board = data.get('board')
        
        if not board:
            return jsonify({'error': 'No board provided'}), 400
        
        # Use constraint solver to find next move
        solver = ConstraintSolver()
        candidates = solver._init_candidates(board)
        
        # Find naked single
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and len(candidates[i][j]) == 1:
                    num = list(candidates[i][j])[0]
                    return jsonify({
                        'success': True,
                        'hint': {
                            'row': i,
                            'col': j,
                            'value': num,
                            'reason': 'Naked single - only one possible value',
                            'candidates': list(candidates[i][j])
                        }
                    })
        
        # Find cell with minimum candidates
        min_len = 10
        best_cell = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and 0 < len(candidates[i][j]) < min_len:
                    min_len = len(candidates[i][j])
                    best_cell = (i, j)
        
        if best_cell:
            i, j = best_cell
            return jsonify({
                'success': True,
                'hint': {
                    'row': i,
                    'col': j,
                    'value': None,
                    'reason': f'Consider this cell - {min_len} possible values',
                    'candidates': list(candidates[i][j])
                }
            })
        
        return jsonify({
            'success': False,
            'error': 'No hints available'
        }), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate', methods=['POST'])
def validate():
    """Validate current board state"""
    try:
        data = request.json
        board = data.get('board')
        
        if not board:
            return jsonify({'error': 'No board provided'}), 400
        
        errors = []
        
        # Check rows
        for i in range(9):
            seen = set()
            for j in range(9):
                if board[i][j] != 0:
                    if board[i][j] in seen:
                        errors.append({
                            'type': 'row',
                            'row': i,
                            'col': j,
                            'value': board[i][j]
                        })
                    seen.add(board[i][j])
        
        # Check columns
        for j in range(9):
            seen = set()
            for i in range(9):
                if board[i][j] != 0:
                    if board[i][j] in seen:
                        errors.append({
                            'type': 'column',
                            'row': i,
                            'col': j,
                            'value': board[i][j]
                        })
                    seen.add(board[i][j])
        
        # Check boxes
        for box_i in range(3):
            for box_j in range(3):
                seen = set()
                for i in range(box_i * 3, box_i * 3 + 3):
                    for j in range(box_j * 3, box_j * 3 + 3):
                        if board[i][j] != 0:
                            if board[i][j] in seen:
                                errors.append({
                                    'type': 'box',
                                    'row': i,
                                    'col': j,
                                    'value': board[i][j]
                                })
                            seen.add(board[i][j])
        
        return jsonify({
            'valid': len(errors) == 0,
            'errors': errors
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
