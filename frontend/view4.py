from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from frontend.tagbutton import TagButton
from kivy.clock import Clock
import ctypes
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import simpledialog
from frontend.view5 import View5
from backend.tagcollection import TagCollection
from backend.tag import Tag

class View4(BoxLayout):
    """Class resposible for the view and process of managing tag collection
    """
    def __init__(self, mainpanel, **kwargs):
        super(View4, self).__init__(**kwargs)
        self.padding = [25, 25, 25, 25]
        self.main_panel = mainpanel
        self.tags = []
        self.tags_changed = set()
        self.collection_loading_only = False
        self.any_tag_added = False

        self.stack = StackLayout()
        self.add_widget(self.stack)

        self.view_5 = View5(self.main_panel)

    def add_tags(self):
        """Adds tags to the view, if collection has been created and no tag collection has been created yet, default collection will be loaded. If collection was red 
        from a file and there were any tags assigned in that collection, these tags will create a tag collection by default. Tag collection can be changed any time by 
        choosing it from a file.
        """
        self.tags_changed.clear()
        self.collection_loading_only = False
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
    
    def start_infinite_loop(self):
        Clock.schedule_interval(self.infinite_loop, 0.3)

    def infinite_loop(self, dt):
        selected_tags = set()
        any_tag = False
        for tag in self.tags:
            if tag.isSelected():
                if self.tags_changed:
                    if tag.getText().strip() in self.tags_changed:
                        any_tag = True
                        selected_tags.add(tag.getText())
                else:
                    any_tag = True
                    selected_tags.add(tag.getText())
        if any_tag:
            self.main_panel.app_layout.getBottomRow().edit_label(f'Selected tags: {str(selected_tags).lstrip("{").rstrip("}")}')
            self.main_panel.get_Button_Bar().hidden_button_3.enable()
        else:
            self.main_panel.app_layout.getBottomRow().edit_label('')
            self.main_panel.get_Button_Bar().hidden_button_3.disable()

    def exit_loop(self, *args):
        Clock.unschedule(self.infinite_loop)

    def goback(self, b):
        """Return to the basic view without saving the changes
        """
        self.exit_loop()
        for child in self.stack.children[:]:
            self.stack.remove_widget(child)
        self.tags.clear()
        self.menage_buttons()

    def save(self, b):
        """Saves the changes and returns to the basic view
        """
        self.exit_loop()
        if self.main_panel.tag_collection:
            if len(self.tags_changed) == 0 and not self.collection_loading_only and not self.any_tag_added:
                ctypes.windll.user32.MessageBoxW(0, "No changes has been applied", "Cannot save", 16)
            else:
                if not self.collection_loading_only:
                    self.main_panel.tag_collection.items = set(Tag(x) for x in self.tags_changed)
                for child in self.stack.children[:]:
                    self.stack.remove_widget(child)
                self.tags.clear()
                self.menage_buttons()
        else:
            ctypes.windll.user32.MessageBoxW(0, "No collection has been loaded yet", "Warning!", 16)
            return

    def add_tag(self, b):
        """Method to add a tag to the collection
        """        
        self.any_tag_added = False
        self.exit_loop()
        self.main_panel.central_panel.clear_widgets()
        self.main_panel.central_panel.add_widget(self.view_5)
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.save)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.view_5.save)
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.goback)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.view_5.goback)
        self.main_panel.get_Button_Bar().hidden_button.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button.disable()
        self.main_panel.get_Button_Bar().hidden_button_2.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button_2.disable()
        self.main_panel.get_Button_Bar().hidden_button_3.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button_3.disable()
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button_tag.disable()

    def remove_tags(self, b):
        """Method to remove a tag from a collection
        """        
        selected_tags = set(tag.getText().strip() for tag in self.tags if tag.isSelected())
        for tag in self.tags:
                if tag.getText().strip() in selected_tags:
                    self.stack.remove_widget(tag)
                else:
                    self.tags_changed.add(tag.getText().strip())
        self.main_panel.app_layout.getBottomRow().edit_label(f'')
        self.collection_loading_only = False

    def save_collection(self, b):
        """Method to save tag collection as file
        """        
        if self.tags_changed:
            initial_tags = self.main_panel.tag_collection.items.copy()
            self.main_panel.tag_collection.items = set(Tag(x) for x in self.tags_changed)
        root = tk.Tk()
        root.withdraw()
        filename = simpledialog.askstring("To save", "Enter your collection's name:")
        path = f'{os.getcwd()}/Projeto/Collections/tagCollecctions'
        try:
            self.main_panel.tag_collection.saveCollection(path, filename)
            ctypes.windll.user32.MessageBoxW(0, "Your collection has been saved", "Success", 1)
        except:
            print('There was en error with saving the collection')
        if self.tags_changed:
            self.main_panel.tag_collection.items = initial_tags
        self.collection_loading_only = True

    def open_collection(self, b):
        """Method to load a tag collection from a file
        """
        root = tk.Tk()
        root.withdraw()
        default_dir = f'{os.getcwd()}/Projeto/Collections/tagCollecctions'
        file = filedialog.askopenfilename(initialdir=default_dir)
        if file  == '':
            print('You must choose a file')
            return
        self.main_panel.tag_collection = TagCollection(os.path.basename(file))
        self.main_panel.tag_collection.loadCollection(file, '')
        self.main_panel.app_layout.getBottomRow().edit_label('')
        for child in self.stack.children[:]:
            self.stack.remove_widget(child)
        self.tags.clear()
        self.add_tags()
        self.collection_loading_only = True

    def menage_buttons(self):
        """Method to manage buttons while saving or discarding progress and going back to the basic view of application
        """
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
        self.main_panel.get_Button_Bar().tag_button.enable()

        self.main_panel.get_Button_Bar().hidden_button.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button.unbind(on_press=self.add_tag)
        self.main_panel.get_Button_Bar().hidden_button.disable()
        self.main_panel.get_Button_Bar().hidden_button_3.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button_3.unbind(on_press=self.remove_tags)
        self.main_panel.get_Button_Bar().hidden_button_3.disable()
        self.main_panel.get_Button_Bar().hidden_button_2.text='    Save\ncollection'
        self.main_panel.get_Button_Bar().hidden_button_2.unbind(on_press=self.save_collection)
        self.main_panel.get_Button_Bar().hidden_button_2.bind(on_press=self.main_panel.central_panel.save_collection)
        self.main_panel.get_Button_Bar().hidden_button_tag.unbind(on_press=self.open_collection)
        self.main_panel.get_Button_Bar().hidden_button_tag.bind(on_press=self.main_panel.central_panel.search)
        self.main_panel.get_Button_Bar().hidden_button_tag.text='Search'

        self.main_panel.central_panel.clear_widgets()
        self.main_panel.central_panel.add_widget(self.main_panel.central_panel.view_2)
        self.main_panel.central_panel.start_infinite_loop()