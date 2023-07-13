from backend.serializable import Serializable
from backend.tag import Tag
from shutil import copyfile
import os.path,time
import hashlib
import json 
import re

class CPImage(Serializable):
    """
    This class represents a single image
    """
    
    def __init__(self, file, folder, ex={}, meta={'tags': set()}):  
        """
        Constructor for a class

        Args:
            file (string): name of the picture file
            folder (string):  path to the picture stored in memory
            ex (dict, optional): EXIF data read from jpg file is saved in this dictionary. Defaults to {} if there is nor EXIF data.
            meta (dict, optional): this dictionary contains all metadata for a picture stored in a set. Defaults to {'tags': set()}.
        """
        self.file_name = file
        self.file_path = folder
        self.exif = ex
        self.metadata = meta
        #self.hex_digest = self.getHexDigest()
    
    # def __eq__(self, other):
    #     return isinstance(other, CPImage) and self.hex_digest == other.hex_digest
        
    # def __hash__(self):
    #     return hash(self.hex_digest)
    
    # def getHexDigest(self):
    #     with open(f'{self.file_path}/{self.file_name}', 'rb') as f:
    #         hashlib.md5(f.read()).hexdigest()
    
    def getDate(self):
        """
        This function retrieves a date of which the file was created

        Returns:
            string: time of the file creation in yyyy/mm/dd format
        """
        if self.exif != {}:
            return self.exif['date']
        else:
            return time.ctime(os.path.getmtime(self.file_path))
        
    def setDate(self, date):
        """
        This method is used to set a new date for a picture

        Args:
            date (string): date that will be set as new date of picture

        Requires: data in specific format yyyy/mm/dd

        Ensures: setting a new date in coherent format
        """
        pattern = re.compile("\d{4}\/(0?[1-9]|1[012])\/(0?[1-9]|[12][0-9]|3[01])$")
        if bool(pattern.match(date)) == False:
            raise Exception('Date format is incorrect')
        try:
            self.exif['date'] = date
        except Exception as e:
            print(str(e))

    def getDimensions(self):
        """
        This method is used to retrieve dimension (width and height) of picture

        Returns:
            tuple: containing int values corresponding to dimensions
        """
        try:
            return(self.exif['width'], self.exif['height'])
        except:
            print('This picture does not have any data about dimension stored')
    
    def getImageFile(self):
        """
        This function is used to fetch the file path of the picture

        Returns:
            string: name attribute of an object
        """
        #return(self.file_name)
        return(self.file_path)
    
    def toJson(self):
        """
        This function is used for saving picture information's in json format

        Returns:
            dict: dictionary in json format containing attributes to be saved
        """
        return {'file': self.file_path, 'exif': self.exif}

    @staticmethod
    def fromJson(json):
        """
        This function is responsible for reading data in json format in order to create an object

        Args:
            json (dict): data about the picture in json format
            folder (string): path of the folder from which the picture comes from

        Returns:
            object: CPImage class object initialized with passed attributes 
        """
        return CPImage(os.path.basename(json['file']), json['file'], json['exif'])

    @staticmethod
    def copyToFolder(filename, folder):
        """
        Static method to copy a picture file from one folder to another

        Args:
            filename (string): path with the filename of picture file
            folder (string): destination path where the picture will be saved
        """
        copyfile(filename, folder)

    def addTag(self, value): #tagcollection
        """
        This methid adds a tag to the picture object 
        Args:
            value (string): value of a tag 
        """
        #tag = Tag(value)
        self.metadata['tags'].add(value)
        #tagcollection.registerItem(tag)

    def removeTag(self, value):  
        """
        Method for deleting a tag of given value

        Args:
            value (string): text value of a tag to be deleted
        """
        try:
            self.metadata['tags'].remove(value)
        except:
            print('Given tag was never added to this picture')

    def hasTag(self, value):
        """
        Function to check wether a picture contains a tag

        Args:
            value (string): text value of a tag to be checked

        Returns:
            bool: True or False value
        """
        return value in self.metadata['tags']
    
    def getTags(self):
        """
        Function to obtain all tags of one picture

        Returns:
            set: string set containing name attribute of each tag
        """
        return self.metadata['tags']
    
    def saveTags(self, path):
        """
        Function to save tags of given picture in corresponding json file
        """
        d = {k: list(v) for k, v in self.metadata.items()}
        with open(f'{path}/{self.file_name}.json', 'w') as file:
            json.dump(d, file)

    def loadTags(self, tags_dir_path):
        """
        Method to load and save tags of a picture from json file in json format
        """
        for root, directories, files in os.walk(tags_dir_path):
            for filename in files:
                if filename.rstrip('.json') == self.file_name:
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r') as file:
                            self.metadata = json.load(file)
                            self.metadata = {k: set(v) for k, v in self.metadata.items()}
                            break
                    except:
                        return