from core.hospital import Hospital

class HospitalManager:
    """Main manager class for the hospital system"""
    
    def __init__(self):
        """Initialize the hospital manager"""
        self.hospitals = []
    
    def create_hospital(self, name, location):
        """Create a new hospital"""
        hospital = Hospital(name, location)
        self.hospitals.append(hospital)
        print(f"🏥 Hospital '{name}' created in {location}")
        return hospital
    
    def get_hospital(self, name):
        """Get hospital by name"""
        for hospital in self.hospitals:
            if hospital.name == name:
                return hospital
        return None
    
    def list_hospitals(self):
        """List all hospitals"""
        print("\n" + "="*50)
        print("AVAILABLE HOSPITALS:")
        if not self.hospitals:
            print("  No hospitals registered")
        else:
            for i, hospital in enumerate(self.hospitals, 1):
                print(f"  {i}. {hospital}")
        return self.hospitals