#!/usr/bin/env python3
"""
Comprehensive dummy data population script for Healthcare Solutions
"""

import sys
import random
from datetime import datetime, date, timedelta, time
from app import app
from models import db, PatientORM, Doctor, Appointment, Resource, ResourceTransaction

def populate_patients():
    """Add comprehensive patient data"""
    print("Populating patients...")
    
    patients_data = [
        {
            'patient_id': 'HMS006',
            'name': 'Sarah Johnson',
            'age': 34,
            'gender': 'Female',
            'locality': 'Downtown Medical District',
            'condition_severity': 'Medium',
            'priority_level': 'Normal',
            'medical_history': 'Hypertension, Seasonal allergies',
            'bill_amount': 2500.00,
            'amount_paid': 1500.00,
            'outstanding_amount': 1000.00
        },
        {
            'patient_id': 'HMS007',
            'name': 'Michael Chen',
            'age': 45,
            'gender': 'Male',
            'locality': 'Westside Heights',
            'condition_severity': 'High',
            'priority_level': 'Urgent',
            'medical_history': 'Type 2 Diabetes, Heart condition',
            'bill_amount': 5000.00,
            'amount_paid': 3000.00,
            'outstanding_amount': 2000.00
        },
        {
            'patient_id': 'HMS008',
            'name': 'Emily Rodriguez',
            'age': 28,
            'gender': 'Female',
            'locality': 'Eastside Gardens',
            'condition_severity': 'Low',
            'priority_level': 'Normal',
            'medical_history': 'No significant medical history',
            'bill_amount': 800.00,
            'amount_paid': 800.00,
            'outstanding_amount': 0.00
        },
        {
            'patient_id': 'HMS009',
            'name': 'James Wilson',
            'age': 67,
            'gender': 'Male',
            'locality': 'Northwood Village',
            'condition_severity': 'Critical',
            'priority_level': 'Emergency',
            'medical_history': 'Prostate cancer, Arthritis, Glaucoma',
            'bill_amount': 12000.00,
            'amount_paid': 8000.00,
            'outstanding_amount': 4000.00
        },
        {
            'patient_id': 'HMS010',
            'name': 'Lisa Thompson',
            'age': 52,
            'gender': 'Female',
            'locality': 'Central Business District',
            'condition_severity': 'Medium',
            'priority_level': 'Normal',
            'medical_history': 'Osteoporosis, Migraines',
            'bill_amount': 1800.00,
            'amount_paid': 1000.00,
            'outstanding_amount': 800.00
        }
    ]
    
    for patient_data in patients_data:
        # Check if patient already exists
        existing = PatientORM.query.filter_by(patient_id=patient_data['patient_id']).first()
        if not existing:
            patient = PatientORM(**patient_data)
            db.session.add(patient)
    
    db.session.commit()
    print(f"Added {len(patients_data)} new patients")

def populate_doctors():
    """Add comprehensive doctor data"""
    print("Populating doctors...")
    
    doctors_data = [
        {
            'name': 'Dr. Amanda Foster',
            'specialization': 'Cardiology',
            'qualification': 'MD, FACC',
            'experience_years': 15,
            'consultation_fee': 250.00,
            'availability_days': 'Mon,Tue,Wed,Thu,Fri',
            'availability_time': '09:00-17:00',
            'about': 'Expert in cardiovascular diseases with 15+ years of experience'
        },
        {
            'name': 'Dr. Robert Martinez',
            'specialization': 'Orthopedics',
            'qualification': 'MD, FAAOS',
            'experience_years': 12,
            'consultation_fee': 200.00,
            'availability_days': 'Mon,Tue,Wed,Thu,Fri',
            'availability_time': '08:00-16:00',
            'about': 'Specializes in bone and joint disorders, sports medicine'
        },
        {
            'name': 'Dr. Jennifer Lee',
            'specialization': 'Pediatrics',
            'qualification': 'MD, FAAP',
            'experience_years': 8,
            'consultation_fee': 150.00,
            'availability_days': 'Mon,Tue,Wed,Thu,Fri,Sat',
            'availability_time': '08:00-17:00',
            'about': 'Dedicated to children\'s health and development'
        },
        {
            'name': 'Dr. David Kumar',
            'specialization': 'Neurology',
            'qualification': 'MD, FAAN',
            'experience_years': 20,
            'consultation_fee': 300.00,
            'availability_days': 'Tue,Wed,Thu,Fri',
            'availability_time': '09:00-17:00',
            'about': 'Expert in neurological disorders and brain conditions'
        },
        {
            'name': 'Dr. Maria Garcia',
            'specialization': 'Dermatology',
            'qualification': 'MD, FAAD',
            'experience_years': 10,
            'consultation_fee': 175.00,
            'availability_days': 'Mon,Tue,Wed,Thu,Fri',
            'availability_time': '08:00-16:00',
            'about': 'Specializes in skin conditions and cosmetic dermatology'
        }
    ]
    
    for doctor_data in doctors_data:
        # Check if doctor already exists
        existing = Doctor.query.filter_by(name=doctor_data['name']).first()
        if not existing:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
    
    db.session.commit()
    print(f"Added {len(doctors_data)} new doctors")

