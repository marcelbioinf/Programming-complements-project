from kivy.uix.label import Label
from frontend.coloredboxlayout import ColoredBoxLayout


class TopRow(ColoredBoxLayout):
    def __init__(self, **kwargs):
        super(TopRow, self).__init__(background_color=(149/255, 197/255, 246/255),**kwargs)
        
        self.orientation = 'horizontal'
        self.padding = 7 
        self.size_hint=(1.0, 0.07)
        
        # Create and add widgets to the layout
        self.label = Label(text='PicLib', color=(1,1,1,1), font_size=23, halign='left', valign='middle')
        self.label.bind(size=self.label.setter('text_size'))    
        self.add_widget(self.label)