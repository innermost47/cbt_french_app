from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class MenuScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.session_manager = session_manager
        layout = BoxLayout(orientation="vertical")

        new_session_button = Button(
            text="Nouvelle Session", on_press=self.start_new_session
        )
        view_sessions_button = Button(
            text="Voir les Sessions", on_press=self.view_sessions
        )

        layout.add_widget(new_session_button)
        layout.add_widget(view_sessions_button)
        self.add_widget(layout)

    def start_new_session(self, instance):
        self.manager.current = "title_session"

    def view_sessions(self, instance):
        self.manager.current = "session_list"
