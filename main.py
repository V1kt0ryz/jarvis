import sys
import threading
import time
from PyQt6.QtWidgets import QApplication
from gui.main_window import JarvisMainWindow
from core.voice_engine import VoiceEngine
from core.llm_engine import LLMEngine
from core.action_handler import ActionHandler
from utils.logger import setup_logger

logger = setup_logger(__name__)

class JarvisApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = JarvisMainWindow()
        
        # Initialize Core Components
        logger.info("Initializing JARVIS...")
        self.llm_engine = LLMEngine()
        self.voice_engine = VoiceEngine()
        self.action_handler = ActionHandler()
        
        # Connect Signals
        self._setup_connections()
        
        # Start Voice Loop
        self._start_voice_loop()
        
        logger.info("JARVIS initialized successfully")
    
    def _setup_connections(self):
        """Connect GUI signals to handlers"""
        self.window.message_sent.connect(self.handle_user_message)
        self.window.voice_toggled.connect(self.toggle_voice)
        self.window.speaker_toggled.connect(self.toggle_speaker)
    
    def handle_user_message(self, user_input):
        """Process user message and generate response"""
        try:
            logger.info(f"User: {user_input}")
            self.window.add_message("Du", user_input)
            
            # Get LLM response
            response = self.llm_engine.process(user_input)
            response_text = response.get("response", "")
            
            self.window.add_message("Jarvis", response_text)
            
            # Handle actions in background thread
            threading.Thread(
                target=self._handle_action_async,
                args=(response,),
                daemon=True
            ).start()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.window.add_message("System", f"Fehler: {e}")
    
    def _handle_action_async(self, response):
        """Handle action asynchronously"""
        try:
            self.action_handler.handle(response)
            
            # Speak response if enabled
            if self.window.speaker_enabled:
                self.voice_engine.speak(response.get("response", ""))
        except Exception as e:
            logger.error(f"Error handling action: {e}")
    
    def _start_voice_loop(self):
        """Start voice listening loop in background"""
        def voice_loop():
            try:
                self.voice_engine.speak("Jarvis ist bereit")
                while True:
                    if not self.window.voice_enabled:
                        time.sleep(0.2)
                        continue
                    
                    if self.voice_engine.wait_for_wake_word(timeout=60):
                        self.window.add_message("System", "🎤 Wake Word erkannt")
                        self.voice_engine.speak("Ja?")
                        
                        user_input = self.voice_engine.listen()
                        if user_input:
                            self.handle_user_message(user_input)
                    else:
                        time.sleep(1)
            except Exception as e:
                logger.error(f"Voice loop error: {e}")
                time.sleep(2)
        
        threading.Thread(target=voice_loop, daemon=True).start()
    
    def toggle_voice(self, enabled):
        """Toggle voice input"""
        logger.info(f"Voice input: {enabled}")
    
    def toggle_speaker(self, enabled):
        """Toggle voice output"""
        logger.info(f"Speaker output: {enabled}")
    
    def run(self):
        """Run the application"""
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = JarvisApp()
    app.run()