from dotenv import load_dotenv
from classes import ChatBotWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    # Load environment variables at application startup
    load_dotenv()
    
    app = QApplication(sys.argv)
    window = ChatBotWindow()
    sys.exit(app.exec())
