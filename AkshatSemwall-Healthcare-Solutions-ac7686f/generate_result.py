
import pandas as pd
import json

data = {
    'status': 'success',
    'rows': 1000,
    'columns': ['patient_id', 'name', 'age', 'gender', 'locality', 'condition_severity', 
                'priority_level', 'medical_history', 'bill_amount', 'amount_paid', 
                'outstanding_amount', 'payment_status', 'insurance_coverage', 
                'insurance_details', 'admission_date', 'discharge_date', 'timestamp']
}

with open('result.json', 'w') as f:
    json.dump(data, f, indent=2)
