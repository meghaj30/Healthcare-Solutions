#!/usr/bin/env python3
"""
Add sample doctors to the database for testing
"""

from app import app
from models import db, Doctor

def add_sample_doctors():
    """Add sample doctors to the database"""
    
    sample_doctors = [
        {
            'name': 'Sarah Johnson',
            'age': 45,
            'gender': 'Female',
            'department': 'Cardiology',
            'specialization': 'Cardiologist',
            'qualification': 'MD, FACC',
            'experience_years': 15,
            'consultation_fee': 500.0,
            'availability_days': 'Mon,Wed,Fri',
            'availability_time': '09:00-17:00',
            'about': 'Specialist in heart diseases and cardiovascular conditions.'
        },
        {
            'name': 'Michael Chen',
            'age': 38,
            'gender': 'Male',
            'department': 'Neurology',
            'specialization': 'Neurologist',
            'qualification': 'MD, PhD',
            'experience_years': 12,
            'consultation_fee': 600.0,
            'availability_days': 'Tue,Thu',
            'availability_time': '10:00-18:00',
            'about': 'Expert in brain and nervous system disorders.'
        },
        {
            'name': 'Emily Rodriguez',
            'age': 42,
            'gender': 'Female',
            'department': 'Pediatrics',
            'specialization': 'Pediatrician',
            'qualification': 'MD, FAAP',
            'experience_years': 18,
            'consultation_fee': 400.0,
            'availability_days': 'Mon,Tue,Wed,Thu,Fri',
            'availability_time': '08:00-16:00',
            'about': 'Dedicated to providing comprehensive healthcare for children.'
        },
        {
            'name': 'David Thompson',
            'age': 50,
            'gender': 'Male',
            'department': 'Orthopedics',
            'specialization': 'Orthopedic Surgeon',
            'qualification': 'MD, MS Ortho',
            'experience_years': 20,
            'consultation_fee': 700.0,
            'availability_days': 'Mon,Wed,Fri',
            'availability_time': '09:00-17:00',
            'about': 'Specialist in bone and joint disorders, sports injuries.'
        },
        {
            'name': 'Lisa Anderson',
            'age': 35,
            'gender': 'Female',
            'department': 'Dermatology',
            'specialization': 'Dermatologist',
            'qualification': 'MD, FAAD',
            'experience_years': 10,
            'consultation_fee': 450.0,
            'availability_days': 'Tue,Thu,Sat',
            'availability_time': '10:00-19:00',
            'about': 'Expert in skin, hair, and nail conditions.'
        }
    ]
    
    with app.app_context():
        # Check if doctors already exist
        existing_doctors = Doctor.query.count()
        if existing_doctors > 0:
            print(f"Database already has {existing_doctors} doctors. Skipping sample data insertion.")
            return
        
        # Add sample doctors
        for doctor_data in sample_doctors:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
        
        db.session.commit()
        print(f"Successfully added {len(sample_doctors)} sample doctors to the database!")

if __name__ == '__main__':
    add_sample_doctors()
