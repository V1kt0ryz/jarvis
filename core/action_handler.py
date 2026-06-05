import webbrowser
import os
import threading
from utils.program_launcher import ProgramLauncher
from core.memory_manager import MemoryManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ActionHandler:
    def __init__(self):
        self.program_launcher = ProgramLauncher()
        self.memory_manager = MemoryManager()
    
    def handle(self, data):
        """Handle action based on data"""
        action = data.get("action")
        
        handlers = {
            "chat": self._handle_chat,
            "open_website": self._handle_open_website,
            "search_google": self._handle_search_google,
            "open_program": self._handle_open_program,
            "remember": self._handle_remember,
            "recall": self._handle_recall,
            "shutdown": self._handle_shutdown,
            "open_file": self._handle_open_file,
        }
        
        handler = handlers.get(action)
        if handler:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Error in {action}: {e}")
        else:
            logger.warning(f"Unknown action: {action}")
    
    def _handle_chat(self, data):
        """Handle chat action"""
        logger.info(f"Chat: {data.get('response')}")
    
    def _handle_open_website(self, data):
        """Open website"""
        try:
            url = data.get("url")
            logger.info(f"Opening website: {url}")
            webbrowser.open(url)
        except Exception as e:
            logger.error(f"Error opening website: {e}")
    
    def _handle_search_google(self, data):
        """Search on Google"""
        try:
            query = data.get("query")
            logger.info(f"Searching Google: {query}")
            webbrowser.open(f"https://google.com/search?q={query}")
        except Exception as e:
            logger.error(f"Error searching Google: {e}")
    
    def _handle_open_program(self, data):
        """Open program"""
        try:
            program = data.get("program")
            logger.info(f"Opening program: {program}")
            self.program_launcher.open(program)
        except Exception as e:
            logger.error(f"Error opening program: {e}")
    
    def _handle_remember(self, data):
        """Remember information"""
        try:
            key = data.get("key")
            value = data.get("value")
            self.memory_manager.save(key, value)
            logger.info(f"Remembered: {key} = {value}")
        except Exception as e:
            logger.error(f"Error remembering: {e}")
    
    def _handle_recall(self, data):
        """Recall information"""
        try:
            key = data.get("key")
            value = self.memory_manager.load(key)
            logger.info(f"Recalled: {key} = {value}")
        except Exception as e:
            logger.error(f"Error recalling: {e}")
    
    def _handle_shutdown(self, data):
        """Shutdown system"""
        try:
            logger.info("Shutting down system")
            os.system("shutdown /s /t 30")
        except Exception as e:
            logger.error(f"Error shutting down: {e}")
    
    def _handle_open_file(self, data):
        """Open file"""
        try:
            filepath = data.get("path")
            logger.info(f"Opening file: {filepath}")
            os.startfile(filepath)
        except Exception as e:
            logger.error(f"Error opening file: {e}")