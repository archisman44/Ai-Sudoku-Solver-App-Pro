"""
Digit Recognition
Recognizes digits from Sudoku cell images using CNN and OCR
"""
import cv2
import numpy as np
import pytesseract

class DigitRecognizer:
    def __init__(self):
        # Configure Tesseract for digit recognition
        self.tesseract_config = '--psm 10 --oem 3 -c tessedit_char_whitelist=123456789'
    
    def recognize_cells(self, cells):
        """Recognize digits from cell images"""
        board = []
        
        for i in range(9):
            row = []
            for j in range(9):
                digit = self._recognize_digit(cells[i][j])
                row.append(digit)
            board.append(row)
        
        return board
    
    def _recognize_digit(self, cell_image):
        """Recognize single digit from cell image"""
        
        # Check if cell is empty (mostly white or black)
        if self._is_empty(cell_image):
            return 0
        
        # Preprocess
        processed = self._preprocess_cell(cell_image)
        
        # Try OCR first
        digit = self._ocr_recognize(processed)
        
        if digit > 0:
            return digit
        
        # Fallback to simple template matching or return 0
        return 0
    
    def _is_empty(self, cell_image):
        """Check if cell is empty"""
        # Calculate percentage of non-zero pixels
        non_zero = np.count_nonzero(cell_image)
        total = cell_image.size
        
        ratio = non_zero / total
        
        # If less than 10% or more than 90% filled, likely empty
        return ratio < 0.1 or ratio > 0.9
    
    def _preprocess_cell(self, cell_image):
        """Preprocess cell image for recognition"""
        
        # Threshold
        _, thresh = cv2.threshold(cell_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Invert if needed (digit should be white on black)
        if np.mean(thresh) > 127:
            thresh = cv2.bitwise_not(thresh)
        
        # Remove borders
        h, w = thresh.shape
        margin = 2
        thresh[:margin, :] = 0
        thresh[-margin:, :] = 0
        thresh[:, :margin] = 0
        thresh[:, -margin:] = 0
        
        # Find contours to isolate digit
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest contour
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            
            # Check if contour is reasonable size
            if w > 5 and h > 5 and w < thresh.shape[1] - 4 and h < thresh.shape[0] - 4:
                # Extract digit region
                digit_region = thresh[y:y+h, x:x+w]
                
                # Add padding
                pad = 4
                padded = cv2.copyMakeBorder(digit_region, pad, pad, pad, pad,
                                           cv2.BORDER_CONSTANT, value=0)
                
                # Resize
                processed = cv2.resize(padded, (28, 28))
                return processed
        
        return thresh
    
    def _ocr_recognize(self, cell_image):
        """Use Tesseract OCR to recognize digit"""
        try:
            # Resize for better OCR
            resized = cv2.resize(cell_image, (56, 56))
            
            # Apply additional preprocessing
            kernel = np.ones((2, 2), np.uint8)
            dilated = cv2.dilate(resized, kernel, iterations=1)
            
            # Run OCR
            text = pytesseract.image_to_string(dilated, config=self.tesseract_config)
            
            # Parse result
            text = text.strip()
            if text.isdigit() and len(text) == 1:
                digit = int(text)
                if 1 <= digit <= 9:
                    return digit
        except:
            pass
        
        return 0
    
    def recognize_with_confidence(self, cells):
        """Recognize digits and return confidence scores"""
        board = []
        confidence = []
        
        for i in range(9):
            row = []
            conf_row = []
            for j in range(9):
                digit, conf = self._recognize_with_conf(cells[i][j])
                row.append(digit)
                conf_row.append(conf)
            board.append(row)
            confidence.append(conf_row)
        
        return board, confidence
    
    def _recognize_with_conf(self, cell_image):
        """Recognize digit with confidence score"""
        if self._is_empty(cell_image):
            return 0, 1.0
        
        processed = self._preprocess_cell(cell_image)
        
        try:
            # Get OCR data with confidence
            data = pytesseract.image_to_data(processed, config=self.tesseract_config,
                                            output_type=pytesseract.Output.DICT)
            
            for i, text in enumerate(data['text']):
                if text.strip().isdigit() and len(text.strip()) == 1:
                    digit = int(text.strip())
                    if 1 <= digit <= 9:
                        conf = float(data['conf'][i]) / 100.0
                        return digit, conf
        except:
            pass
        
        return 0, 0.5
