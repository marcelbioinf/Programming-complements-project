import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from frontend.coloredboxlayout import ColoredBoxLayout
from frontend.central_panel import CentralPanel
from frontend.button_bar import ButtonBar


class MainPanel(BoxLayout):
    """Class representing main panel of the application. Panel is composed of button bar on the side and central panel in the center of application's view

    Args:
        BoxLayout (class): layout superclass 
    """
    def __init__(self, app_layout, **kwargs):
        super(MainPanel, self).__init__(**kwargs)
        self.app_layout = app_layout
        self.button_bar = ButtonBar()
        self.central_panel = CentralPanel(self)

        self.pic_collection = None
        self.tag_collection = None

        self.orientation = 'horizontal'
        self.padding = [5, 5, 5, 5]  
        self.size_hint=(1, 0.87)

        self.add_widget(self.button_bar)
        self.add_widget(self.central_panel)

    def get_Button_Bar(self):
        """Function used to get the button bar in order to modify it

        Returns:
            button_bar (class): object contiaing all the buttons of application
        """
        return self.button_bar
