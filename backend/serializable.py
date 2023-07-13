from abc import ABC, abstractmethod

class Serializable(ABC):
    """
    This is a superclass for every other class in the application.
    """
    def toJson(self):
        """Function to return object in json format which here is dictionary

        Returns:
            dictionary: contains instance's attributes as key-value pairs
        """
        return self.__dict__
    
    @staticmethod
    @abstractmethod
    def fromJson(jsonDict):
        """
        Abstract method which will ensure that all subclasses contains it's implementation
        Role of this function is to initialize objects by reading a file in json format 

        Args:
            jsonDict (dictionary): contains instance's attributes as key-value pairs

        Requires: json dictionary

        Ensures: creation of specific object
        """        
        pass