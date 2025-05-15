from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

def get_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    return palette

# Message colors
USER_MSG_BG = "#2C3E50"  # Dark blue-gray
ASSISTANT_MSG_BG = "#2D4263"  # Dark purple-blue

STYLES = {
    "chat_area": """
        QTextEdit {
            border: 1px solid #555;
            border-radius: 4px;
            padding: 8px;
            background-color: #1E1E1E;
            color: #ffffff;
            font-size: 14px;
        }
    """,
    "input_field": """
        QTextEdit {
            border: 1px solid #555;
            border-radius: 4px;
            padding: 8px;
            background-color: #363636;
            color: #ffffff;
            font-size: 14px;
        }
    """,
    "send_button": """
        QPushButton {
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #0b5ed7;
        }
        QPushButton:pressed {
            background-color: #0a58ca;
        }
    """,
    "clear_button": """
        QPushButton {
            background-color: #dc3545;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #bb2d3b;
        }
        QPushButton:pressed {
            background-color: #a52834;
        }
    """,
    "message_styles": {
        "user": f"""
            <div style='
                background-color: {USER_MSG_BG};
                border-radius: 10px;
                padding: 10px;
                margin: 5px 0;
                margin-left: 20%;
                margin-right: 5px;
            '>
            <span style='color: #888; font-size: 12px;'>[%time%] User:</span><br>
            %content%
            </div>
        """,
        "assistant": f"""
            <div style='
                background-color: {ASSISTANT_MSG_BG};
                border-radius: 10px;
                padding: 10px;
                margin: 5px 0;
                margin-right: 20%;
                margin-left: 5px;
            '>
            <span style='color: #888; font-size: 12px;'>[%time%] Assistant:</span><br>
            %content%
            </div>
        """
    }
} 