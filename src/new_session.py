from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import datetime


class NewSessionScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super(NewSessionScreen, self).__init__(**kwargs)
        self.session_manager = session_manager
        self.current_question = 0
        self.questions = [
            "Décrivez les faits de la situation de manière neutre, sans jugement ni interprétation.",
            "Quels sont les sentiments ou les émotions que vous ressentez actuellement dans cette situation ?",
            "Quelles sont les pensées qui vous traversent l'esprit à propos de cette situation ?",
            "Est-ce que cette pensée est complètement exacte ? Pouvez-vous identifier des faits ou des éléments qui contredisent cette pensée ?",
            "Les informations sur lesquelles vous basez cette pensée sont-elles fiables et précises ?",
            "Est-ce que vous confondez des probabilités avec des certitudes ? Si oui, pourquoi ?",
            "Est-ce que vous vous sentez contraint d'agir de cette manière ? Si oui, pourquoi ?",
            "Pouvez-vous imaginer d'autres explications ou hypothèses pour cette situation ?",
            "Comment pensez-vous que votre entourage (famille, amis, personnalités publiques) réagirait à cette situation ?",
            "Quel pourrait être votre point de vue idéal sur cette situation dans 5 ans ?",
            "Que conseilleriez-vous à votre meilleur ami s'il était dans cette situation ?",
            "Comment quelqu'un d'autre pourrait-il percevoir cette situation ?",
            "Si cette pensée ou croyance était vraie, quelles seraient les conséquences concrètes pour vous à court terme, moyen terme et long terme ?",
            "Cette situation est-elle vraiment aussi catastrophique que vous le percevez ? Quels sont les éléments qui vous font penser cela ?",
            "Malgré cette situation ou cette croyance, croyez-vous qu'il soit encore possible pour vous de trouver du bonheur ? Qu'est-ce qui pourrait vous en empêcher ou, au contraire, vous y aider ?",
            "Cette situation compromet-elle réellement votre avenir ?",
            "Quels moyens pourriez-vous utiliser pour vous adapter à cette situation ? Comment feriez-vous face aux défis qu'elle présente ?",
        ]
        self.entries = [{}] * len(self.questions)

        self.layout = BoxLayout(orientation="vertical")
        self.title = ""

        self.question_label = Label(
            text="Décrivez la situation de manière objective :",
            size_hint_y=0.4,
            text_size=(700, None),
            halign="left",
            valign="middle",
        )
        self.response_input = TextInput(
            hint_text="Votre réponse ici",
            size_hint_y=0.4,
            input_type="text",
            write_tab=False,
            keyboard_suggestions=True,
        )

        self.button_layout = BoxLayout(size_hint_y=0.2)
        self.prev_button = Button(
            text="Précédent", on_press=self.prev_question, size_hint=(0.5, 1)
        )
        self.prev_button.disabled = True
        self.next_button = Button(
            text="Suivant", on_press=self.next_question, size_hint=(0.5, 1)
        )

        self.button_layout.add_widget(self.prev_button)
        self.button_layout.add_widget(self.next_button)

        self.layout.add_widget(self.question_label)
        self.layout.add_widget(self.response_input)
        self.layout.add_widget(self.button_layout)

        self.add_widget(self.layout)

    def start_new_session(self, title):
        try:
            self.title = title
            self.current_question = 0
            self.entries = [{}] * len(self.questions)
            self.response_input.text = ""
            self.update_ui()
        except Exception as e:
            print(f"Error creating new session: {e}")

    def update_ui(self):
        self.question_label.text = self.questions[self.current_question]
        current_entry = self.entries[self.current_question]
        self.response_input.text = current_entry.get("response", "")

        self.prev_button.disabled = self.current_question == 0

    def next_question(self, instance):
        try:
            self.save_current_response()
            if self.current_question < len(self.questions) - 1:
                self.current_question += 1
                self.update_ui()
            else:
                self.save_session()
        except Exception as e:
            print(f"An error occured while trying to navigate to next question: {e}")

    def prev_question(self, instance):
        try:
            self.save_current_response()
            if self.current_question > 0:
                self.current_question -= 1
                self.update_ui()
        except Exception as e:
            print(
                f"An error occured while trying to navigate to previous question: {e}"
            )

    def save_current_response(self):
        try:
            response = self.response_input.text.strip()
            self.entries[self.current_question] = {
                "question": self.questions[self.current_question],
                "response": response,
            }
        except Exception as e:
            print(f"An error occured while trying to save current response: {e}")

    def save_session(self):
        try:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            valid_entries = [entry for entry in self.entries if entry.get("response")]
            session_exists = False
            for session in self.session_manager.sessions:
                if session["title"] == self.title:
                    session["date"] = date
                    session["entries"] = valid_entries
                    session_exists = True
                    break
            if not session_exists:
                self.session_manager.add_session(self.title, date, valid_entries)
            self.session_manager.save_sessions()
            session_list_screen = self.manager.get_screen("session_list")
            session_list_screen.update_sessions_list()
            self.manager.current = "menu"
        except Exception as e:
            print(f"An error occured while trying to save session: {e}")

    def load_session(self, session):
        try:
            self.title = session["title"]
            self.current_question = 0
            self.entries = [{}] * len(self.questions)
            for entry in session["entries"]:
                for i, question in enumerate(self.questions):
                    if entry["question"] == question:
                        self.entries[i] = entry
                        break

            self.update_ui()
        except Exception as e:
            print(f"Error loading session: {e}")
