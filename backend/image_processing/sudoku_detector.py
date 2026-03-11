"""
Sudoku Grid Detector
Detects and extracts Sudoku grid from images using OpenCV
"""
import cv2
import numpy as np

class SudokuDetector:
    def detect_grid(self, image_path):
        """Detect and extract Sudoku grid from image"""
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return None, None
        
        # Preprocess
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find largest contour (should be the grid)
        if not contours:
            return None, None
        
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding rectangle
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        
        # If we have 4 corners, it's likely the grid
        if len(approx) == 4:
            grid_corners = self._order_points(approx.reshape(4, 2))
            warped = self._warp_perspective(gray, grid_corners)
            
            # Extract cells
            cells = self._extract_cells(warped)
            
            return warped, cells
        
        # Fallback: use bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Make it square
        size = max(w, h)
        grid = gray[y:y+size, x:x+size]
        
        if grid.size == 0:
            return None, None
        
        # Resize to standard size
        grid = cv2.resize(grid, (450, 450))
        cells = self._extract_cells(grid)
        
        return grid, cells
    
    def _order_points(self, pts):
        """Order points in top-left, top-right, bottom-right, bottom-left order"""
        rect = np.zeros((4, 2), dtype=np.float32)
        
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect
    
    def _warp_perspective(self, image, corners):
        """Warp perspective to get top-down view"""
        (tl, tr, br, bl) = corners
        
        # Compute width
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        
        # Compute height
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        
        # Destination points
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype=np.float32)
        
        # Compute perspective transform
        M = cv2.getPerspectiveTransform(corners, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        
        return warped
    
    def _extract_cells(self, grid):
        """Extract individual cells from grid"""
        cells = []
        
        # Ensure grid is square and proper size
        if grid.shape[0] != grid.shape[1]:
            size = min(grid.shape[0], grid.shape[1])
            grid = grid[:size, :size]
        
        if grid.shape[0] < 90:
            grid = cv2.resize(grid, (450, 450))
        
        cell_size = grid.shape[0] // 9
        
        for i in range(9):
            row_cells = []
            for j in range(9):
                # Extract cell with margin
                y1 = i * cell_size + 2
                y2 = (i + 1) * cell_size - 2
                x1 = j * cell_size + 2
                x2 = (j + 1) * cell_size - 2
                
                cell = grid[y1:y2, x1:x2]
                
                if cell.size > 0:
                    # Resize to standard size
                    cell = cv2.resize(cell, (28, 28))
                    row_cells.append(cell)
                else:
                    row_cells.append(np.zeros((28, 28), dtype=np.uint8))
            
            cells.append(row_cells)
        
        return cells
