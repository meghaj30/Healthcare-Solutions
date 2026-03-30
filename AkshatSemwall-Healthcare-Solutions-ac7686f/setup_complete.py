from app import app
from models import db, Doctor
from seed_doctors import seed_doctors

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully!")
    
    print("Seeding doctors...")
    seed_doctors()
    print("Database setup complete!")
    
    # Verify doctors are added
    doctors = Doctor.query.all()
    print(f"Total doctors in database: {len(doctors)}")
    for doctor in doctors[:3]:
        print(f"- Dr. {doctor.name} ({doctor.department})")
