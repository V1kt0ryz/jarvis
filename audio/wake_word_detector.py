import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from scipy.io.wavfile import write
import time
import os
from config import (
    SAMPLE_RATE, VOICE_LANGUAGE, MICROPHONE_DEVICE,
    WAKE_WORDS
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

class WakeWordDetector:
    def __init__(self):
        try:
            self.model = WhisperModel("base", device="cpu")
            logger.info("Wake word detector initialized")
        except Exception as e:
            logger.error(f"Wake word detector init error: {e}")
    
    def detect(self, timeout=None):
        """Detect wake word"""
        try:
            logger.info("👂 Waiting for wake word...")
            
            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                device=MICROPHONE_DEVICE
            ) as stream:
                buffer = []
                start_time = time.time()
                
                while True:
                    if timeout and time.time() - start_time > timeout:
                        raise TimeoutError("Wake word detection timeout")
                    
                    data, _ = stream.read(int(SAMPLE_RATE * 0.5))
                    buffer.append(data)
                    
                    if len(buffer) < 20:
                        continue
                    
                    audio = np.concatenate(buffer[-20:], axis=0)
                    audio = np.squeeze(audio)
                    
                    volume = np.abs(audio).mean()
                    if volume < 0.01:
                        continue
                    
                    temp_file = "temp_wake.wav"
                    write(temp_file, SAMPLE_RATE, audio)
                    
                    segments, _ = self.model.transcribe(
                        temp_file,
                        language=VOICE_LANGUAGE
                    )
                    
                    text = " ".join([s.text for s in segments]).lower().strip()
                    
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    
                    buffer.clear()
                    
                    if any(word in text for word in WAKE_WORDS):
                        logger.info("✅ Wake word detected!")
                        return True
        except Exception as e:
            logger.error(f"Wake word detection error: {e}")
            return False