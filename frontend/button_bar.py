from kivy.uix.boxlayout import BoxLayout
from frontend.squarebutton import SquareButton

class ButtonBar(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonBar, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint=(0.1, 0.55)

        self.hidden_button_tag = SquareButton(text=' Open tag\ncollection')
        self.add_widget(self.hidden_button_tag)
        self.hidden_button_tag.opacity = 0
        self.hidden_button_tag.disable()
        self.hidden_button_3 = SquareButton(text='-T')
        self.add_widget(self.hidden_button_3)
        self.hidden_button_3.opacity = 0
        self.hidden_button_3.disable()
        self.hidden_button = SquareButton(text='+T')
        self.add_widget(self.hidden_button)
        self.hidden_button.opacity = 0
        self.hidden_button.disable()
        self.hidden_button_2 = SquareButton(text='   Save\ncollection')
        self.add_widget(self.hidden_button_2)
        self.hidden_button_2.opacity = 0
        self.hidden_button_2.disable()
        self.tag_button = SquareButton(text='T')
        self.add_widget(self.tag_button)
        self.tag_button.disable()
        self.button_B1 = SquareButton(text='   Create\ncollection')
        self.add_widget(self.button_B1)
        self.button_B2 = SquareButton(text='   Open\ncollection')
        self.add_widget(self.button_B2)
        self.button_B3 = SquareButton(text='Next\npage')
        self.add_widget(self.button_B3)
        self.button_T = SquareButton(text='Previous\n   page')
        self.add_widget(self.button_T)
        self.button_X = SquareButton(text='    Exit\ncollection')
        self.add_widget(self.button_X)
