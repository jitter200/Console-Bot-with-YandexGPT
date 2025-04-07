# Console Bot with YandexGPT

A simple but powerful terminal-based chatbot using YandexGPT.
It supports conversation memory, multiple modes (assistant, translator, friend), and works without VPN.

## 🚀 Features

-  Multi-turn conversation with memory
-  Modes: assistant, translator, friend
-  Remembers dialogue context (automatically trims history)
- Chat history saved to chat_history.json
-  Command /reset to clear memory mid-session
- Works with YandexGPT Lite via API
- No VPN needed

## 📦 Requirements

-  Python 3.8+
-  requests
-  python-dotenv

## 🛠 Commands

-  /mode assistant	Smart helpful assistant (default)
-  /mode translator	Translates anything into Russian
-  /mode friend	Casual and friendly conversation
-  /reset	Clears chat history
-  /exit	Quits the program

## 🧠 Memory

The bot keeps your chat history and automatically shortens it if token limits are reached.
The history is saved locally in chat_history.json and reloaded when you restart the bot.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
