from PyQt6.QtGui import QFont, QColor

class Colors:
    # Primary
    BG = "#0a0e27"
    PANEL = "#151a2e"
    PANEL_LIGHT = "#1f2637"
    
    # Accent
    CYAN = "#00d9ff"
    BLUE = "#0099ff"
    GREEN = "#00ff88"
    ORANGE = "#ffaa00"
    RED = "#ff3366"
    
    # Text
    TEXT = "#e0e6ff"
    MUTED = "#8899cc"
    
    # Special
    CHAT_BG = "#0d1117"
    ACCENT = "#00d9ff"

class Fonts:
    TITLE = QFont("Segoe UI", 32, QFont.Weight.Bold)
    HEADER = QFont("Segoe UI", 18, QFont.Weight.Bold)
    NORMAL = QFont("Segoe UI", 11)
    MONO = QFont("Consolas", 10)

class Styles:
    @staticmethod
    def button():
        return f"""
            QPushButton {{
                background-color: {Colors.PANEL_LIGHT};
                color: {Colors.TEXT};
                border: 2px solid {Colors.CYAN};
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {Colors.CYAN};
                color: {Colors.BG};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BLUE};
            }}
        """
    
    @staticmethod
    def input():
        return f"""
            QLineEdit {{
                background-color: {Colors.PANEL};
                color: {Colors.TEXT};
                border: 2px solid {Colors.CYAN};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.BLUE};
            }}
        """
    
    @staticmethod
    def text_edit():
        return f"""
            QTextEdit {{
                background-color: {Colors.CHAT_BG};
                color: {Colors.CYAN};
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-family: Consolas;
                font-size: 11px;
            }}
        """
    
    @staticmethod
    def panel():
        return f"""
            QFrame {{
                background-color: {Colors.PANEL};
                border-radius: 8px;
            }}
        """