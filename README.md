# Python-Playing-With-LLM

A modern and feature-rich Python application for interacting with language models like GPT-3.5 and GPT-4. This application provides a clean and intuitive GUI interface for chatting with AI models, with support for code generation, conversation history, and more.

## Features

- 🎨 Modern, dark-themed GUI interface
- 💾 Persistent conversation history with SQLite
- 📤 Export conversations to JSON
- ⚙️ Configurable AI model parameters
- 🔄 Asynchronous message processing
- 🎯 Code-focused responses with proper formatting
- 🛡️ Robust error handling
- 📝 Message timestamps and metadata
- 🔍 Search through conversation history
- 🧹 Clear chat functionality

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Python-Playing-With-LLM.git
cd Python-Playing-With-LLM
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
Create a `.env` file in the project root and add your API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the application:
```bash
python main.py
```

### Features Guide

1. **Chat Interface**
   - Type messages in the input field
   - Press Enter to send (Shift+Enter for new line)
   - Code blocks are automatically formatted
   - Timestamps show when messages were sent

2. **Configuration**
   - Model selection (GPT-3.5, GPT-4)
   - Temperature control
   - Max tokens limit
   - System message customization

3. **History Management**
   - Export conversations to JSON
   - Clear chat history
   - Search through past messages
   - Persistent storage in SQLite database

4. **Code Generation**
   - Automatic code block formatting
   - Syntax highlighting
   - Copy code button
   - Multiple language support

## Project Structure

```
Python-Playing-With-LLM/
├── main.py              # Application entry point
├── requirements.txt     # Project dependencies
├── .env                # Environment variables
├── classes/
│   ├── ChatBot.py      # AI interaction logic
│   ├── ChatBotWindow.py # GUI implementation
│   ├── MessageDatabase.py # Database operations
│   └── styles.py       # UI styling
└── data/               # Database and exports
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for their powerful language models
- PyQt6 for the GUI framework
- The open-source community for inspiration and support

