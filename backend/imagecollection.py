from backend.cpcollection import CPCollection
from backend.cpimage import CPImage
import os
import time

def allJPGfiles(path):
    """
    This function is used to find all the files with .jpg format

    Args:
        path (string): path of the folder to be scanned

    Returns:
        list: contains names of all of files that were found
        list: contains full path to all files that were found

    Requires: existing in the system folder path

    Ensures: finding all .jpg files in given folder and it's subfolders
    """
    file_list, file_names = [], []
    for root, directories, files in os.walk(path):
        for filename in files:
            if filename.endswith('jpg'):
                file_path = os.path.join(root, filename)
                file_list.append(file_path)
                file_names.append(filename)
    return file_list, file_names


class ImageCollection(CPCollection):
    """
    This class represents a collection of images and it's a subclass of CPCollection class
    """

    def __init__(self, filename):
        """
        __init__ Constructor for ImageCollection class

        Args:
            filename (string): name of the file that collection will be saved with
        """
        super().__init__(filename)

    @staticmethod
    def elementFromJson(jsonDict, dir_path):
        """
        Complete the read of collection from file by creating
        objects of either CPimage or Tag class, and adding these objects
        to the collection

        Args:
            jsonDict (dictionary): Dictionary containing the filename and an itemset of collection         
            folder (string): Folder where the collection is saved in memory   
        
        Requires: json dcitionary containing information about each object and folder path where collection was saves

        Ensures: creation of CPImage object from the json data
        
        Returns:
            object: object of CPImage class
        """
        img = CPImage.fromJson(jsonDict)
        img.loadTags(dir_path)
        return img
    
    @staticmethod
    def makeCPImage(file, filename):  #datamodyfikacji???
        """
        Function to feauture image in collection (copy it to directory of collection) and create object of CPImage class

        Args:
            file (string): path where the picture to be copied is saved in memory
            filename (string): name of the picture file

        Requires: path to the picture and it's name

        Ensures: creation of CPImage object

        Returns:
            object: CPImage class object
        """
        date = time.gmtime(os.path.getmtime(file))
        destination = f"{os.getcwd()}/Projeto/Collections/picCollections/pictures/{time.strftime(f'%Y/%m/%d/', date)}"
        destination = destination.replace('\\', '/')
        if not os.path.exists(destination):
            os.makedirs(destination)
        try:
            CPImage.copyToFolder(file, os.path.join(destination, filename))
        except Exception as e:
            print(f'There was something wrong with copying files to desired directory: {str(e)}')
        return CPImage(filename, file, {'date': time.strftime(f'%Y/%m/%d/', date)})

    def ScanFolder(self, folder):
        """
        Function to scan a given folder with presence of jpg files and register every found 
        file as item of the collection

        Args:
            folder (string): path to folder to be scanned

        Requires: path to the folder in memory that stores the pictures

        Ensures: creation and registration of CPImage object in collection
        """
        files, files_names = allJPGfiles(folder)
        if (len(files) == 0):
            print('There were no jpg files in given directory')
        for i, file in enumerate(files):
            img = ImageCollection.makeCPImage(file, files_names[i])
            self.registerItem(img)

    def save_each_image(self, path):
        list(map(lambda img:  img.saveTags(path), self.items))

    def findWithTag(self, value):
        """
        Function to find all the pictures of collection that contain specific given tag

        Args:
            value (string): tag of interest

        Requires: string value representing a tag of interest

        Ensures: returning collection of filtered objects containing only tag of interest

        Returns:
            set: collection of objects containing specific value in items attribute
        """
        return set([img for img in self.items if img.hasTag(value)])
    
    #def addTag(self, value, tagcollection):
        """
        Function to add a tag to whole collection

        Args:
            value (string): tag to be added

        Requires: string value representing a tag to be added

        Ensures: assigning a given tag to every object of collection
        """
        for item in self.items:
            item.addTag(value, tagcollection)