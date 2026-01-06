"""
Admin Staff class
"""

from models.staff import Staff

class AdminStaff(Staff):
    def __init__(self, *args, access_level):
        super().__init__(*args)
        self.access_level = access_level
        self.responsibilities = []

    def process_appointment(self):
        pass

    def manage_inventory(self):
        pass

    def generate_report(self):
        return "Report generated"
