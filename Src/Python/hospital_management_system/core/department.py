"""
Department class
"""
from models.patient import Patient
from models.staff import Staff

class Department:
    """Department class manages patients and staff"""
    
    def __init__(self, name):
        """
        Initialize a department
        
        Args:
            name (str): Department name
        """
        self.name = name
        self.patients = []  # List of Patient objects
        self.staff_members = []  # List of Staff objects
    
    def add_patient(self, patient):
        """
        Add a patient to the department
        
        Args:
            patient (Patient): Patient object to add
        """
        if patient not in self.patients:
            self.patients.append(patient)
            patient.admitted_department = self
            print(f"✅ Patient '{patient.name}' added to {self.name}")
        else:
            print(f" Patient '{patient.name}' is already in {self.name}")
    
    def remove_patient(self, patient):
        """
        Remove a patient from the department
        
        Args:
            patient (Patient): Patient object to remove
        """
        if patient in self.patients:
            self.patients.remove(patient)
            patient.admitted_department = None
            print(f"✅ Patient '{patient.name}' removed from {self.name}")
            return True
        else:
            print(f" Patient '{patient.name}' not found in {self.name}")
            return False
    
    def add_staff(self, staff_member):
        """
        Add a staff member to the department
        
        Args:
            staff_member (Staff): Staff object to add
        """
        if staff_member not in self.staff_members:
            self.staff_members.append(staff_member)
            staff_member.assigned_department = self
            print(f"✅ Staff '{staff_member.name}' added to {self.name}")
        else:
            print(f" Staff '{staff_member.name}' is already in {self.name}")
    
    def remove_staff(self, staff_member):
        """
        Remove a staff member from the department
        
        Args:
            staff_member (Staff): Staff object to remove
        """
        if staff_member in self.staff_members:
            self.staff_members.remove(staff_member)
            staff_member.assigned_department = None
            print(f"✅ Staff '{staff_member.name}' removed from {self.name}")
            return True
        else:
            print(f" Staff '{staff_member.name}' not found in {self.name}")
            return False
    
    def list_patients(self):
        """List all patients in the department"""
        print(f"\n Patients in {self.name} Department:")
        if not self.patients:
            print("  No patients")
        else:
            for i, patient in enumerate(self.patients, 1):
                print(f"  {i}. {patient.name} (Age: {patient.age})")
        return len(self.patients)
    
    def list_staff(self):
        """List all staff in the department"""
        print(f"\n Staff in {self.name} Department:")
        if not self.staff_members:
            print("  No staff members")
        else:
            for i, staff in enumerate(self.staff_members, 1):
                print(f"  {i}. {staff.name} - {staff.position}")
        return len(self.staff_members)
    
    def get_patient_count(self):
        """Get number of patients"""
        return len(self.patients)
    
    def get_staff_count(self):
        """Get number of staff"""
        return len(self.staff_members)
    
    def __str__(self):
        """String representation"""
        return f"Department: {self.name} | Patients: {self.get_patient_count()} | Staff: {self.get_staff_count()}"

    