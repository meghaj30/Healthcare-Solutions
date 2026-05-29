
import pandas as pd

print("Testing pandas read...")
df = pd.read_csv("patient_records_dummy.csv")
print(f"Loaded data has", len(df), "rows")

print("\nData columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
