"""
Patient class
"""
from models.person import Person

class Patient(Person):
    """Patient class inherits from Person"""
    
    def __init__(self, name, age, medical_record=""):
        """
        Initialize a patient
        
        Args:
            name (str): Patient's name
            age (int): Patient's age
            medical_record (str): Initial medical record
        """
        super().__init__(name, age)
        self.medical_record = medical_record
        self.admitted_department = None
    
    def view_record(self):
        """
        View patient's medical record
        
        Returns:
            str: Medical record information
        """
        if self.medical_record:
            return f"Medical Record for {self.name}: {self.medical_record}"
        else:
            return f"No medical record available for {self.name}"
    
    def view_info(self):
        """
        Override parent method to include patient info
        
        Returns:
            str: Complete patient information
        """
        base_info = super().view_info()
        return f"{base_info} | Patient"
    
    def admit_to_department(self, department):
        """Admit patient to a department"""
        self.admitted_department = department
        return f"{self.name} admitted to {department.name}"
    
    def discharge(self):
        """Discharge patient from department"""
        if self.admitted_department:
            dept_name = self.admitted_department.name
            self.admitted_department = None
            return f"{self.name} discharged from {dept_name}"
        return f"{self.name} is not admitted to any department"

