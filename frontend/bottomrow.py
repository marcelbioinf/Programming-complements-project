from kivy.uix.label import Label
from frontend.coloredboxlayout import ColoredBoxLayout

class BottomRow(ColoredBoxLayout):
    def __init__(self, **kwargs):
        super(BottomRow, self).__init__(background_color=(160/256,82/256,45/256,0.55), **kwargs)

        self.orientation = 'horizontal'
        self.padding = [10, 10, 10, 10]  
        self.size_hint=(1, 0.06)

        self.label = Label(text='Create new collection or open exisiting one', color=(1,1,1,1), font_size=18, halign='center', valign='middle')
        self.label.bind(size=self.label.setter('text_size'))    
        self.add_widget(self.label)

    def edit_label(self, n):
        self.label.text = str(n)




