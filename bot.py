import os
import requests
from dotenv import load_dotenv
from memory import ChatMemory

load_dotenv()

IAM_TOKEN = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

YANDEXGPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
HEADERS = {
    "Authorization": f"Bearer {IAM_TOKEN}",
    "Content-Type": "application/json"
}

memory = ChatMemory()

MODES = {
    "assistant": "You are a helpful assistant.",
    "translator": "Translate any incoming message into Russian.",
    "friend": "You are a friendly and casual conversation partner.",
}

current_mode = "assistant"

def set_mode(mode):
    global current_mode
    if mode in MODES:
        current_mode = mode
        memory.add("system", MODES[mode])
        print(f"[🤖] Mode switched to: {mode}")
    else:
        print("[!] Unknown mode")

def generate_prompt():
    messages = memory.get()
    prompt = ""
    for msg in messages:
        role = msg["role"]
        prefix = "User:" if role == "user" else "Assistant:" if role == "assistant" else ""
        prompt += f"{prefix} {msg['content']}\n"
    prompt += "Assistant:"
    return prompt

def ask_yandex(prompt):
    payload = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 200
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    response = requests.post(YANDEXGPT_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["result"]["alternatives"][0]["message"]["text"]

def chat():
    print("Hello! Type your message (or /mode [assistant|translator|friend], /reset, /exit):")
    set_mode(current_mode)

    while True:
        user_input = input("You: ")

        if user_input.startswith("/mode"):
            parts = user_input.split()
            if len(parts) == 2:
                _, new_mode = parts
                set_mode(new_mode)
            else:
                print("[!] Use format: /mode assistant")
            continue

        elif user_input == "/reset":
            memory.reset()
            set_mode(current_mode)
            print("[🤖] Chat history has been reset.")
            continue

        elif user_input == "/exit":
            print("Goodbye!")
            break

        memory.add("user", user_input)

        try:
            prompt = generate_prompt()
            reply = ask_yandex(prompt)
            print("YandexGPT:", reply)
            memory.add("assistant", reply)

        except Exception as e:
            print("[Error while communicating with YandexGPT API]", str(e))

if __name__ == "__main__":
    chat()
