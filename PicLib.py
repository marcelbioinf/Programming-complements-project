from kivy.app import App
from frontend.myAppLayout import MyAppLayout

class PicLib(App):
    """
    Class used to run application
    """
    def build(self):
        return MyAppLayout()

if __name__ == '__main__':
    PicLib().run()