import os
from flask import Flask
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created:")
    
    # Check if tables exist
    inspector = db.inspect(db.engine)
    for table_name in inspector.get_table_names():
        print(f"- {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            print(f"  - {column['name']}: {column['type']}")
    
    print("Database created successfully!")
