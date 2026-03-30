from app import app
from models import db

with app.app_context():
    # Drop all existing tables
    db.drop_all()
    # Create all tables with new schema
    db.create_all()
    print("Database initialized successfully!")
