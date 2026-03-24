import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.helpers import ConfigManager, MemoryLayer
from modules.voice import VoiceSystem
from modules.automation import DesktopAutomation
from modules.browser import BrowserAutomation
from modules.communication import CommunicationSystem
from modules.vision import VisionSystem
from core.brain import Brain

def main():
    print("Initializing ATHENA...")
    
    # Load Configuration
    config_mgr = ConfigManager()
    config = config_mgr.config
    
    # Initialize Modules
    try:
        print("Loading Voice System...")
        voice = VoiceSystem(config)
        
        print("Loading Automation System...")
        automation = DesktopAutomation()
        
        print("Loading Browser System...")
        browser = BrowserAutomation()
        
        print("Loading Communication System...")
        communication = CommunicationSystem(config)
        
        print("Loading Vision System...")
        vision = VisionSystem(config)
        
        # Initialize Brain
        print("Initializing Core Brain...")
        brain = Brain(voice, automation, browser, communication, vision, config)
    except Exception as e:
        print(f"Failed to initialize ATHENA components: {e}")
        sys.exit(1)
        
    # Wake up
    greeting = f"Online and ready. Good to see you, {config.get('user_name', 'Sir')}."
    voice.speak(greeting)
    
    print("\n--- ATHENA is in SLEEP mode ---")
    print("Say 'wake up athena' to activate her.")
    print("Say 'exit' or 'goodbye' to stop completely.")
    
    is_awake = False
    
    while True:
        try:
            if not is_awake:
                # Listen specifically for the wake word
                command = voice.listen(timeout=2, phrase_time_limit=4)
                if command and ("wake up" in command or "athena" in command):
                    is_awake = True
                    voice.speak("Yes, Sir? I am listening.")
                    print("\n--- ATHENA is AWAKE ---")
                elif command and ("exit" in command or "goodbye" in command):
                    voice.speak("Goodbye, shutting down.")
                    break
                else:
                    time.sleep(0.5)
            else:
                # Active listening mode
                command = voice.listen(timeout=5, phrase_time_limit=10)
                if command:
                    response = brain.process_command(command)
                    
                    if response == "SLEEP":
                        is_awake = False
                        print("\n--- ATHENA is in SLEEP mode ---")
                        continue
                        
                    # Log interaction
                    if response and response not in ["EXIT", "SLEEP"]:
                        brain.memory.log_interaction(command, response)
                    
                    if response == "EXIT":
                        break
                else:
                    time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nShutting down by keyboard interrupt...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
