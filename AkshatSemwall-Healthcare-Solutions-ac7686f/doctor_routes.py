from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Doctor, Appointment, PatientORM
from datetime import date

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        doctor = Doctor.query.filter(Doctor.name.ilike(name)).first()
        if doctor:
            session['doctor_id'] = doctor.doctor_id
            flash('Logged in as ' + doctor.name, 'success')
            return redirect(url_for('doctor.doctor_dashboard'))
        else:
            flash('Doctor not found. Please enter your correct name.', 'danger')
    return render_template('doctor_login.html')

@doctor_bp.route('/doctor/logout')
def doctor_logout():
    session.pop('doctor_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('doctor.doctor_login'))

@doctor_bp.route('/doctor/dashboard')
def doctor_dashboard():
    doctor_id = session.get('doctor_id')
    if not doctor_id:
        flash('Please log in as doctor.', 'danger')
        return redirect(url_for('doctor.doctor_login'))
    doctor = Doctor.query.get(doctor_id)
    today = date.today()
    
    # Get all appointments for this doctor (today and future)
    all_appointments = Appointment.query.filter_by(doctor_id=doctor_id).filter(Appointment.appointment_date >= today).order_by(Appointment.appointment_date.asc(), Appointment.appointment_time.asc(), Appointment.queue_number.asc()).all()
    
    # Also get recent past appointments for reference
    past_appointments = Appointment.query.filter_by(doctor_id=doctor_id).filter(Appointment.appointment_date < today).order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).limit(5).all()
    
    # Separate today's appointments and upcoming appointments
    todays_appointments = [apt for apt in all_appointments if apt.appointment_date == today]
    upcoming_appointments = [apt for apt in all_appointments if apt.appointment_date > today]
    
    return render_template('doctor_dashboard.html', 
                         doctor=doctor, 
                         todays_appointments=todays_appointments,
                         upcoming_appointments=upcoming_appointments,
                         past_appointments=past_appointments,
                         all_appointments=all_appointments)

@doctor_bp.route('/doctor/appointment/<int:appointment_id>/update_status', methods=['GET', 'POST'])
def update_appointment_status(appointment_id):
    doctor_id = session.get('doctor_id')
    if not doctor_id:
        flash('Please log in as doctor.', 'danger')
        return redirect(url_for('doctor.doctor_login'))
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.doctor_id != doctor_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('doctor.doctor_dashboard'))
    if request.method == 'POST':
        status = request.form.get('status')
        if status in ['Pending', 'Confirmed', 'Ongoing', 'Completed', 'Cancelled']:
            appointment.status = status
            db.session.commit()
            flash('Status updated.', 'success')
            return redirect(url_for('doctor.doctor_dashboard'))
        else:
            flash('Invalid status.', 'danger')
    return render_template('update_appointment_status.html', appointment=appointment)

@doctor_bp.route('/doctor/patient/<patient_id>')
def view_patient_details(patient_id):
    doctor_id = session.get('doctor_id')
    if not doctor_id:
        flash('Please log in as doctor.', 'danger')
        return redirect(url_for('doctor.doctor_login'))
    patient = PatientORM.query.filter_by(patient_id=patient_id).first_or_404()
    return render_template('patient_detail.html', patient=patient, doctor_view=True)
