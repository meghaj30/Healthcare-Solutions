import os
import shutil

src = 'patient_records_dummy.csv'
dst = 'patient_records_with_timestamp.csv'

print(f"Checking {src} exists: {os.path.exists(src)}")

if os.path.exists(src):
    shutil.copyfile(src, dst)
    print(f"Copied {src} to {dst}")
