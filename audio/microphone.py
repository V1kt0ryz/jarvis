import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from scipy.io.wavfile import write
import os
from config import SAMPLE_RATE, VOICE_LANGUAGE, MICROPHONE_DEVICE
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Microphone:
    def __init__(self):
        try:
            self.model = WhisperModel("base", device="cpu")
            logger.info("Microphone initialized")
        except Exception as e:
            logger.error(f"Microphone init error: {e}")
    
    def record_and_transcribe(self, seconds=4):
        """Record audio and transcribe to text"""
        try:
            audio = sd.rec(
                int(seconds * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                device=MICROPHONE_DEVICE
            )
            sd.wait()
            
            audio = np.squeeze(audio)
            temp_file = "temp.wav"
            write(temp_file, SAMPLE_RATE, audio)
            
            segments, _ = self.model.transcribe(temp_file, language=VOICE_LANGUAGE)
            text = " ".join([s.text for s in segments]).strip()
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return text
        except Exception as e:
            logger.error(f"Microphone error: {e}")
            return ""