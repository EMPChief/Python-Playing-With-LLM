from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QWidget, QProgressBar, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
import dotenv
from datetime import datetime
import json
from .MessageDatabase import MessageDatabase
from .ChatBot import ChatBot
from .styles import STYLES, get_dark_palette

dotenv.load_dotenv()

class ChatBotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Chat Assistant")
        self.setGeometry(100, 100, 1000, 800)
        
        # Set dark theme
        self.setPalette(get_dark_palette())
        
        self.setup_ui()
        self.setup_menu()
        
        self.chatbot = ChatBot()
        self.message_db = MessageDatabase()
        self.load_messages()
        
        self.show()
    
    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        export_action = QAction('Export Chat', self)
        export_action.triggered.connect(self.export_chat)
        file_menu.addAction(export_action)
        
        clear_action = QAction('Clear Chat', self)
        clear_action.triggered.connect(self.clear_chat)
        file_menu.addAction(clear_action)
    
    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet(STYLES["chat_area"])
        layout.addWidget(self.chat_area)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(70)
        self.input_field.setStyleSheet(STYLES["input_field"])
        input_layout.addWidget(self.input_field)
        
        button_layout = QVBoxLayout()
        
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet(STYLES["send_button"])
        self.send_button.clicked.connect(self.send_message)
        button_layout.addWidget(self.send_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet(STYLES["clear_button"])
        self.clear_button.clicked.connect(self.clear_chat)
        button_layout.addWidget(self.clear_button)
        
        input_layout.addLayout(button_layout)
        layout.addLayout(input_layout)
        
        # Connect enter key to send message
        self.input_field.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        if obj is self.input_field and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)
    
    def send_message(self):
        user_message = self.input_field.toPlainText().strip()
        if user_message:
            self.input_field.clear()
            self.add_message_to_ui(role="user", content=user_message)
            
            # Show progress bar
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            self.send_button.setEnabled(False)
            
            # Use QTimer to process the response asynchronously
            QTimer.singleShot(0, lambda: self.process_response(user_message))
    
    def process_response(self, user_message):
        try:
            assistant_response = self.chatbot.chat(user_message)
            self.add_message_to_ui(role="assistant", content=assistant_response)
        except Exception as e:
            self.show_error("Error", f"Failed to get response: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)
            self.send_button.setEnabled(True)
    
    def add_message_to_ui(self, role, content):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {role.capitalize()}:\n{content}\n"
        
        # Store in database
        self.message_db.add_message(role=role, content=content)
        
        # Add to UI
        self.chat_area.append(formatted_message)
        # Scroll to bottom
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def load_messages(self):
        try:
            messages = self.message_db.get_messages()
            for message in messages:
                role = message[2]
                content = message[4]
                self.add_message_to_ui(role=role, content=content)
        except Exception as e:
            self.show_error("Error", f"Failed to load messages: {str(e)}")
    
    def clear_chat(self):
        reply = QMessageBox.question(
            self, 'Clear Chat',
            'Are you sure you want to clear the chat history?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_area.clear()
            self.message_db.clear_messages()
    
    def export_chat(self):
        messages = self.message_db.get_messages()
        chat_data = [{
            'timestamp': msg[1],
            'role': msg[2],
            'content': msg[4]
        } for msg in messages]
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_export_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Success", f"Chat exported to {filename}")
        except Exception as e:
            self.show_error("Error", f"Failed to export chat: {str(e)}")
    
    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)
