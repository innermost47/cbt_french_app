from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore
from kivy.app import App
from kivy.core.window import Window
import os
from kivy.uix.popup import Popup


class ChatScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.session_manager = session_manager

        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)

        self.clear_button = Button(
            text="Effacer l'historique",
            size_hint=(1, 0.1),
            on_press=self.show_confirmation_popup,
        )
        self.layout.add_widget(self.clear_button)

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.chat_log = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_log.bind(minimum_height=self.chat_log.setter("height"))
        self.scroll_view.add_widget(self.chat_log)
        self.layout.add_widget(self.scroll_view)

        self.input_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.2))
        self.message_input = TextInput(
            hint_text="Entrez votre message ici...",
            multiline=False,
            input_type="text",
            write_tab=False,
            keyboard_suggestions=True,
        )
        send_button = Button(text="Envoyer", on_press=self.send_message)
        back_button = Button(text="Retour", on_press=self.go_back, size_hint=(1, 0.1))
        self.input_layout.add_widget(self.message_input)
        self.input_layout.add_widget(send_button)
        self.layout.add_widget(self.input_layout)
        self.layout.add_widget(back_button)

        self.chat_store = JsonStore(
            os.path.join(App.get_running_app().user_data_dir, "memory.json")
        )
        self.chat_history = []
        self.max_history = 6
        self.load_chat_history()

    def go_back(self, instance):
        self.manager.current = "menu"

    def send_message(self, instance):
        user_message = self.message_input.text
        if user_message.strip():
            self.add_message_to_chat("Vous", user_message)
            self.message_input.text = ""

            bot_response = self.bot_response(user_message)
            self.add_message_to_chat("Bot", bot_response)

            self.save_message_to_history("Vous", user_message)
            self.save_message_to_history("Bot", bot_response)

    def add_message_to_chat(self, sender, message):
        label_width = Window.width * 0.9
        message_label = Label(
            text=f"[{sender}] {message}",
            size_hint_y=None,
            height=40,
            text_size=(label_width, None),
            halign="left",
            valign="middle",
        )

        message_label.bind(
            texture_size=lambda *x: setattr(
                message_label, "height", message_label.texture_size[1] + 10
            )
        )

        self.chat_log.add_widget(message_label)
        self.scroll_view.scroll_to(message_label)

    def bot_response(self, user_message):
        raise NotImplementedError("This method is not yet implemented.")

    def save_message_to_history(self, sender, message):
        if not self.chat_store.exists("chat"):
            self.chat_store.put("chat", messages=[])

        chat_history = self.chat_store.get("chat")["messages"]
        chat_history.append({"sender": sender, "message": message})
        self.chat_store.put("chat", messages=chat_history)
        self.chat_history = chat_history

    def load_chat_history(self):
        if self.chat_store.exists("chat"):
            chat_history = self.chat_store.get("chat")["messages"]
            self.chat_history = chat_history
            for message in chat_history:
                self.add_message_to_chat(message["sender"], message["message"])

    def reset_chat(self):
        self.chat_history = []
        if self.chat_store.exists("chat"):
            self.chat_store.put("chat", messages=[])
        self.chat_log.clear_widgets()

    def show_confirmation_popup(self, instance):
        layout = BoxLayout(orientation="vertical")
        label = Label(text="Êtes-vous sûr de vouloir effacer l'historique ?")

        popup = Popup(
            title="Confirmation",
            content=layout,
            size_hint=(None, None),
            size=(400, 200),
        )

        confirm_button = Button(
            text="Oui", on_press=lambda x: self.clear_history(popup)
        )
        cancel_button = Button(text="Non", on_press=popup.dismiss)

        layout.add_widget(label)
        layout.add_widget(confirm_button)
        layout.add_widget(cancel_button)

        popup.open()

    def clear_history(self, popup):
        self.reset_chat()
        popup.dismiss()
