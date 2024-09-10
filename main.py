from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src import (
    SessionDetailScreen,
    NewSessionScreen,
    TitleSessionScreen,
    MenuScreen,
    SessionManager,
    SessionListScreen,
    ContactListScreen,
    ContactManager,
    ChatScreen,
    DistortionsScreen,
)


class TCCApp(App):
    def build(self):
        try:
            session_manager = SessionManager("sessions.json")
            contact_manager = ContactManager()
            sm = ScreenManager()
            sm.add_widget(MenuScreen(session_manager, name="menu"))
            sm.add_widget(TitleSessionScreen(session_manager, name="title_session"))
            sm.add_widget(NewSessionScreen(session_manager, name="new_session"))
            sm.add_widget(ChatScreen(session_manager, name="chat_screen"))
            sm.add_widget(
                SessionListScreen(session_manager, contact_manager, name="session_list")
            )
            sm.add_widget(ContactListScreen(contact_manager, name="contact_list"))
            sm.add_widget(SessionDetailScreen(name="session_detail"))
            sm.add_widget(DistortionsScreen(name="distortions_screen"))
            return sm
        except Exception as e:
            print(f"An error occurred while creating the application: {e}")


if __name__ == "__main__":
    try:
        TCCApp().run()
    except Exception as e:
        print(f"An error occured at runtime: {e}")
