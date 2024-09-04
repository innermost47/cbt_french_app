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
from jnius import autoclass, cast
from kivy.utils import platform
from .ui_elements import ImageButton


class SessionListScreen(Screen):
    def __init__(self, session_manager, contact_manager, **kwargs):
        super(SessionListScreen, self).__init__(**kwargs)
        self.session_manager = session_manager
        self.contact_manager = contact_manager
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
                size_hint=(1 / 3, 1),
            )
            edit_btn.bind(on_press=lambda x, s=session: self.edit_session(s))
            space_middle = Widget(size_hint_x=None, width=dp(10))
            space_between = Widget(size_hint_x=None, width=dp(10))
            space_right = Widget(size_hint_x=None, width=dp(10))
            delete_btn = ImageButton(
                source=("assets/images/delete.png"),
                size_hint=(1 / 3, 1),
            )
            delete_btn.bind(
                on_press=lambda x, s=session: self.confirm_delete_session(s)
            )

            share_btn = ImageButton(
                source=("assets/images/share.png"),
                size_hint=(1 / 3, 1),
            )
            share_btn.bind(on_press=lambda x, s=session: self.share_session(s))

            actions_layout.add_widget(edit_btn)
            actions_layout.add_widget(space_middle)
            actions_layout.add_widget(delete_btn)
            actions_layout.add_widget(space_between)
            actions_layout.add_widget(share_btn)
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

    def share_session(self, session):
        self.selected_session = session
        self.show_contact_selection_popup()

    def show_contact_selection_popup(self):
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

        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_layout.add_widget(scroll_view)

        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        confirm_btn = Button(text="Confirmer", on_press=self.show_confirmation_popup)
        cancel_btn = Button(text="Annuler", on_press=lambda x: self.dismiss_popup())

        buttons_layout.add_widget(confirm_btn)
        buttons_layout.add_widget(cancel_btn)

        popup_layout.add_widget(buttons_layout)

        self.popup = Popup(
            title="Sélectionnez les contacts pour partager",
            content=popup_layout,
            size_hint=(0.8, 0.8),
        )
        self.popup.open()

    def toggle_contact_selection(self, contact, active):
        if active:
            self.selected_contacts.append(contact)
        else:
            self.selected_contacts.remove(contact)

    def show_confirmation_popup(self, instance):
        if not self.selected_contacts:
            return

        contact_names = "\n".join(
            [
                f"{c['name']} {c['surname']} ({c['email']})"
                for c in self.selected_contacts
            ]
        )

        confirmation_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        message = Label(
            text=f"Vous allez partager cette session avec :\n{contact_names}",
            text_size=(250, None),
            halign="center",
            valign="middle",
        )
        confirmation_layout.add_widget(message)

        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        send_btn = Button(text="Envoyer", on_press=self.send_emails)
        cancel_btn = Button(text="Annuler", on_press=lambda x: self.dismiss_popup())

        buttons_layout.add_widget(send_btn)
        buttons_layout.add_widget(cancel_btn)

        confirmation_layout.add_widget(buttons_layout)

        self.popup.content = confirmation_layout

    def send_emails(self, instance):
        errors = []
        for contact in self.selected_contacts:
            success = self.send_email(contact["email"], self.selected_session)
            if not success:
                errors.append(contact["email"])

        if errors:
            self.show_error_popup(
                f"Les emails suivants n'ont pas pu être envoyés : {', '.join(errors)}"
            )
        else:
            self.show_success_popup("Tous les emails ont été envoyés avec succès.")

    def send_email(self, email, session):
        if platform == "android":
            try:
                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")

                intent = Intent(Intent.ACTION_SEND)
                intent.setType("message/rfc822")

                intent.putExtra(Intent.EXTRA_EMAIL, [email])

                intent.putExtra(Intent.EXTRA_SUBJECT, f"Session '{session['title']}'")

                body = f"Voici les détails de ma session :\n\n{session['title']}\n{session['date']}\n\n"
                for entry in session["entries"]:
                    body += f"Question: {entry['question']}\nRéponse: {entry['response']}\n\n"

                intent.putExtra(Intent.EXTRA_TEXT, body)

                chooser = Intent.createChooser(intent, "Envoyer l'email avec :")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                currentActivity = cast("android.app.Activity", PythonActivity.mActivity)
                currentActivity.startActivity(chooser)

                return True
            except Exception as e:
                print(f"Error sending email: {e}")
                return False
        else:
            return False

    def show_error_popup(self, error_message):
        self.dismiss_popup()
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        message = Label(
            text=error_message,
            text_size=(250, None),
            halign="center",
            valign="middle",
        )
        popup_layout.add_widget(message)

        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        ok_btn = Button(text="OK", on_press=lambda x: self.dismiss_error_popup())

        buttons_layout.add_widget(ok_btn)
        popup_layout.add_widget(buttons_layout)

        self.popup = Popup(title="Erreur", content=popup_layout, size_hint=(0.8, 0.4))
        self.popup.open()

    def show_success_popup(self):
        self.dismiss_popup()
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        message = Label(
            text="L'email a été envoyé avec succès !",
            text_size=(250, None),
            halign="center",
            valign="middle",
        )
        popup_layout.add_widget(message)

        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        ok_btn = Button(text="OK", on_press=lambda x: self.dismiss_success_popup())

        buttons_layout.add_widget(ok_btn)
        popup_layout.add_widget(buttons_layout)

        self.popup = Popup(title="Succès", content=popup_layout, size_hint=(0.8, 0.4))
        self.popup.open()

    def dismiss_success_popup(self):
        if self.popup:
            self.popup.dismiss()
        self.manager.current = "session_list"

    def dismiss_error_popup(self):
        if self.popup:
            self.popup.dismiss()
        self.manager.current = "session_list"
