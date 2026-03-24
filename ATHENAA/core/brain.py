import torch
import random
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import MemoryLayer
from core.neural_net import NeuralNet
from core.nltk_utils import bag_of_words, tokenize

def command_str(cmd):
    return str(cmd).lower()

class Brain:
    def __init__(self, voice, automation, browser, communication, vision, config=None):
        self.voice = voice
        self.automation = automation
        self.browser = browser
        self.communication = communication
        self.vision = vision
        self.memory = MemoryLayer()
        self.config = config or {}
        
        # Disable overly verbose torch warnings
        import warnings
        warnings.filterwarnings("ignore")
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load intents
        intent_path = os.path.join(os.path.dirname(__file__), 'intents.json')
        try:
            with open(intent_path, 'r') as f:
                self.intents = json.load(f)
        except FileNotFoundError:
            self.intents = None
            print("Brain: intents.json not found.")

        # Load trained PyTorch model
        model_path = os.path.join(os.path.dirname(__file__), 'data.pth')
        self.model = None
        self.all_words = []
        self.tags = []
        if os.path.exists(model_path):
            try:
                data = torch.load(model_path, map_location=self.device)
                input_size = data["input_size"]
                hidden_size = data["hidden_size"]
                output_size = data["output_size"]
                self.all_words = data["all_words"]
                self.tags = data["tags"]
                model_state = data["model_state"]
                
                self.model = NeuralNet(input_size, hidden_size, output_size).to(self.device)
                self.model.load_state_dict(model_state)
                self.model.eval()
                print("Brain: Custom PyTorch Language Model initialized.")
            except Exception as e:
                print(f"Brain Error loading PyTorch model: {e}")
        else:
            print("Brain: Native PyTorch model data.pth not found. Please run train.py.")

    def predict_intent(self, sentence):
        if not self.model:
            return None, 0.0
            
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)
        
        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]
        
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        return tag, prob.item()

    def process_command(self, command: str) -> str:
        """Process the user command using custom PyTorch NN."""
        if not command:
            return ""

        print(f"Brain processing: {command}")
        cmd_lower = command_str(command)
        
        # Immediate interrupts
        if "sleep" in cmd_lower or "stop listening" in cmd_lower or "pause" in cmd_lower:
            response = "Going to sleep."
            self.voice.speak(response)
            return "SLEEP"

        if "goodbye" in cmd_lower or "exit" in cmd_lower or "quit" in cmd_lower or "stop" in cmd_lower:
            response = "Goodbye, Mr. Bhattacharjee. Shutting down systems."
            self.voice.speak(response)
            return "EXIT"

        if self.model and self.intents:
            tag, prob = self.predict_intent(cmd_lower)
            print(f"Intent classified by Neural Net: {tag} (Confidence: {prob:.2f})")
            
            if prob > 0.70:
                # Dynamic conversational response from intents.json
                for intent in self.intents['intents']:
                    if tag == intent["tag"]:
                        bot_response = random.choice(intent['responses'])
                        self.voice.speak(bot_response)
                        
                        # Execute the routing action
                        return self._execute_intent_action(tag, cmd_lower, bot_response)
                        
            response = "My neural network couldn't safely classify that command. Could you rephrase?"
            self.voice.speak(response)
            return response

        # Fallback Mode
        response = "My PyTorch matrix is currently disconnected or untrained. Please check data.pth."
        self.voice.speak(response)
        return response

    def _execute_intent_action(self, tag, command_text, bot_response):
        if tag == "open_app":
            app_name = command_text
            for word in ["open", "start", "launch"]:
                if word in command_text:
                    parts = command_text.split(word, 1)
                    if len(parts) > 1:
                        app_name = parts[1].strip()
                    break
            self.automation.open_application(app_name)
            
        elif tag == "search":
            query = command_text.replace("search google for", "").replace("search for", "").replace("google this", "").strip()
            self.browser.search_google(query)
            
        elif tag == "clear_text":
            self.automation.clear_text()
            
        elif tag == "read_screen":
            success, text = self.vision.analyze_screen_text()
            if success and text:
                self.voice.speak(f"My vision module reads: {text[:150]}")
            else:
                self.voice.speak("I couldn't detect clear text.")
                
        elif tag == "time":
            from datetime import datetime
            now = datetime.now().strftime("%I:%M %p")
            self.voice.speak(f"The time is {now}")
            
        elif tag == "whatsapp":
            print("Preparing whatsapp interaction...")
            
        return bot_response
