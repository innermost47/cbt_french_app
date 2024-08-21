from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class TitleSessionScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super(TitleSessionScreen, self).__init__(**kwargs)
        self.session_manager = session_manager
        self.layout = BoxLayout(orientation="vertical")

        self.title_input = TextInput(
            hint_text="Donner un titre à la session",
            size_hint_y=0.2,
            input_type="text",
            keyboard_suggestions=True,
        )
        self.start_button = Button(
            text="Commencer",
            on_press=self.start_session,
            size_hint=(1, 0.1),
        )

        self.layout.add_widget(self.title_input)
        self.layout.add_widget(self.start_button)
        self.add_widget(self.layout)

    def start_session(self, instance):
        try:
            title = self.title_input.text.strip()
            if title:
                self.manager.get_screen("new_session").start_new_session(title)
                self.manager.current = "new_session"
            else:
                self.title_input.hint_text = "Le titre ne peut pas être vide"
        except Exception as e:
            print(f"Error starting session: {e}")
