import os
from dotenv import load_dotenv

load_dotenv()

# LLM CONFIGURATION
LLM_MODEL = os.getenv("LLM_MODEL", "phi4-mini:latest")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# VOICE CONFIGURATION
VOICE_LANGUAGE = "de"
VOICE_RATE = 180
VOICE_VOLUME = 1.0
MICROPHONE_DEVICE = 1
SAMPLE_RATE = 16000
RECORD_SECONDS = 4

# GUI CONFIGURATION
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000
THEME = "dark"

# WAKE WORD CONFIGURATION
WAKE_WORDS = ["jarvis", "jervis", "jarwis", "ciao", "charvis"]
WAKE_WORD_THRESHOLD = 60

# PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

os.makedirs(DATA_DIR, exist_ok=True)
