#!/usr/bin/env python3
"""
Update sample patients with login credentials for testing
"""

from app import app
from models import db, PatientORM
from werkzeug.security import generate_password_hash

def update_patient_credentials():
    """Add login credentials to sample patients"""
    
    patient_credentials = [
        {
            'patient_id': 'HMS001',
            'email': 'john.smith@email.com',
            'password': 'HMS001',
            'phone': '+1234567890'
        },
        {
            'patient_id': 'HMS002',
            'email': 'sarah.johnson@email.com',
            'password': 'HMS002',
            'phone': '+1234567891'
        },
        {
            'patient_id': 'HMS003',
            'email': 'michael.chen@email.com',
            'password': 'HMS003',
            'phone': '+1234567892'
        },
        {
            'patient_id': 'HMS004',
            'email': 'emily.davis@email.com',
            'password': 'HMS004',
            'phone': '+1234567893'
        },
        {
            'patient_id': 'HMS005',
            'email': 'robert.wilson@email.com',
            'password': 'HMS005',
            'phone': '+1234567894'
        }
    ]
    
    with app.app_context():
        updated_count = 0
        
        for credentials in patient_credentials:
            patient = PatientORM.query.filter_by(patient_id=credentials['patient_id']).first()
            if patient:
                patient.email = credentials['email']
                patient.password_hash = generate_password_hash(credentials['password'])
                patient.phone = credentials['phone']
                patient.is_active = 'true'
                updated_count += 1
                print(f"✅ Updated credentials for {credentials['patient_id']}")
        
        db.session.commit()
        print(f"\n🎉 Successfully updated {updated_count} patients with login credentials!")
        
        print("\n📋 Login Credentials for Testing:")
        print("-" * 50)
        for credentials in patient_credentials:
            print(f"Email: {credentials['email']}")
            print(f"Password: {credentials['password']}")
            print(f"HMS ID: {credentials['patient_id']}")
            print("-" * 50)

if __name__ == '__main__':
    update_patient_credentials()
