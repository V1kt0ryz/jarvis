import logging
import os
from config import BASE_DIR

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name):
    """Setup logger for a module"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(
            os.path.join(LOG_DIR, f"{name.split('.')[-1]}.log")
        )
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)
    
    return logger