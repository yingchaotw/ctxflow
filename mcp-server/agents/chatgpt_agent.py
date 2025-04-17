# agents/chatgpt_agent.py

import os
import openai
from core.messages import MCPMessage

class ChatGPTAgent:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def handle(self, message: MCPMessage):
        if message.action != "chat":
            return {"error": f"Unsupported action: {message.action}"}

        response = openai.ChatCompletion.create(
            model="gpt-4",  # 可改成 gpt-3.5-turbo 也可
            messages=[{"role": "user", "content": message.content}],
            max_tokens=1000,
            temperature=0.7
        )

        return {
            "response": response.choices[0].message["content"]
        }
