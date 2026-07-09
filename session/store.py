import os
import json
from datetime import datetime

class SessionStore:
    def __init__(self, base_dir="data"):
        self.base_dir = base_dir
        self.sessions = {}

    def create_session(self, title = "新会话"):
        session_data = {
            "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "title": title,
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.sessions[session_data["session_id"]] = session_data
        return session_data

    def save_session(self, session):
        session_id = session["session_id"]

        if session_id in self.sessions:
            self.sessions[session_id]["messages"] = session["messages"]
            self.sessions[session_id]["updated_at"] = datetime.now().isoformat()
            
            os.makedirs(f"{self.base_dir}/sessions/{session_id}", exist_ok=True)
            
            with open(f"{self.base_dir}/sessions/{session_id}/data.json", "w", encoding="utf-8") as f:
                json.dump(self.sessions[session_id], f, ensure_ascii=False, indent=4)
        else:
            raise ValueError(f"Session ID {session_id} does not exist.")
        
    def load_session(self, session_id):
        file_path = f"{self.base_dir}/sessions/{session_id}/data.json"

        if os.path.exists(file_path):
            
            with open(file_path, "r", encoding="utf-8") as f:
               session_data = json.load(f)
               self.sessions[session_id] = session_data
            
            return session_data
    
        else:
            raise ValueError(f"Session ID {session_id} does not exist.")
    
    def list_sessions(self):
        session_diry = os.path.join(self.base_dir, "sessions")

        if not os.path.exists(session_diry):
            return []
        
        sessions = []
        for session_id in os.listdir(session_diry):
            file_path = os.path.join(session_diry, session_id, "data.json")

            if os.path.exists(file_path):

                with open(file_path, "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                    sessions.append((session_data["session_id"], session_data["title"]))

        return sessions
        
    def set_current_session_id(self, session_id):
        os.makedirs(f"{self.base_dir}", exist_ok=True)

        file_path = os.path.join(self.base_dir, "current_session.txt")

        with open(file_path, "w") as f:
            f.write(session_id)

    def get_current_session_id(self):
        file_path = os.path.join(self.base_dir, "current_session.txt")

        if not os.path.exists(file_path):
            return None
        
        with open(file_path, "r") as f:
            session_id = f.read().strip()
        
        if not session_id:
            return None
        
        return session_id
    
    def switch_session(self, session_id):

        self.load_session(session_id)  
        self.set_current_session_id(session_id)

        if session_id not in self.sessions:
            raise ValueError(f"Session ID {session_id} does not exist.")

    def rename_session(self, session_id, new_title):

        self.load_session(session_id)  

        if session_id not in self.sessions:
            raise ValueError(f"Session ID {session_id} does not exist.")
        
        self.sessions[session_id]["title"] = new_title
        self.sessions[session_id]["updated_at"] = datetime.now().isoformat()
        self.save_session(self.sessions[session_id])

    def delete_session(self, session_id):

        self.load_session(session_id)
        current_file = os.path.join(self.base_dir, "current_session.txt")

        if session_id not in self.sessions:
            raise ValueError(f"Session ID {session_id} does not exist.")
        
        del self.sessions[session_id]
        os.remove(f"{self.base_dir}/sessions/{session_id}/data.json")
        os.rmdir(f"{self.base_dir}/sessions/{session_id}")
        
        if os.path.exists(current_file) and self.get_current_session_id() == session_id:
            os.remove(current_file)