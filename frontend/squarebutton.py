import kivy
from kivy.uix.button import Button

class SquareButton(Button):
    """
    SquareButton is a subclass of class Button that implements a square button 
    to be used in a CommandBar widget.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = self.text
        self.color = (1,1,1,1)
        self.bold = True
        self.height = 70
        self.size_hint_y = None
        self.bind(size=self.update_button_size)
        self.width = 70
        #self.size_hint_x = None
        self.disabled = False

    def disable(self):
        """
        disable changes the state of the button to «disabled»
        """
        self.disabled = True

    def enable(self):
        """
        disable changes the state of the button to «enabled» 
        (not disabled)
        """
        self.disabled = False

    def __str__(self):
        return 'SquareButton-' + self.text
    
    def update_button_size(self, instance, value):
        self.height = self.texture_size[1] + 20
