from kivy.uix.boxlayout import BoxLayout
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import ctypes
import zipfile
import json
import os
from kivy.clock import Clock
from frontend.view1 import View1
from frontend.view2 import View2
from frontend.view3 import View3
from frontend.view4 import View4
from frontend.view6 import View6
from backend.imagecollection import ImageCollection


class CentralPanel(BoxLayout):
    """Class representing dynamic view of central panel - main component of application
    """
    def __init__(self, mainpanel, **kwargs):
        super(CentralPanel, self).__init__(**kwargs)
        self.main_panel= mainpanel  
        self.view_1 = View1()
        self.view_2 = View2(self.main_panel)
        self.view_3 = View3(self.main_panel)
        self.view_4 = View4(self.main_panel)
        self.view_6 = View6(self.main_panel)

        #default view:
        self.add_widget(self.view_1)
        self.main_panel.get_Button_Bar().button_B3.disable()
        self.main_panel.get_Button_Bar().button_T.disable()
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.create_collection)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.open_collection)
        self.main_panel.get_Button_Bar().button_X.bind(on_press=self.exit_collection)
        self.main_panel.get_Button_Bar().button_X.disable()

        self.collection_created = False
        self.collection_red = False
        self.selected_tags = []

    def create_collection(self, b):
        """Method to create a picture collection from a chosen directory
        """
        self.collection_red = False
        self.collection_created = True
        if self.view_1.t.text == '':
            ctypes.windll.user32.MessageBoxW(0, "You must insert name of your collection", "Warning!", 16)
            return
        self.main_panel.pic_collection = ImageCollection(self.view_1.t.text)
        root = tk.Tk()
        root.withdraw()
        default_dir = f'{os.getcwd()}/Project/fotos'
        directory = filedialog.askdirectory(initialdir=default_dir)
        if directory == '':
            print('You must choose a directory')
            return
        self.main_panel.pic_collection.ScanFolder(directory)
        self.main_panel.get_Button_Bar().button_B1.disable()
        self.main_panel.get_Button_Bar().button_B2.disable()
        self.main_panel.get_Button_Bar().button_X.enable()
        self.clear_widgets()
        self.add_widget(self.view_2)
        self.main_panel.app_layout.getBottomRow().edit_label('')
        self.view_2.add_pictures()
        self.main_panel.get_Button_Bar().hidden_button_2.enable()
        self.main_panel.get_Button_Bar().hidden_button_2.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_2.bind(on_press=self.save_collection)
        self.main_panel.get_Button_Bar().tag_button.enable()
        self.main_panel.get_Button_Bar().tag_button.bind(on_press=self.manage_tags)
        self.main_panel.get_Button_Bar().hidden_button_tag.text='Search'
        self.main_panel.get_Button_Bar().hidden_button_tag.bind(on_press=self.search)
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_tag.enable()
        self.start_infinite_loop()
    
    def open_collection(self, b):
        """Method to open a picture collection from a chosen directory
        """
        self.collection_red = True
        self.collection_created = False
        root = tk.Tk()
        root.withdraw()
        default_dir = f'{os.getcwd()}/Projeto/Collections/picCollections/collections'
        file = filedialog.askopenfilename(initialdir=default_dir)
        if file  == '':
            print('You must choose a file')
            return
        self.main_panel.pic_collection = ImageCollection(os.path.basename(file))
        self.main_panel.pic_collection.loadCollection(file, os.path.dirname(file))# os.path.dirname(file)
        self.main_panel.get_Button_Bar().button_B1.disable()
        self.main_panel.get_Button_Bar().button_B2.disable()
        self.main_panel.get_Button_Bar().button_X.enable()
        self.clear_widgets()
        self.add_widget(self.view_2)
        self.main_panel.app_layout.getBottomRow().edit_label('')
        self.view_2.add_pictures()
        self.main_panel.get_Button_Bar().hidden_button_2.enable()
        self.main_panel.get_Button_Bar().hidden_button_2.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_2.bind(on_press=self.save_collection)
        self.main_panel.get_Button_Bar().tag_button.enable()
        self.main_panel.get_Button_Bar().tag_button.bind(on_press=self.manage_tags)
        self.main_panel.get_Button_Bar().hidden_button_tag.text='Search'
        self.main_panel.get_Button_Bar().hidden_button_tag.bind(on_press=self.search)
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_tag.enable()
        self.start_infinite_loop()

    def exit_collection(self, b):
        """Method to exit collection and restart the application
        """
        self.exit_loop()
        self.collection_created = False
        self.collection_red = False
        self.clear_widgets()
        self.add_widget(self.view_1)
        self.main_panel.app_layout.getBottomRow().edit_label('Create new collection or open exisiting one')
        self.main_panel.get_Button_Bar().button_B1.text = '   Create\ncollection'
        self.main_panel.get_Button_Bar().button_B1.unbind()
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.create_collection)
        self.main_panel.get_Button_Bar().hidden_button.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button.disable()
        self.main_panel.get_Button_Bar().button_B1.enable()
        self.main_panel.get_Button_Bar().button_B2.enable()
        self.main_panel.get_Button_Bar().button_X.disable()
        self.main_panel.get_Button_Bar().button_B3.disable()
        self.main_panel.get_Button_Bar().button_T.disable()
        self.main_panel.get_Button_Bar().tag_button.disable()
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button_tag.disable()
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button_2.opacity=0
        self.main_panel.get_Button_Bar().hidden_button_2.disable()
        self.main_panel.pic_collection=None
        self.main_panel.tag_collection=None
        self.view_2.reset_layout()

    def start_infinite_loop(self):
        Clock.schedule_interval(self.infinite_loop, 0.3)

    def infinite_loop(self, dt):
        """Method to perform inifite loop which constatntly checks for selected items and guarantees application's dynamicity
        """
        counter = 0
        selected_pic=None
        for pic in self.view_2.pics:
            if pic.selected == True: 
                counter+=1
                selected_pic=pic
        if counter >= 1:
            self.main_panel.get_Button_Bar().hidden_button.opacity = 1
            self.main_panel.get_Button_Bar().hidden_button.bind(on_press=self.add_tags)
            self.main_panel.get_Button_Bar().hidden_button.enable()
            self.main_panel.get_Button_Bar().hidden_button_3.opacity = 1
            self.main_panel.get_Button_Bar().hidden_button_3.bind(on_press=self.remove_tags)
            self.main_panel.get_Button_Bar().hidden_button_3.enable()
            self.main_panel.get_Button_Bar().button_B1.text='ZIP'
            self.main_panel.get_Button_Bar().button_B1.enable()
            self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.create_collection)
            self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.zip)
            if counter == 1:
                date = selected_pic.cpImage.getDate()
                added_tags = selected_pic.cpImage.getTags()
                if added_tags:
                    self.main_panel.app_layout.getBottomRow().edit_label(f'Date: {date.rstrip("/")}, Tags: {", ".join(list(added_tags))}')
                else:
                    self.main_panel.app_layout.getBottomRow().edit_label(f'Date: {date.rstrip("/")}')
            else:
                self.main_panel.app_layout.getBottomRow().edit_label(f'Number of selected pictures: {counter}')
        else:
            self.main_panel.app_layout.getBottomRow().edit_label(f'Number of pictures on current page: {len(self.view_2.pages[self.view_2.actual_page].children)}')
            self.main_panel.get_Button_Bar().hidden_button.opacity = 0
            self.main_panel.get_Button_Bar().hidden_button.unbind(on_press=self.add_tags)
            self.main_panel.get_Button_Bar().hidden_button.disable()
            self.main_panel.get_Button_Bar().hidden_button_3.opacity = 0
            self.main_panel.get_Button_Bar().hidden_button_3.disable()
            self.main_panel.get_Button_Bar().button_B1.disable()

    def exit_loop(self, *args):
        Clock.unschedule(self.infinite_loop)

    def add_tags(self, b):
        """Method to add tags to one or few pictures
        """
        if self.view_3.add_tags() != 0:
            self.exit_loop()
            self.clear_widgets()
            self.main_panel.get_Button_Bar().button_B3.disable()
            self.main_panel.get_Button_Bar().button_T.disable()
            self.add_widget(self.view_3)
            self.main_panel.get_Button_Bar().hidden_button.disable()
            self.main_panel.get_Button_Bar().hidden_button.opacity = 0
            self.main_panel.get_Button_Bar().hidden_button_3.disable()
            self.main_panel.get_Button_Bar().hidden_button_3.opacity = 0
            self.main_panel.get_Button_Bar().hidden_button_2.disable()
            self.main_panel.get_Button_Bar().hidden_button_2.opacity = 0
            self.main_panel.get_Button_Bar().button_B1.text='OK'
            self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.create_collection)
            self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.view_3.save)
            self.main_panel.get_Button_Bar().button_B1.enable()
            self.main_panel.get_Button_Bar().button_B2.text='<<<'
            self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.open_collection)
            self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.view_3.goback)
            self.main_panel.get_Button_Bar().button_B2.enable()
            self.main_panel.get_Button_Bar().tag_button.disable()
            self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 0
            self.main_panel.get_Button_Bar().hidden_button_tag.disable()
            self.view_3.start_infinite_loop()

    def remove_tags(self,b):
        """Method to remove selected tags from one or few pictures
        """
        selected_pics = [pic for pic in self.view_2.pics if pic.isSelected()]
        if not any([t.cpImage.getTags() for t in selected_pics]):
            ctypes.windll.user32.MessageBoxW(0, "None of selected pictures has tags assigned", "Warning", 16)
            return
        self.main_panel.get_Button_Bar().hidden_button_3.disable()
        self.main_panel.get_Button_Bar().hidden_button_3.opacity = 0
        self.main_panel.get_Button_Bar().hidden_button.disable()
        self.main_panel.get_Button_Bar().hidden_button.opacity = 0
        self.view_3.add_specific_tags()
        self.exit_loop()
        self.clear_widgets()
        self.main_panel.get_Button_Bar().button_B3.disable()
        self.main_panel.get_Button_Bar().button_T.disable()
        self.add_widget(self.view_3)
        self.main_panel.get_Button_Bar().button_B1.text='OK'
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.create_collection)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.view_3.delete)
        self.main_panel.get_Button_Bar().button_B1.enable()
        self.main_panel.get_Button_Bar().button_B2.text='<<<'
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.open_collection)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.view_3.goback)
        self.main_panel.get_Button_Bar().button_B2.enable()
        self.main_panel.get_Button_Bar().tag_button.disable()
        self.view_3.start_infinite_loop()

    def save_collection(self,b):
        """Method to save a picture collection
        """
        directory = self.main_panel.pic_collection.filename
        parent_dir = f'{os.getcwd()}/Projeto/Collections/picCollections/collections'
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        try:
            self.main_panel.pic_collection.saveCollection(path)
            self.main_panel.pic_collection.save_each_image(path)
            ctypes.windll.user32.MessageBoxW(0, "Your collection has been saved", "Success", 1)
        except:
            print('There was en error with saving the collection')

    def manage_tags(self, b):
        """Method which opens a window to manage the tag collection - reading, saving, modifying etc.
        """
        self.view_4.add_tags()
        self.exit_loop()
        self.clear_widgets()
        self.main_panel.get_Button_Bar().button_B3.disable()
        self.main_panel.get_Button_Bar().button_T.disable()
        self.add_widget(self.view_4)
        self.main_panel.get_Button_Bar().button_B1.text='OK'
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.create_collection)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.view_4.save)
        self.main_panel.get_Button_Bar().button_B1.enable()
        self.main_panel.get_Button_Bar().button_B2.text='<<<'
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.open_collection)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.view_4.goback)
        self.main_panel.get_Button_Bar().button_B2.enable()
        self.main_panel.get_Button_Bar().tag_button.disable()

        self.main_panel.get_Button_Bar().hidden_button.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button.unbind(on_press=self.add_tags)
        self.main_panel.get_Button_Bar().hidden_button.bind(on_press=self.view_4.add_tag)
        self.main_panel.get_Button_Bar().hidden_button.enable()
        self.main_panel.get_Button_Bar().hidden_button_3.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_3.unbind(on_press=self.remove_tags)
        self.main_panel.get_Button_Bar().hidden_button_3.bind(on_press=self.view_4.remove_tags)
        self.main_panel.get_Button_Bar().hidden_button_2.unbind(on_press=self.save_collection)
        self.main_panel.get_Button_Bar().hidden_button_2.bind(on_press=self.view_4.save_collection)
        self.main_panel.get_Button_Bar().hidden_button_2.text='  Save tag\ncollection'
        self.main_panel.get_Button_Bar().hidden_button_tag.opacity = 1
        self.main_panel.get_Button_Bar().hidden_button_tag.unbind(on_press=self.search)
        self.main_panel.get_Button_Bar().hidden_button_tag.bind(on_press=self.view_4.open_collection)
        self.main_panel.get_Button_Bar().hidden_button_tag.text=' Open tag\ncollection'
        self.main_panel.get_Button_Bar().hidden_button_tag.enable()
        self.view_4.start_infinite_loop()    

    def search(self, b):
        """Method to filter actual collection based on selected tags
        """        
        self.exit_loop()
        self.clear_widgets()
        self.add_widget(self.view_6)
        self.view_6.add_tags()
        self.main_panel.get_Button_Bar().button_B3.disable()
        self.main_panel.get_Button_Bar().button_T.disable()
        self.main_panel.get_Button_Bar().hidden_button_tag.disable()
        self.main_panel.get_Button_Bar().hidden_button_2.disable()

        self.main_panel.get_Button_Bar().button_B1.text='OK'
        self.main_panel.get_Button_Bar().button_B1.unbind(on_press=self.create_collection)
        self.main_panel.get_Button_Bar().button_B1.bind(on_press=self.view_6.save)
        self.main_panel.get_Button_Bar().button_B1.enable()
        self.main_panel.get_Button_Bar().button_B2.text='<<<'
        self.main_panel.get_Button_Bar().button_B2.unbind(on_press=self.open_collection)
        self.main_panel.get_Button_Bar().button_B2.bind(on_press=self.view_6.goback)
        self.main_panel.get_Button_Bar().button_B2.enable()
        self.main_panel.get_Button_Bar().tag_button.disable()

        self.view_6.start_infinite_loop() 

    def rotate(self, b):
        """Method to rotate chosen picture by 90 degrees
        """
        for pic in self.view_2.pics:
            if pic.selected:
                self.view_2.stack.remove_widget(pic)
                pic.angle += 90
                self.view_2.stack.add_widget(pic)
        
    def zip(self, b):
        """Method to save a collection (json file, img files and tag json files) as a zip file in given directory
        """        
        temporary_collection = ImageCollection('exported')
        for pic in self.view_2.pics:
            if pic.selected == True: 
                temporary_collection.registerItem(pic.cpImage)
        root = tk.Tk()
        root.withdraw()
        filename = simpledialog.askstring("To save", "Enter your zip's name:")
        path = f'{os.getcwd()}/Projeto/Collections/zips'
        file_path = os.path.join(path, filename)
        try:
            CentralPanel.save_collection_as_zip(temporary_collection, file_path)
            ctypes.windll.user32.MessageBoxW(0, "Your collection has been saved", "Success", 1)
        except:
             print('There was en error with saving the collection')

    @classmethod
    def save_collection_as_zip(cls, collection, zip_file_path):
        json_data = {'filename': os.path.basename(zip_file_path), 'items': collection.toJson()}
        imgs_paths = [x.file_path for x in collection.items]
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            zipf.writestr(collection.filename + '.json', json.dumps(json_data))
            for path in imgs_paths:
                if os.path.isfile(path):
                    zipf.write(path, os.path.basename(path))
            for img in collection.items:
                d = {k: list(v) for k, v in img.metadata.items()}
                zipf.writestr(img.file_name + '.json', json.dumps(d))
        