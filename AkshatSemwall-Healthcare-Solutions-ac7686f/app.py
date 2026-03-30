import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db  # import SQLAlchemy instance

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///hospital.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Import blueprints
from patient_routes import patient_bp
from doctor_routes import doctor_bp
from appointment_routes import appointment_bp
from admin_routes import admin_bp
from patient_auth import patient_auth_bp
from resource_management import resource_bp
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(patient_auth_bp)
app.register_blueprint(resource_bp)

# Import routes after app creation to avoid circular imports
from routes import *
from emergency import *
from billing import *
from ml_insights import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