def populate_appointments():
    """Add comprehensive appointment data"""
    print("Populating appointments...")
    
    patients = PatientORM.query.all()
    doctors = Doctor.query.all()
    
    if len(patients) < 5 or len(doctors) < 5:
        print("Not enough patients or doctors for appointments")
        return
    
    appointments_data = [
        {
            'patient_id': 'HMS006',
            'doctor_id': doctors[0].doctor_id,
            'department': 'Cardiology',
            'symptoms': 'Chest pain, shortness of breath',
            'appointment_date': date.today() + timedelta(days=1),
            'appointment_time': time(10, 30),
            'consultation_type': 'Video',
            'status': 'Confirmed',
            'queue_number': 1
        },
        {
            'patient_id': 'HMS007',
            'doctor_id': doctors[1].doctor_id,
            'department': 'Orthopedics',
            'symptoms': 'Knee pain, difficulty walking',
            'appointment_date': date.today() + timedelta(days=2),
            'appointment_time': time(14, 0),
            'consultation_type': 'In-Person',
            'status': 'Pending',
            'queue_number': 2
        },
        {
            'patient_id': 'HMS008',
            'doctor_id': doctors[2].doctor_id,
            'department': 'Pediatrics',
            'symptoms': 'Fever, cough, loss of appetite',
            'appointment_date': date.today() + timedelta(days=3),
            'appointment_time': time(11, 15),
            'consultation_type': 'Video',
            'status': 'Confirmed',
            'queue_number': 3
        },
        {
            'patient_id': 'HMS009',
            'doctor_id': doctors[3].doctor_id,
            'department': 'Neurology',
            'symptoms': 'Severe headaches, dizziness',
            'appointment_date': date.today() + timedelta(days=1),
            'appointment_time': time(9, 0),
            'consultation_type': 'In-Person',
            'status': 'Confirmed',
            'queue_number': 4
        },
        {
            'patient_id': 'HMS010',
            'doctor_id': doctors[4].doctor_id,
            'department': 'Dermatology',
            'symptoms': 'Skin rash, itching',
            'appointment_date': date.today() + timedelta(days=4),
            'appointment_time': time(16, 30),
            'consultation_type': 'Video',
            'status': 'Pending',
            'queue_number': 5
        }
    ]
    
    for appointment_data in appointments_data:
        # Check if appointment already exists
        existing = Appointment.query.filter_by(
            patient_id=appointment_data['patient_id'],
            appointment_date=appointment_data['appointment_date']
        ).first()
        if not existing:
            appointment = Appointment(
                **appointment_data,
                video_enabled='true' if appointment_data['consultation_type'] == 'Video' else 'false',
                created_at=datetime.now()
            )
            db.session.add(appointment)
    
    db.session.commit()
    print(f"Added {len(appointments_data)} new appointments")

