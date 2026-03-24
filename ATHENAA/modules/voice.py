import speech_recognition as sr
import pyttsx3

class VoiceSystem:
    def __init__(self, config=None):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure voice (try to find a female voice for ATHENA like Zira or Hazel)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower() or "hazel" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', 170)
        self.engine.setProperty('volume', 1.0)
    
    def speak(self, text: str):
        """Convert text to speech."""
        print(f"ATHENA: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=5, phrase_time_limit=5) -> str:
        """Listen from microphone and convert to text using local Whisper or Google."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("Processing speech...")
                
                use_whisper = self.config and self.config.get("use_whisper", False)
                if use_whisper:
                    model = self.config.get("whisper_model", "base")
                    text = self.recognizer.recognize_whisper(audio, model=model, language="english")
                else:
                    text = self.recognizer.recognize_google(audio)
                    
                print(f"User: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError as e:
                print(f"Speech recognition error; {e}")
                return ""
            except Exception as e:
                print(f"Error during listening: {e}")
                return ""
