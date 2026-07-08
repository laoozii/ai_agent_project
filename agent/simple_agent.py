from llm.client import DeepSeekClient
from config.settings import settings

class SimpleAgent:
    def __init__(self):
        settings.validate_required()
        self.client = DeepSeekClient()

    def run(self, user_message: str) -> str:
        response = self.client.chat(user_message)
        return response
