from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from gui.styles import Colors
import datetime
import psutil

class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_updates()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Status
        self.status_label = QLabel("🟢 SYSTEM ONLINE")
        self.status_label.setStyleSheet(f"color: {Colors.GREEN}; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.status_label)
        
        # Clock
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet(f"color: {Colors.TEXT}; font-family: Consolas; font-size: 18px;")
        layout.addWidget(self.clock_label)
        
        # CPU
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_label.setStyleSheet(f"color: {Colors.MUTED}; font-size: 12px;")
        layout.addWidget(self.cpu_label)
        
        # RAM
        self.ram_label = QLabel("RAM: 0%")
        self.ram_label.setStyleSheet(f"color: {Colors.MUTED}; font-size: 12px;")
        layout.addWidget(self.ram_label)
        
        # GPU
        self.gpu_label = QLabel("GPU: N/A")
        self.gpu_label.setStyleSheet(f"color: {Colors.MUTED}; font-size: 12px;")
        layout.addWidget(self.gpu_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def start_updates(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)
        self.update_stats()
    
    def update_stats(self):
        # Clock
        self.clock_label.setText(datetime.datetime.now().strftime("%H:%M:%S"))
        
        # CPU
        cpu = psutil.cpu_percent(interval=0.1)
        self.cpu_label.setText(f"CPU: {cpu}%")
        
        # RAM
        ram = psutil.virtual_memory().percent
        self.ram_label.setText(f"RAM: {ram}%")