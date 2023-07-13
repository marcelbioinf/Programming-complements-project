from backend.serializable import Serializable

class Tag(Serializable):
    """
    This class represents a single tag - text based description of a picture
    """

    def __init__(self, value):
        """
        Constructor for a class which assigns the value of tag to the name attribute

        Args:
            value (string): represents the text value that will describe a picture
        """
        self.name = value

    def __eq__(self, other):
        return isinstance(other, Tag) and self.name == other.name
        
    def __hash__(self):
        return hash(self.name)
    
    @staticmethod
    def fromJson(jsonDict):
        """
        Creates a tag object from Json dictionary passed from a read file

        Args:
            jsonDict (dict): contains information written in the file about tag's value

        Returns:
            object: Tag class object
        """
        return Tag(jsonDict['name'])