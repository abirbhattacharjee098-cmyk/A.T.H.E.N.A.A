# ATHENA Virtual Assistant

ATHENA (Artificial Task Handling and Efficiency Navigator Assistant) is an advanced voice-activated AI desktop assistant for Windows.

## Features
- **Voice System**: Continuous listening via SpeechRecognition (configurable to use local Whisper or Google API) and PyTTSx3 for voice synthesis.
- **Desktop Automation**: Opens applications, types, clicks, and scrolls using PyAutoGUI.
- **Browser Automation**: Navigates the web and performs searches using Selenium.
- **Communication**: Sends emails via SMTP and WhatsApp messages via PyWhatKit.
- **Vision System**: Captures screen and performs OCR using OpenCV and PyTesseract.
- **Memory**: Remembers recent interactions in a local SQLite database (`memory.db`).

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) for Windows. Install it and note the path (default is `C:\Program Files\Tesseract-OCR\tesseract.exe`).

### 2. Installation
1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
   *(Note: `openai-whisper` will require PyTorch. If you prefer not to install PyTorch, you can remove `openai-whisper` from requirements and the system will fallback to Google's speech recognition API.)*

### 3. Configuration
1. Run `main.py` once. It will create a `config.json` file.
2. Open `config.json` and configure:
   - Your name (`user_name`)
   - Tesseract path (`tesseract_cmd`)
   - Email credentials (`email` block) if you want email functionality
   - Set `"use_whisper": true` if you have installed PyTorch and `openai-whisper`.

### 4. Running ATHENA
```cmd
python main.py
```
Wait for the "Online and ready" greeting, then speak your commands! Try saying "open notepad", "search google for latest news", or "what's on my screen". Say "goodbye" to exit.
