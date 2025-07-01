from datetime import datetime
from typing import List

class Message:
    def __init__(self, user: str, text: str, timestamp: datetime):
        self.user = user
        self.text = text
        self.timestamp = timestamp

class Conversation:
    def __init__(self, id: str, messages: List[Message], status: str, created_at: datetime, updated_at: datetime):
        self.id = id
        self.messages = messages
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
