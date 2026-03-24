import cv2
import pytesseract
import pyautogui
import os

class VisionSystem:
    def __init__(self, config=None):
        self.config = config
        if config and config.get("tesseract_cmd"):
            pytesseract.pytesseract.tesseract_cmd = config.get("tesseract_cmd")
            
    def capture_screen(self, filename="screenshot.png"):
        """Capture the screen and save it."""
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return True, f"Screenshot saved as {filename}"
        except Exception as e:
            return False, f"Failed to capture screen: {e}"

    def read_text_from_image(self, image_path: str):
        """Extract text from an image using OCR."""
        try:
            if not os.path.exists(image_path):
                return False, f"Image {image_path} not found."
                
            img = cv2.imread(image_path)
            if img is None:
                return False, "Could not load image file."
            
            # Convert to grayscale for better OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            return True, text.strip()
        except Exception as e:
            return False, f"OCR failed: {e}. Ensure Tesseract is installed and path is set in config."

    def analyze_screen_text(self):
        """Capture screen and read text from it."""
        success, msg = self.capture_screen("temp_screen.png")
        if success:
            return self.read_text_from_image("temp_screen.png")
        return False, msg
