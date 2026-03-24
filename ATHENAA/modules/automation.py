import pyautogui
import os
import subprocess
import time

class DesktopAutomation:
    def __init__(self):
        # Fail-safe to avoid out of control mouse behavior
        pyautogui.FAILSAFE = True

    def open_application(self, app_name: str):
        """Open a system application like notepad, calculator."""
        try:
            # Simple mapping for common Windows applications
            app_mapping = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "calc": "calc.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe",
                "explorer": "explorer.exe",
                "chrome": "chrome.exe",
                "edge": "msedge.exe",
                "brave": "brave.exe",
                "task manager": "taskmgr.exe"
            }
            
            cmd = app_mapping.get(app_name.lower())
            if cmd:
                subprocess.Popen(cmd)
                return True, f"Opened {app_name}"
            else:
                # Fallback to pressing windows key and typing the app name
                pyautogui.press('win')
                time.sleep(0.5)
                pyautogui.write(app_name)
                time.sleep(1)
                pyautogui.press('enter')
                return True, f"Attempted to open {app_name} via Windows search"
        except Exception as e:
            return False, f"Failed to open {app_name}: {e}"

    def type_text(self, text: str):
        """Type text using keyboard."""
        try:
            pyautogui.write(text, interval=0.03)
            return True, "Typed text successfully"
        except Exception as e:
            return False, str(e)

    def press_key(self, key: str):
        """Press a specific keyboard key (e.g., 'enter', 'esc', 'space')."""
        try:
            pyautogui.press(key)
            return True, f"Pressed {key}"
        except Exception as e:
            return False, str(e)
            
    def click_mouse(self, x=None, y=None, button='left'):
        """Click the mouse at optional coordinates."""
        try:
            if x is not None and y is not None:
                pyautogui.click(x=x, y=y, button=button)
            else:
                pyautogui.click(button=button)
            return True, f"Clicked mouse {button} button"
        except Exception as e:
            return False, str(e)
            
    def scroll(self, amount: int):
        """Scroll mouse. Positive amount scroll up, negative scroll down."""
        pyautogui.scroll(amount)
        return True, "Scrolled successfully"

    def select_all(self):
        """Select all text in the current window (Ctrl+A)."""
        try:
            pyautogui.hotkey('ctrl', 'a')
            return True, "Selected all text."
        except Exception as e:
            return False, str(e)

    def clear_text(self):
        """Clear text in the current window (Ctrl+A then Delete)."""
        try:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            return True, "Cleared text."
        except Exception as e:
            return False, str(e)
