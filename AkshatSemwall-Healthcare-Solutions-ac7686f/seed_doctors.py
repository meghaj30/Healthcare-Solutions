from app import app
from models import db, Doctor

def seed_doctors():
    doctors = [
        Doctor(name="Dr. Aarav Sharma", age=45, gender="Male", department="Cardiology", specialization="Cardiologist", qualification="MD, DM (Cardiology)", experience_years=20, consultation_fee=1000, availability_days="Mon,Wed,Fri", availability_time="10:00-13:00", about="Expert in cardiac care, critical cardiac emergencies, preventive cardiology."),
        Doctor(name="Dr. Meera Iyer", age=50, gender="Female", department="Neurology", specialization="Neurologist", qualification="MD, DM (Neurology)", experience_years=22, consultation_fee=1200, availability_days="Tue,Thu,Sat", availability_time="09:00-12:00", about="Renowned for treating strokes, epilepsy, Parkinson's, and neurodegenerative disorders."),
        Doctor(name="Dr. Rahul Verma", age=42, gender="Male", department="Orthopedics", specialization="Orthopedic Surgeon", qualification="MS (Ortho)", experience_years=17, consultation_fee=900, availability_days="Mon,Tue,Fri", availability_time="14:00-17:00", about="Specialist in joint replacement, trauma, sports injuries."),
        Doctor(name="Dr. Sunita Mishra", age=39, gender="Female", department="Pediatrics", specialization="Pediatrician", qualification="MD (Pediatrics)", experience_years=14, consultation_fee=700, availability_days="Wed,Thu,Sat", availability_time="11:00-16:00", about="Child health, vaccinations, neonatology and adolescent care."),
        Doctor(name="Dr. Arjun Gupta", age=36, gender="Male", department="General Medicine", specialization="Physician", qualification="MD (General Medicine)", experience_years=10, consultation_fee=600, availability_days="Mon-Sat", availability_time="09:00-11:00", about="Internal medicine, diabetes, hypertension, fever management."),
        Doctor(name="Dr. Aparna Sethi", age=41, gender="Female", department="Dermatology", specialization="Dermatologist", qualification="MD (Dermatology)", experience_years=15, consultation_fee=800, availability_days="Tue,Fri,Sat", availability_time="12:00-15:00", about="Expert in skin allergies, acne, cosmetic dermatology."),
        Doctor(name="Dr. Praveen Rao", age=48, gender="Male", department="ENT", specialization="ENT Specialist", qualification="MS (ENT)", experience_years=19, consultation_fee=900, availability_days="Mon,Wed,Thu", availability_time="10:00-13:30", about="Ear, nose, throat surgeries, hearing loss, sinusitis."),
        Doctor(name="Dr. Kavita Joshi", age=46, gender="Female", department="Oncology", specialization="Oncologist", qualification="MD, DM (Oncology)", experience_years=21, consultation_fee=1500, availability_days="Fri,Sat", availability_time="15:00-18:00", about="All types of cancer therapy, palliative care, chemotherapy."),
    ]
    with app.app_context():
        db.create_all()  # Ensure tables exist
        db.session.query(Doctor).delete()  # Clear if already seeded
        db.session.bulk_save_objects(doctors)
        db.session.commit()
        print("Seeded sample doctors.")

if __name__ == "__main__":
    seed_doctors()
