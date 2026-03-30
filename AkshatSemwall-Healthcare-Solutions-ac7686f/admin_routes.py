from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Doctor

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/doctors')
def manage_doctors():
    doctors = Doctor.query.order_by(Doctor.department).all()
    return render_template('manage_doctors.html', doctors=doctors)

@admin_bp.route('/admin/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        form = request.form
        doc = Doctor(
            name=form.get('name'),
            age=form.get('age'),
            gender=form.get('gender'),
            department=form.get('department'),
            specialization=form.get('specialization'),
            qualification=form.get('qualification'),
            experience_years=form.get('experience_years'),
            consultation_fee=form.get('consultation_fee'),
            availability_days=form.get('availability_days'),
            availability_time=form.get('availability_time'),
            about=form.get('about')
        )
        db.session.add(doc)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))
    return render_template('edit_doctor.html', edit_mode=False, doctor=None)

@admin_bp.route('/admin/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        form = request.form
        doctor.name = form.get('name')
        doctor.age = form.get('age')
        doctor.gender = form.get('gender')
        doctor.department = form.get('department')
        doctor.specialization = form.get('specialization')
        doctor.qualification = form.get('qualification')
        doctor.experience_years = form.get('experience_years')
        doctor.consultation_fee = form.get('consultation_fee')
        doctor.availability_days = form.get('availability_days')
        doctor.availability_time = form.get('availability_time')
        doctor.about = form.get('about')
        db.session.commit()
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))
    return render_template('edit_doctor.html', edit_mode=True, doctor=doctor)

@admin_bp.route('/admin/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted.', 'warning')
    return redirect(url_for('admin.manage_doctors'))
