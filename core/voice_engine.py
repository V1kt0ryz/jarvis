import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from scipy.io.wavfile import write
import pyttsx3
import queue
import threading
import time
import os
import subprocess
import sys
from config import (
    SAMPLE_RATE, RECORD_SECONDS, VOICE_LANGUAGE,
    VOICE_RATE, VOICE_VOLUME, MICROPHONE_DEVICE,
    WAKE_WORDS, WAKE_WORD_THRESHOLD
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

class VoiceEngine:
    def __init__(self):
        """Initialize voice engine"""
        try:
            self.whisper_model = WhisperModel("base", device="cpu")
            self.tts_engine = pyttsx3.init()
            self._configure_tts()
            
            self.speech_queue = queue.Queue()
            self.is_running = True
            self._start_tts_worker()
            logger.info("Voice Engine initialized")
        except Exception as e:
            logger.error(f"Voice Engine init error: {e}")
    
    def _configure_tts(self):
        """Configure text-to-speech engine"""
        try:
            # Set to use SAPI5 on Windows for better compatibility
            voices = self.tts_engine.getProperty("voices")
            if voices:
                # Try to use German voice
                for voice in voices:
                    if "german" in str(voice.languages).lower() or "de" in voice.id.lower():
                        self.tts_engine.setProperty("voice", voice.id)
                        break
                else:
                    self.tts_engine.setProperty("voice", voices[0].id)
            
            self.tts_engine.setProperty("volume", VOICE_VOLUME)
            self.tts_engine.setProperty("rate", VOICE_RATE)
            logger.info("TTS configured")
        except Exception as e:
            logger.error(f"TTS config error: {e}")
    
    def _start_tts_worker(self):
        """Start TTS worker thread - uses system voice with proper synchronization"""
        def worker():
            while self.is_running:
                try:
                    text = self.speech_queue.get(timeout=1)
                    if text is None:
                        break
                    
                    if text.strip():
                        logger.info(f"Speaking: {text}")
                        try:
                            # Use PowerShell on Windows for more reliable TTS
                            if sys.platform == "win32":
                                # PowerShell command to speak text
                                ps_command = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak(\'{text.replace(chr(39), "")}\');'
                                subprocess.run(
                                    ["powershell", "-Command", ps_command],
                                    check=False,
                                    capture_output=True,
                                    timeout=30
                                )
                            else:
                                # Fallback to pyttsx3 for non-Windows
                                self.tts_engine.say(text)
                                self.tts_engine.runAndWait()
                        except subprocess.TimeoutExpired:
                            logger.error("TTS timeout")
                        except Exception as e:
                            logger.error(f"TTS playback error: {e}")
                            try:
                                # Fallback to pyttsx3
                                self.tts_engine.say(text)
                                self.tts_engine.runAndWait()
                            except Exception as retry_e:
                                logger.error(f"TTS retry failed: {retry_e}")
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"TTS Worker Error: {e}")
        
        self.tts_thread = threading.Thread(target=worker, daemon=True)
        self.tts_thread.start()
    
    def speak(self, text):
        """Add text to speech queue"""
        if text and text.strip():
            self.speech_queue.put(text)
            logger.info(f"Queued speech: {text[:50]}...")
    
    def listen(self, seconds=RECORD_SECONDS):
        """Listen to microphone and transcribe"""
        try:
            logger.info(f"Listening for {seconds} seconds...")
            
            audio = sd.rec(
                int(seconds * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                device=MICROPHONE_DEVICE
            )
            sd.wait()
            
            audio = np.squeeze(audio)
            temp_file = "temp_listen.wav"
            write(temp_file, SAMPLE_RATE, audio)
            
            segments, _ = self.whisper_model.transcribe(
                temp_file,
                language=VOICE_LANGUAGE
            )
            
            text = " ".join([s.text for s in segments]).strip()
            logger.info(f"Heard: {text}")
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return text
        except Exception as e:
            logger.error(f"Listen Error: {e}")
            return ""
    
    def wait_for_wake_word(self, timeout=None):
        """Wait for wake word detection"""
        try:
            logger.info("Waiting for wake word...")
            
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
                    
                    segments, _ = self.whisper_model.transcribe(
                        temp_file,
                        language=VOICE_LANGUAGE
                    )
                    
                    text = " ".join([s.text for s in segments]).lower().strip()
                    
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    
                    buffer.clear()
                    
                    if any(word in text for word in WAKE_WORDS):
                        logger.info("Wake word detected!")
                        return True
        except Exception as e:
            logger.error(f"Wake word detection error: {e}")
            return False
    
    def stop(self):
        """Stop voice engine"""
        self.is_running = False
        self.speech_queue.put(None)
        try:
            self.tts_engine.stop()
        except:
            pass
        # Wait for TTS thread to finish
        if hasattr(self, 'tts_thread'):
            self.tts_thread.join(timeout=2)
