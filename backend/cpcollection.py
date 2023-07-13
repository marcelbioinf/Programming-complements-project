from backend.serializable import Serializable
# from backend.tagcollection import TagCollection
# from backend.imagecollection import ImageCollection
from abc import ABC, abstractmethod
import json
import functools
import ctypes
from pathlib import Path


class CPCollection(Serializable):
    """
    This class represetns a collection of items that could
    be either tags or pictures
    """
    def __init__(self, filename):
        """
        Constructor for CPCollection class

        Args:
            filename (string): name of the file that collection will be saved with
        """
        self.filename = filename
        self.items = set()

    def registerItem(self, item):
        """
        Adds an item to the itemset which represents the collection itself

        Args:
            item (obj): object of either CPimage or Tag class
        """
        self.items.add(item)

    def saveCollection(self, mypath, name_aletered=None): 
        """
        Saves a collection of objects to a file in json format

        Args:
            mypath (string): path where the collection will be saved
        
        Requires: mypath is an existing path in system 

        Ensures: creation of json file that will contain information about collection
        """
        if name_aletered: self.filename = name_aletered
        d = {'filename': self.filename, 'items': self.toJson()}
        #mypath = f"{os.getcwd()}/Project/collections/{next(iter(IC_1.items)).toJson()['exif']['date']}"
        try:
            with open(f'{mypath}/{self.filename}.json', 'w') as file:
                json.dump(d, file)
        except Exception as e:
            print(f'There was something wrong with saving collection to file: {str(e)}')

    def loadCollection(self, path, dir_path): 
        """
        Loads a collection of objects from a file in json format

        Args:
            path (string): path where the collection is saved
        
        Requires: path is an existing path in system 

        Ensures: creation of specific objects (Tag class or CPImage class) from json file
        """
        path_to_open = Path(path)
        try:
            with open(path_to_open, 'r') as file:
                d = json.load(file)
            path = path[:path.rfind('/')]
            self.items = self.fromJson(d, dir_path)
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"There is a problem with reading a collection: ({str(e)})", "Warning!", 16)
            return 0

    def size(self):
        """
        Returns the size of a collection

        Returns:
            int: number of items in the itemset
        """
        return len(self.items)
    
    def fromJson(self, jsonDict, dir_path):
        """
        Completes the read of collection from file by creating
        objects of either CPimage or Tag class, and adding these objects
        to the collection

        Args:
            jsonDict (dictionary): Dictionary containing the filename and an itemset of collection         
            folder (string): Folder where the collection is saved in memory                                                     
        """
        #return set(map(TagCollection.elementFromJson, jsonDict['items'])) if 'tags' in jsonDict['items'][0] else set(map(functools.partial(ImageCollection.elementFromJson, folder=folder), jsonDict['items']))
        return set(map(lambda x: self.elementFromJson(x, dir_path), jsonDict['items']))   #### DO DOKONCZENIA

    def toJson(self):
        """
        Creates an object that stores information about every item from collection
        in json format and is used in a method saving collection to the file

        Returns:
            list: list of dictionaries, each concerning one item of itemset
        """
        return [item.toJson() for item in self.items]
    
    @staticmethod
    @abstractmethod
    def elementFromJson(jsonDict):
        """
        Abstract method to return an object of an appropriate type, which is either CPimage or Tag, from 
        given dictionary. This function will be implemented in subclasses of CPCollection

        Args:
            jsonDict (dictionary): object containing information about given item
        """
        pass