import json
import os
from config import MEMORY_FILE
from utils.logger import setup_logger

logger = setup_logger(__name__)

class MemoryManager:
    def __init__(self):
        self.memory = self._load_memory()
    
    def _load_memory(self):
        """Load memory from file"""
        try:
            if os.path.exists(MEMORY_FILE):
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
        
        return {}
    
    def save(self, key, value):
        """Save to memory"""
        try:
            self.memory[key] = value
            self._write_memory()
            logger.info(f"Memory saved: {key}")
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def load(self, key):
        """Load from memory"""
        return self.memory.get(key, None)
    
    def _write_memory(self):
        """Write memory to file"""
        try:
            os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error writing memory: {e}")
    
    def clear(self):
        """Clear all memory"""
        self.memory = {}
        self._write_memory()
        logger.info("Memory cleared")