from kivy.app import App
from kivy.storage.jsonstore import JsonStore
import os


class SessionManager:
    def __init__(self, filename):
        self.filename = filename
        self.storage_path = App.get_running_app().user_data_dir
        self.store = JsonStore(os.path.join(self.storage_path, filename))
        self.sessions = self.load_sessions()

    def load_sessions(self):
        if self.store.exists("sessions"):
            return self.store.get("sessions").get("sessions", [])
        return []

    def save_sessions(self):
        self.store.put("sessions", sessions=self.sessions)

    def add_session(self, title, date, entries):
        self.sessions.append({"title": title, "date": date, "entries": entries})
        self.save_sessions()

    def get_sessions(self):
        return self.sessions
