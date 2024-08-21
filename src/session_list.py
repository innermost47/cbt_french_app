from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


class SessionListScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super(SessionListScreen, self).__init__(**kwargs)
        self.session_manager = session_manager
        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)
        self.update_sessions_list()

    def update_sessions_list(self):
        self.layout.clear_widgets()
        sessions = self.session_manager.get_sessions()

        session_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        session_layout.bind(minimum_height=session_layout.setter("height"))

        for session in sessions:
            btn = Button(
                text=f"{session['title']} - {session['date']}",
                size_hint=(0.8, None),
                height=dp(40),
                halign="center",
                valign="middle",
                on_press=lambda x, s=session: self.show_session_details(s),
            )
            btn.text_size = (btn.width - 20, None)
            btn.bind(
                size=lambda instance, size: setattr(
                    instance, "text_size", (instance.width - 20, None)
                )
            )
            btn.bind(
                texture_size=lambda instance, texture_size: setattr(
                    instance, "height", max(dp(40), instance.texture_size[1] + dp(20))
                )
            )
            session_layout.add_widget(btn)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(session_layout)

        self.layout.add_widget(scroll_view)

        self.layout.add_widget(Widget(size_hint_y=0.1))

        back_button = Button(text="Retour", on_press=self.go_back, size_hint=(1, 0.1))
        self.layout.add_widget(back_button)

    def show_session_details(self, session):
        try:
            self.manager.get_screen("session_detail").show_session(session)
            self.manager.current = "session_detail"
        except KeyError as e:
            print(f"Error: Screen not found - {e}")

    def go_back(self, instance):
        self.manager.current = "menu"

    def show_session_details(self, session):
        self.manager.get_screen("session_detail").show_session(session)
        self.manager.current = "session_detail"

    def go_back(self, instance):
        self.manager.current = "menu"
