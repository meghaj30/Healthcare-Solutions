"""Utility script to populate hospital.db from CSV data and seed sample appointments."""
from __future__ import annotations

import random
from collections import defaultdict
from datetime import date, time, timedelta
from typing import Tuple

from app import app
from models import Appointment, Doctor, PatientORM, db
from seed_doctors import seed_doctors
from utils import load_patients_from_csv


def _normalize_patient_id(raw_id: str | None, fallback_idx: int) -> str:
    candidate = (raw_id or "").strip()
    return candidate or f"CSV-{fallback_idx:05d}"


def _patient_kwargs(patient, fallback_idx: int) -> dict:
    def to_int(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def to_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    pid = _normalize_patient_id(patient.patient_id, fallback_idx)
    return {
        "patient_id": pid,
        "name": (patient.name or "Unknown").strip() or "Unknown",
        "age": to_int(patient.age, default=0),
        "gender": (patient.gender or "Unknown").strip() or "Unknown",
        "locality": (patient.locality or "").strip(),
        "condition_severity": (patient.condition_severity or "").strip(),
        "priority_level": (patient.priority_level or "").strip(),
        "medical_history": (patient.medical_history or "").strip(),
        "bill_amount": to_float(patient.bill_amount, default=0.0),
        "amount_paid": to_float(patient.amount_paid, default=0.0),
        "outstanding_amount": to_float(patient.outstanding_amount, default=0.0),
        "payment_status": (patient.payment_status or "Unpaid").strip() or "Unpaid",
        "insurance_coverage": (patient.insurance_coverage or "No").strip() or "No",
        "insurance_details": (patient.insurance_details or "").strip(),
        "admission_date": (patient.admission_date or "").strip(),
        "discharge_date": (patient.discharge_date or None),
        "timestamp": (patient.timestamp or "").strip(),
    }


def sync_patients_from_csv() -> Tuple[int, int, int]:
    csv_patients = load_patients_from_csv()
    if not csv_patients:
        return 0, 0, 0

    existing = {patient.patient_id: patient for patient in PatientORM.query.all()}
    created = updated = 0

    for idx, csv_patient in enumerate(csv_patients, start=1):
        kwargs = _patient_kwargs(csv_patient, idx)
        patient_id = kwargs["patient_id"]
        orm_patient = existing.get(patient_id)

        if orm_patient:
            for field, value in kwargs.items():
                setattr(orm_patient, field, value)
            updated += 1
        else:
            db.session.add(PatientORM(**kwargs))
            created += 1

    db.session.commit()
    return created, updated, len(csv_patients)


def ensure_sample_appointments(target_patients: int = 150) -> int:
    doctors = Doctor.query.all()
    if not doctors:
        return 0

    patients_without_appt = (
        PatientORM.query.filter(~PatientORM.appointments.any())
        .order_by(PatientORM.timestamp.desc())
        .limit(target_patients)
        .all()
    )

    if not patients_without_appt:
        return 0

    queue_tracker = defaultdict(int)
    created = 0

    for patient in patients_without_appt:
        doctor = random.choice(doctors)
        appt_date = date.today() + timedelta(days=random.randint(0, 14))
        appt_time = time(hour=random.randint(9, 16), minute=random.choice([0, 15, 30, 45]))

        queue_key = (doctor.doctor_id, appt_date)
        queue_tracker[queue_key] += 1

        appointment = Appointment(
            patient_id=patient.patient_id,
            doctor_id=doctor.doctor_id,
            department=doctor.department or "General",
            symptoms=(patient.medical_history or "General consultation")[:200],
            appointment_date=appt_date,
            appointment_time=appt_time,
            queue_number=queue_tracker[queue_key],
            status=random.choice(["Pending", "Confirmed"]),
        )
        db.session.add(appointment)
        created += 1

    db.session.commit()
    return created


def populate_database():
    with app.app_context():
        db.create_all()

    # Seed doctors (clears existing doctor data each run)
    seed_doctors()

    with app.app_context():
        created, updated, total = sync_patients_from_csv()
        appointments_created = ensure_sample_appointments()

        print(f"Patients in CSV: {total}")
        print(f"Patients created: {created}")
        print(f"Patients updated: {updated}")
        print(f"Sample appointments created: {appointments_created}")


if __name__ == "__main__":
    populate_database()
