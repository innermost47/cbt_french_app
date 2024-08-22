from kivy.app import App
from kivy.storage.jsonstore import JsonStore
import os
import uuid


class SessionManager:
    def __init__(self, filename):
        self.filename = filename
        self.storage_path = App.get_running_app().user_data_dir
        self.store = JsonStore(os.path.join(self.storage_path, filename))
        self.sessions = self.load_sessions()
        self.ensure_sessions_have_ids()

    def load_sessions(self):
        if self.store.exists("sessions"):
            return self.store.get("sessions").get("sessions", [])
        return []

    def save_sessions(self):
        self.store.put("sessions", sessions=self.sessions)

    def add_session(self, title, date, entries):
        session_id = str(uuid.uuid4())
        self.sessions.append(
            {"id": session_id, "title": title, "date": date, "entries": entries}
        )
        self.save_sessions()

    def get_sessions(self):
        return self.sessions

    def delete_session(self, session_id):
        self.sessions = [
            session for session in self.sessions if session["id"] != session_id
        ]
        self.save_sessions()

    def ensure_sessions_have_ids(self):
        changed = False
        for session in self.sessions:
            if "id" not in session:
                session["id"] = str(uuid.uuid4())
                changed = True
        if changed:
            self.save_sessions()
