import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.clock import Clock
import json
import os
import datetime

font_dir = os.path.join(os.path.dirname(__file__), "fonts")

LabelBase.register(
    name="Roboto",
    fn_regular=os.path.join(font_dir, "Roboto-Regular.ttf"),
    fn_bold=os.path.join(font_dir, "Roboto-Bold.ttf"),
)


SESSIONS_FILE = "sessions.json"


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            self.parent.select_with_touch(self.index, touch)
            return True

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            session = rv.data[index]["session"]
            rv.parent.parent.show_session_details(session)


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

        back_button = Button(
            text="Retour", on_press=self.go_back, size_hint_y=None, height=40
        )
        self.layout.add_widget(back_button)

    def show_session_details(self, session):
        self.manager.get_screen("session_detail").show_session(session)
        self.manager.current = "session_detail"

    def go_back(self, instance):
        self.manager.current = "menu"

    def show_session_details(self, session):
        self.manager.get_screen("session_detail").show_session(session)
        self.manager.current = "session_detail"

    def go_back(self, instance):
        self.manager.current = "menu"


class SessionManager:
    def __init__(self, filename):
        self.filename = filename
        self.sessions = self.load_sessions()

    def load_sessions(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f).get("sessions", [])
        return []

    def save_sessions(self):
        with open(self.filename, "w") as f:
            json.dump({"sessions": self.sessions}, f)

    def add_session(self, title, date, entries):
        self.sessions.append({"title": title, "date": date, "entries": entries})
        self.save_sessions()

    def get_sessions(self):
        return self.sessions


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


class TitleSessionScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super(TitleSessionScreen, self).__init__(**kwargs)
        self.session_manager = session_manager
        self.layout = BoxLayout(orientation="vertical")

        self.title_input = TextInput(
            hint_text="Donner un titre à la session", size_hint_y=0.2
        )
        self.start_button = Button(text="Commencer", on_press=self.start_session)

        self.layout.add_widget(self.title_input)
        self.layout.add_widget(self.start_button)
        self.add_widget(self.layout)

    def start_session(self, instance):
        title = self.title_input.text.strip()
        if title:
            self.manager.get_screen("new_session").start_new_session(title)
            self.manager.current = "new_session"
        else:
            self.title_input.hint_text = "Le titre ne peut pas être vide"


class NewSessionScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super(NewSessionScreen, self).__init__(**kwargs)
        self.session_manager = session_manager
        self.current_question = 0
        self.entries = []

        self.layout = BoxLayout(orientation="vertical")
        self.title = ""

        self.question_label = Label(
            text="Décrivez la situation de manière objective :",
            size_hint_y=0.4,
            text_size=(700, None),
            halign="left",
            valign="middle",
        )
        self.response_input = TextInput(hint_text="Votre réponse ici", size_hint_y=0.4)

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

        self.questions = [
            "Décrivez la situation de manière objective :",
            "Quelles émotions ressentez-vous ?",
            "Quelles pensées avez-vous ?",
            "La pensée est-elle bien vraie ? Contre-preuves spécifiques ?",
            "Ma source d’information est-elle la bonne ?",
            "Est-ce que je remplace des probabilités par des certitudes ? et pourquoi ?",
            "Suis-je obligé d’agir ainsi ? et pourquoi ?",
            "Pouvez-vous envisager d'autres explications/hypothèses ?",
            "Que dirait votre entourage (famille, amis, célébrités) ?",
            "Quel est le point de vue idéal (dans 5 ans) ?",
            "Que diriez-vous à votre meilleur ami dans cette situation ?",
            "Quel serait le point de vue de quelqu'un d'autre ?",
            "Et si c’est le cas, quelles seraient les conséquences à court terme, moyen terme, long terme ?",
            "Est-ce que c’est si terrible ? et pourquoi ?",
            "Pourriez-vous quand même être heureux(se) ? et pourquoi ?",
            "L’avenir est-il compromis ?",
            "Quels moyens pourriez-vous utiliser pour vous adapter ? Comment feriez-vous face ?",
        ]

    def start_new_session(self, title):
        self.title = title
        self.current_question = 0
        self.entries = []
        self.update_ui()

    def update_ui(self):
        self.question_label.text = self.questions[self.current_question]
        self.response_input.text = ""
        self.prev_button.disabled = self.current_question == 0

    def next_question(self, instance):
        response = self.response_input.text.strip()
        if response:
            self.entries.append(
                {
                    "question": self.questions[self.current_question],
                    "response": response,
                }
            )

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.update_ui()
        else:
            self.save_session()

    def prev_question(self, instance):
        if self.current_question > 0:
            self.current_question -= 1
            self.entries.pop()
            self.update_ui()

    def save_session(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.session_manager.add_session(self.title, date, self.entries)
        self.manager.current = "menu"


class SessionDetailScreen(Screen):
    def __init__(self, **kwargs):
        super(SessionDetailScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)

    def show_session(self, session):
        self.layout.clear_widgets()
        Clock.schedule_once(lambda dt: self.build_session(session), 0.1)

    def build_session(self, session):
        scroll_view = ScrollView(size_hint=(1, 1))
        grid_layout = GridLayout(cols=1, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter("height"))

        title_label = Label(
            text=f"[b]Titre: {session['title']}[/b]",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="top",
            text_size=(self.width - 20, None),
        )
        title_label.bind(
            size=lambda lbl, _: lbl.setter("text_size")(lbl, (lbl.width, None))
        )
        title_label.texture_update()
        title_label.height = title_label.texture_size[1]
        grid_layout.add_widget(title_label)

        date_label = Label(
            text=f"[b]Date [/b]: {session['date']}\n",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="top",
            text_size=(self.width - 20, None),
        )
        date_label.bind(
            size=lambda lbl, _: lbl.setter("text_size")(lbl, (lbl.width, None))
        )
        date_label.texture_update()
        date_label.height = date_label.texture_size[1]
        grid_layout.add_widget(date_label)

        for entry in session["entries"]:
            question_label = Label(
                text=f"[b]Question: {entry['question']}[/b]",
                markup=True,
                size_hint_y=None,
                halign="left",
                valign="top",
                text_size=(self.width - 20, None),
            )
            question_label.bind(
                size=lambda lbl, _: lbl.setter("text_size")(lbl, (lbl.width, None))
            )
            question_label.texture_update()
            question_label.height = question_label.texture_size[1]

            response_label = Label(
                text=f"Réponse: {entry['response']}\n",
                size_hint_y=None,
                halign="left",
                valign="top",
                text_size=(self.width - 20, None),
            )
            response_label.bind(
                size=lambda lbl, _: lbl.setter("text_size")(lbl, (lbl.width, None))
            )
            response_label.texture_update()
            response_label.height = response_label.texture_size[1]

            grid_layout.add_widget(question_label)
            grid_layout.add_widget(response_label)

        scroll_view.add_widget(grid_layout)

        self.layout.add_widget(scroll_view)

        back_button = Button(
            text="Retour", on_press=self.go_back, size_hint_y=None, height=40
        )
        self.layout.add_widget(back_button)

        grid_layout.height = grid_layout.minimum_height
        scroll_view.scroll_y = 1
        grid_layout.do_layout()

    def go_back(self, instance):
        self.manager.current = "session_list"


class TCCApp(App):
    def build(self):
        session_manager = SessionManager(SESSIONS_FILE)

        sm = ScreenManager()
        sm.add_widget(MenuScreen(session_manager, name="menu"))
        sm.add_widget(TitleSessionScreen(session_manager, name="title_session"))
        sm.add_widget(NewSessionScreen(session_manager, name="new_session"))
        sm.add_widget(SessionListScreen(session_manager, name="session_list"))
        sm.add_widget(SessionDetailScreen(name="session_detail"))

        return sm


if __name__ == "__main__":
    TCCApp().run()
