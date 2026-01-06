"""
Hospital Management System - Streamlit GUI
"""

import streamlit as st
import sys
import os
import uuid
import plotly.graph_objects as go
import plotly.express as px
st.set_page_config(page_title="Hospital Management System")

# Add current path to Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.hospital_manager import HospitalManager
from core.department import Department
from models.patient import Patient
from models.staff import Staff
from models.nurse import Nurse
from models.admin_staff import AdminStaff
from models.doctor import Doctor

# ============================================================================
# Application Setup
# ============================================================================

def setup_session_state():
    """Setup session state for data"""
    if 'manager' not in st.session_state:
        st.session_state.manager = HospitalManager()
    
    if 'current_hospital' not in st.session_state:
        st.session_state.current_hospital = None
    
    if 'setup_complete' not in st.session_state:
        # Don't setup sample data automatically - let user choose
        st.session_state.setup_complete = False
    
    if 'widget_keys' not in st.session_state:
        st.session_state.widget_keys = {}

def get_widget_key(base_name):
    """Generate a unique widget key"""
    if base_name not in st.session_state.widget_keys:
        st.session_state.widget_keys[base_name] = str(uuid.uuid4())
    return st.session_state.widget_keys[base_name]

def setup_sample_data():
    """Setup sample data"""
    if st.session_state.setup_complete:
        return
    
    manager = st.session_state.manager
    hospital = manager.create_hospital("Cairo General Hospital", "Cairo, Egypt")
    st.session_state.current_hospital = hospital
    
    # Create departments
    emergency = Department("Emergency")
    cardiology = Department("Cardiology")
    pediatrics = Department("Pediatrics")
    neurology = Department("Neurology")
    
    # Add departments to hospital
    hospital.add_department(emergency)
    hospital.add_department(cardiology)
    hospital.add_department(pediatrics)
    hospital.add_department(neurology)
    
    # Create patients
    patient1 = Patient("Ahmed Mohamed", 35, "High blood pressure")
    patient2 = Patient("Sara Ali", 28, "Broken arm")
    patient3 = Patient("Mohamed Hassan", 45, "Heart condition")
    patient4 = Patient("Fatima Mahmoud", 8, "Flu symptoms")
    patient5 = Patient("Youssef Ahmed", 62, "Neurological disorder")
    patient6 = Patient("Nadia Salem", 41, "Cardiac arrhythmia")
    
    # Create staff
    doctor1 = Doctor("Dr. Omar Khalil", 45, "Cardiologist", 
                    specialization="Cardiology", 
                    license_number="MD12345", 
                    max_patients=20)
    doctor2 = Doctor("Dr. Layla Samir", 52, "Emergency Doctor",
                    specialization="Emergency Medicine",
                    license_number="MD67890",
                    max_patients=15)
    doctor3 = Doctor("Dr. Hana Mostafa", 38, "Neurologist",
                    specialization="Neurology",
                    license_number="MD54321",
                    max_patients=18)
    
    nurse1 = Nurse("Nurse Amira", 32, "Head Nurse", 
                  nurse_level="Senior")
    nurse2 = Nurse("Nurse Karim", 29, "Pediatric Nurse",
                  nurse_level="Junior")
    nurse3 = Nurse("Nurse Samira", 35, "Cardiac Nurse",
                  nurse_level="Intermediate")
    
    admin1 = AdminStaff("Receptionist Sara", 28, "Receptionist",
                      access_level="Basic")
    admin2 = AdminStaff("Manager Ali", 40, "Hospital Manager",
                      access_level="Admin")
    admin3 = AdminStaff("Coordinator Rana", 33, "Department Coordinator",
                      access_level="Supervisor")
    
    # Add patients and staff to departments
    emergency.add_patient(patient1)
    emergency.add_patient(patient2)
    emergency.add_staff(doctor2)
    emergency.add_staff(nurse1)
    emergency.add_staff(admin1)
    
    cardiology.add_patient(patient3)
    cardiology.add_patient(patient6)
    cardiology.add_staff(doctor1)
    cardiology.add_staff(nurse3)
    
    pediatrics.add_patient(patient4)
    pediatrics.add_staff(nurse2)
    
    neurology.add_patient(patient5)
    neurology.add_staff(doctor3)
    neurology.add_staff(admin3)
    
    # Assign patients to doctors
    doctor1.current_patients.append(patient3)
    doctor1.current_patients.append(patient6)
    doctor2.current_patients.extend([patient1, patient2])
    doctor3.current_patients.append(patient5)
    
    # Assign ward to nurse
    nurse1.assign_to_ward("Emergency Ward A")
    nurse2.assign_to_ward("Pediatric Ward B")
    nurse3.assign_to_ward("Cardiac Ward C")
    
    st.session_state.setup_complete = True
    st.success("✅ Sample data loaded successfully!")

# ============================================================================
# Dashboard Functions (NEW)
# ============================================================================

