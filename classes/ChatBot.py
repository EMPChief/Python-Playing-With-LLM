import dotenv
from openai import OpenAI
import os
import textwrap
from .MessageDatabase import MessageDatabase

dotenv.load_dotenv()

class ChatBot:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.client = OpenAI(api_key=self.api_key)
        self.messages = []

        self.add_system_message(
            "I'm a coding assistant. "
            "I specialize in generating code using Markdown format. "
            "I can help with any coding-related questions or tasks. "
            "Feel free to provide additional context or context, and I will provide detailed explanations as needed."
        )

    def add_system_message(self, message):
        self.messages.append({"role": "system", "content": message})

    def chat(self, user_message):
        self.add_user_message(user_message)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )
        self.add_assistant_message(response.choices[0].message.content)
        return response.choices[0].message.content
        

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})
        MessageDatabase().add_message(role="user", username="user", content=message)

    def add_assistant_message(self, response):
        if "```" in response:
            response = textwrap.dedent(response)
        self.messages.append({"role": "assistant", "content": response})
        MessageDatabase().add_message(role="assistant", username="assistant", content=response)
