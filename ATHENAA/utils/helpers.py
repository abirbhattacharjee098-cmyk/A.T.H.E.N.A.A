import json
import os
import sqlite3
from typing import Dict, Any

class MemoryLayer:
    def __init__(self, db_path='memory.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_input TEXT,
                athena_response TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_keyval (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_interaction(self, user_input: str, response: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO interactions (user_input, athena_response) VALUES (?, ?)', (user_input, response))
        conn.commit()
        conn.close()

    def get_recent_interactions(self, limit=5):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT user_input, athena_response FROM interactions ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def set_memory(self, key: str, value: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO memory_keyval (key, value) VALUES (?, ?)', (key, value))
        conn.commit()
        conn.close()
        
    def get_memory(self, key: str) -> str:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM memory_keyval WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None


class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            default_config = {
                "user_name": "Mr. Bhattacharjee",
                "tesseract_cmd": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                "email": {
                    "address": "your_email@gmail.com",
                    "password": "your_app_password",
                    "imap_server": "imap.gmail.com",
                    "smtp_server": "smtp.gmail.com"
                },
                "whisper_model": "base",
                "use_whisper": False, # Switch to True if whisper is installed
                "gemini_api_key": "YOUR_API_KEY_HERE"
            }
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get(self, key: str, default=None):
        return self.config.get(key, default)
