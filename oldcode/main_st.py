import os
from openai import OpenAI
import dotenv
import json
import random
import textwrap
import datetime
import streamlit as st

dotenv.load_dotenv()


class ChatApp:
    def __init__(self, api_key=None):
        self.api_key = api_key
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

    def chat(self, user_message, model="gpt-3.5-turbo"):
        self.add_user_message(user_message)
        response = self.client.chat.completions.create(
            model=model,
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
        with open(f"data/messages_self_{self.created_at}_{self.random_number}.json", "w") as f:
            json.dump(self.messages, f, indent=4)


def main():
    st.title("Chat with OpenAI GPT Models")
    st.sidebar.header("Settings")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    model_choice = st.sidebar.selectbox(
        "Select a GPT Model",
        [
            "gpt-3.5-turbo",
            "gpt-4-0125-preview",
            "gpt-4-turbo-preview",
            "gpt-4-1106-preview",
            "gpt-4",
            "gpt-3.5-turbo-0125",

        ],
    )
    app = ChatApp(api_key)

    st.markdown(
        "Welcome! This is a chat application powered by OpenAI's GPT models. "
        "Enter your message on the left, select a model from the sidebar, "
        "and the AI will respond on the right."
    )

    user_input = st.text_area("User Input", "")
    if st.button("Send"):
        assistant_response = app.chat(user_input, model=model_choice)
        st.write("Assistant:", assistant_response)

    if st.button("Exit"):
        app.save_messages()
        st.stop()


if __name__ == "__main__":
    main()
