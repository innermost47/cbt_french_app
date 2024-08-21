from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src import (
    SessionDetailScreen,
    NewSessionScreen,
    TitleSessionScreen,
    MenuScreen,
    SessionManager,
    SessionListScreen,
    SelectableLabel,
    LabelBase,
    font_dir,
)


class TCCApp(App):
    def build(self):
        try:
            session_manager = SessionManager("sessions.json")
            sm = ScreenManager()
            sm.add_widget(MenuScreen(session_manager, name="menu"))
            sm.add_widget(TitleSessionScreen(session_manager, name="title_session"))
            sm.add_widget(NewSessionScreen(session_manager, name="new_session"))
            sm.add_widget(SessionListScreen(session_manager, name="session_list"))
            sm.add_widget(SessionDetailScreen(name="session_detail"))
            return sm
        except Exception as e:
            print(f"An error occurred while creating the application: {e}")


if __name__ == "__main__":
    try:
        TCCApp().run()
    except Exception as e:
        print(f"An error occured at runtime: {e}")