def display_dashboard():
    """Display dashboard similar to the provided image"""
    # Initialize session state first
    setup_session_state()
    
    if not st.session_state.current_hospital:
        st.warning("⚠️ No hospital selected! Create or load a hospital first.")
        return
    
    hospital = st.session_state.current_hospital
    
    st.markdown('<h1 class="main-header">🏥 Hospital Management System</h1>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="section-header">{hospital.name}</h2>', unsafe_allow_html=True)
    
    # Hospital location
    st.markdown(f'<div style="margin-bottom: 20px;"><strong>📍</strong> {hospital.location}</div>', unsafe_allow_html=True)
    
    # Key metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_patients = sum(dept.get_patient_count() for dept in hospital.departments)
    total_staff = sum(dept.get_staff_count() for dept in hospital.departments)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f0f8ff; border-radius: 10px; border: 1px solid #e0e0e0;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">Patients</div>
            <div style="font-size: 24px; font-weight: bold; color: #1E3A8A;">{}</div>
            <div style="font-size: 12px; color: #666;">{}/50 beds occupied</div>
        </div>
        """.format(total_patients, total_patients), unsafe_allow_html=True)
    
    with col2:
        # Count different staff types
        doctors = nurses = admins = 0
        for dept in hospital.departments:
            for staff in dept.staff_members:
                if isinstance(staff, Doctor):
                    doctors += 1
                elif isinstance(staff, Nurse):
                    nurses += 1
                elif isinstance(staff, AdminStaff):
                    admins += 1
        
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f0f8ff; border-radius: 10px; border: 1px solid #e0e0e0;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">Staff</div>
            <div style="font-size: 24px; font-weight: bold; color: #1E3A8A;">{}</div>
            <div style="font-size: 12px; color: #666;">{} Dr | {} Nurses | {} Admin</div>
        </div>
        """.format(total_staff, doctors, nurses, admins), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f0f8ff; border-radius: 10px; border: 1px solid #e0e0e0;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">Departments</div>
            <div style="font-size: 24px; font-weight: bold; color: #1E3A8A;">{}</div>
            <div style="font-size: 12px; color: #666;">Active departments</div>
        </div>
        """.format(len(hospital.departments)), unsafe_allow_html=True)
    
    with col4:
        occupancy_rate = (total_patients / 50) * 100 if 50 > 0 else 0
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f0f8ff; border-radius: 10px; border: 1px solid #e0e0e0;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">Occupancy</div>
            <div style="font-size: 24px; font-weight: bold; color: #1E3A8A;">{:.1f}%</div>
            <div style="font-size: 12px; color: #666;">Bed occupancy rate</div>
        </div>
        """.format(occupancy_rate), unsafe_allow_html=True)
    
    with col5:
        # You can add another metric here
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f0f8ff; border-radius: 10px; border: 1px solid #e0e0e0;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">Available</div>
            <div style="font-size: 24px; font-weight: bold; color: #1E3A8A;">{}</div>
            <div style="font-size: 12px; color: #666;">Available beds</div>
        </div>
        """.format(50 - total_patients), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create two columns for charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### Department Overview")
        
        # Department data
        dept_names = []
        dept_patients = []
        dept_staff = []
        
        for dept in hospital.departments:
            dept_names.append(dept.name)
            dept_patients.append(dept.get_patient_count())
            dept_staff.append(dept.get_staff_count())
        
        if dept_names:
            # Create horizontal bar chart
            fig = go.Figure()
            
            # Add patient bars
            fig.add_trace(go.Bar(
                y=dept_names,
                x=dept_patients,
                name='Patients',
                orientation='h',
                marker=dict(color='#3B82F6'),
                text=dept_patients,
                textposition='auto',
            ))
            
            # Add staff bars
            fig.add_trace(go.Bar(
                y=dept_names,
                x=dept_staff,
                name='Staff',
                orientation='h',
                marker=dict(color='#10B981'),
                text=dept_staff,
                textposition='auto',
            ))
            
            fig.update_layout(
                barmode='group',
                height=300,
                plot_bgcolor='white',
                showlegend=True,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis_title="Count",
                yaxis_title="",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No departments available")
    
    with col_right:
        st.markdown("### Staff Distribution")
        
        # Calculate staff distribution by type
        doctors = nurses = admins = other = 0
        for dept in hospital.departments:
            for staff in dept.staff_members:
                if isinstance(staff, Doctor):
                    doctors += 1
                elif isinstance(staff, Nurse):
                    nurses += 1
                elif isinstance(staff, AdminStaff):
                    admins += 1
                else:
                    other += 1
        
        labels = ['Doctors', 'Nurses', 'Admin', 'Other']
        values = [doctors, nurses, admins, other]
        colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
        
        if total_staff > 0:
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.4,
                marker=dict(colors=colors),
                textinfo='percent+label',
                textposition='inside',
                hoverinfo='label+percent+value'
            )])
            
            fig.update_layout(
                height=300,
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0),
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show percentages below
            cols = st.columns(4)
            percentages = []
            for val in values:
                percentages.append((val / total_staff * 100) if total_staff > 0 else 0)
            
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 16px; font-weight: bold; color: {colors[i]};">{percentages[i]:.1f}%</div>
                        <div style="font-size: 12px; color: #666;">{labels[i]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No staff available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Department details section
    st.markdown("### Department Details")
    
    if hospital.departments:
        cols = st.columns(min(len(hospital.departments), 4))
        
        for idx, (col, dept) in enumerate(zip(cols, hospital.departments)):
            with col:
                # Count staff types in this department
                dept_doctors = dept_nurses = dept_admins = 0
                for staff in dept.staff_members:
                    if isinstance(staff, Doctor):
                        dept_doctors += 1
                    elif isinstance(staff, Nurse):
                        dept_nurses += 1
                    elif isinstance(staff, AdminStaff):
                        dept_admins += 1
                
                st.markdown(f"""
                <div style="padding: 15px; background-color: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                    <div style="font-size: 16px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;">{dept.name}</div>
                    <div style="margin-bottom: 5px;"><span style="color: #666;">Patients:</span> <strong>{dept.get_patient_count()}</strong></div>
                    <div style="margin-bottom: 5px;"><span style="color: #666;">Staff:</span> <strong>{dept.get_staff_count()}</strong></div>
                    <div style="margin-bottom: 5px;"><span style="color: #666;">Doctors:</span> <strong>{dept_doctors}</strong></div>
                    <div style="margin-bottom: 5px;"><span style="color: #666;">Nurses:</span> <strong>{dept_nurses}</strong></div>
                    <div><span style="color: #666;">Admin:</span> <strong>{dept_admins}</strong></div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No departments available")

