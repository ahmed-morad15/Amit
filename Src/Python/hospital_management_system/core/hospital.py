"""
Hospital class
"""
from core.department import Department

class Hospital:
    """Main Hospital class that contains departments"""
    
    def __init__(self, name, location):
        """
        Initialize a hospital
        
        Args:
            name (str): Hospital name
            location (str): Hospital location
        """
        self.name = name
        self.location = location
        self.departments = []  # List of Department objects
    
    def add_department(self, department):
        """
        Add a department to the hospital
        
        Args:
            department (Department): Department object to add
        """
        if department not in self.departments:
            self.departments.append(department)
            print(f"✅ Department '{department.name}' added to {self.name}")
        else:
            print(f" Department '{department.name}' already exists in {self.name}")
    
    def remove_department(self, department_name):
        """
        Remove a department from the hospital
        
        Args:
            department_name (str): Name of department to remove
        """
        for dept in self.departments:
            if dept.name == department_name:
                self.departments.remove(dept)
                print(f"✅ Department '{department_name}' removed from {self.name}")
                return True
        print(f" Department '{department_name}' not found")
        return False
    
    def find_department(self, department_name):
        """
        Find a department by name
        
        Args:
            department_name (str): Name of department to find
            
        Returns:
            Department: Department object if found, None otherwise
        """
        for dept in self.departments:
            if dept.name == department_name:
                return dept
        return None
    
    def list_departments(self):
        """List all departments in the hospital"""
        print(f"\n Departments in {self.name}:")
        if not self.departments:
            print("  No departments")
        else:
            for i, dept in enumerate(self.departments, 1):
                print(f"  {i}. {dept}")
        return len(self.departments)
    
    def get_total_patients(self):
        """Get total number of patients in all departments"""
        total = 0
        for dept in self.departments:
            total += dept.get_patient_count()
        return total
    
    def get_total_staff(self):
        """Get total number of staff in all departments"""
        total = 0
        for dept in self.departments:
            total += dept.get_staff_count()
        return total
    
    def view_hospital_info(self):
        """Display hospital information"""
        print("\n" + "="*50)
        print(f"HOSPITAL: {self.name}")
        print(f"Location: {self.location}")
        print(f"Total Departments: {len(self.departments)}")
        print(f"Total Patients: {self.get_total_patients()}")
        print(f"Total Staff: {self.get_total_staff()}")
        print("="*50)
    
    def __str__(self):
        """String representation"""
        return f"Hospital: {self.name} | Location: {self.location} | Departments: {len(self.departments)}"