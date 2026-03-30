from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, PatientORM, Appointment
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import uuid

patient_auth_bp = Blueprint('patient_auth', __name__)

@patient_auth_bp.route('/patient/login', methods=['GET', 'POST'])
def patient_login():
    """Patient login portal"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        patient_id = request.form.get('patient_id', '').strip()
        
        # Try to find patient by email or patient_id
        patient = None
        if email:
            patient = PatientORM.query.filter_by(email=email).first()
        elif patient_id:
            patient = PatientORM.query.filter_by(patient_id=patient_id).first()
        
        if patient and patient.is_active == 'true':
            # For demo purposes, use patient_id as password (in production, use proper password)
            if password == patient.patient_id or check_password_hash(patient.password_hash, password):
                session['patient_logged_in'] = True
                session['patient_id'] = patient.patient_id
                session['patient_name'] = patient.name
                
                # Update last login
                patient.last_login = datetime.utcnow()
                db.session.commit()
                
                flash(f'Welcome back, {patient.name}!', 'success')
                return redirect(url_for('patient_auth.patient_dashboard'))
            else:
                flash('Invalid credentials. Please try again.', 'error')
        else:
            flash('Patient not found or account inactive.', 'error')
    
    return render_template('patient_login.html')

@patient_auth_bp.route('/patient/register', methods=['GET', 'POST'])
def patient_register():
    """Patient registration with login credentials"""
    if request.method == 'POST':
        patient_id = request.form.get('patient_id', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Check if patient exists
        patient = PatientORM.query.filter_by(patient_id=patient_id).first()
        if not patient:
            flash('Patient ID not found. Please register with the hospital first.', 'error')
            return redirect(url_for('patient_auth.patient_register'))
        
        # Check if email already registered
        if PatientORM.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('patient_auth.patient_register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('patient_auth.patient_register'))
        
        # Update patient with login credentials
        patient.email = email
        patient.password_hash = generate_password_hash(password)
        patient.is_active = 'true'
        db.session.commit()
        
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('patient_auth.patient_login'))
    
    return render_template('patient_register.html')

@patient_auth_bp.route('/patient/dashboard')
def patient_dashboard():
    """Patient dashboard with appointments and notifications"""
    if not session.get('patient_logged_in'):
        flash('Please login to access your dashboard.', 'error')
        return redirect(url_for('patient_auth.patient_login'))
    
    patient_id = session.get('patient_id')
    patient = PatientORM.query.get(patient_id)
    
    if not patient:
        session.clear()
        flash('Patient not found. Please login again.', 'error')
        return redirect(url_for('patient_auth.patient_login'))
    
    # Get patient's appointments
    appointments = Appointment.query.filter_by(patient_id=patient_id)\
                                 .order_by(Appointment.created_at.desc()).all()
    
    # Separate confirmed and pending appointments
    confirmed_appointments = [apt for apt in appointments if apt.status == 'Confirmed']
    pending_appointments = [apt for apt in appointments if apt.status == 'Pending']
    
    return render_template('patient_dashboard.html', 
                         patient=patient,
                         appointments=appointments,
                         confirmed_appointments=confirmed_appointments,
                         pending_appointments=pending_appointments)

@patient_auth_bp.route('/patient/logout')
def patient_logout():
    """Patient logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('patient_auth.patient_login'))

@patient_auth_bp.route('/patient/appointments')
def patient_appointments():
    """View patient's appointments"""
    if not session.get('patient_logged_in'):
        return redirect(url_for('patient_auth.patient_login'))
    
    patient_id = session.get('patient_id')
    appointments = Appointment.query.filter_by(patient_id=patient_id)\
                                 .order_by(Appointment.created_at.desc()).all()
    
    return render_template('patient_appointments.html', appointments=appointments)

@patient_auth_bp.route('/patient/video_call/<room_id>')
def patient_video_call(room_id):
    """Patient video consultation room"""
    if not session.get('patient_logged_in'):
        flash('Please login to access video consultation.', 'error')
        return redirect(url_for('patient_auth.patient_login'))
    
    # Find appointment by room ID
    appointment = Appointment.query.filter_by(video_room_id=room_id).first()
    if not appointment:
        flash('Invalid consultation room.', 'error')
        return redirect(url_for('patient_auth.patient_dashboard'))
    
    # Verify this appointment belongs to the logged-in patient
    if appointment.patient_id != session.get('patient_id'):
        flash('Unauthorized access.', 'error')
        return redirect(url_for('patient_auth.patient_dashboard'))
    
    # Get patient and doctor details
    patient = PatientORM.query.get(appointment.patient_id)
    doctor = appointment.doctor
    
    return render_template('patient_video_consultation.html', 
                         appointment=appointment, 
                         patient=patient, 
                         doctor=doctor)

@patient_auth_bp.route('/patient/check_notifications')
def check_notifications():
    """Check for new appointment confirmations (AJAX endpoint)"""
    if not session.get('patient_logged_in'):
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    patient_id = session.get('patient_id')
    
    # Check for recently confirmed appointments (within last 5 minutes)
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    recent_confirmations = Appointment.query.filter(
        Appointment.patient_id == patient_id,
        Appointment.status == 'Confirmed',
        Appointment.updated_at >= five_minutes_ago
    ).all()
    
    notifications = []
    for apt in recent_confirmations:
        notifications.append({
            'id': apt.appointment_id,
            'message': f'Appointment with Dr. {apt.doctor.name} has been confirmed!',
            'video_link': apt.video_link if apt.consultation_type == 'Video' else None,
            'time': apt.updated_at.strftime('%H:%M')
        })
    
    return jsonify({'status': 'success', 'notifications': notifications})