def populate_additional_resources():
    """Add more comprehensive resource data"""
    print("Populating additional resources...")
    
    resources_data = [
        {
            'name': 'Surgical Masks',
            'category': 'Supplies',
            'description': 'N95 surgical masks for medical procedures',
            'current_stock': 500,
            'minimum_stock': 100,
            'maximum_stock': 2000,
            'unit': 'pieces',
            'location': 'Storage Room A',
            'supplier': 'Medical Supplies Co.',
            'cost_per_unit': 2.50,
            'expiry_date': date.today() + timedelta(days=365)
        },
        {
            'name': 'Hand Sanitizer',
            'category': 'Supplies',
            'description': 'Alcohol-based hand sanitizer 500ml bottles',
            'current_stock': 150,
            'minimum_stock': 50,
            'maximum_stock': 500,
            'unit': 'bottles',
            'location': 'Nurse Station',
            'supplier': 'Health Products Ltd.',
            'cost_per_unit': 8.00,
            'expiry_date': date.today() + timedelta(days=730)
        },
        {
            'name': 'X-Ray Machine',
            'category': 'Equipment',
            'description': 'Digital X-ray imaging system',
            'current_stock': 2,
            'minimum_stock': 1,
            'maximum_stock': 3,
            'unit': 'units',
            'location': 'Radiology Department',
            'supplier': 'Medical Imaging Systems',
            'cost_per_unit': 150000.00
        },
        {
            'name': 'Blood Pressure Monitor',
            'category': 'Equipment',
            'description': 'Digital automatic blood pressure monitor',
            'current_stock': 15,
            'minimum_stock': 5,
            'maximum_stock': 25,
            'unit': 'units',
            'location': 'All Departments',
            'supplier': 'Healthcare Devices Inc.',
            'cost_per_unit': 89.99
        },
        {
            'name': 'Insulin',
            'category': 'Medicine',
            'description': 'Rapid-acting insulin 100U/ml',
            'current_stock': 200,
            'minimum_stock': 50,
            'maximum_stock': 500,
            'unit': 'vials',
            'location': 'Pharmacy',
            'supplier': 'Pharma Corp',
            'cost_per_unit': 45.00,
            'expiry_date': date.today() + timedelta(days=180)
        },
        {
            'name': 'Antibiotics',
            'category': 'Medicine',
            'description': 'Broad-spectrum antibiotics 500mg tablets',
            'current_stock': 1000,
            'minimum_stock': 200,
            'maximum_stock': 3000,
            'unit': 'tablets',
            'location': 'Pharmacy',
            'supplier': 'Pharma Corp',
            'cost_per_unit': 15.00,
            'expiry_date': date.today() + timedelta(days=90)
        },
        {
            'name': 'IV Catheters',
            'category': 'Supplies',
            'description': '18G IV catheters for intravenous therapy',
            'current_stock': 80,
            'minimum_stock': 30,
            'maximum_stock': 200,
            'unit': 'pieces',
            'location': 'Emergency Room',
            'supplier': 'Medical Supplies Co.',
            'cost_per_unit': 3.50
        },
        {
            'name': 'Ventilator',
            'category': 'Equipment',
            'description': 'ICU ventilator with advanced monitoring',
            'current_stock': 5,
            'minimum_stock': 2,
            'maximum_stock': 8,
            'unit': 'units',
            'location': 'ICU',
            'supplier': 'Critical Care Equipment',
            'cost_per_unit': 45000.00
        },
        {
            'name': 'ECG Machine',
            'category': 'Equipment',
            'description': '12-lead ECG machine with printer',
            'current_stock': 4,
            'minimum_stock': 2,
            'maximum_stock': 6,
            'unit': 'units',
            'location': 'Cardiology',
            'supplier': 'Medical Imaging Systems',
            'cost_per_unit': 12000.00
        },
        {
            'name': 'Pain Killers',
            'category': 'Medicine',
            'description': 'Paracetamol 500mg tablets',
            'current_stock': 3000,
            'minimum_stock': 500,
            'maximum_stock': 5000,
            'unit': 'tablets',
            'location': 'Pharmacy',
            'supplier': 'Pharma Corp',
            'cost_per_unit': 0.50,
            'expiry_date': date.today() + timedelta(days=365)
        }
    ]
    
    for resource_data in resources_data:
        # Check if resource already exists
        existing = Resource.query.filter_by(name=resource_data['name']).first()
        if not existing:
            resource = Resource(
                **resource_data,
                last_restocked=datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.session.add(resource)
    
    db.session.commit()
    print(f"Added {len(resources_data)} new resources")

def populate_resource_transactions():
    """Add sample resource transactions"""
    print("Populating resource transactions...")
    
    resources = Resource.query.all()
    
    for resource in resources[:10]:  # Add transactions for first 10 resources
        # Add 3-5 transactions per resource
        for i in range(random.randint(3, 5)):
            transaction_types = ['Stock In', 'Stock Out', 'Used']
            transaction_type = random.choice(transaction_types)
            
            quantity = random.randint(1, 50)
            remaining_stock = resource.current_stock + (quantity if transaction_type == 'Stock In' else -quantity)
            
            transaction = ResourceTransaction(
                resource_id=resource.resource_id,
                transaction_type=transaction_type,
                quantity=quantity,
                remaining_stock=max(0, remaining_stock),
                reason=f"Sample {transaction_type.lower()} transaction",
                performed_by=f"Staff Member {random.randint(1, 5)}",
                transaction_date=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(transaction)
    
    db.session.commit()
    print("Added sample resource transactions")

def main():
    """Main function to populate all data"""
    with app.app_context():
        print("Starting comprehensive data population...")
        print("=" * 50)
        
        try:
            populate_patients()
            populate_doctors()
            populate_appointments()
            populate_additional_resources()
            populate_resource_transactions()
            
            print("=" * 50)
            print("Data population completed successfully!")
            print("\nFinal Database Summary:")
            print(f"Patients: {PatientORM.query.count()}")
            print(f"Doctors: {Doctor.query.count()}")
            print(f"Appointments: {Appointment.query.count()}")
            print(f"Resources: {Resource.query.count()}")
            print(f"Resource Transactions: {ResourceTransaction.query.count()}")
            
        except Exception as e:
            print(f"Error populating data: {e}")
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    main()
