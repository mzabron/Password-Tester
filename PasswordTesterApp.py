from kivy.app import App
from PasswordTesterLayout import PasswordTesterLayout


class PasswordTesterApp(App):
    def build(self):

        self.title = "Password Tester"

        return PasswordTesterLayout()