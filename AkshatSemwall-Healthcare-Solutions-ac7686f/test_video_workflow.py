#!/usr/bin/env python3
"""
Test script to verify the video consultation workflow
"""

from app import app
from models import db, Appointment, PatientORM, Doctor
from datetime import datetime, date, time
import uuid

def test_video_workflow():
    """Test the complete video consultation workflow"""
    
    with app.app_context():
        print("🔍 Testing Video Consultation Workflow...")
        print("=" * 50)
        
        # 1. Check if doctors exist
        doctors = Doctor.query.all()
        print(f"✅ Found {len(doctors)} doctors in database")
        
        # 2. Check if patients exist
        patients = PatientORM.query.all()
        print(f"✅ Found {len(patients)} patients in database")
        
        if not doctors or not patients:
            print("❌ No doctors or patients found. Please add some first.")
            return
        
        # 3. Create a test video appointment
        test_appointment = Appointment(
            patient_id=patients[0].patient_id,
            doctor_id=doctors[0].doctor_id,
            department=doctors[0].department,
            symptoms="Test video consultation",
            appointment_date=date.today(),
            appointment_time=time(14, 30),
            queue_number=1,
            consultation_type="Video",
            video_enabled="true",
            video_room_id=str(uuid.uuid4()),
            video_link=f"/video_consultation/{uuid.uuid4()}",
            status="Confirmed"
        )
        
        db.session.add(test_appointment)
        db.session.commit()
        
        print(f"✅ Created test video appointment (ID: {test_appointment.appointment_id})")
        print(f"   - Patient: {test_appointment.patient_id}")
        print(f"   - Doctor: Dr. {test_appointment.doctor.name}")
        print(f"   - Type: {test_appointment.consultation_type}")
        print(f"   - Video Room: {test_appointment.video_room_id}")
        print(f"   - Status: {test_appointment.status}")
        
        # 4. Test video consultation URL generation
        video_url = test_appointment.video_link
        print(f"✅ Video consultation URL: {video_url}")
        
        # 5. Verify database schema
        print("\n🔍 Verifying database schema...")
        appointment_columns = [column.name for column in Appointment.__table__.columns]
        required_columns = ['consultation_type', 'video_room_id', 'video_link', 'video_enabled']
        
        for column in required_columns:
            if column in appointment_columns:
                print(f"✅ Column '{column}' exists")
            else:
                print(f"❌ Column '{column}' missing")
        
        print("\n🎉 Video consultation workflow test completed!")
        print("\n📋 Manual Testing Steps:")
        print("1. Open http://localhost:5000 in browser")
        print("2. Click 'Appointments' in navigation")
        print("3. Click 'Book New Appointment'")
        print("4. Select 'Video Consultation' type")
        print("5. Fill form and submit")
        print("6. Accept the appointment")
        print("7. Click 'Join Video Call' button")
        print("8. Test webcam and microphone functionality")

if __name__ == '__main__':
    test_video_workflow()
