from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Doctor, Appointment, PatientORM
from datetime import datetime, time
from utils import load_patients_from_csv

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/departments')
def departments():
    departments = db.session.query(Doctor.department).distinct().all()
    departments = [d[0] for d in departments]
    return render_template('departments.html', departments=departments)

@patient_bp.route('/doctors/<department>')
def doctors_by_department(department):
    doctors = Doctor.query.filter_by(department=department).all()
    return render_template('doctors.html', doctors=doctors, department=department)

@patient_bp.route('/doctor/<int:doctor_id>')
def doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('doctor_profile.html', doctor=doctor)

@patient_bp.route('/book_appointment/<int:doctor_id>', methods=['GET', 'POST'])
def book_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        form = request.form
        patient_id = form.get('patient_id', '').strip()
        symptoms = form.get('symptoms', '').strip()
        appointment_date = form.get('appointment_date', '').strip()
        appointment_time = form.get('appointment_time', '').strip()

        if not all([patient_id, symptoms, appointment_date, appointment_time]):
            flash('All fields are required.', 'danger')
            return render_template('book_appointment.html', doctor=doctor)
        
        # First check database for patient
        patient = PatientORM.query.filter_by(patient_id=patient_id).first()
        
        # If not found in database, check CSV file
        if not patient:
            patients_from_csv = load_patients_from_csv()
            csv_patient = next((p for p in patients_from_csv if p.patient_id == patient_id), None)
            if csv_patient:
                # Create patient in database from CSV data
                patient = PatientORM(
                    patient_id=patient_id,
                    name=csv_patient.name,
                    age=csv_patient.age,
                    gender=csv_patient.gender,
                    locality=csv_patient.locality,
                    condition_severity=csv_patient.condition_severity,
                    priority_level=csv_patient.priority_level,
                    medical_history=csv_patient.medical_history,
                    bill_amount=csv_patient.bill_amount,
                    amount_paid=csv_patient.amount_paid,
                    outstanding_amount=csv_patient.outstanding_amount,
                    payment_status=csv_patient.payment_status,
                    insurance_coverage=csv_patient.insurance_coverage,
                    insurance_details=csv_patient.insurance_details,
                    admission_date=csv_patient.admission_date,
                    discharge_date=csv_patient.discharge_date,
                    timestamp=csv_patient.timestamp
                )
                db.session.add(patient)
                db.session.commit()
        
        if not patient:
            flash('Patient ID not found.', 'danger')
            return render_template('book_appointment.html', doctor=doctor)
        date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        time_obj = datetime.strptime(appointment_time, '%H:%M').time()
        same_day_appointments = Appointment.query.filter_by(doctor_id=doctor_id, appointment_date=date_obj).all()
        queue_number = 1 + max([a.queue_number for a in same_day_appointments], default=0)
        new_appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            department=doctor.department,
            symptoms=symptoms,
            appointment_date=date_obj,
            appointment_time=time_obj,
            queue_number=queue_number,
            status='Pending'
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient.my_appointments', patient_id=patient_id))
    return render_template('book_appointment.html', doctor=doctor)

@patient_bp.route('/patient/appointments')
def my_appointments():
    patient_id = request.args.get('patient_id', '').strip()
    appointments = []
    if patient_id:
        appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.appointment_date.desc(), Appointment.queue_number.asc()).all()
    return render_template('my_appointments.html', appointments=appointments, patient_id=patient_id)

@patient_bp.route('/patient/appointment/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    patient_id = request.args.get('patient_id', '')
    if appt.status in ['Pending', 'Confirmed']:
        appt.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled.', 'warning')
    else:
        flash('Appointment cannot be cancelled.', 'danger')
    return redirect(url_for('patient.my_appointments', patient_id=appt.patient_id))
