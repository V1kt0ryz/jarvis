from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor, QFont
from gui.styles import Colors, Fonts

class ReactorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pulse = 0
        self.direction = 1
        self.setMinimumHeight(300)
        self.init_animation()
    
    def init_animation(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(40)
    
    def update_animation(self):
        self.pulse += self.direction * 2
        
        if self.pulse > 20:
            self.direction = -1
        if self.pulse < 0:
            self.direction = 1
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(Colors.PANEL))
        
        # Draw circles
        center_x = self.width() // 2
        center_y = self.height() // 2
        size = 80 + self.pulse
        
        # Outer circle
        painter.setPen(QColor(Colors.CYAN))
        painter.drawEllipse(
            center_x - size - 10,
            center_y - size - 10,
            size * 2 + 20,
            size * 2 + 20
        )
        
        # Inner circle
        painter.setBrush(QColor(Colors.CYAN))
        painter.drawEllipse(
            center_x - size // 2,
            center_y - size // 2,
            size,
            size
        )
        
        # Text
        painter.setFont(Fonts.HEADER)
        painter.setPen(QColor(Colors.TEXT))
        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            "JARVIS"
        )