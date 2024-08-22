from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from .ui_elements import ImageButton


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

        session_layout = GridLayout(cols=2, size_hint_y=None, spacing=10)
        session_layout.bind(minimum_height=session_layout.setter("height"))

        for session in sessions:
            btn = Button(
                text=f"{session['title']}\n{session['date']}",
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

            actions_layout = BoxLayout(orientation="horizontal", size_hint=(0.2, 1))

            edit_btn = ImageButton(
                source=("assets/images/update.png"),
                size_hint=(0.5, 1),
            )
            edit_btn.bind(on_press=lambda x, s=session: self.edit_session(s))
            space_middle = Widget(size_hint_x=None, width=dp(10))
            space_right = Widget(size_hint_x=None, width=dp(10))
            delete_btn = ImageButton(
                source=("assets/images/delete.png"),
                size_hint=(0.5, 1),
            )
            delete_btn.bind(
                on_press=lambda x, s=session: self.confirm_delete_session(s)
            )

            actions_layout.add_widget(edit_btn)
            actions_layout.add_widget(space_middle)
            actions_layout.add_widget(delete_btn)
            actions_layout.add_widget(space_right)

            session_layout.add_widget(actions_layout)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(session_layout)

        self.layout.add_widget(scroll_view)

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

    def edit_session(self, session):
        try:
            new_session_screen = self.manager.get_screen("new_session")
            new_session_screen.load_session(session)
            self.manager.current = "new_session"
        except KeyError as e:
            print(f"Error: Screen not found - {e}")

    def confirm_delete_session(self, session):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        message = Label(
            text=f"Voulez-vous vraiment supprimer la session '{session['title']}' ?",
            text_size=(250, None),
            halign="center",
            valign="middle",
        )
        popup_layout.add_widget(message)

        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        yes_btn = Button(text="Oui", on_press=lambda x: self.delete_session(session))
        no_btn = Button(text="Non", on_press=lambda x: self.dismiss_popup())

        buttons_layout.add_widget(yes_btn)
        buttons_layout.add_widget(no_btn)

        popup_layout.add_widget(buttons_layout)

        self.popup = Popup(
            title="Confirmer la suppression", content=popup_layout, size_hint=(0.8, 0.4)
        )
        self.popup.open()

    def dismiss_popup(self):
        if self.popup:
            self.popup.dismiss()

    def delete_session(self, session):
        self.session_manager.delete_session(session["id"])
        self.dismiss_popup()
        self.update_sessions_list()
