from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Time, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class PatientORM(db.Model):
    __tablename__ = 'patients'
    patient_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    locality = Column(String(100))
    condition_severity = Column(String(50))
    priority_level = Column(String(50))
    medical_history = Column(Text)
    bill_amount = Column(Float)
    amount_paid = Column(Float)
    outstanding_amount = Column(Float)
    payment_status = Column(String(32))
    insurance_coverage = Column(String(50))
    insurance_details = Column(Text)
    admission_date = Column(String(32))
    discharge_date = Column(String(32))
    timestamp = Column(String(32))
    # Authentication fields
    email = Column(String(100), unique=True)
    password_hash = Column(String(255))
    phone = Column(String(20))
    is_active = Column(String(10), default='true')
    last_login = Column(DateTime)

    appointments = relationship("Appointment", back_populates="patient")

class Doctor(db.Model):
    __tablename__ = 'doctors'
    doctor_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    department = Column(String(100))
    specialization = Column(String(100))
    qualification = Column(String(200))
    experience_years = Column(Integer)
    consultation_fee = Column(Float)
    availability_days = Column(String(50))  # CSV string like "Mon,Tue,Wed"
    availability_time = Column(String(50))  # CSV or range string like "10:00-14:00"
    about = Column(Text)

    appointments = relationship("Appointment", back_populates="doctor")

class Appointment(db.Model):
    __tablename__ = 'appointments'
    appointment_id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.doctor_id'), nullable=False)
    department = Column(String(100), nullable=False)
    symptoms = Column(Text)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    queue_number = Column(Integer, nullable=False)
    status = Column(String(20), default='Pending')
    consultation_type = Column(String(20), default='In-Person')  # 'In-Person' or 'Video'
    video_room_id = Column(String(100))  # Unique room ID for video consultation
    video_link = Column(String(500))  # Video consultation link
    video_enabled = Column(String(10), default='false')  # 'true' or 'false'
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("PatientORM", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    locality: str
    condition_severity: str
    priority_level: str
    medical_history: str
    bill_amount: float
    amount_paid: float
    outstanding_amount: float
    payment_status: str
    insurance_coverage: str
    insurance_details: str
    admission_date: str
    discharge_date: Optional[str] = None
    timestamp: Optional[str] = None
    
    @property
    def is_emergency(self) -> bool:
        """Check if patient is an emergency case (High severity, no discharge date)"""
        return (self.condition_severity == 'Critical' or self.condition_severity == 'High') and not self.discharge_date

class Resource(db.Model):
    __tablename__ = 'resources'
    resource_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # 'Medicine', 'Equipment', 'Supplies'
    description = Column(Text)
    current_stock = Column(Integer, nullable=False)
    minimum_stock = Column(Integer, nullable=False)
    maximum_stock = Column(Integer, nullable=False)
    unit = Column(String(20), nullable=False)  # 'units', 'boxes', 'liters', etc.
    location = Column(String(100))
    supplier = Column(String(100))
    last_restocked = Column(DateTime)
    expiry_date = Column(Date)  # For medicines
    cost_per_unit = Column(Float)
    status = Column(String(20), default='Available')  # 'Available', 'Low Stock', 'Out of Stock', 'Expired'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ResourceTransaction(db.Model):
    __tablename__ = 'resource_transactions'
    transaction_id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.resource_id'), nullable=False)
    transaction_type = Column(String(20), nullable=False)  # 'Stock In', 'Stock Out', 'Used', 'Expired'
    quantity = Column(Integer, nullable=False)
    remaining_stock = Column(Integer, nullable=False)
    reason = Column(Text)
    performed_by = Column(String(100))  # Staff member who performed the transaction
    transaction_date = Column(DateTime, default=datetime.utcnow)
    
    resource = relationship("Resource", backref="transactions")

@dataclass
class EmergencyCase:
    patient_id: str
    name: str
    condition: str
    priority: str
    priority_level: int
    priority_name: str
    time_added: str
    formatted_time: str

@dataclass
class ReportData:
    title: str
    generated_at: str
    total_patients: int
    total_billed: float
    total_paid: float
    total_outstanding: float
    collection_rate: float
    data: list

@dataclass
class MLInsights:
    visit_predictions: dict
    disease_predictions: dict
