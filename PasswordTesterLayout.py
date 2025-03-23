from kivy.uix.boxlayout import BoxLayout
from LogicManager import LogicManager


class PasswordTesterLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.attack_method = None
        self.hash_method = None
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
        self.hash_password = self.ids.hash_password.active

        if not self.hash_password:
            self.ids.hash_method.text = "Select Hashing Method"
            self.hash_method = None

        print(f"criteria: {self.has_numbers, self.has_uppercase, self.has_lowercase, self.has_special_chars, self.hash_password}")

    def update_hash_method(self, method):
        if method == "Select Hashing Method":
            self.hash_method = None
        else:
            self.hash_method = method
        print(f"Selected hash method: {self.hash_method}")

    def update_attack_method(self, method):
        self.attack_method = method
        print(f"Selected attack method: {self.attack_method}")

    def start_test(self):
        self.target_password = self.ids.password_input.text
        logic_manager = LogicManager(
            has_numbers=self.has_numbers,
            has_uppercase=self.has_uppercase,
            has_lowercase=self.has_lowercase,
            has_special_chars=self.has_special_chars,
            hash_password=self.hash_password,
            hash_method=self.hash_method,
            attack_method=self.attack_method,
            target_password = self.target_password
        )
        logic_manager.run_test()