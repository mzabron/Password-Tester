from kivy.app import App
from PasswordTesterController import PasswordTesterController


class PasswordTesterApp(App):
    def build(self):

        self.title = "Password Tester"

        return PasswordTesterController()