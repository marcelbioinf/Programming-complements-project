from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from frontend.tagbutton import TagButton
from kivy.clock import Clock
from backend.tag import Tag
from backend.tagcollection import TagCollection

class View3(BoxLayout):
    """Class resposible for displaying and adding tags to selected pictures
    """
    def __init__(self, mainpanel, **kwargs):
        super(View3, self).__init__(**kwargs)
        self.padding = [25, 25, 25, 25]
        self.main_panel = mainpanel
        self.tags = []

        self.stack = StackLayout()
        self.add_widget(self.stack)

    def add_tags(self):
        """Adds tags to the layout - if no tag collection has been loaded, the default tag collection is shown and used
        """
        if not self.main_panel.tag_collection:
            self.main_panel.tag_collection = TagCollection('default-tags')
            try:
                self.main_panel.tag_collection.loadCollection('Projeto/Collections/tagCollecctions/default-tags.json', '')
            except:
                return 0
        for tag in self.main_panel.tag_collection.items:
            self.tags.append(TagButton(text=tag.name))
            self.stack.add_widget(self.tags[-1])
        self.main_panel.app_layout.getBottomRow().edit_label('')
     
    def add_specific_tags(self):
        """Adds chosen tags to chosen pictures
        """
        temporary_tag_collection = set()
        for pic in self.main_panel.central_panel.view_2.pics:
            if pic.isSelected():
                for tag in pic.cpImage.metadata['tags']:
                    temporary_tag_collection.add(Tag(tag))
        for tag in temporary_tag_collection:
                self.tags.append(TagButton(text=tag.name))
                self.stack.add_widget(self.tags[-1])
        self.main_panel.app_layout.getBottomRow().edit_label('')
        
    def start_infinite_loop(self):
        Clock.schedule_interval(self.infinite_loop, 0.3)

    def infinite_loop(self, dt):
        """Handels dynamic aspect of selecting tags
        """
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
        """Returns to basic view of application without saving any changes
        """
        self.exit_loop()
        for child in self.stack.children[:]:
            self.stack.remove_widget(child)
        self.tags.clear()
        self.main_panel.get_Button_Bar().button_B3.enable()
        self.main_panel.get_Button_Bar().button_T.enable()
        self.main_panel.get_Button_Bar().button_B1.text='   Create\ncollection'
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.save)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.main_panel.central_panel.create_collection)
        self.main_panel.get_Button_Bar().button_B1.disable()
        self.main_panel.get_Button_Bar().button_B2.text='   Open\ncollection'
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.goback)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.main_panel.central_panel.open_collection)
        self.main_panel.get_Button_Bar().button_B2.disable()
        self.main_panel.get_Button_Bar().hidden_button_2.enable()
        self.main_panel.get_Button_Bar().hidden_button_2.opacity = 1
        self.main_panel.get_Button_Bar().tag_button.enable()
        self.main_panel.central_panel.clear_widgets()
        self.main_panel.central_panel.add_widget(self.main_panel.central_panel.view_2)
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_tag.enable()
        self.main_panel.central_panel.start_infinite_loop()

    def save(self, b):
        """Saves the changes and return to the basic view of application
        """        
        self.exit_loop()
        selected_tags = [tag.getText() for tag in self.tags if tag.isSelected()]
        for pic in self.main_panel.central_panel.view_2.pics:
            if pic.isSelected():
                for tag in pic.cpImage.metadata['tags']:
                    selected_tags.append(tag)
                pic.cpImage.metadata={'tags':  set(selected_tags)}
        for child in self.stack.children[:]:
             self.stack.remove_widget(child)
        self.tags.clear()
        self.main_panel.get_Button_Bar().button_B3.enable()
        self.main_panel.get_Button_Bar().button_T.enable()
        self.main_panel.get_Button_Bar().button_B1.text='   Create\ncollection'
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.save)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.main_panel.central_panel.create_collection)
        self.main_panel.get_Button_Bar().button_B1.disable()
        self.main_panel.get_Button_Bar().button_B2.text='   Open\ncollection'
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.goback)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.main_panel.central_panel.open_collection)
        self.main_panel.get_Button_Bar().button_B2.disable()
        self.main_panel.get_Button_Bar().hidden_button_2.enable()
        self.main_panel.get_Button_Bar().hidden_button_2.opacity = 1
        self.main_panel.get_Button_Bar().tag_button.enable()
        self.main_panel.central_panel.clear_widgets()
        self.main_panel.central_panel.add_widget(self.main_panel.central_panel.view_2)
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_tag.enable()
        self.main_panel.central_panel.start_infinite_loop()

    def delete(self,b):
        """Deletes chosen tags from chosen pictures
        """        
        self.exit_loop()
        selected_tags = set(tag.getText().strip() for tag in self.tags if tag.isSelected())
        for pic in self.main_panel.central_panel.view_2.pics:
            if pic.isSelected():
                already_assigned_tags = set()
                for tag in pic.cpImage.metadata['tags']:
                    already_assigned_tags.add(tag.strip())
                pic.cpImage.metadata={'tags':  already_assigned_tags.difference(selected_tags)}
        for child in self.stack.children[:]:
             self.stack.remove_widget(child)
        self.tags.clear()
        self.main_panel.get_Button_Bar().button_B3.enable()
        self.main_panel.get_Button_Bar().button_T.enable()
        self.main_panel.get_Button_Bar().button_B1.text='   Create\ncollection'
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.delete)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.main_panel.central_panel.create_collection)
        self.main_panel.get_Button_Bar().button_B1.disable()
        self.main_panel.get_Button_Bar().button_B2.text='   Open\ncollection'
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.goback)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.main_panel.central_panel.open_collection)
        self.main_panel.get_Button_Bar().button_B2.disable()
        self.main_panel.get_Button_Bar().hidden_button_2.enable()
        self.main_panel.get_Button_Bar().hidden_button_2.opacity = 1
        self.main_panel.get_Button_Bar().tag_button.enable()
        self.main_panel.central_panel.clear_widgets()
        self.main_panel.central_panel.add_widget(self.main_panel.central_panel.view_2)
        self.main_panel.central_panel.start_infinite_loop()
               
        
