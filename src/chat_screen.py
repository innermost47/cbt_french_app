from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore
from kivy.app import App
import os
import subprocess


class ChatScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.install_llama_in_termux()
        self.copy_script_to_termux()
        self.session_manager = session_manager
        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)

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
            os.path.join(App.get_running_app().user_data_dir, "chat_history.json")
        )
        self.load_chat_history()

    def llama_installed(self):
        llama_binary = "/data/data/com.termux/files/home/llama.cpp/main"
        model_file = "/data/data/com.termux/files/home/llama.cpp/models/GGUF/model.gguf"
        return os.path.exists(llama_binary) and os.path.exists(model_file)

    def install_llama_in_termux(self):
        if not self.llama_installed():
            try:
                script_src = os.path.join(
                    App.get_running_app().user_data_dir,
                    "assets",
                    "scripts",
                    "install_llama.sh",
                )
                execute_command = f"termux-open --send sh {script_src}"
                subprocess.run(execute_command, shell=True)
                print("Installing llama.cpp in Termux...")
            except Exception as e:
                print(f"Error installing llama.cpp in Termux: {e}")

    def script_copied(self):
        file = "/data/data/com.termux/files/home/run_llama.sh"
        return os.path.exists(file)

    def copy_script_to_termux(self):
        if not self.script_copied():
            try:
                script_src = os.path.join(
                    App.get_running_app().user_data_dir,
                    "assets",
                    "scripts",
                    "run_llama.sh",
                )

                termux_dest = "/data/data/com.termux/files/home/run_llama.sh"

                copy_command = f"cp {script_src} {termux_dest}"
                subprocess.run(["termux-open", "--send", copy_command], shell=True)

                chmod_command = f"chmod +x {termux_dest}"
                subprocess.run(["termux-open", "--send", chmod_command], shell=True)

                print("Script copied and made executable in Termux.")

            except Exception as e:
                print(f"Error copying script to Termux: {e}")

    def go_back(self, instance):
        self.manager.current = "menu"

    def send_message(self, instance):
        user_message = self.message_input.text
        if user_message.strip():
            self.add_message_to_chat("Vous", user_message)

            bot_response = self.bot_response(user_message)
            self.add_message_to_chat("Bot", bot_response)

            self.save_message_to_history("Vous", user_message)
            self.save_message_to_history("Bot", bot_response)

            self.message_input.text = ""

    def add_message_to_chat(self, sender, message):
        message_label = Label(text=f"[{sender}] {message}", size_hint_y=None, height=40)
        self.chat_log.add_widget(message_label)
        self.scroll_view.scroll_to(message_label)

    def bot_response(self, user_message):
        try:
            execute_command = (
                f'sh /data/data/com.termux/files/home/run_llama.sh "{user_message}"'
            )
            process = subprocess.Popen(
                ["termux-open", "--send", execute_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            output, error = process.communicate()

            if error:
                return "Error while executing the model."
            else:
                return output.decode("utf-8").strip()

        except Exception as e:
            print(f"Error in bot_response: {e}")
            return "The model could not respond."

    def save_message_to_history(self, sender, message):
        if not self.chat_store.exists("chat"):
            self.chat_store.put("chat", messages=[])
        chat_history = self.chat_store.get("chat")["messages"]
        chat_history.append({"sender": sender, "message": message})
        self.chat_store.put("chat", messages=chat_history)

    def load_chat_history(self):
        if self.chat_store.exists("chat"):
            chat_history = self.chat_store.get("chat")["messages"]
            for message in chat_history:
                self.add_message_to_chat(message["sender"], message["message"])

    def reset_chat(self):
        if self.chat_store.exists("chat"):
            self.chat_store.put("chat", messages=[])
        self.chat_log.clear_widgets()
