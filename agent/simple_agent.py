from llm.client import DeepSeekClient
from config.settings import settings
from session.store import SessionStore


class SimpleAgent:

    def __init__(self, store):
        self.client = DeepSeekClient()
        self.store = store

    def run(self, user_message: str) -> str:

        current_session_id = self.store.get_current_session_id()
        if current_session_id is None:
            raise RuntimeError("当前没有会话，请先使用 /session new <title> 创建会话")

        session = self.store.load_session(current_session_id)
        
        user_entry = {"role": "user", "content": user_message}
        
        messages_for_request = session["messages"] + [user_entry]

        response = self.client.chat(messages_for_request)
        
        session["messages"].append({"role": "user", "content": user_message})
        session["messages"].append({"role": "assistant", "content": response})

        self.store.save_session(session)

        return response
