# 🏥 Hospital Management System

A comprehensive Hospital Management System built with Python using Object-Oriented Programming (OOP) principles with both **Console Interface** and **Streamlit Web GUI**.

## 🎯 Dual Interface System

### 📟 Console Interface (Original)
The original command-line interface providing direct access to all system functionalities through an interactive console menu.

### 🌐 Streamlit Web GUI (New)
Modern web-based interface built with Streamlit offering enhanced user experience with visual dashboards, charts, and interactive components.

![Hospital Management System Dashboard](hospital_1.jpg)


## 🏥 System Overview

This system manages hospital operations including patient registration, staff management, department administration, and medical record keeping. It supports multiple hospital instances with detailed tracking of doctors, nurses, administrative staff, and patients.


### UML Class Diagram
![Hospital Management System UML](images/UML_3.png)

## 🚀 Features

### 🏛️ Hospital Management
- Create and manage multiple hospitals
- Switch between different hospital instances
- View comprehensive hospital information
- Track departments, staff, and patients

### 👨‍⚕️ Staff Management
- **Doctors**: Specialized medical professionals with patient assignments
- **Nurses**: Ward-based care providers with different experience levels
- **Admin Staff**: Administrative personnel with access control
- **General Staff**: Support staff members

### 🏥 Department Operations
- Create and manage medical departments
- Assign staff and patients to departments
- Track department statistics and occupancy
- Department-specific operations

### 👥 Patient Management
- Patient registration and admission
- Medical record management
- Department assignment and transfers
- Doctor-patient assignment
- Discharge procedures

### 📊 Reporting & Operations
- Generate reports
- Track inventory
- Schedule appointments
- Medical prescriptions
- Surgery scheduling

## 🗂️ Project Structure

```
hospital_management_system/
├── __init__.py
├── main.py                    # Main application entry point
├── app.py                     # Streamlit web application
├── README.md                  # This documentation file
├── core/                      # Core system modules
│   ├── __init__.py
│   ├── department.py          # Department class and management
│   ├── hospital_manager.py    # Hospital management system
│   └── hospital.py            # Hospital class definition
├── models/                    # Data models
│   ├── __init__.py
│   ├── person.py             # Base Person class
│   ├── patient.py            # Patient model
│   ├── staff.py              # Base Staff class
│   ├── doctor.py             # Doctor specialization
│   ├── nurse.py              # Nurse specialization
│   └── admin_staff.py        # Administrative staff
└── requirements.txt          # Python dependencies
```

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd hospital_management_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Run the Streamlit Web GUI (New)**
   ```bash
   streamlit run app.py
   ```

## 📋 Class Hierarchy

### Inheritance Structure
```
Person
├── Patient
└── Staff
    ├── Doctor
    ├── Nurse
    └── AdminStaff
```

### Class Details

#### **Person** (Base Class)
- Basic attributes: name, age
- Common methods for all persons

#### **Patient** 
- Medical record management
- Admission/discharge functionality
- Department assignment

#### **Staff** (Base for all staff)
- Position tracking
- Department assignment
- General staff operations

#### **Doctor**
- Specialization tracking
- Medical license management
- Patient assignment (max capacity)
- Medical operations (prescriptions, surgeries)

#### **Nurse**
- Nurse level (Junior/Senior/Head)
- Ward assignment
- Patient care operations
- Medication administration

#### **AdminStaff**
- Access level management
- Administrative operations
- Report generation
- Appointment processing

## 💡 Key Features in Detail

### Multi-Hospital Support
- Manage multiple hospitals simultaneously
- Switch contexts seamlessly
- Independent data for each hospital

### Staff Specialization
- **Doctors**: Track specialization, license, patient limits
- **Nurses**: Different levels with ward assignments
- **Admin**: Varying access levels for security

### Patient Care
- Complete medical record tracking
- Department-based organization
- Doctor-patient relationships
- Admission and discharge workflow

### Data Management
- In-memory data storage
- Sample data for demonstration
- Easy data manipulation through UI

## 🔮 Future Enhancements

Planned features for future releases:

### Phase 2
- [ ] Database persistence (SQLite/PostgreSQL)
- [ ] Appointment scheduling system
- [ ] Billing and payment tracking
- [ ] Pharmacy inventory management

### Phase 3
- [ ] Web interface (Flask/Django)
- [ ] API endpoints for integration
- [ ] Mobile application
- [ ] Reporting dashboard

### Phase 4
- [ ] Machine learning for patient predictions
- [ ] Integration with medical devices
- [ ] Telemedicine capabilities
- [ ] AI-powered diagnostics support

## 🏆 Credits

**Developed by**: Ahmed Morad  
**Version**: 1.0.0  
**Last Updated**: 6/1/2026

---

## 🔗 Useful Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [OOP Concepts in Python](https://realpython.com/python3-object-oriented-programming/)
- [Hospital Management Best Practices](https://www.who.int/healthsystems/en/)
- [Medical Software Standards](https://www.iso.org/standard/67868.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Graphing Library](https://plotly.com/python/)

---