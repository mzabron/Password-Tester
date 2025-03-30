from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.factory import Factory

class CustomSwitch(ButtonBehavior, Widget):

    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rect = None
        self.knob = None
        self.size_hint = (None, None)
        self.size = (40, 20)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.draw_switch()

    def draw_switch(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.7, 0.7, 0.7, 1) if not self.active else Color(0, 0.8, 0, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height / 2])

            Color(1, 1, 1, 1)
            knob_size = self.height * 0.7
            x_offset = self.pos[0] + (self.width - knob_size - 4 if self.active else 4)
            self.knob = Ellipse(pos=(x_offset, self.pos[1] + (self.height - knob_size) / 2), size=(knob_size, knob_size))

    def update_graphics(self, *args):
        self.draw_switch()

    def on_press(self):
        self.active = not self.active
        self.draw_switch()

Factory.register('CustomSwitch', cls=CustomSwitch)
