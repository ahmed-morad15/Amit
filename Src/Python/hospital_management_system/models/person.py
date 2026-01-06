"""
Base Person class
"""

class Person:
    """Base class for all people in the hospital"""
    
    def __init__(self, name, age):
        """
        Initialize a person
        
        Args:
            name (str): Person's name
            age (int): Person's age
        """
        self.name = name
        self.age = age
    
    def view_info(self):
        """
        View person information
        
        Returns:
            str: Formatted information string
        """
        return f"Name: {self.name}, Age: {self.age}"
    
    def __str__(self):
        """String representation"""
        return self.view_info()

