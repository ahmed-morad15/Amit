"""
Nurse class
"""

from models.staff import Staff

class Nurse(Staff):
    def __init__(self, *args, nurse_level):
        super().__init__(*args)
        self.nurse_level = nurse_level
        self.assigned_ward = None
        self.certifications = []

    def assign_to_ward(self, ward):
        self.assigned_ward = ward

    def administer_medication(self):
        pass

    def monitor_patient(self):
        pass


