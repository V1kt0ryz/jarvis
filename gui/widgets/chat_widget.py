from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtCore import pyqtSignal
from gui.styles import Styles, Colors, Fonts

class ChatWidget(QWidget):
    message_sent = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(Styles.text_edit())
        self.chat_display.setFont(Fonts.MONO)
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Frag Jarvis etwas...")
        self.input_field.setStyleSheet(Styles.input())
        self.input_field.setMinimumHeight(40)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("SEND")
        self.send_btn.setStyleSheet(Styles.button())
        self.send_btn.setMaximumWidth(100)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)
    
    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            self.message_sent.emit(text)
            self.input_field.clear()
    
    def add_message(self, sender, text):
        self.chat_display.append(f"<b style='color: #00d9ff'>[{sender}]</b> {text}")