# ============================================================================
# Display Functions
# ============================================================================

def display_hospital_info():
    """Display hospital information"""
    # Initialize session state first
    setup_session_state()
    
    if not st.session_state.current_hospital:
        st.warning("⚠️ No hospital selected! Create or load a hospital first.")
        return
    
    hospital = st.session_state.current_hospital
    
    st.title("🏠 Hospital Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"**{hospital.name}**")
        st.info(f"**Location:** {hospital.location}")
    
    with col2:
        total_patients = sum(dept.get_patient_count() for dept in hospital.departments)
        total_staff = sum(dept.get_staff_count() for dept in hospital.departments)
        st.metric("👥 Number of Patients", total_patients)
        st.metric("👨‍⚕️ Number of Staff", total_staff)
    
    # Display departments
    st.subheader("📋 Departments")
    
    if not hospital.departments:
        st.warning("No departments in this hospital.")
        return
    
    for dept in hospital.departments:
        with st.expander(f"**{dept.name}** ({dept.get_patient_count()} patients, {dept.get_staff_count()} staff)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Patients")
                if dept.patients:
                    for patient in dept.patients:
                        st.write(f"• **{patient.name}** ({patient.age} years)")
                else:
                    st.write("No patients")
            
            with col2:
                st.markdown("#### Staff")
                if dept.staff_members:
                    for staff in dept.staff_members:
                        if isinstance(staff, Doctor):
                            staff_type = f"👨‍⚕️ Doctor ({staff.specialization})"
                        elif isinstance(staff, Nurse):
                            staff_type = f"👩‍⚕️ Nurse (Level: {staff.nurse_level})"
                        elif isinstance(staff, AdminStaff):
                            staff_type = f"💼 Admin (Access: {staff.access_level})"
                        else:
                            staff_type = "👤 Staff"
                        st.write(f"• **{staff.name}** - {staff_type}")

def manage_departments():
    """Manage departments"""
    # Initialize session state first
    setup_session_state()
    
    if not st.session_state.current_hospital:
        st.warning("⚠️ No hospital selected! Create or load a hospital first.")
        return
    
    hospital = st.session_state.current_hospital
    
    st.title("📁 Department Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View Departments", "Add Department", "Remove Department", "Department Details"])
    
    with tab1:
        st.subheader("📋 Department List")
        if not hospital.departments:
            st.info("No departments in this hospital.")
        else:
            for i, dept in enumerate(hospital.departments, 1):
                st.write(f"{i}. **{dept.name}** - {dept.get_patient_count()} patients, {dept.get_staff_count()} staff")
    
    with tab2:
        st.subheader("➕ Add New Department")
        with st.form("add_department_form"):
            name = st.text_input("Department Name", placeholder="Enter department name", key="dept_name_input")
            submit = st.form_submit_button("Add", key="add_dept_button")
            
            if submit:
                if not name:
                    st.error("Department name cannot be empty!")
                else:
                    department = Department(name)
                    hospital.add_department(department)
                    st.success(f"✅ Department '{name}' added successfully!")
                    st.rerun()
    
    with tab3:
        st.subheader("🗑️ Remove Department")
        if not hospital.departments:
            st.info("No departments to remove.")
        else:
            dept_names = [dept.name for dept in hospital.departments]
            selected_dept = st.selectbox(
                "Select department to remove", 
                dept_names,
                key="remove_dept_select"
            )
            
            if st.button("Remove Department", type="secondary", key="remove_dept_button"):
                hospital.remove_department(selected_dept)
                st.success(f"✅ Department '{selected_dept}' removed successfully!")
                st.rerun()
    
    with tab4:
        st.subheader("🔍 Department Details")
        if not hospital.departments:
            st.info("No departments to view details.")
        else:
            dept_names = [dept.name for dept in hospital.departments]
            selected_dept_name = st.selectbox(
                "Select department to view", 
                dept_names,
                key="view_dept_select"
            )
            
            if selected_dept_name:
                department = hospital.find_department(selected_dept_name)
                if department:
                    st.markdown(f"### **{department.name}**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Patients")
                        if department.patients:
                            for patient in department.patients:
                                st.write(f"• **{patient.name}** ({patient.age} years)")
                                st.write(f"  Medical Record: {patient.medical_record}")
                        else:
                            st.write("No patients")
                    
                    with col2:
                        st.markdown("#### Staff")
                        if department.staff_members:
                            for staff in department.staff_members:
                                st.write(f"• **{staff.name}**")
                                st.write(f"  Position: {staff.position}")
                        else:
                            st.write("No staff")

