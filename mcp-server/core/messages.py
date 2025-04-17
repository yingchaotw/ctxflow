# messages.py

class MCPMessage:
    def __init__(self, sender, receiver, action, content, metadata=None):
        self.sender = sender
        self.receiver = receiver
        self.action = action
        self.content = content
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "action": self.action,
            "content": self.content,
            "metadata": self.metadata
        }

    @staticmethod
    def from_dict(d):
        return MCPMessage(
            sender=d["sender"],
            receiver=d["receiver"],
            action=d["action"],
            content=d["content"],
            metadata=d.get("metadata", {})
        )
