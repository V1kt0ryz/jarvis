from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal
from gui.styles import Styles, Colors

class ControlsWidget(QWidget):
    voice_toggled = pyqtSignal(bool)
    speaker_toggled = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.voice_enabled = True
        self.speaker_enabled = True
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Voice button
        self.voice_btn = QPushButton("🎤 VOICE ON")
        self.voice_btn.setStyleSheet(Styles.button())
        self.voice_btn.setMinimumHeight(45)
        self.voice_btn.clicked.connect(self.toggle_voice)
        layout.addWidget(self.voice_btn)
        
        # Speaker button
        self.speaker_btn = QPushButton("🔊 SPEAKER ON")
        self.speaker_btn.setStyleSheet(Styles.button())
        self.speaker_btn.setMinimumHeight(45)
        self.speaker_btn.clicked.connect(self.toggle_speaker)
        layout.addWidget(self.speaker_btn)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        self.voice_btn.setText(f"🎤 VOICE {'ON' if self.voice_enabled else 'OFF'}")
        self.voice_toggled.emit(self.voice_enabled)
    
    def toggle_speaker(self):
        self.speaker_enabled = not self.speaker_enabled
        self.speaker_btn.setText(f"🔊 SPEAKER {'ON' if self.speaker_enabled else 'OFF'}")
        self.speaker_toggled.emit(self.speaker_enabled)