from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from backend.tag import Tag
import ctypes
from backend.tagcollection import TagCollection
from frontend.tagbutton import TagButton

class View5(BoxLayout):
    """Class which represents the apperance and behaviour of adding new tag the collection
    """
    def __init__(self, main_panel, **kwargs):
        super(View5, self).__init__(**kwargs)
        self.main_panel = main_panel
        self.orientation = 'vertical'
        self.valign = 'center'
        
        self.label1 = Label(text='New tag:', font_size=50, size_hint_y=None, height=60)
        self.t = TextInput(font_size=21,
                           size_hint_y=None,
                           height=40,
                           hint_text='If you wish to add few tags, separate them with comma without tabulation')
        
        self.add_widget(self.label1)
        self.add_widget(self.t)

    def goback(self, b):
        self.manage_view_and_buttons()

    def save(self, b):
        if self.t.text.find(' ') != -1:
            ctypes.windll.user32.MessageBoxW(0, "You inserted tabulation, add tags only with comma spearator", "Warning", 16)
        else:
            tags_to_add = set(Tag(x) for x in self.t.text.split(','))
            if self.main_panel.tag_collection:
                self.main_panel.tag_collection.items.update(tags_to_add)
            else:
                self.main_panel.tag_collection = TagCollection('new_collection')
                for tag in tags_to_add:
                    self.main_panel.tag_collection.registerItem(tag)

            for tag in tags_to_add:
                self.main_panel.central_panel.view_4.stack.add_widget(TagButton(text=tag.name))
        self.main_panel.central_panel.view_4.any_tag_added = True
        self.manage_view_and_buttons()

    def manage_view_and_buttons(self):
        self.main_panel.central_panel.clear_widgets()
        self.main_panel.central_panel.add_widget(self.main_panel.central_panel.view_4)
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.save)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.main_panel.central_panel.view_4.save)
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.goback)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.main_panel.central_panel.view_4.goback)
        self.main_panel.get_Button_Bar().hidden_button.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button.enable()
        self.main_panel.get_Button_Bar().hidden_button_2.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_2.enable()
        self.main_panel.get_Button_Bar().hidden_button_3.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_3.enable()
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_tag.enable()
        self.main_panel.central_panel.view_4.start_infinite_loop()