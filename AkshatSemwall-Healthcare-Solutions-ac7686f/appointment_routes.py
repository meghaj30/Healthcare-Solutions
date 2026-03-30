from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Appointment, PatientORM, Doctor
from datetime import datetime, date, time
import uuid

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    """Book a new appointment"""
    if request.method == 'POST':
        try:
            # Extract form data
            patient_id = request.form.get('patient_id')
            doctor_id = request.form.get('doctor_id')
            department = request.form.get('department')
            symptoms = request.form.get('symptoms', '')
            appointment_date = datetime.strptime(request.form.get('appointment_date'), '%Y-%m-%d').date()
            appointment_time = datetime.strptime(request.form.get('appointment_time'), '%H:%M').time()
            consultation_type = request.form.get('consultation_type', 'In-Person')
            
            # Generate queue number (simplified)
            queue_number = 1
            
            # Create appointment
            appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                department=department,
                symptoms=symptoms,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                queue_number=queue_number,
                consultation_type=consultation_type,
                video_enabled='true' if consultation_type == 'Video' else 'false'
            )
            
            # Generate video room ID if video consultation
            if consultation_type == 'Video':
                appointment.video_room_id = str(uuid.uuid4())
                appointment.video_link = f"/video_consultation/{appointment.video_room_id}"
            
            db.session.add(appointment)
            db.session.commit()
            
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('appointment.my_appointments'))
            
        except Exception as e:
            flash(f'Error booking appointment: {str(e)}', 'error')
            return redirect(url_for('appointment.book_appointment'))
    
    # GET request - show booking form
    doctors = Doctor.query.all()
    patients = PatientORM.query.all()
    return render_template('book_appointment.html', doctors=doctors, patients=patients)

@appointment_bp.route('/my_appointments')
def my_appointments():
    """View appointments for current user"""
    # This would typically filter by current user ID
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    return render_template('appointments_list.html', appointments=appointments)

@appointment_bp.route('/appointment/<int:appointment_id>')
def view_appointment(appointment_id):
    """View appointment details"""
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('appointment_detail.html', appointment=appointment)

@appointment_bp.route('/accept_appointment/<int:appointment_id>', methods=['POST'])
def accept_appointment(appointment_id):
    """Accept an appointment (doctor action)"""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        appointment.status = 'Confirmed'
        
        # Generate video link if video consultation
        if appointment.consultation_type == 'Video' and not appointment.video_room_id:
            appointment.video_room_id = str(uuid.uuid4())
            appointment.video_link = f"/video_consultation/{appointment.video_room_id}"
        
        db.session.commit()
        flash('Appointment accepted successfully!', 'success')
        return redirect(url_for('appointment.view_appointment', appointment_id=appointment_id))
        
    except Exception as e:
        flash(f'Error accepting appointment: {str(e)}', 'error')
        return redirect(url_for('appointment.my_appointments'))

@appointment_bp.route('/video_consultation/<room_id>')
def video_consultation(room_id):
    """Video consultation room"""
    # Find appointment by room ID
    appointment = Appointment.query.filter_by(video_room_id=room_id).first_or_404()
    
    # Get patient and doctor details
    patient = PatientORM.query.get(appointment.patient_id)
    doctor = Doctor.query.get(appointment.doctor_id)
    
    # Check if appointment is confirmed
    if appointment.status != 'Confirmed':
        flash('Video consultation is only available for confirmed appointments.', 'error')
        return redirect(url_for('appointment.view_appointment', appointment_id=appointment.appointment_id))
    
    return render_template('video_consultation.html', 
                         appointment=appointment, 
                         patient=patient, 
                         doctor=doctor)

@appointment_bp.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        appointment.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled successfully!', 'success')
        return redirect(url_for('appointment.my_appointments'))
        
    except Exception as e:
        flash(f'Error cancelling appointment: {str(e)}', 'error')
        return redirect(url_for('appointment.my_appointments'))
