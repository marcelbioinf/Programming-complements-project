from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from frontend.tagbutton import TagButton
from kivy.clock import Clock
from kivy.clock import Clock
from backend.tag import Tag
from frontend import view2
from backend.tagcollection import TagCollection

class View6(BoxLayout):
    """Class resposible for displaying and selecting tags, and filtering the pictures from basic view to only those containing at least one of selected tags.
    """
    def __init__(self, mainpanel, **kwargs):
        super(View6, self).__init__(**kwargs)
        self.padding = [25, 25, 25, 25]
        self.main_panel = mainpanel
        self.tags = []

        self.stack = StackLayout()
        self.add_widget(self.stack)

    def add_tags(self):
        """Adds all the tags from the collection, if not present - uses default tags collection
        """        
        self.main_panel.app_layout.getBottomRow().edit_label('')
        if self.main_panel.central_panel.collection_created:
            if not self.main_panel.tag_collection:
                self.main_panel.tag_collection = TagCollection('default-tags')
                try:
                    self.main_panel.tag_collection.loadCollection('Projeto/Collections/tagCollecctions/default-tags.json', '')
                except:
                    return 0
                self.main_panel.app_layout.getBottomRow().edit_label('No tag collection has been loaded, default collection is shown')

        if self.main_panel.central_panel.collection_red:
            tags_set =  set([Tag(x) for y in self.main_panel.pic_collection.items for x in y.getTags()])
            if not self.main_panel.tag_collection:
                if len(tags_set) != 0:
                    self.main_panel.tag_collection = TagCollection(self.main_panel.pic_collection.filename)
                    self.main_panel.tag_collection.items = tags_set
                else:
                    self.main_panel.tag_collection = TagCollection('default-tags')
                    try:
                        self.main_panel.tag_collection.loadCollection('Projeto/Collections/tagCollecctions/default-tags.json', '')
                    except:
                        return 0
            elif self.main_panel.tag_collection and self.main_panel.tag_collection.filename == 'default-tags' and len(tags_set) != 0:
                self.main_panel.tag_collection.items = tags_set

        if self.main_panel.tag_collection:
            for tag in self.main_panel.tag_collection.items:
                self.tags.append(TagButton(text=tag.name))
                self.stack.add_widget(self.tags[-1])
                self.main_panel.get_Button_Bar().hidden_button_2.enable()
                self.main_panel.get_Button_Bar().hidden_button_3.enable()
        else:
            self.main_panel.get_Button_Bar().hidden_button_2.disable()
            self.main_panel.get_Button_Bar().hidden_button_3.disable()
            self.main_panel.app_layout.getBottomRow().edit_label('No tag collection has been loaded yet')

        for tag in self.tags:
            if tag.getText().strip() in self.main_panel.central_panel.selected_tags:
                tag.Select()

    def start_infinite_loop(self):
        Clock.schedule_interval(self.infinite_loop, 0.3)

    def infinite_loop(self, dt):
        selected_tags = set()
        any_tag = False
        for tag in self.tags:
            if tag.isSelected(): 
                any_tag = True
                selected_tags.add(tag.getText())
        if any_tag:
            self.main_panel.app_layout.getBottomRow().edit_label(f'Selected tags: {str(selected_tags).lstrip("{").rstrip("}")}')
        if not selected_tags:
            self.main_panel.app_layout.getBottomRow().edit_label(f'Selected tags: ')

    def exit_loop(self, *args):
        Clock.unschedule(self.infinite_loop)

    def goback(self, b):
        """Discards the filtering process and goes back to basic view
        """        
        self.exit_loop()
        for child in self.stack.children[:]:
            self.stack.remove_widget(child)
        self.tags.clear()
        self.main_panel.central_panel.clear_widgets()
        self.main_panel.central_panel.add_widget(self.main_panel.central_panel.view_2)
        self.main_panel.central_panel.start_infinite_loop()
        self.manage_buttons()

    def save(self, b):
        """Saves the progress by filtering only the pictures containing selected tags
        """        
        self.exit_loop()
        self.main_panel.central_panel.view_2 = view2.View2(self.main_panel)
        self.main_panel.central_panel.selected_tags = [tag.getText().strip() for tag in self.tags if tag.isSelected()]
        self.main_panel.central_panel.clear_widgets()
        self.main_panel.central_panel.add_widget(self.main_panel.central_panel.view_2)
        print(self.main_panel.central_panel.selected_tags)
        if self.main_panel.central_panel.selected_tags:
            self.main_panel.central_panel.view_2.add_pictures(self.main_panel.central_panel.selected_tags, True)
        else:
             self.main_panel.central_panel.view_2.add_pictures()
        for child in self.stack.children[:]:
             self.stack.remove_widget(child)
        self.tags.clear()
        self.manage_buttons()
        self.main_panel.central_panel.start_infinite_loop()

    def manage_buttons(self):
        self.main_panel.get_Button_Bar().button_B3.enable()
        self.main_panel.get_Button_Bar().button_T.enable()
        self.main_panel.get_Button_Bar().hidden_button_tag.enable()
        self.main_panel.get_Button_Bar().hidden_button_2.enable()

        self.main_panel.get_Button_Bar().hidden_button_3.text='-T'
        self.main_panel.get_Button_Bar().hidden_button_3.unbind(on_press=self.reset)
        self.main_panel.get_Button_Bar().hidden_button_3.bind(on_oress=self.main_panel.central_panel.remove_tags)
        self.main_panel.get_Button_Bar().hidden_button_3.disable()

        self.main_panel.get_Button_Bar().button_B1.text='   Create\ncollection'
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.save)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.main_panel.central_panel.create_collection)
        self.main_panel.get_Button_Bar().button_B1.disable()
        self.main_panel.get_Button_Bar().button_B2.text='   Open\ncollection'
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.goback)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.main_panel.central_panel.open_collection)
        self.main_panel.get_Button_Bar().button_B2.disable()
        self.main_panel.get_Button_Bar().tag_button.enable()

