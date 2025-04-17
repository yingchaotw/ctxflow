import os
from anthropic import Anthropic
from mcp_server.messages import MCPMessage

class ClaudeAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def handle(self, message: MCPMessage):
        if message.action != "chat":
            return {"error": f"Unsupported action: {message.action}"}

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": message.content}
            ]
        )
        return {
            "response": response.content[0].text
        }
