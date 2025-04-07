import tiktoken
import json
import os

class ChatMemory:
    def __init__(self, max_tokens=3000, history_file="chat_history.json"):
        self.history = []
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.history_file = history_file
        self.load()

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        self._trim_memory()
        self.save()

    def _count_tokens(self, messages):
        return sum(len(self.encoding.encode(msg["content"])) for msg in messages)

    def _trim_memory(self):
        while self._count_tokens(self.history) > self.max_tokens:
            for i in range(len(self.history)):
                if self.history[i]["role"] != "system":
                    self.history.pop(i)
                    break

    def get(self):
        return self.history

    def save(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("[!] Failed to save chat history:", str(e))

    def load(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception as e:
                print("[!] Failed to load chat history:", str(e))
                self.history = []
    def reset(self):
        self.history = []
        self.save()