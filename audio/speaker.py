import pyttsx3
import queue
import threading
from config import VOICE_RATE, VOICE_VOLUME
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Speaker:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self._configure()
            
            self.queue = queue.Queue()
            self.is_running = True
            self._start_worker()
            logger.info("Speaker initialized")
        except Exception as e:
            logger.error(f"Speaker init error: {e}")
    
    def _configure(self):
        """Configure speaker"""
        try:
            voices = self.engine.getProperty("voices")
            if voices:
                for voice in voices:
                    if "german" in voice.languages or "de" in voice.id.lower():
                        self.engine.setProperty("voice", voice.id)
                        break
                else:
                    self.engine.setProperty("voice", voices[0].id)
            
            self.engine.setProperty("volume", VOICE_VOLUME)
            self.engine.setProperty("rate", VOICE_RATE)
            logger.info("Speaker configured")
        except Exception as e:
            logger.error(f"Speaker config error: {e}")
    
    def _start_worker(self):
        """Start worker thread"""
        def worker():
            while self.is_running:
                try:
                    text = self.queue.get()
                    if text is None:
                        break
                    
                    logger.info(f"Speaking: {text}")
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e:
                    logger.error(f"Speaker error: {e}")
        
        threading.Thread(target=worker, daemon=True).start()
    
    def speak(self, text):
        """Add text to speak queue"""
        if text:
            self.queue.put(text)
    
    def stop(self):
        """Stop speaker"""
        self.is_running = False
        self.queue.put(None)