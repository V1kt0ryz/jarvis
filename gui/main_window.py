from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from gui.styles import Colors, Fonts, Styles
from gui.widgets import ChatWidget, ReactorWidget, StatusWidget, ControlsWidget

class JarvisMainWindow(QMainWindow):
    message_sent = pyqtSignal(str)
    voice_toggled = pyqtSignal(bool)
    speaker_toggled = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.voice_enabled = True
        self.speaker_enabled = True
        self.init_ui()
    
    def init_ui(self):
        # Main window
        self.setWindowTitle("JARVIS HUD 6.0")
        self.setGeometry(100, 100, 1600, 1000)
        self.setStyleSheet(f"background-color: {Colors.BG};")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Left sidebar
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Center reactor
        center_panel = self.create_center_panel()
        main_layout.addWidget(center_panel, 1)
        
        # Right chat
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
        
        central_widget.setLayout(main_layout)
    
    def create_left_panel(self):
        """Create left sidebar"""
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {Colors.PANEL}; border-radius: 8px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("JARVIS")
        title.setFont(Fonts.TITLE)
        title.setStyleSheet(f"color: {Colors.CYAN};")
        layout.addWidget(title)
        
        # Status widget
        self.status_widget = StatusWidget()
        layout.addWidget(self.status_widget)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
    
    def create_center_panel(self):
        """Create center reactor panel"""
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {Colors.PANEL}; border-radius: 8px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel("SYSTEM CORE")
        header.setFont(Fonts.HEADER)
        header.setStyleSheet(f"color: {Colors.TEXT};")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Reactor
        self.reactor = ReactorWidget()
        layout.addWidget(self.reactor)
        
        # Controls
        self.controls = ControlsWidget()
        self.controls.voice_toggled.connect(self.toggle_voice)
        self.controls.speaker_toggled.connect(self.toggle_speaker)
        layout.addWidget(self.controls)
        
        frame.setLayout(layout)
        return frame
    
    def create_right_panel(self):
        """Create right chat panel"""
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {Colors.PANEL_LIGHT}; border-radius: 8px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat widget
        self.chat_widget = ChatWidget()
        self.chat_widget.message_sent.connect(self.on_message_sent)
        layout.addWidget(self.chat_widget)
        
        frame.setLayout(layout)
        return frame
    
    def on_message_sent(self, text):
        """Handle message sent"""
        self.message_sent.emit(text)
    
    def add_message(self, sender, text):
        """Add message to chat"""
        self.chat_widget.add_message(sender, text)
    
    def toggle_voice(self, enabled):
        """Toggle voice input"""
        self.voice_enabled = enabled
        self.voice_toggled.emit(enabled)
    
    def toggle_speaker(self, enabled):
        """Toggle speaker output"""
        self.speaker_enabled = enabled
        self.speaker_toggled.emit(enabled)