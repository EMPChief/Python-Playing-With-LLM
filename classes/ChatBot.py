import dotenv
from openai import OpenAI
import os
import textwrap
import json
from typing import List, Dict, Optional, Union
from .MessageDatabase import MessageDatabase

dotenv.load_dotenv()

class ChatBotConfig:
    """Configuration class for ChatBot settings."""
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        system_message: str = (
            "I'm a coding assistant specialized in generating code using Markdown format. "
            "I can help with any coding-related questions or tasks. "
            "I provide detailed explanations and follow best practices in software development."
        )
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.system_message = system_message

class ChatBot:
    def __init__(self, config: Optional[ChatBotConfig] = None):
        """
        Initialize the ChatBot with optional configuration.
        
        Args:
            config: Optional ChatBotConfig instance for customization
        """
        self.config = config or ChatBotConfig()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.messages: List[Dict[str, str]] = []
        self.message_db = MessageDatabase()
        
        # Initialize with system message
        self.add_system_message(self.config.system_message)
    
    def add_system_message(self, message: str) -> None:
        """Add a system message to the conversation."""
        self.messages.append({"role": "system", "content": message})
    
    def chat(self, user_message: str) -> str:
        """
        Process a user message and get a response from the AI.
        
        Args:
            user_message: The user's input message
        
        Returns:
            str: The AI's response
        
        Raises:
            Exception: If there's an error communicating with the API
        """
        try:
            # Add user message
            self.add_user_message(user_message)
            
            # Create chat completion
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=self.messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                presence_penalty=self.config.presence_penalty,
                frequency_penalty=self.config.frequency_penalty
            )
            
            # Process and store response
            assistant_message = response.choices[0].message.content
            self.add_assistant_message(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error in chat completion: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
    
    def add_user_message(self, message: str) -> None:
        """
        Add a user message to the conversation history.
        
        Args:
            message: The user's message
        """
        self.messages.append({"role": "user", "content": message})
        self.message_db.add_message(
            role="user",
            content=message,
            metadata={"timestamp": "user_message"}
        )
    
    def add_assistant_message(self, response: str) -> None:
        """
        Add an assistant message to the conversation history.
        
        Args:
            response: The assistant's response
        """
        # Format code blocks if present
        if "```" in response:
            response = textwrap.dedent(response)
        
        self.messages.append({"role": "assistant", "content": response})
        self.message_db.add_message(
            role="assistant",
            content=response,
            metadata={"timestamp": "assistant_response"}
        )
    
    def get_conversation_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Args:
            limit: Optional limit on number of messages to retrieve
        
        Returns:
            List of message dictionaries
        """
        return self.messages[-limit:] if limit else self.messages
    
    def clear_conversation(self) -> None:
        """Clear the conversation history, keeping only the system message."""
        system_message = next((msg for msg in self.messages if msg["role"] == "system"), None)
        self.messages.clear()
        if system_message:
            self.messages.append(system_message)
    
    def save_conversation(self, filename: str) -> bool:
        """
        Save the conversation history to a file.
        
        Args:
            filename: The name of the file to save to
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def load_conversation(self, filename: str) -> bool:
        """
        Load a conversation history from a file.
        
        Args:
            filename: The name of the file to load from
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return False
