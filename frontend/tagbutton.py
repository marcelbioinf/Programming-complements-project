import kivy
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

from frontend.coloredlabel import ColoredLabel

class TagButton(Button):
    """
    TagButton class represent a button for tags. It has square corners and two 
    states: selected and unselected. The size (width) of the button is adjusted 
    according to the text of the button.  
    """
    def __init__(self, background_color=(0,0,0,1), color=(1,1,1,1), **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        # the dot symbolize the hole in a label.
        self.text = '• ' + self.text 
        # ' ◎' 
        # ' \u25C9'
        # ' •'
        self.button_color = background_color # used when button is pressed
        self.text_color = color
        self.background_color = background_color
        self.background_normal = ''
        self.padding_x = 10
        self.size_hint = (None, None)
        self.height = self.font_size * 1.7
        with self.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.__update_rect, size=self.__update_rect)
        self.texture_update()

    def __setText(self, text):
        self.text = text
        self.texture_update()
        TagButton.__update_rect(self,None)

    def getText(self):
        return self.text[1:]

    def on_press(self):
        if self.selected:
            color = self.text_color
            bcolor = self.button_color
        else:
            color = self.button_color
            bcolor = self.text_color 
        print('select: ' + str(self.selected) + ' t ' +
            str(color) + ' b ' + str(bcolor))
        self.background_color = bcolor
        self.color = color            
        self.texture_update()


    def on_release(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True
        #*********************
        # add code to do something

    def isSelected(self):
        return self.selected

    def unSelect(self):
        self.selected = False

    def Select(self):
        self.on_press()
        self.selected = True

    def getLabel(self):
        """
        getLabel May be used to obtain a Label that corresponds to the tag, to 
        be used elsewhere in the UI

        Returns:
            ColoredLabel: an instance of ColoredLabel with same text as 
            the button instance
        """
        label = ColoredLabel(text=self.text[0:-2], background_color=self.button_color, color=self.text_color)
        label.size_hint_y = None
        label.height = 35
        label.font_size = 20
        return label

    @staticmethod
    def __update_rect(instance, value):
        instance.background_rect.pos = instance.pos
        instance.background_rect.size = instance.size
        instance.width = instance.texture_size[0]
