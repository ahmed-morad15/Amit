"""
Doctor class
"""

from models.staff import Staff

class Doctor(Staff):
    def __init__(self, *args, specialization, license_number, max_patients):
        super().__init__(*args)
        self.specialization = specialization
        self.license_number = license_number
        self.max_patients = max_patients
        self.current_patients = []

    def write_prescription(self):
        return "Prescription written"

    def schedule_surgery(self):
        pass

    def view_patient_list(self):
        for p in self.current_patients:
            print(p.name)
