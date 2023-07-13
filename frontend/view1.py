from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
  

class View1(BoxLayout):
    """Class resposible for basic, starting application's view
    """
    def __init__(self, **kwargs):
        super(View1, self).__init__(**kwargs)
        self.orientation='vertical'
        self.label2 = Label(text='PicLib is your\nnew picture library', font_size=50)
        self.t = TextInput(font_size = 21,
                      size_hint_y = None,
                      height = 40,
                      hint_text = 'Name your new collection here')
        self.add_widget(self.label2)
        self.add_widget(self.t)