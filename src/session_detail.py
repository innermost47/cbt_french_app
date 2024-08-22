from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock


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
            text="Retour", on_press=self.go_back, size_hint=(1, 0.1)
        )
        self.layout.add_widget(back_button)

        grid_layout.height = grid_layout.minimum_height
        scroll_view.scroll_y = 1
        grid_layout.do_layout()

    def go_back(self, instance):
        self.manager.current = "session_list"
