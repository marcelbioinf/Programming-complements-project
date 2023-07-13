from backend.cpcollection import CPCollection
from backend.tag import Tag

class TagCollection(CPCollection): 
    """
    This class represents a collection of tag objects. It is a subclass of CPCollection class
    """
    
    def __init__(self, filename):
        """
        Constructor for a class which initializes the supperclass 

        Args:
            filename (string): name of the file in which the collection will be saved
        """
        super().__init__(filename)

    @staticmethod
    def elementFromJson(jsonDict, dcit):
        """
        This method returns an object of Tag, from given dictionary that is passed from superclasses' calls. 

        Args:
            jsonDict (dictionary): object containing information about given object
        
        Returns:
            object: Tag class object with attributes read from dictionary
        """
        return Tag.fromJson(jsonDict)

    # def saveCollection(self, mypath):
    #     """
    #     This function is used to save the collection of tags

    #     Args:
    #         mypath (string): path to which the collection will be saved
    #         imagecollection (object): object of Image collection with corresponding name

    #     Requires: existing in memory path and existing object

    #     Ensures: self.getHour() == h
    #     """
    #     if self.filename.rstrip('tags.json').rstrip('-') == imagecollection.filename.rstrip('.json'):
    #         map(lambda img:  img.saveTags, imagecollection.items)
    #         super().saveCollection(mypath)
    #     else:
    #         raise Exception("Image collection and Tag collection do not have corresponding names. This tag collection does not concern given Image collection")