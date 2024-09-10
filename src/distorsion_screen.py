from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button


class DistortionsScreen(Screen):
    def __init__(self, **kwargs):
        super(DistortionsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        save_button = Button(text="Enregistrer et revenir au menu", size_hint_y=0.2)
        save_button.bind(on_press=self.save_distortions)
        self.layout.add_widget(save_button)

        self.cognitive_distortions = [
            (
                "La pensée dichotomique",
                "C'est le fait de penser que si une chose n'est pas exactement comme nous le souhaitons, alors il s'agit d'un échec. Cela entraîne une perte totale des nuances.",
            ),
            (
                "La surgénéralisation",
                "Construire des règles pour son comportement futur à partir de quelques événements négatifs passés. Exemple : 'Je n'arrive jamais à réussir.'",
            ),
            (
                "L'abstraction sélective",
                "Se concentrer uniquement sur les détails négatifs d'une situation, en négligeant les aspects positifs.",
            ),
            (
                "La disqualification du positif",
                "Transformer une expérience positive en expérience négative, ou ignorer les aspects positifs d'une situation.",
            ),
            (
                "Les conclusions hâtives",
                "Tirer des conclusions négatives sans preuves. Cela inclut la lecture des pensées d'autrui et les prédictions pessimistes.",
            ),
            (
                "Exagération (dramatisation) et minimalisation",
                "Exagérer ses erreurs ou minimiser ses réussites.",
            ),
            (
                "Le raisonnement émotionnel",
                "Utiliser ses émotions comme preuve de la réalité. Exemple : 'Je me sens désespéré, donc mes problèmes sont insolubles.'",
            ),
            (
                "Les fausses obligations",
                "Se fixer arbitrairement des buts ou des obligations. Exemple : 'Je dois être parfait.'",
            ),
            (
                "L'étiquetage",
                "Attribuer des jugements définitifs à soi-même ou aux autres. Exemple : 'Je suis un raté.'",
            ),
            (
                "La personnalisation",
                "Se sentir responsable des actions ou des émotions des autres, même lorsque cela n'est pas fondé.",
            ),
        ]

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.add_cognitive_distortions()

    def add_cognitive_distortions(self):
        self.layout.clear_widgets()
        distortions_layout = GridLayout(cols=1, size_hint_y=None)
        distortions_layout.bind(minimum_height=distortions_layout.setter("height"))
        selected_distortions = []
        if self.manager:
            new_session_screen = self.manager.get_screen("new_session")
            selected_distortions = new_session_screen.selected_distortions
        else:
            print("Error: ScreenManager not found.")

        self.distortion_checkboxes = {}
        for distortion, description in self.cognitive_distortions:
            box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
            label = Label(text=distortion, halign="left", valign="middle")
            checkbox = CheckBox()

            if distortion in selected_distortions:
                checkbox.active = True

            self.distortion_checkboxes[distortion] = checkbox

            box.add_widget(label)
            box.add_widget(checkbox)

            info_button = Button(text="?", size_hint=(0.2, 1))
            info_button.bind(
                on_press=lambda instance, desc=description: self.show_description(desc)
            )

            box.add_widget(info_button)
            distortions_layout.add_widget(box)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(distortions_layout)
        self.layout.add_widget(scroll_view)

        save_button = Button(text="Enregistrer et revenir au menu", size_hint=(1, 0.1))
        save_button.bind(on_press=self.save_distortions)
        self.layout.add_widget(save_button)

    def show_description(self, description):
        popup_layout = BoxLayout(orientation="vertical")
        popup_label = Label(
            text=description, text_size=(400, None), halign="left", valign="middle"
        )
        close_button = Button(text="Fermer", size_hint_y=None, height=40)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Description de la distorsion",
            content=popup_layout,
            size_hint=(0.8, 0.8),
        )
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def save_distortions(self, instance):
        selected_distortions = [
            distortion
            for distortion, checkbox in self.distortion_checkboxes.items()
            if checkbox.active
        ]
        new_session_screen = self.manager.get_screen("new_session")
        new_session_screen.selected_distortions = selected_distortions
        new_session_screen.save_session()
        self.manager.current = "menu"
