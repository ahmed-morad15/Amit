"""
Staff abstract class
"""
from models.person import Person

class Staff(Person):
    """Staff class inherits from Person"""
    
    def __init__(self, name, age, position):
        """
        Initialize a staff member
        
        Args:
            name (str): Staff's name
            age (int): Staff's age
            position (str): Staff's position/job title
        """
        super().__init__(name, age)
        self.position = position
        self.assigned_department = None
    
    def view_info(self):
        """
        Override parent method to include staff info
        
        Returns:
            str: Complete staff information
        """
        base_info = super().view_info()
        return f"{base_info} | Position: {self.position}"
    
    def assign_to_department(self, department):
        """Assign staff to a department"""
        self.assigned_department = department
        return f"{self.name} assigned to {department.name}"
