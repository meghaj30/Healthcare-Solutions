#!/usr/bin/env python3
"""
Add sample patients to the database for testing
"""

from app import app
from models import db, PatientORM

def add_sample_patients():
    """Add sample patients to the database"""
    
    sample_patients = [
        {
            'patient_id': 'HMS001',
            'name': 'John Smith',
            'age': 35,
            'gender': 'Male',
            'locality': 'Downtown',
            'condition_severity': 'Moderate',
            'priority_level': 'Medium',
            'medical_history': 'Hypertension, occasional headaches',
            'bill_amount': 500.0,
            'amount_paid': 200.0,
            'outstanding_amount': 300.0,
            'payment_status': 'Partially Paid',
            'insurance_coverage': 'Yes',
            'insurance_details': 'HealthPlus Insurance - Policy #HP123456',
            'admission_date': '2025-03-15',
            'discharge_date': None,
            'timestamp': '2025-03-15T10:30:00'
        },
        {
            'patient_id': 'HMS002',
            'name': 'Sarah Johnson',
            'age': 28,
            'gender': 'Female',
            'locality': 'Westside',
            'condition_severity': 'Mild',
            'priority_level': 'Low',
            'medical_history': 'Seasonal allergies',
            'bill_amount': 300.0,
            'amount_paid': 300.0,
            'outstanding_amount': 0.0,
            'payment_status': 'Fully Paid',
            'insurance_coverage': 'No',
            'insurance_details': '',
            'admission_date': '2025-03-20',
            'discharge_date': '2025-03-22',
            'timestamp': '2025-03-20T14:15:00'
        },
        {
            'patient_id': 'HMS003',
            'name': 'Michael Chen',
            'age': 42,
            'gender': 'Male',
            'locality': 'East End',
            'condition_severity': 'High',
            'priority_level': 'High',
            'medical_history': 'Diabetes Type 2, heart condition',
            'bill_amount': 1200.0,
            'amount_paid': 500.0,
            'outstanding_amount': 700.0,
            'payment_status': 'Partially Paid',
            'insurance_coverage': 'Yes',
            'insurance_details': 'MediCare Plus - Policy #MC789012',
            'admission_date': '2025-03-25',
            'discharge_date': None,
            'timestamp': '2025-03-25T09:45:00'
        },
        {
            'patient_id': 'HMS004',
            'name': 'Emily Davis',
            'age': 31,
            'gender': 'Female',
            'locality': 'North District',
            'condition_severity': 'Critical',
            'priority_level': 'Emergency',
            'medical_history': 'Asthma, recent respiratory infection',
            'bill_amount': 2500.0,
            'amount_paid': 0.0,
            'outstanding_amount': 2500.0,
            'payment_status': 'Unpaid',
            'insurance_coverage': 'Yes',
            'insurance_details': 'Premium Health - Policy #PH345678',
            'admission_date': '2025-03-28',
            'discharge_date': None,
            'timestamp': '2025-03-28T16:20:00'
        },
        {
            'patient_id': 'HMS005',
            'name': 'Robert Wilson',
            'age': 55,
            'gender': 'Male',
            'locality': 'South Park',
            'condition_severity': 'Moderate',
            'priority_level': 'Medium',
            'medical_history': 'Arthritis, high cholesterol',
            'bill_amount': 800.0,
            'amount_paid': 800.0,
            'outstanding_amount': 0.0,
            'payment_status': 'Fully Paid',
            'insurance_coverage': 'No',
            'insurance_details': '',
            'admission_date': '2025-03-10',
            'discharge_date': '2025-03-12',
            'timestamp': '2025-03-10T11:00:00'
        }
    ]
    
    with app.app_context():
        # Check if patients already exist
        existing_patients = PatientORM.query.count()
        if existing_patients > 0:
            print(f"Database already has {existing_patients} patients.")
            return
        
        # Add sample patients
        for patient_data in sample_patients:
            patient = PatientORM(**patient_data)
            db.session.add(patient)
        
        db.session.commit()
        print(f"Successfully added {len(sample_patients)} sample patients to database!")
        print("\nSample Patients:")
        for patient in sample_patients:
            print(f"- {patient['patient_id']}: {patient['name']} (Age: {patient['age']})")

if __name__ == '__main__':
    add_sample_patients()
