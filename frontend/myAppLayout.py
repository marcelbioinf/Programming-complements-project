import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from frontend.bottomrow import BottomRow
from frontend.mainpanel import MainPanel
from frontend.toprow import TopRow


class MyAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyAppLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'  

        self.topRow = TopRow()
        self.add_widget(self.topRow)

        self.mainPanel = MainPanel(self)
        self.add_widget(self.mainPanel)

        self.bottomRow = BottomRow()
        self.add_widget(self.bottomRow)

    def getBottomRow(self):
        return self.bottomRow