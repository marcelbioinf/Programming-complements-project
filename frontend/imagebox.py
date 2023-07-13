import kivy
import math

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle# , RoundedRectangle

class ImageBox(RelativeLayout):
    """
    ImageBox is a classe that implements a selectable image. The image 
    is drawn in a white frame. When the image is selected, the frame becomes red. 
    An ImageBox instance contain an instance of CPImage. 
    """

    # a class attribute that contain a dictionary of ImageBoxes created. The 
    # objective is to speed up the application by avoiding the creation of 
    # new objects each time a image is shown in the UI.
    imb_dict = dict()

    def __init__(self, cpimage, **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        self.size_hint = (None, None)
        self.height = 300
        self.image = Image(source=cpimage.getImageFile())
        self.cpImage = cpimage
        self.add_widget(self.image)
        self.image.allow_stretch = True
        self.image.keep_ratio = False
        self.image.size_hint_x = None
        self.image.size_hint_y = None
        imageratio = self.image.get_image_ratio()
        self.width = 290 * imageratio + 10
        self.image.size = (290 * imageratio,290)
        self.image.pos = (5, 5)
        with self.canvas.before:
            Color(1,1,1,1)
            self.rect = Rectangle(size=self.size, pos=(0,0))
        self.bind(pos=ImageBox.__update_rect, size=ImageBox.__update_rect)
        self.angle = 0
        self.__update_image_rotation()

    def __update_image_rotation(self):
        # Calculate the rotation in radians based on the angle attribute
        rotation = math.radians(self.angle)
        self.image.rotation = rotation

    # Rest of the class code...

    def on_angle(self, instance, value):
        # Called when the angle attribute changes
        self.__update_image_rotation()

    @staticmethod    
    def __update_rect(instance, value):
        instance.rect.pos = (0,0)
        instance.rect.size = instance.size

    @classmethod
    def makeImageBox(cls, cpimage):
        imfile = cpimage.getImageFile()
        if imfile in ImageBox.imb_dict:
            return ImageBox.imb_dict[imfile]
        imb = ImageBox(cpimage)
        ImageBox.imb_dict[imfile] = imb
        return imb

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(self.image.source + ' pressed')
            #*******************
            # add code below to do something
            self.select()
            
    def select(self):
        if self.selected:
            with self.canvas.before:
                Color(1,1,1,1)
                self.rect = Rectangle(size=self.size, pos=(0,0))
            self.selected = False
        else:
            with self.canvas.before:
                Color(1,0,0,1)
                self.rect = Rectangle(size=self.size, pos=(0,0))
            self.selected = True

    def isSelected(self):
        return self.selected

