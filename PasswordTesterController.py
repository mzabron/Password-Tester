from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

from LogicManager import LogicManager
from threading import Thread
import re


class PasswordTesterController(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.logic_manager = None
        self.attack_method = None
        self.target_password = None
        self.has_numbers = False
        self.has_uppercase = False
        self.has_lowercase = False
        self.has_special_chars = False
        self.hash_password = False

    def update_criteria(self):
        self.has_numbers = self.ids.has_numbers.active
        self.has_uppercase = self.ids.has_uppercase.active
        self.has_lowercase = self.ids.has_lowercase.active
        self.has_special_chars = self.ids.has_special_chars.active

        print(f"criteria: {self.has_numbers, self.has_uppercase, self.has_lowercase, self.has_special_chars, self.hash_password}")

    def show_error_popup(self, message):
        popup_layout = GridLayout(cols=1, padding=10)
        popup_layout.add_widget(Label(
            text=message,
            font_size="18sp",
            text_size=(self.width * 0.5, None),
            halign="center"
        ))
        close_button = Button(text="Close", size_hint_y=0.3)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Invalid Password",
            content=popup_layout,
            size_hint=(0.6, 0.4)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def validate_password(self, password):
        if self.has_numbers is False and re.search(r'\d', password):
            self.show_error_popup("Password contains numbers, but 'Has numbers' is not selected.")
            return False
        if self.has_uppercase is False and re.search(r'[A-Z]', password):
            self.show_error_popup("Password contains uppercase letters, but 'Has uppercase' is not selected.")
            return False
        if self.has_lowercase is False and re.search(r'[a-z]', password):
            self.show_error_popup("Password contains lowercase letters, but 'Has lowercase' is not selected.")
            return False
        if self.has_special_chars is False and re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            self.show_error_popup("Password contains special characters, but 'Has special chars' is not selected.")
            return False
        return True

    def update_ui(self, tested_count, elapsed_time, last_password):
        self.ids.tested_count.text = str(tested_count)
        self.ids.elapsed_time.text = f"{elapsed_time:.2f} s"
        self.ids.tested_password.text = last_password

    def update_attack_method(self, method):
        self.attack_method = method
        print(f"Selected attack method: {self.attack_method}")

    def start_test(self):
        if self.logic_manager:
            self.show_error_popup("Test is already running.")
            return

        if not self.attack_method:
            self.show_error_popup("Please select an attack method before starting the test.")
            return

        self.target_password = self.ids.password_input.text
        if not self.validate_password(self.target_password):
            return

        self.logic_manager = LogicManager(
            has_numbers=self.has_numbers,
            has_uppercase=self.has_uppercase,
            has_lowercase=self.has_lowercase,
            has_special_chars=self.has_special_chars,
            attack_method=self.attack_method,
            target_password = self.target_password,
            update_ui = self.update_ui,
            update_test = self.end_test
        )
        test_thread = Thread(target=self.logic_manager.run_test)
        test_thread.start()
        self.ids.cancel_button.disabled = False

    def cancel_test(self):
        if self.logic_manager:
            self.logic_manager.cancel_test = True
            self.logic_manager = None
        self.ids.cancel_button.disabled = True

    def end_test(self):
        self.logic_manager = None
        self.ids.cancel_button.disabled = True