def manage_patients():
    """Manage patients"""
    # Initialize session state first
    setup_session_state()
    
    if not st.session_state.current_hospital:
        st.warning("⚠️ No hospital selected! Create or load a hospital first.")
        return
    
    hospital = st.session_state.current_hospital
    
    st.title("👥 Patient Management")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Register Patient", "Admit Patient", "Discharge Patient", 
        "Medical Record", "Patient List", "Assign to Doctor"
    ])
    
    with tab1:
        st.subheader("📝 Register New Patient")
        with st.form("register_patient_form"):
            name = st.text_input("Patient Name", placeholder="Enter full name", key="reg_patient_name")
            age = st.number_input("Age", min_value=1, max_value=120, value=30, key="reg_patient_age")
            medical_record = st.text_area("Medical Record", placeholder="Enter medical details", key="reg_patient_record")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Register", key="reg_patient_submit")
            with col2:
                admit_now = st.checkbox("Admit patient immediately", key="reg_admit_now")
            
            if submit:
                if not name:
                    st.error("Patient name cannot be empty!")
                else:
                    patient = Patient(name, int(age), medical_record)
                    st.success(f"✅ Patient '{name}' registered successfully!")
                    
                    if admit_now:
                        st.info("Please use the 'Admit Patient' tab to admit this patient.")
    
    with tab2:
        st.subheader("🏥 Admit Patient to Department")
        
        # Get all unadmitted patients
        all_patients = get_all_patients(hospital)
        unadmitted_patients = [p for p in all_patients if not p.admitted_department]
        
        if not unadmitted_patients:
            st.info("All patients are already admitted.")
        else:
            patient_options = {f"{p.name} ({p.age} years)": p for p in unadmitted_patients}
            selected_patient_label = st.selectbox(
                "Select patient", 
                list(patient_options.keys()),
                key="admit_patient_select"
            )
            
            if selected_patient_label:
                selected_patient = patient_options[selected_patient_label]
                
                if hospital.departments:
                    dept_names = [dept.name for dept in hospital.departments]
                    selected_dept = st.selectbox(
                        "Select department", 
                        dept_names,
                        key="admit_dept_select"
                    )
                    
                    if st.button("Admit Patient", key="admit_patient_button"):
                        department = hospital.find_department(selected_dept)
                        if department:
                            department.add_patient(selected_patient)
                            st.success(f"✅ Patient '{selected_patient.name}' admitted to '{selected_dept}' department!")
                            st.rerun()
    
    with tab3:
        st.subheader("🚪 Discharge Patient")
        
        admitted_patients = get_admitted_patients(hospital)
        
        if not admitted_patients:
            st.info("No patients currently admitted.")
        else:
            patient_options = {f"{p.name} - {p.admitted_department.name}": p for p in admitted_patients}
            selected_patient_label = st.selectbox(
                "Select patient to discharge", 
                list(patient_options.keys()),
                key="discharge_patient_select"
            )
            
            if selected_patient_label:
                selected_patient = patient_options[selected_patient_label]
                
                if st.button("Discharge Patient", type="secondary", key="discharge_button"):
                    result = selected_patient.discharge()
                    st.success(result)
                    st.rerun()
    
    with tab4:
        st.subheader("📋 Medical Record")
        
        all_patients = get_all_patients(hospital)
        
        if not all_patients:
            st.info("No registered patients.")
        else:
            patient_names = [p.name for p in all_patients]
            selected_patient_name = st.selectbox(
                "Select patient", 
                patient_names,
                key="medical_record_select"
            )
            
            if selected_patient_name:
                patient = next((p for p in all_patients if p.name == selected_patient_name), None)
                if patient:
                    st.markdown(f"### **{patient.name}**")
                    st.markdown(f"**Age:** {patient.age} years")
                    if patient.admitted_department:
                        st.markdown(f"**Department:** {patient.admitted_department.name}")
                    st.markdown("**Medical Record:**")
                    st.write(patient.medical_record)
    
    with tab5:
        st.subheader("📊 All Patients List")
        
        all_patients = get_all_patients(hospital)
        
        if not all_patients:
            st.info("No patients.")
        else:
            st.write(f"**Total Patients:** {len(all_patients)}")
            
            for idx, patient in enumerate(all_patients):
                with st.expander(f"**{patient.name}** ({patient.age} years)"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Department:** {patient.admitted_department.name if patient.admitted_department else 'Not admitted'}")
                    with col2:
                        st.write(f"**Record:** {patient.medical_record[:100]}..." if len(patient.medical_record) > 100 else patient.medical_record)
    
    with tab6:
        st.subheader("👨‍⚕️ Assign Patient to Doctor")
        
        admitted_patients = get_admitted_patients(hospital)
        
        if not admitted_patients:
            st.info("No admitted patients.")
        else:
            # Get all doctors
            doctors = []
            for dept in hospital.departments:
                for staff in dept.staff_members:
                    if isinstance(staff, Doctor):
                        doctors.append(staff)
            
            if not doctors:
                st.info("No doctors available.")
            else:
                # Select patient
                patient_options = {p.name: p for p in admitted_patients}
                selected_patient_name = st.selectbox(
                    "Select patient", 
                    list(patient_options.keys()),
                    key="assign_patient_select"
                )
                
                if selected_patient_name:
                    selected_patient = patient_options[selected_patient_name]
                    
                    # Select doctor
                    doctor_options = {
                        f"Dr. {doc.name} ({doc.specialization}) - {len(doc.current_patients)}/{doc.max_patients}": doc 
                        for doc in doctors
                    }
                    selected_doctor_label = st.selectbox(
                        "Select doctor", 
                        list(doctor_options.keys()),
                        key="assign_doctor_select"
                    )
                    
                    if selected_doctor_label:
                        selected_doctor = doctor_options[selected_doctor_label]
                        
                        if st.button("Assign Patient to Doctor", key="assign_patient_doctor_button"):
                            if len(selected_doctor.current_patients) >= selected_doctor.max_patients:
                                st.error(f"❌ Doctor {selected_doctor.name} has reached maximum patients!")
                            elif selected_patient in selected_doctor.current_patients:
                                st.warning("⚠️ Patient already assigned to this doctor!")
                            else:
                                selected_doctor.current_patients.append(selected_patient)
                                st.success(f"✅ Patient '{selected_patient.name}' assigned to Dr. '{selected_doctor.name}'!")

def manage_staff():
    """Manage staff"""
    # Initialize session state first
    setup_session_state()
    
    if not st.session_state.current_hospital:
        st.warning("⚠️ No hospital selected! Create or load a hospital first.")
        return
    
    hospital = st.session_state.current_hospital
    
    st.title("👨‍⚕️ Staff Management")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Hire General", "Hire Specific", "Assign to Department", 
        "Staff List", "Doctor Operations", "Nurse Operations", "Admin Operations"
    ])
    
    with tab1:
        st.subheader("👤 Hire General Staff")
        with st.form("hire_general_staff_form"):
            name = st.text_input("Staff Name", placeholder="Enter full name", key="hire_name_input")
            age = st.number_input("Age", min_value=18, max_value=70, value=30, key="hire_age_input")
            position = st.text_input("Position", placeholder="Enter position", key="hire_position_input")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Hire", key="hire_general_submit")
            with col2:
                assign_now = st.checkbox("Assign to department immediately", key="hire_assign_now")
            
            if submit:
                if not name or not position:
                    st.error("Name and position cannot be empty!")
                else:
                    staff = Staff(name, int(age), position)
                    st.success(f"✅ Staff '{name}' hired successfully!")
                    
                    if assign_now:
                        st.info("Please use the 'Assign to Department' tab to assign this staff.")
    
    with tab2:
        st.subheader("🎯 Hire Specific Staff")
        
        staff_type = st.radio(
            "Select staff type:", 
            ["Doctor", "Nurse", "Admin"],
            key="staff_type_radio"
        )
        
        if staff_type == "Doctor":
            with st.form("hire_doctor_form"):
                name = st.text_input("Doctor Name", placeholder="Dr. Full Name", key="hire_doc_name")
                age = st.number_input("Doctor Age", min_value=25, max_value=70, value=45, key="hire_doc_age")
                position = st.text_input("Position", value="Doctor", placeholder="Doctor/Specialist", key="hire_doc_position")
                specialization = st.text_input("Specialization", placeholder="Enter specialization", key="hire_doc_special")
                license_number = st.text_input("License Number", placeholder="Enter license number", key="hire_doc_license")
                max_patients = st.number_input("Maximum Patients", min_value=1, max_value=100, value=20, key="hire_doc_max")
                
                if st.form_submit_button("Hire Doctor", key="hire_doc_submit"):
                    if not all([name, specialization, license_number]):
                        st.error("All fields are required!")
                    else:
                        doctor = Doctor(
                            name, int(age), position,
                            specialization=specialization,
                            license_number=license_number,
                            max_patients=int(max_patients)
                        )
                        st.success(f"✅ Doctor '{name}' hired successfully!")
        
        elif staff_type == "Nurse":
            with st.form("hire_nurse_form"):
                name = st.text_input("Nurse Name", placeholder="Nurse Full Name", key="hire_nurse_name")
                age = st.number_input("Nurse Age", min_value=21, max_value=65, value=30, key="hire_nurse_age")
                position = st.text_input("Position", value="Nurse", placeholder="Nurse", key="hire_nurse_position")
                nurse_level = st.selectbox("Level", ["Junior", "Intermediate", "Senior", "Head"], key="hire_nurse_level")
                
                if st.form_submit_button("Hire Nurse", key="hire_nurse_submit"):
                    if not name:
                        st.error("Nurse name is required!")
                    else:
                        nurse = Nurse(name, int(age), position, nurse_level=nurse_level)
                        st.success(f"✅ Nurse '{name}' hired successfully!")
        
        elif staff_type == "Admin":
            with st.form("hire_admin_form"):
                name = st.text_input("Admin Staff Name", placeholder="Enter full name", key="hire_admin_name")
                age = st.number_input("Age", min_value=18, max_value=70, value=35, key="hire_admin_age")
                position = st.text_input("Position", placeholder="Manager/Receptionist/etc", key="hire_admin_position")
                access_level = st.selectbox("Access Level", ["Basic", "Admin", "Supervisor"], key="hire_admin_access")
                
                if st.form_submit_button("Hire Admin", key="hire_admin_submit"):
                    if not name:
                        st.error("Staff name is required!")
                    else:
                        admin = AdminStaff(name, int(age), position, access_level=access_level)
                        st.success(f"✅ Admin staff '{name}' hired successfully!")
    
    with tab3:
        st.subheader("🏢 Assign Staff to Department")
        
        all_staff = get_all_staff(hospital)
        unassigned_staff = [s for s in all_staff if not s.assigned_department]
        
        if not unassigned_staff:
            st.info("All staff are already assigned.")
        else:
            staff_options = {}
            for staff in unassigned_staff:
                if isinstance(staff, Doctor):
                    staff_type = "Doctor"
                elif isinstance(staff, Nurse):
                    staff_type = "Nurse"
                elif isinstance(staff, AdminStaff):
                    staff_type = "Admin"
                else:
                    staff_type = "Staff"
                staff_options[f"{staff.name} ({staff_type})"] = staff
            
            selected_staff_label = st.selectbox(
                "Select staff", 
                list(staff_options.keys()),
                key="assign_staff_select"
            )
            
            if selected_staff_label:
                selected_staff = staff_options[selected_staff_label]
                
                if hospital.departments:
                    dept_names = [dept.name for dept in hospital.departments]
                    selected_dept = st.selectbox(
                        "Select department", 
                        dept_names,
                        key="assign_dept_select"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Assign to Department", key="assign_dept_button"):
                            department = hospital.find_department(selected_dept)
                            if department:
                                department.add_staff(selected_staff)
                                st.success(f"✅ '{selected_staff.name}' assigned to '{selected_dept}' department!")
                                st.rerun()
                    
                    # If nurse, add ward assignment option
                    if isinstance(selected_staff, Nurse):
                        with col2:
                            ward_name = st.text_input("Ward Name (for nurses only)", placeholder="Enter ward name", key="assign_ward_input")
                            if st.button("Assign to Ward", key="assign_ward_button"):
                                selected_staff.assign_to_ward(ward_name)
                                st.success(f"✅ Nurse assigned to '{ward_name}' ward!")
    
    with tab4:
        st.subheader("📋 All Staff List")
        
        all_staff = get_all_staff(hospital)
        
        if not all_staff:
            st.info("No staff.")
        else:
            st.write(f"**Total Staff:** {len(all_staff)}")
            
            for idx, staff in enumerate(all_staff):
                dept = staff.assigned_department.name if staff.assigned_department else "Not assigned"
                
                if isinstance(staff, Doctor):
                    staff_type = f"👨‍⚕️ Doctor ({staff.specialization})"
                    details = f"Patients: {len(staff.current_patients)}/{staff.max_patients}"
                elif isinstance(staff, Nurse):
                    staff_type = f"👩‍⚕️ Nurse (Level: {staff.nurse_level})"
                    details = f"Ward: {staff.assigned_ward if staff.assigned_ward else 'Not assigned'}"
                elif isinstance(staff, AdminStaff):
                    staff_type = f"💼 Admin (Access: {staff.access_level})"
                    details = ""
                else:
                    staff_type = "👤 General Staff"
                    details = ""
                
                with st.expander(f"**{staff.name}** - {staff_type}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Position:** {staff.position}")
                        st.write(f"**Age:** {staff.age}")
                        st.write(f"**Department:** {dept}")
                    with col2:
                        if details:
                            st.write(f"**Details:** {details}")
    
    with tab5:
        st.subheader("🩺 Doctor Operations")
        
        doctors = []
        for dept in hospital.departments:
            for staff in dept.staff_members:
                if isinstance(staff, Doctor):
                    doctors.append(staff)
        
        if not doctors:
            st.info("No doctors.")
        else:
            doctor_options = {f"Dr. {doc.name} ({doc.specialization})": doc for doc in doctors}
            selected_doctor_label = st.selectbox(
                "Select doctor", 
                list(doctor_options.keys()),
                key="doc_ops_select"
            )
            
            if selected_doctor_label:
                doctor = doctor_options[selected_doctor_label]
                
                operation = st.radio(
                    "Select operation:", 
                    ["Write Prescription", "View Patient List", "Schedule Surgery", "View Doctor Information"],
                    key="doc_ops_radio"
                )
                
                if st.button("Execute Operation", key="doc_execute_button"):
                    if operation == "Write Prescription":
                        prescription = doctor.write_prescription()
                        st.success(f"📝 **Prescription:** {prescription}")
                        st.info(f"Prescription written by Dr. {doctor.name}")
                    
                    elif operation == "View Patient List":
                        st.subheader(f"Patients of Dr. {doctor.name}")
                        if doctor.current_patients:
                            for patient in doctor.current_patients:
                                st.write(f"• **{patient.name}** ({patient.age} years)")
                        else:
                            st.info("No patients assigned to this doctor.")
                    
                    elif operation == "Schedule Surgery":
                        doctor.schedule_surgery()
                        st.success(f"✅ Surgery scheduled by Dr. {doctor.name}")
                    
                    elif operation == "View Doctor Information":
                        st.markdown(f"### Dr. {doctor.name}")
                        st.write(f"**Specialization:** {doctor.specialization}")
                        st.write(f"**License Number:** {doctor.license_number}")
                        st.write(f"**Maximum Patients:** {doctor.max_patients}")
                        st.write(f"**Current Patients:** {len(doctor.current_patients)}")
    
    with tab6:
        st.subheader("💉 Nurse Operations")
        
        nurses = []
        for dept in hospital.departments:
            for staff in dept.staff_members:
                if isinstance(staff, Nurse):
                    nurses.append(staff)
        
        if not nurses:
            st.info("No nurses.")
        else:
            nurse_options = {f"{nurse.name} (Level: {nurse.nurse_level})": nurse for nurse in nurses}
            selected_nurse_label = st.selectbox(
                "Select nurse", 
                list(nurse_options.keys()),
                key="nurse_ops_select"
            )
            
            if selected_nurse_label:
                nurse = nurse_options[selected_nurse_label]
                
                operation = st.radio(
                    "Select operation:", 
                    ["Administer Medication", "Monitor Patient", "View Nurse Information"],
                    key="nurse_ops_radio"
                )
                
                if st.button("Execute Operation", key="nurse_execute_button"):
                    if operation == "Administer Medication":
                        nurse.administer_medication()
                        st.success(f"✅ Medication administered by {nurse.name}")
                    
                    elif operation == "Monitor Patient":
                        nurse.monitor_patient()
                        st.success(f"✅ Patient monitoring by {nurse.name}")
                    
                    elif operation == "View Nurse Information":
                        st.markdown(f"### {nurse.name}")
                        st.write(f"**Level:** {nurse.nurse_level}")
                        st.write(f"**Ward:** {nurse.assigned_ward if nurse.assigned_ward else 'Not assigned'}")
                        if nurse.assigned_department:
                            st.write(f"**Department:** {nurse.assigned_department.name}")
    
    with tab7:
        st.subheader("📊 Admin Operations")
        
        admins = []
        for dept in hospital.departments:
            for staff in dept.staff_members:
                if isinstance(staff, AdminStaff):
                    admins.append(staff)
        
        if not admins:
            st.info("No admin staff.")
        else:
            admin_options = {f"{admin.name} (Access: {admin.access_level})": admin for admin in admins}
            selected_admin_label = st.selectbox(
                "Select admin staff", 
                list(admin_options.keys()),
                key="admin_ops_select"
            )
            
            if selected_admin_label:
                admin = admin_options[selected_admin_label]
                
                operation = st.radio(
                    "Select operation:", 
                    ["Process Appointment", "Manage Inventory", "Generate Report", "View Staff Information"],
                    key="admin_ops_radio"
                )
                
                if st.button("Execute Operation", key="admin_execute_button"):
                    if operation == "Process Appointment":
                        admin.process_appointment()
                        st.success(f"✅ Appointment processed by {admin.name}")
                    
                    elif operation == "Manage Inventory":
                        admin.manage_inventory()
                        st.success(f"✅ Inventory managed by {admin.name}")
                    
                    elif operation == "Generate Report":
                        report = admin.generate_report()
                        st.success(f"📄 **Report:** {report}")
                        st.info(f"Report generated by {admin.name}")
                    
                    elif operation == "View Staff Information":
                        st.markdown(f"### {admin.name}")
                        st.write(f"**Access Level:** {admin.access_level}")
                        if admin.assigned_department:
                            st.write(f"**Department:** {admin.assigned_department.name}")

def create_hospital():
    """Create new hospital"""
    # Initialize session state first
    setup_session_state()
    
    st.title("🏗️ Create New Hospital")
    
    with st.form("create_hospital_form"):
        name = st.text_input("Hospital Name", placeholder="Enter hospital name", key="create_hosp_name")
        location = st.text_input("Hospital Location", placeholder="Enter location", key="create_hosp_location")
        
        if st.form_submit_button("Create Hospital", key="create_hosp_button"):
            if not name or not location:
                st.error("Hospital name and location are required!")
            else:
                manager = st.session_state.manager
                hospital = manager.create_hospital(name, location)
                st.session_state.current_hospital = hospital
                st.success(f"✅ Hospital '{name}' created successfully!")
                st.success(f"🏥 '{name}' is now the current hospital!")
                st.rerun()

def switch_hospital():
    """Switch between hospitals"""
    # Initialize session state first
    setup_session_state()
    
    st.title("🔄 Switch Hospital")
    
    manager = st.session_state.manager
    hospitals = manager.list_hospitals()
    
    if not hospitals:
        st.info("No hospitals available. Create a hospital first.")
        return
    
    current_hospital_name = st.session_state.current_hospital.name if st.session_state.current_hospital else "None"
    
    st.info(f"Current Hospital: **{current_hospital_name}**")
    
    hospital_options = {f"{hospital.name} - {hospital.location}": hospital for hospital in hospitals}
    selected_hospital_label = st.selectbox(
        "Select hospital", 
        list(hospital_options.keys()),
        key="switch_hosp_select"
    )
    
    if selected_hospital_label:
        if st.button("Switch to this Hospital", key="switch_hosp_button"):
            selected_hospital = hospital_options[selected_hospital_label]
            st.session_state.current_hospital = selected_hospital
            st.success(f"✅ Switched to hospital '{selected_hospital.name}'!")
            st.rerun()

def load_sample_data():
    """Load sample data page"""
    # Initialize session state first
    setup_session_state()
    
    st.title("📊 Load Sample Data")
    
    st.info("""
    This will load sample data including:
    - Cairo General Hospital with 3 departments
    - 4 sample patients
    - 6 staff members (doctors, nurses, admin)
    - Pre-configured assignments
    """)
    
    if st.button("Load Sample Data", type="primary", key="load_sample_button"):
        setup_sample_data()
        st.success("✅ Sample data loaded successfully!")
        st.rerun()

# ============================================================================
# Helper Functions
# ============================================================================

def get_all_patients(hospital):
    """Get all patients"""
    all_patients = []
    for department in hospital.departments:
        all_patients.extend(department.patients)
    return all_patients

def get_admitted_patients(hospital):
    """Get admitted patients"""
    all_patients = get_all_patients(hospital)
    return [p for p in all_patients if p.admitted_department]

def get_all_staff(hospital):
    """Get all staff"""
    all_staff = []
    for department in hospital.departments:
        all_staff.extend(department.staff_members)
    return all_staff

# ============================================================================
# Main Interface
# ============================================================================

def main():
    """Main application interface"""
    
    # Page setup
    st.set_page_config(
        page_title="Hospital Management System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-header {
            color: #2563EB;
            border-bottom: 2px solid #60A5FA;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .stButton>button {
            width: 100%;
            background-color: #3B82F6;
            color: white;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #2563EB;
        }
        .success-message {
            padding: 15px;
            background-color: #D1FAE5;
            border-radius: 5px;
            border-right: 5px solid #10B981;
        }
        .warning-message {
            padding: 15px;
            background-color: #FEF3C7;
            border-radius: 5px;
            border-right: 5px solid #F59E0B;
        }
        .metric-card {
            text-align: center; 
            padding: 15px; 
            background-color: #f0f8ff; 
            border-radius: 10px; 
            border: 1px solid #e0e0e0;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 24px; 
            font-weight: bold; 
            color: #1E3A8A;
        }
        .metric-label {
            font-size: 14px; 
            color: #666; 
            margin-bottom: 5px;
        }
        .metric-subtext {
            font-size: 12px; 
            color: #666;
        }
        section[data-testid="stSidebar"] h3 {
            font-size: 1.3rem !important;
            font-weight: 700;
        }

        section[data-testid="stSidebar"] label {
            font-size: 1.5rem !important;
            font-weight: 600;
        }

        section[data-testid="stSidebar"] .stRadio div {
            gap: 8px;
        }

        section[data-testid="stSidebar"] input:checked + div {
            color: #1E40AF;
            font-weight: 700;
        }
        
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state at the beginning
    setup_session_state()
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3710/3710277.png", width=100)
        st.markdown("### 🏥 Main Menu")
        
        # Add a button to load sample data
        if not st.session_state.get('setup_complete', False):
            st.markdown("### 📊 Quick Start")
            if st.button("Load Sample Data", type="primary", key="sidebar_sample_button"):
                setup_sample_data()
                st.rerun()
        
        st.markdown("---")
        
        # Updated menu options to include Dashboard
        menu_options = {
            "📊 Dashboard": display_dashboard,
            "🏠 Hospital Information": display_hospital_info,
            "📁 Department Management": manage_departments,
            "👥 Patient Management": manage_patients,
            "👨‍⚕️ Staff Management": manage_staff,
            "🏗️ Create Hospital": create_hospital,
            "🔄 Switch Hospital": switch_hospital
        }
        
        selected = st.radio(
            "Select Section:",
            list(menu_options.keys()),
            key="main_menu_radio"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Information")
        st.markdown("""
        Comprehensive hospital management system that manages:
        - Patients and medical records
        - Staff (doctors, nurses, admin)
        - Departments and operations
        - Multiple hospitals
        """)
    
    # Main display
    if selected != "📊 Dashboard":
        st.markdown(f'<h1 class="main-header">🏥 Hospital Management System</h1>', unsafe_allow_html=True)
        st.markdown(f'<h2 class="section-header">{selected}</h2>', unsafe_allow_html=True)
    
    # Display selected section
    menu_options[selected]()

if __name__ == "__main__":
    main()
