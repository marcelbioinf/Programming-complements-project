from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from frontend.imagebox import ImageBox

class View2(BoxLayout):
    """Class which represents dynamic view of loaded pictures separated into pages depending on how many
       images fit in one page
    """
    def __init__(self, mainpanel, **kwargs):
        super(View2, self).__init__(**kwargs)
        self.padding = [10, 10, 10, 10]
        self.main_panel = mainpanel
        self.stack = StackLayout()
        self.number_of_pics = 0
        self.pics = []
        self.add_widget(self.stack)
        self.pages = []
        self.num_of_pages = 0
        self.actual_page = 0

    def add_pictures(self, selected_tags=[], filtering=False):
        """Method to add pictures to layout
        """
        self.pics.clear()
        self.total_width = 0
        self.total_height = 0
        for p in list(self.main_panel.pic_collection.items):
            if filtering and not (set(x.strip() for x in p.getTags()) & set(selected_tags)):
                continue
            self.pics.append(ImageBox(p))
            if self.total_height + self.pics[-1].height <= self.main_panel.central_panel.height:
                if self.total_width + self.pics[-1].width <= self.main_panel.central_panel.width:
                    self.total_width += self.pics[-1].width
                    self.stack.add_widget(self.pics[-1])
                    self.number_of_pics +=1
                    continue
                else:
                    self.total_width = self.pics[-1].width
                    self.total_height += self.pics[-1].height
                    if self.total_height + self.pics[-1].height <= self.main_panel.central_panel.height:
                        self.stack.add_widget(self.pics[-1])
                        self.number_of_pics +=1
                        continue
            self.pages.append(self.stack)
            self.num_of_pages += 1
            self.main_panel.get_Button_Bar().button_B3.enable()
            self.main_panel.get_Button_Bar().button_B3.bind(on_press=self.next_page)
            self.main_panel.get_Button_Bar().button_T.disable()
            self.stack = StackLayout()
            self.stack.add_widget(self.pics[-1])
            self.total_height = 0
            self.total_width = self.pics[-1].width
        self.pages.append(self.stack)
        self.main_panel.app_layout.getBottomRow().edit_label(f'Number of pictures on current page: {len(self.pages[0].children)}')

    def next_page(self, b):
        """Method to go to next page of pictures
        """        
        if self.actual_page < self.num_of_pages:
            self.actual_page += 1
            self.clear_widgets()
            self.add_widget(self.pages[self.actual_page])
            if not any(pic.selected == True for pic in self.pics):
                self.main_panel.app_layout.getBottomRow().edit_label(f'Number of pictures on current page: {len(self.pages[self.actual_page].children)}')
        if self.actual_page == self.num_of_pages:
            self.main_panel.get_Button_Bar().button_B3.disable()
        self.main_panel.get_Button_Bar().button_T.enable()
        self.main_panel.get_Button_Bar().button_T.bind(on_press=self.prev_page)

    def prev_page(self, b):
        """Method to go to previous page of pictures
        """        
        if self.actual_page - 1 < self.num_of_pages:
            self.main_panel.get_Button_Bar().button_B3.enable()
        if self.actual_page > 0:
            self.actual_page -= 1
            self.clear_widgets()
            self.add_widget(self.pages[self.actual_page])
            if not any(pic.selected == True for pic in self.pics):
                self.main_panel.app_layout.getBottomRow().edit_label(f'Number of pictures on current page: {len(self.pages[self.actual_page].children)}')
        if self.actual_page == 0:
            self.main_panel.get_Button_Bar().button_T.disable()
            self.main_panel.get_Button_Bar().button_B3.enable()

    def reset_layout(self):
        """Method to reset layout of all the pictures and pages
        """        
        self.actual_page = 0
        self.clear_widgets()
        self.stack.clear_widgets()
        self.pages.clear()
        self.num_of_pages = 0
        self.number_of_pics = 0
        self.pics = []