import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('en_IN')

# Define constants
NUM_RECORDS = 1000
LOCALITIES = [
    'Indiranagar', 'Koramangala', 'HSR Layout', 'Marathahalli', 'Whitefield',
    'JP Nagar', 'Banashankari', 'Rajajinagar', 'Malleswaram', 'Basavanagudi',
    'Banaswadi', 'Kalyan Nagar', 'HBR Layout', 'RT Nagar', 'Hebbal',
    'Yelahanka', 'Electronic City', 'Sarjapur Road', 'Bellandur', 'MG Road',
    'Brigade Road', 'Residency Road', 'Commercial Street', 'Cunningham Road'
]

MEDICAL_CONDITIONS = [
    'Hypertension', 'Diabetes', 'Asthma', 'Heart Disease', 'Cancer - Breast',
    'Cancer - Lung', 'Arthritis', 'Chronic Back Pain', 'Migraine', 'Anxiety',
    'Depression', 'Thyroid Disorder', 'Kidney Disease', 'Liver Disease',
    'Peptic Ulcer', 'Pneumonia', 'Bronchitis', 'Skin Infection', 'Fracture',
    'Sprain', 'Dengue', 'Malaria', 'Typhoid', 'Tuberculosis', 'COVID-19',
    'Allergy', 'Eye Infection', 'Ear Infection', 'Dental Problem', 'Obesity',
    'Sleep Apnea', 'High Cholesterol', 'Stroke', 'Coronary Artery Disease',
    'Atrial Fibrillation', 'Heart Failure', 'Kidney Stones', 'Gallstones',
    'Appendicitis', 'Hemorrhoids', 'Varicose Veins', 'Psoriasis', 'Eczema',
    'Acne', 'Gout', 'Osteoporosis', 'Rheumatoid Arthritis', 'Lupus',
    'Multiple Sclerosis', 'Parkinson\'s Disease', 'Alzheimer\'s Disease',
    'Pregnancy Care', 'Postpartum Care', 'Wound Care', 'Burn Care', 'Cellulitis',
    'Abscess', 'Blood Clot', 'Anemia', 'Vitamin Deficiency', 'Dehydration',
    'Food Poisoning', 'Gastroenteritis', 'Constipation', 'Diarrhea', 'IBS',
    'IBD', 'GERD', 'Sinusitis', 'Tonsillitis', 'Pharyngitis', 'Laryngitis'
]

SEVERITIES = ['Low', 'Medium', 'High', 'Critical']
PRIORITIES = ['Routine', 'Urgent', 'Emergency', 'Life-threatening']
INSURANCE_PROVIDERS = ['Apollo Munich', 'Star Health', 'ICICI Lombard',
                       'HDFC Ergo', 'Max Bupa', 'Religare', 'None']
GENDERS = ['Male', 'Female', 'Other']


def generate_patient_record(patient_id):
    name = fake.name()
    age = random.randint(0, 95)
    gender = random.choice(GENDERS)
    locality = random.choice(LOCALITIES)
    medical_condition = random.choice(MEDICAL_CONDITIONS)
    severity = random.choice(SEVERITIES)
    priority = random.choice(PRIORITIES)

    # Generate admission/discharge dates
    admission_date = fake.date_between(start_date='-2y', end_date='today')
    discharge_date = None
    if random.random() > 0.1:  # 90% discharged
        discharge_days = random.randint(1, 30)
        discharge_date = admission_date + timedelta(days=discharge_days)
        if discharge_date > datetime.now().date():
            discharge_date = None

    # Billing
    bill_amount = round(random.uniform(500, 50000), 2)
    amount_paid = round(random.uniform(0, bill_amount), 2) if discharge_date else 0
    outstanding_amount = round(bill_amount - amount_paid, 2)
    payment_status = 'Paid' if outstanding_amount == 0 else ('Partially Paid' if amount_paid > 0 else 'Unpaid')

    insurance_coverage = random.choice(INSURANCE_PROVIDERS)
    insurance_details = f"Policy {fake.uuid4()}" if insurance_coverage != 'None' else ""

    # Timestamp for the record
    timestamp = fake.date_time_between(start_date='-2y', end_date='now').isoformat()

    return {
        'patient_id': patient_id,
        'name': name,
        'age': age,
        'gender': gender,
        'locality': locality,
        'condition_severity': severity,
        'priority_level': priority,
        'medical_history': medical_condition,
        'bill_amount': bill_amount,
        'amount_paid': amount_paid,
        'outstanding_amount': outstanding_amount,
        'payment_status': payment_status,
        'insurance_coverage': insurance_coverage,
        'insurance_details': insurance_details,
        'admission_date': admission_date.strftime('%Y-%m-%d'),
        'discharge_date': discharge_date.strftime('%Y-%m-%d') if discharge_date else '',
        'timestamp': timestamp
    }


def main():
    print(f"Generating {NUM_RECORDS} dummy patient records...")
    records = []

    for i in range(1, NUM_RECORDS + 1):
        patient_id = f"PAT{i:04d}"
        records.append(generate_patient_record(patient_id))

    # Save to CSV
    csv_filename = 'patient_records_dummy.csv'
    fieldnames = list(records[0].keys())

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Successfully generated {NUM_RECORDS} dummy records in {csv_filename}")


if __name__ == "__main__":
    main()
