from PyQt6.QtWidgets import QMainWindow, QTextEdit, QPushButton
import dotenv
from .MessageDatabase import MessageDatabase
from .ChatBot import ChatBot

dotenv.load_dotenv()

class ChatBotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 800, 600)

        self.setup_ui()

        self.chatbot = ChatBot()
        self.load_messages()

        self.show()

    def setup_ui(self):
        self.create_chat_area()
        self.create_input_field()
        self.create_send_button()

    def create_chat_area(self):
        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(10, 10, 780, 500)
        self.chat_area.setReadOnly(True)
        self.chat_area.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

    def create_input_field(self):
        self.input_field = QTextEdit(self)
        self.input_field.setGeometry(10, 520, 780, 40)

    def create_send_button(self):
        self.send_button = QPushButton("Send", self)
        self.send_button.setGeometry(700, 520, 80, 40)
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        user_message = self.input_field.toPlainText().strip()
        if user_message:
            self.add_message_to_ui(role="user", content=user_message)
            assistant_response = self.chatbot.chat(user_message)
            self.add_message_to_ui(role="assistant", content=assistant_response)
            self.input_field.clear()

    def add_message_to_ui(self, role, content):
        formatted_message = f"{role}: {content}"
        self.chat_area.append(formatted_message)

    def load_messages(self):
        messages = MessageDatabase().get_messages()
        for message in messages:
            role = message[2]
            content = message[4]
            formatted_message = f"{role}: {content}"
            self.add_message_to_ui(role=role, content=content)
