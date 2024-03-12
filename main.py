import os
from openai import OpenAI
import dotenv
import json
import random
import textwrap
dotenv.load_dotenv()
import datetime

class ChatApp:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.client = OpenAI(api_key=self.api_key)
        self.messages = []
        self.random_number = random.randint(0, 99999999)
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d")
        
        self.add_system_message(
            "Welcome! As a coding assistant, I specialize in generating code using Markdown format."
            "My expertise allows me to create code like a seasoned professional."
            "Feel free to provide additional questions or context, and I will provide detailed explanations as needed."
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
        self.save_messages()
        return response.choices[0].message.content

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, response):
        if "```" in response:
            response = textwrap.dedent(response)
        self.messages.append({"role": "assistant", "content": response})

    def save_messages(self):
        with open(f"messages_self_{self.created_at}_{self.random_number}.json", "w") as f:
            json.dump(self.messages, f, indent=4)


if __name__ == "__main__":
    app = ChatApp()
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = app.chat(user_input)
        print(f"Assistant: {response}")
