from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from .ui_elements import ImageButton, EmailTextInput


class ContactListScreen(Screen):
    def __init__(self, contact_manager, **kwargs):
        super(ContactListScreen, self).__init__(**kwargs)
        self.contact_manager = contact_manager
        self.layout = BoxLayout(orientation="vertical")
        self.add_widget(self.layout)
        self.update_contact_list()

    def update_contact_list(self):
        self.layout.clear_widgets()
        contacts = self.contact_manager.get_contacts()

        contact_layout = GridLayout(cols=2, size_hint_y=None, spacing=10)
        contact_layout.bind(minimum_height=contact_layout.setter("height"))

        for contact in contacts:
            btn = Button(
                text=f"{contact['name']} {contact['surname']} - {contact['email']} ({contact['role']})",
                size_hint=(0.8, None),
                height=dp(40),
                halign="center",
                valign="middle",
                on_press=lambda x, c=contact: self.edit_contact(c),
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
            contact_layout.add_widget(btn)

            actions_layout = BoxLayout(orientation="horizontal", size_hint=(0.2, 1))

            edit_btn = ImageButton(
                source=("assets/images/update.png"),
                size_hint=(0.5, 1),
            )
            edit_btn.bind(on_press=lambda x, c=contact: self.edit_contact(c))
            space_middle = Widget(size_hint_x=None, width=dp(10))
            space_right = Widget(size_hint_x=None, width=dp(10))
            delete_btn = ImageButton(
                source=("assets/images/delete.png"),
                size_hint=(0.5, 1),
            )
            delete_btn.bind(
                on_press=lambda x, c=contact: self.confirm_delete_contact(c)
            )

            actions_layout.add_widget(edit_btn)
            actions_layout.add_widget(space_middle)
            actions_layout.add_widget(delete_btn)
            actions_layout.add_widget(space_right)

            contact_layout.add_widget(actions_layout)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(contact_layout)

        self.layout.add_widget(scroll_view)

        add_button = Button(
            text="Ajouter un contact",
            on_press=self.add_contact_popup,
            size_hint=(1, 0.1),
        )
        self.layout.add_widget(add_button)

        back_button = Button(text="Retour", on_press=self.go_back, size_hint=(1, 0.1))
        self.layout.add_widget(back_button)

    def add_contact_popup(self, instance):
        self.show_contact_popup()

    def edit_contact(self, contact):
        self.show_contact_popup(contact)

    def show_contact_popup(self, contact=None):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        name_input = TextInput(
            hint_text="Nom",
            text=contact["name"] if contact else "",
            input_type="text",
            write_tab=False,
            keyboard_suggestions=True,
        )
        surname_input = TextInput(
            hint_text="Prénom",
            text=contact["surname"] if contact else "",
            input_type="text",
            write_tab=False,
            keyboard_suggestions=True,
        )
        email_input = EmailTextInput(
            hint_text="Email",
            text=contact["email"] if contact else "",
            input_type="mail",
            write_tab=False,
            keyboard_suggestions=True,
        )
        role_input = TextInput(
            hint_text="Rôle",
            text=contact["role"] if contact else "",
            input_type="text",
            write_tab=False,
            keyboard_suggestions=True,
        )

        popup_layout.add_widget(name_input)
        popup_layout.add_widget(surname_input)
        popup_layout.add_widget(email_input)
        popup_layout.add_widget(role_input)

        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        save_btn = Button(
            text="Sauvegarder",
            on_press=lambda x: self.save_contact(
                contact,
                name_input.text,
                surname_input.text,
                email_input.text,
                role_input.text,
            ),
        )
        cancel_btn = Button(text="Annuler", on_press=lambda x: self.dismiss_popup())

        buttons_layout.add_widget(save_btn)
        buttons_layout.add_widget(cancel_btn)

        popup_layout.add_widget(buttons_layout)

        self.popup = Popup(
            title="Ajouter/Editer un contact",
            content=popup_layout,
            size_hint=(0.8, 0.6),
        )
        self.popup.open()

    def save_contact(self, contact, name, surname, email, role):
        if contact:
            self.contact_manager.edit_contact(contact["id"], name, surname, email, role)
        else:
            self.contact_manager.add_contact(name, surname, email, role)

        self.update_contact_list()
        self.dismiss_popup()

    def dismiss_popup(self):
        if self.popup:
            self.popup.dismiss()

    def confirm_delete_contact(self, contact):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        message = Label(
            text=f"Voulez-vous vraiment supprimer le contact '{contact['name']} {contact['surname']}' ?",
            text_size=(250, None),
            halign="center",
            valign="middle",
        )
        popup_layout.add_widget(message)

        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        yes_btn = Button(text="Oui", on_press=lambda x: self.delete_contact(contact))
        no_btn = Button(text="Non", on_press=lambda x: self.dismiss_popup())

        buttons_layout.add_widget(yes_btn)
        buttons_layout.add_widget(no_btn)

        popup_layout.add_widget(buttons_layout)

        self.popup = Popup(
            title="Confirmer la suppression", content=popup_layout, size_hint=(0.8, 0.4)
        )
        self.popup.open()

    def delete_contact(self, contact):
        self.contact_manager.delete_contact(contact["id"])
        self.dismiss_popup()
        self.update_contact_list()

    def go_back(self, instance):
        self.manager.current = "menu"

    def select_contact_for_sharing(self, session):
        self.selected_session = session
        self.layout.clear_widgets()
        contacts = self.contact_manager.get_contacts()

        contact_layout = GridLayout(cols=2, size_hint_y=None, spacing=10)
        contact_layout.bind(minimum_height=contact_layout.setter("height"))

        self.selected_contacts = []

        for contact in contacts:
            contact_label = Label(
                text=f"{contact['name']} {contact['surname']} ({contact['role']})",
                size_hint=(0.7, None),
                height=dp(40),
            )
            checkbox = CheckBox(size_hint=(0.3, None), height=dp(40))
            checkbox.bind(
                active=lambda checkbox, active, c=contact: self.toggle_contact_selection(
                    c, active
                )
            )
            contact_layout.add_widget(contact_label)
            contact_layout.add_widget(checkbox)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(contact_layout)

        self.layout.add_widget(scroll_view)

        share_button = Button(
            text="Partager",
            on_press=self.share_session_with_selected_contacts,
            size_hint=(1, 0.1),
        )
        self.layout.add_widget(share_button)

        back_button = Button(text="Retour", on_press=self.go_back, size_hint=(1, 0.1))
        self.layout.add_widget(back_button)

    def toggle_contact_selection(self, contact, active):
        if active:
            self.selected_contacts.append(contact)
        else:
            self.selected_contacts.remove(contact)

    def share_session_with_selected_contacts(self, instance):
        for contact in self.selected_contacts:
            self.send_email(contact["email"], self.selected_session)
        self.manager.current = "session_list"
