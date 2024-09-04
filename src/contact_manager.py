import os
import uuid
from kivy.app import App
from kivy.storage.jsonstore import JsonStore


class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.storage_path = App.get_running_app().user_data_dir
        self.store = JsonStore(os.path.join(self.storage_path, filename))
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if self.store.exists("contacts"):
            return self.store.get("contacts").get("contacts", [])
        return []

    def save_contacts(self):
        self.store.put("contacts", contacts=self.contacts)

    def get_contacts(self):
        return self.contacts

    def add_contact(self, name, surname, email, role):
        contact_id = str(uuid.uuid4())
        self.contacts.append(
            {
                "id": contact_id,
                "name": name,
                "surname": surname,
                "email": email,
                "role": role,
            }
        )
        self.save_contacts()

    def edit_contact(self, contact_id, name, surname, email, role):
        for contact in self.contacts:
            if contact["id"] == contact_id:
                contact["name"] = name
                contact["surname"] = surname
                contact["email"] = email
                contact["role"] = role
                break
        self.save_contacts()

    def delete_contact(self, contact_id):
        self.contacts = [c for c in self.contacts if c["id"] != contact_id]
        self.save_contacts()
