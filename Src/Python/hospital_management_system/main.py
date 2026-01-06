"""
Hospital Management System - User Interface
"""

from core.hospital_manager import HospitalManager
from core.department import Department
from models.patient import Patient
from models.staff import Staff
from models.nurse import Nurse
from models.admin_staff import AdminStaff
from models.doctor import Doctor


class HospitalUI:
    """User Interface for Hospital Management System"""
    
    def __init__(self):
        """Initialize the UI"""
        self.manager = HospitalManager()
        self.current_hospital = None
        self.setup_sample_data()
    
    def setup_sample_data(self):
        """Setup sample data for demonstration"""
        # Create a sample hospital
        hospital = self.manager.create_hospital("Cairo General Hospital", "Cairo, Egypt")
        self.current_hospital = hospital
        
        # Create departments
        emergency = Department("Emergency")
        cardiology = Department("Cardiology")
        pediatrics = Department("Pediatrics")
        
        # Add departments to hospital
        hospital.add_department(emergency)
        hospital.add_department(cardiology)
        hospital.add_department(pediatrics)
        
        # Create patients
        patient1 = Patient("Ahmed Mohamed", 35, "High blood pressure")
        patient2 = Patient("Sara Ali", 28, "Broken arm")
        patient3 = Patient("Mohamed Hassan", 45, "Heart condition")
        patient4 = Patient("Fatima Mahmoud", 8, "Flu symptoms")
        
        # Create staff with new classes
        doctor1 = Doctor("Dr. Omar Khalil", 45, "Cardiologist", 
                        specialization="Cardiology", 
                        license_number="MD12345", 
                        max_patients=20)
        doctor2 = Doctor("Dr. Layla Samir", 52, "Emergency Doctor",
                        specialization="Emergency Medicine",
                        license_number="MD67890",
                        max_patients=15)
        
        nurse1 = Nurse("Nurse Amira", 32, "Head Nurse", 
                      nurse_level="Senior")
        nurse2 = Nurse("Nurse Karim", 29, "Pediatric Nurse",
                      nurse_level="Junior")
        
        admin1 = AdminStaff("Receptionist Sara", 28, "Receptionist",
                          access_level="Basic")
        admin2 = AdminStaff("Manager Ali", 40, "Hospital Manager",
                          access_level="Admin")
        
        # Add patients and staff to departments
        emergency.add_patient(patient1)
        emergency.add_patient(patient2)
        emergency.add_staff(doctor2)
        emergency.add_staff(nurse1)
        emergency.add_staff(admin1)
        
        cardiology.add_patient(patient3)
        cardiology.add_staff(doctor1)
        
        pediatrics.add_patient(patient4)
        pediatrics.add_staff(nurse2)
        
        # Assign patients to doctors
        doctor1.current_patients.append(patient3)
        doctor2.current_patients.extend([patient1, patient2])
        
        # Assign ward to nurse
        nurse1.assign_to_ward("Emergency Ward A")
        
        print("\n Sample data loaded successfully!")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print(" HOSPITAL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. View Hospital Information")
        print("2. Manage Departments")
        print("3. Manage Patients")
        print("4. Manage Staff")
        print("5. Create New Hospital")
        print("6. Switch Hospital")
        print("7. Exit")
        print("="*50)
    
    def run(self):
        """Run the main UI loop"""
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == '1':
                    self.view_hospital_info()
                elif choice == '2':
                    self.manage_departments()
                elif choice == '3':
                    self.manage_patients()
                elif choice == '4':
                    self.manage_staff()
                elif choice == '5':
                    self.create_hospital()
                elif choice == '6':
                    self.switch_hospital()
                elif choice == '7':
                    print("\n Thank you for using Hospital Management System!")
                    break
                else:
                    print(" Invalid choice! Please enter 1-7.")
            except Exception as e:
                print(f" Error: {e}")
    
    def view_hospital_info(self):
        """View current hospital information"""
        if not self.current_hospital:
            print(" No hospital selected!")
            return
        
        self.current_hospital.view_hospital_info()
        
        # List all departments with details
        print("\n DEPARTMENT DETAILS:")
        for dept in self.current_hospital.departments:
            print(f"\n  {dept.name}:")
            print(f"    Patients: {dept.get_patient_count()}")
            print(f"    Staff: {dept.get_staff_count()}")
            
            if dept.get_patient_count() > 0:
                print("    Current Patients:")
                for patient in dept.patients:
                    print(f"      - {patient.name} ({patient.age} years)")
            
            if dept.get_staff_count() > 0:
                print("    Current Staff:")
                for staff in dept.staff_members:
                    if isinstance(staff, Doctor):
                        staff_type = f"Doctor ({staff.specialization})"
                    elif isinstance(staff, Nurse):
                        staff_type = f"Nurse (Level: {staff.nurse_level})"
                    elif isinstance(staff, AdminStaff):
                        staff_type = f"Admin (Access: {staff.access_level})"
                    else:
                        staff_type = "Staff"
                    print(f"      - {staff.name} - {staff_type}")
    
    def manage_departments(self):
        """Manage departments menu"""
        if not self.current_hospital:
            print(" No hospital selected!")
            return
        
        print("\n" + "="*50)
        print(" DEPARTMENT MANAGEMENT")
        print("="*50)
        print("1. List All Departments")
        print("2. Add New Department")
        print("3. Remove Department")
        print("4. View Department Details")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            self.current_hospital.list_departments()
        elif choice == '2':
            self.add_department()
        elif choice == '3':
            self.remove_department()
        elif choice == '4':
            self.view_department_details()
        elif choice == '5':
            return
        else:
            print(" Invalid choice!")
    
    def add_department(self):
        """Add a new department"""
        name = input("Enter department name: ").strip()
        if not name:
            print(" Department name cannot be empty!")
            return
        
        department = Department(name)
        self.current_hospital.add_department(department)
    
    def remove_department(self):
        """Remove a department"""
        self.current_hospital.list_departments()
        
        if self.current_hospital.departments:
            name = input("\nEnter department name to remove: ").strip()
            self.current_hospital.remove_department(name)
    
    def view_department_details(self):
        """View details of a specific department"""
        self.current_hospital.list_departments()
        
        if self.current_hospital.departments:
            name = input("\nEnter department name to view: ").strip()
            department = self.current_hospital.find_department(name)
            
            if department:
                print(f"\n Department: {department.name}")
                print("="*30)
                department.list_patients()
                department.list_staff()
            else:
                print(" Department not found!")
    
    def manage_patients(self):
        """Manage patients menu"""
        if not self.current_hospital:
            print(" No hospital selected!")
            return
        
        print("\n" + "="*50)
        print(" PATIENT MANAGEMENT")
        print("="*50)
        print("1. Register New Patient")
        print("2. Admit Patient to Department")
        print("3. Discharge Patient")
        print("4. View Patient Medical Record")
        print("5. List All Patients")
        print("6. Assign Patient to Doctor")
        print("7. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            self.register_patient()
        elif choice == '2':
            self.admit_patient()
        elif choice == '3':
            self.discharge_patient()
        elif choice == '4':
            self.view_patient_record()
        elif choice == '5':
            self.list_all_patients()
        elif choice == '6':
            self.assign_patient_to_doctor()
        elif choice == '7':
            return
        else:
            print(" Invalid choice!")
    
    def register_patient(self):
        """Register a new patient"""
        name = input("Enter patient name: ").strip()
        if not name:
            print(" Name cannot be empty!")
            return
        
        try:
            age = int(input("Enter patient age: ").strip())
            if age <= 0 or age > 120:
                print(" Please enter a valid age (1-120)")
                return
        except ValueError:
            print(" Age must be a number!")
            return
        
        medical_record = input("Enter initial medical record (optional): ").strip()
        
        patient = Patient(name, age, medical_record)
        print(f"\n Patient '{name}' registered successfully!")
        print(f"   Patient Info: {patient.view_info()}")
        
        # Ask if they want to admit immediately
        admit = input("\nAdmit this patient now? (yes/no): ").strip().lower()
        if admit == 'yes':
            self.admit_patient_to_department(patient)
        
        return patient
    
    def admit_patient(self):
        """Admit an existing patient to a department"""
        # First, find the patient
        print("\nAvailable patients in hospital:")
        all_patients = self.get_all_patients()
        
        if not all_patients:
            print(" No patients found!")
            return
        
        for i, patient in enumerate(all_patients, 1):
            dept = patient.admitted_department.name if patient.admitted_department else "Not admitted"
            print(f"{i}. {patient.name} - Age: {patient.age} - Department: {dept}")
        
        try:
            choice = int(input("\nSelect patient number: ").strip())
            if 1 <= choice <= len(all_patients):
                patient = all_patients[choice-1]
                self.admit_patient_to_department(patient)
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def admit_patient_to_department(self, patient):
        """Helper to admit patient to department"""
        self.current_hospital.list_departments()
        
        if self.current_hospital.departments:
            dept_name = input("\nEnter department name: ").strip()
            department = self.current_hospital.find_department(dept_name)
            
            if department:
                department.add_patient(patient)
            else:
                print(" Department not found!")
    
    def discharge_patient(self):
        """Discharge a patient"""
        all_patients = self.get_all_patients()
        admitted_patients = [p for p in all_patients if p.admitted_department]
        
        if not admitted_patients:
            print(" No admitted patients found!")
            return
        
        print("\nAdmitted Patients:")
        for i, patient in enumerate(admitted_patients, 1):
            print(f"{i}. {patient.name} - {patient.admitted_department.name}")
        
        try:
            choice = int(input("\nSelect patient number to discharge: ").strip())
            if 1 <= choice <= len(admitted_patients):
                patient = admitted_patients[choice-1]
                print(patient.discharge())
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def view_patient_record(self):
        """View patient medical record"""
        all_patients = self.get_all_patients()
        
        if not all_patients:
            print(" No patients found!")
            return
        
        print("\nPatients:")
        for i, patient in enumerate(all_patients, 1):
            print(f"{i}. {patient.name}")
        
        try:
            choice = int(input("\nSelect patient number: ").strip())
            if 1 <= choice <= len(all_patients):
                patient = all_patients[choice-1]
                print(f"\n{patient.view_record()}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def list_all_patients(self):
        """List all patients across all departments"""
        all_patients = self.get_all_patients()
        
        if not all_patients:
            print(" No patients found!")
            return
        
        print(f"\n Total Patients: {len(all_patients)}")
        for i, patient in enumerate(all_patients, 1):
            dept = patient.admitted_department.name if patient.admitted_department else "Not admitted"
            print(f"{i}. {patient.name} | Age: {patient.age} | Department: {dept}")
    
    def assign_patient_to_doctor(self):
        """Assign a patient to a doctor"""
        all_patients = self.get_all_patients()
        admitted_patients = [p for p in all_patients if p.admitted_department]
        
        if not admitted_patients:
            print(" No admitted patients found!")
            return
        
        print("\nAdmitted Patients:")
        for i, patient in enumerate(admitted_patients, 1):
            print(f"{i}. {patient.name}")
        
        try:
            patient_choice = int(input("\nSelect patient number: ").strip())
            if not (1 <= patient_choice <= len(admitted_patients)):
                print(" Invalid selection!")
                return
            
            patient = admitted_patients[patient_choice-1]
            
            # Find doctors
            doctors = []
            for dept in self.current_hospital.departments:
                for staff in dept.staff_members:
                    if isinstance(staff, Doctor):
                        doctors.append(staff)
            
            if not doctors:
                print(" No doctors available!")
                return
            
            print("\nAvailable Doctors:")
            for i, doctor in enumerate(doctors, 1):
                current_count = len(doctor.current_patients)
                print(f"{i}. {doctor.name} - {doctor.specialization} ({current_count}/{doctor.max_patients})")
            
            doctor_choice = int(input("\nSelect doctor number: ").strip())
            if 1 <= doctor_choice <= len(doctors):
                doctor = doctors[doctor_choice-1]
                
                if len(doctor.current_patients) >= doctor.max_patients:
                    print(f" Doctor {doctor.name} has reached maximum patients!")
                    return
                
                if patient not in doctor.current_patients:
                    doctor.current_patients.append(patient)
                    print(f" Patient {patient.name} assigned to Dr. {doctor.name}")
                else:
                    print(" Patient already assigned to this doctor!")
            else:
                print(" Invalid selection!")
                
        except ValueError:
            print(" Please enter a number!")
    
    def get_all_patients(self):
        """Get all patients from all departments"""
        all_patients = []
        for department in self.current_hospital.departments:
            all_patients.extend(department.patients)
        return all_patients
    
    def manage_staff(self):
        """Manage staff menu"""
        if not self.current_hospital:
            print(" No hospital selected!")
            return
        
        print("\n" + "="*50)
        print(" STAFF MANAGEMENT")
        print("="*50)
        print("1. Hire New Staff")
        print("2. Assign Staff to Department")
        print("3. List All Staff")
        print("4. Hire Specific Staff Type")
        print("5. Doctor Operations")
        print("6. Nurse Operations")
        print("7. Admin Operations")
        print("8. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            self.hire_staff_general()
        elif choice == '2':
            self.assign_staff()
        elif choice == '3':
            self.list_all_staff()
        elif choice == '4':
            self.hire_specific_staff()
        elif choice == '5':
            self.doctor_operations()
        elif choice == '6':
            self.nurse_operations()
        elif choice == '7':
            self.admin_operations()
        elif choice == '8':
            return
        else:
            print(" Invalid choice!")
    
    def hire_staff_general(self):
        """Hire new general staff (legacy method)"""
        name = input("Enter staff name: ").strip()
        if not name:
            print(" Name cannot be empty!")
            return
        
        try:
            age = int(input("Enter staff age: ").strip())
            if age < 18 or age > 70:
                print(" Please enter a valid age (18-70)")
                return
        except ValueError:
            print(" Age must be a number!")
            return
        
        position = input("Enter staff position: ").strip()
        if not position:
            print(" Position cannot be empty!")
            return
        
        staff = Staff(name, age, position)
        print(f"\n Staff '{name}' hired successfully!")
        print(f"   Staff Info: {staff.view_info()}")
        
        # Ask if they want to assign immediately
        assign = input("\nAssign this staff to a department now? (yes/no): ").strip().lower()
        if assign == 'yes':
            self.assign_staff_to_department(staff)
        
        return staff
    
    def hire_specific_staff(self):
        """Hire specific type of staff"""
        print("\nSelect Staff Type:")
        print("1. Doctor")
        print("2. Nurse")
        print("3. Admin Staff")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            self.hire_doctor()
        elif choice == '2':
            self.hire_nurse()
        elif choice == '3':
            self.hire_admin_staff()
        else:
            print(" Invalid choice!")
    
    def hire_doctor(self):
        """Hire a new doctor"""
        name = input("Enter doctor name: ").strip()
        if not name:
            print(" Name cannot be empty!")
            return
        
        try:
            age = int(input("Enter doctor age: ").strip())
            if age < 25 or age > 70:
                print(" Please enter a valid age (25-70)")
                return
        except ValueError:
            print(" Age must be a number!")
            return
        
        position = input("Enter position (e.g., 'Cardiologist'): ").strip()
        specialization = input("Enter specialization: ").strip()
        license_number = input("Enter license number: ").strip()
        
        try:
            max_patients = int(input("Enter maximum patients: ").strip())
        except ValueError:
            print(" Must be a number!")
            return
        
        doctor = Doctor(name, age, position, 
                       specialization=specialization,
                       license_number=license_number,
                       max_patients=max_patients)
        
        print(f"\n Doctor '{name}' hired successfully!")
        print(f"   Specialization: {specialization}")
        print(f"   License: {license_number}")
        print(f"   Max Patients: {max_patients}")
        
        assign = input("\nAssign to department now? (yes/no): ").strip().lower()
        if assign == 'yes':
            self.assign_staff_to_department(doctor)
        
        return doctor
    
    def hire_nurse(self):
        """Hire a new nurse"""
        name = input("Enter nurse name: ").strip()
        if not name:
            print(" Name cannot be empty!")
            return
        
        try:
            age = int(input("Enter nurse age: ").strip())
            if age < 21 or age > 65:
                print(" Please enter a valid age (21-65)")
                return
        except ValueError:
            print(" Age must be a number!")
            return
        
        position = input("Enter position (e.g., 'Head Nurse'): ").strip()
        nurse_level = input("Enter nurse level (Junior/Senior/Head): ").strip()
        
        nurse = Nurse(name, age, position, nurse_level=nurse_level)
        
        print(f"\n Nurse '{name}' hired successfully!")
        print(f"   Level: {nurse_level}")
        
        assign = input("\nAssign to department now? (yes/no): ").strip().lower()
        if assign == 'yes':
            self.assign_staff_to_department(nurse)
        
        return nurse
    
    def hire_admin_staff(self):
        """Hire a new admin staff"""
        name = input("Enter admin staff name: ").strip()
        if not name:
            print(" Name cannot be empty!")
            return
        
        try:
            age = int(input("Enter age: ").strip())
            if age < 18 or age > 70:
                print(" Please enter a valid age (18-70)")
                return
        except ValueError:
            print(" Age must be a number!")
            return
        
        position = input("Enter position (e.g., 'Receptionist'): ").strip()
        access_level = input("Enter access level (Basic/Admin/Super): ").strip()
        
        admin = AdminStaff(name, age, position, access_level=access_level)
        
        print(f"\n Admin staff '{name}' hired successfully!")
        print(f"   Access Level: {access_level}")
        
        assign = input("\nAssign to department now? (yes/no): ").strip().lower()
        if assign == 'yes':
            self.assign_staff_to_department(admin)
        
        return admin
    
    def assign_staff(self):
        """Assign existing staff to department"""
        all_staff = self.get_all_staff()
        unassigned_staff = [s for s in all_staff if not s.assigned_department]
        
        if not unassigned_staff:
            print(" All staff are already assigned!")
            return
        
        print("\nUnassigned Staff:")
        for i, staff in enumerate(unassigned_staff, 1):
            if isinstance(staff, Doctor):
                staff_type = "Doctor"
            elif isinstance(staff, Nurse):
                staff_type = "Nurse"
            elif isinstance(staff, AdminStaff):
                staff_type = "Admin"
            else:
                staff_type = "Staff"
            print(f"{i}. {staff.name} - {staff_type}")
        
        try:
            choice = int(input("\nSelect staff number: ").strip())
            if 1 <= choice <= len(unassigned_staff):
                staff = unassigned_staff[choice-1]
                self.assign_staff_to_department(staff)
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def assign_staff_to_department(self, staff):
        """Helper to assign staff to department"""
        self.current_hospital.list_departments()
        
        if self.current_hospital.departments:
            dept_name = input("\nEnter department name: ").strip()
            department = self.current_hospital.find_department(dept_name)
            
            if department:
                department.add_staff(staff)
                
                # If it's a nurse, ask for ward assignment
                if isinstance(staff, Nurse):
                    assign_ward = input(f"Assign nurse {staff.name} to a ward? (yes/no): ").strip().lower()
                    if assign_ward == 'yes':
                        ward = input("Enter ward name: ").strip()
                        staff.assign_to_ward(ward)
                        print(f" Nurse assigned to {ward}")
            else:
                print(" Department not found!")
    
    def list_all_staff(self):
        """List all staff across all departments"""
        all_staff = self.get_all_staff()
        
        if not all_staff:
            print(" No staff found!")
            return
        
        print(f"\n Total Staff: {len(all_staff)}")
        for i, staff in enumerate(all_staff, 1):
            dept = staff.assigned_department.name if staff.assigned_department else "Not assigned"
            
            if isinstance(staff, Doctor):
                staff_type = f"Doctor ({staff.specialization})"
                details = f"Patients: {len(staff.current_patients)}/{staff.max_patients}"
            elif isinstance(staff, Nurse):
                staff_type = f"Nurse (Level: {staff.nurse_level})"
                details = f"Ward: {staff.assigned_ward}" if staff.assigned_ward else "No ward assigned"
            elif isinstance(staff, AdminStaff):
                staff_type = f"Admin (Access: {staff.access_level})"
                details = ""
            else:
                staff_type = "General Staff"
                details = ""
            
            print(f"{i}. {staff.name} | {staff_type} | Department: {dept} | {details}")
    
    def get_all_staff(self):
        """Get all staff from all departments"""
        all_staff = []
        for department in self.current_hospital.departments:
            all_staff.extend(department.staff_members)
        return all_staff
    
    def doctor_operations(self):
        """Doctor-specific operations"""
        doctors = []
        for dept in self.current_hospital.departments:
            for staff in dept.staff_members:
                if isinstance(staff, Doctor):
                    doctors.append(staff)
        
        if not doctors:
            print(" No doctors available!")
            return
        
        print("\n" + "="*50)
        print(" DOCTOR OPERATIONS")
        print("="*50)
        print("1. Write Prescription")
        print("2. View Patient List")
        print("3. Schedule Surgery")
        print("4. List All Doctors")
        print("5. Back to Staff Menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            self.doctor_write_prescription(doctors)
        elif choice == '2':
            self.doctor_view_patients(doctors)
        elif choice == '3':
            self.doctor_schedule_surgery(doctors)
        elif choice == '4':
            self.list_doctors(doctors)
        elif choice == '5':
            return
        else:
            print(" Invalid choice!")
    
    def doctor_write_prescription(self, doctors):
        """Doctor writes a prescription"""
        print("\nSelect Doctor:")
        for i, doctor in enumerate(doctors, 1):
            print(f"{i}. Dr. {doctor.name} - {doctor.specialization}")
        
        try:
            choice = int(input("\nSelect doctor number: ").strip())
            if 1 <= choice <= len(doctors):
                doctor = doctors[choice-1]
                prescription = doctor.write_prescription()
                print(f"\n {prescription}")
                print(f" Prescription written by Dr. {doctor.name}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def doctor_view_patients(self, doctors):
        """Doctor views their patient list"""
        print("\nSelect Doctor:")
        for i, doctor in enumerate(doctors, 1):
            print(f"{i}. Dr. {doctor.name} - {doctor.specialization}")
        
        try:
            choice = int(input("\nSelect doctor number: ").strip())
            if 1 <= choice <= len(doctors):
                doctor = doctors[choice-1]
                print(f"\n Patients under Dr. {doctor.name}:")
                doctor.view_patient_list()
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def doctor_schedule_surgery(self, doctors):
        """Doctor schedules surgery"""
        print("\nSelect Doctor:")
        for i, doctor in enumerate(doctors, 1):
            print(f"{i}. Dr. {doctor.name} - {doctor.specialization}")
        
        try:
            choice = int(input("\nSelect doctor number: ").strip())
            if 1 <= choice <= len(doctors):
                doctor = doctors[choice-1]
                doctor.schedule_surgery()
                print(f" Surgery scheduled by Dr. {doctor.name}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def list_doctors(self, doctors):
        """List all doctors with details"""
        print(f"\n Total Doctors: {len(doctors)}")
        for i, doctor in enumerate(doctors, 1):
            dept = doctor.assigned_department.name if doctor.assigned_department else "Not assigned"
            print(f"{i}. Dr. {doctor.name}")
            print(f"   Specialization: {doctor.specialization}")
            print(f"   Department: {dept}")
            print(f"   License: {doctor.license_number}")
            print(f"   Patients: {len(doctor.current_patients)}/{doctor.max_patients}")
    
    def nurse_operations(self):
        """Nurse-specific operations"""
        nurses = []
        for dept in self.current_hospital.departments:
            for staff in dept.staff_members:
                if isinstance(staff, Nurse):
                    nurses.append(staff)
        
        if not nurses:
            print(" No nurses available!")
            return
        
        print("\n" + "="*50)
        print(" NURSE OPERATIONS")
        print("="*50)
        print("1. Administer Medication")
        print("2. Monitor Patient")
        print("3. List All Nurses")
        print("4. Back to Staff Menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            self.nurse_administer_medication(nurses)
        elif choice == '2':
            self.nurse_monitor_patient(nurses)
        elif choice == '3':
            self.list_nurses(nurses)
        elif choice == '4':
            return
        else:
            print(" Invalid choice!")
    
    def nurse_administer_medication(self, nurses):
        """Nurse administers medication"""
        print("\nSelect Nurse:")
        for i, nurse in enumerate(nurses, 1):
            print(f"{i}. Nurse {nurse.name} - Level: {nurse.nurse_level}")
        
        try:
            choice = int(input("\nSelect nurse number: ").strip())
            if 1 <= choice <= len(nurses):
                nurse = nurses[choice-1]
                nurse.administer_medication()
                print(f" Medication administered by Nurse {nurse.name}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def nurse_monitor_patient(self, nurses):
        """Nurse monitors a patient"""
        print("\nSelect Nurse:")
        for i, nurse in enumerate(nurses, 1):
            print(f"{i}. Nurse {nurse.name} - Level: {nurse.nurse_level}")
        
        try:
            choice = int(input("\nSelect nurse number: ").strip())
            if 1 <= choice <= len(nurses):
                nurse = nurses[choice-1]
                nurse.monitor_patient()
                print(f" Patient monitoring by Nurse {nurse.name}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def list_nurses(self, nurses):
        """List all nurses with details"""
        print(f"\n Total Nurses: {len(nurses)}")
        for i, nurse in enumerate(nurses, 1):
            dept = nurse.assigned_department.name if nurse.assigned_department else "Not assigned"
            print(f"{i}. Nurse {nurse.name}")
            print(f"   Level: {nurse.nurse_level}")
            print(f"   Department: {dept}")
            print(f"   Ward: {nurse.assigned_ward if nurse.assigned_ward else 'Not assigned'}")
    
    def admin_operations(self):
        """Admin-specific operations"""
        admins = []
        for dept in self.current_hospital.departments:
            for staff in dept.staff_members:
                if isinstance(staff, AdminStaff):
                    admins.append(staff)
        
        if not admins:
            print(" No admin staff available!")
            return
        
        print("\n" + "="*50)
        print(" ADMIN OPERATIONS")
        print("="*50)
        print("1. Process Appointment")
        print("2. Manage Inventory")
        print("3. Generate Report")
        print("4. List All Admin Staff")
        print("5. Back to Staff Menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            self.admin_process_appointment(admins)
        elif choice == '2':
            self.admin_manage_inventory(admins)
        elif choice == '3':
            self.admin_generate_report(admins)
        elif choice == '4':
            self.list_admins(admins)
        elif choice == '5':
            return
        else:
            print(" Invalid choice!")
    
    def admin_process_appointment(self, admins):
        """Admin processes an appointment"""
        print("\nSelect Admin Staff:")
        for i, admin in enumerate(admins, 1):
            print(f"{i}. {admin.name} - Access: {admin.access_level}")
        
        try:
            choice = int(input("\nSelect admin number: ").strip())
            if 1 <= choice <= len(admins):
                admin = admins[choice-1]
                admin.process_appointment()
                print(f" Appointment processed by {admin.name}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def admin_manage_inventory(self, admins):
        """Admin manages inventory"""
        print("\nSelect Admin Staff:")
        for i, admin in enumerate(admins, 1):
            print(f"{i}. {admin.name} - Access: {admin.access_level}")
        
        try:
            choice = int(input("\nSelect admin number: ").strip())
            if 1 <= choice <= len(admins):
                admin = admins[choice-1]
                admin.manage_inventory()
                print(f" Inventory managed by {admin.name}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def admin_generate_report(self, admins):
        """Admin generates a report"""
        print("\nSelect Admin Staff:")
        for i, admin in enumerate(admins, 1):
            print(f"{i}. {admin.name} - Access: {admin.access_level}")
        
        try:
            choice = int(input("\nSelect admin number: ").strip())
            if 1 <= choice <= len(admins):
                admin = admins[choice-1]
                report = admin.generate_report()
                print(f"\n {report}")
                print(f" Report generated by {admin.name}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")
    
    def list_admins(self, admins):
        """List all admin staff with details"""
        print(f"\n Total Admin Staff: {len(admins)}")
        for i, admin in enumerate(admins, 1):
            dept = admin.assigned_department.name if admin.assigned_department else "Not assigned"
            print(f"{i}. {admin.name}")
            print(f"   Position: {admin.position}")
            print(f"   Access Level: {admin.access_level}")
            print(f"   Department: {dept}")
    
    def create_hospital(self):
        """Create a new hospital"""
        print("\n" + "="*50)
        print(" CREATE NEW HOSPITAL")
        print("="*50)
        
        name = input("Enter hospital name: ").strip()
        if not name:
            print(" Hospital name cannot be empty!")
            return
        
        location = input("Enter hospital location: ").strip()
        if not location:
            print(" Location cannot be empty!")
            return
        
        hospital = self.manager.create_hospital(name, location)
        self.current_hospital = hospital
        print(f"\n Hospital '{name}' is now the current hospital!")
    
    def switch_hospital(self):
        """Switch to a different hospital"""
        hospitals = self.manager.list_hospitals()
        
        if not hospitals:
            print(" No hospitals available!")
            return
        
        try:
            choice = int(input("\nEnter hospital number to switch to: ").strip())
            if 1 <= choice <= len(hospitals):
                self.current_hospital = hospitals[choice-1]
                print(f"\n Switched to hospital: {self.current_hospital.name}")
            else:
                print(" Invalid selection!")
        except ValueError:
            print(" Please enter a number!")


def main():
    """Main function to run the hospital system"""
    print("\n" + "="*60)
    print(" WELCOME TO HOSPITAL MANAGEMENT SYSTEM")
    print("="*60)
    
    ui = HospitalUI()
    ui.run()


if __name__ == "__main__":
    main()