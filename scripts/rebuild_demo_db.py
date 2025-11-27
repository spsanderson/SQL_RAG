import rdata
import pandas as pd
import sqlite3
import os
import random
import string
from datetime import datetime, timedelta

try:
    from faker import Faker
    fake = Faker()
    HAS_FAKER = True
except ImportError:
    HAS_FAKER = False
    print("Faker not found, using simple random data generation.")

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_demographics(num_patients):
    data = []
    for i in range(num_patients):
        if HAS_FAKER:
            first_name = fake.first_name()
            last_name = fake.last_name()
            dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
            gender = random.choice(['M', 'F'])
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        else:
            first_name = f"Patient{i}"
            last_name = generate_random_string()
            dob = datetime(1980, 1, 1).date()
            gender = random.choice(['M', 'F'])
            email = f"patient{i}@example.com"
            
        data.append({
            "FirstName": first_name,
            "LastName": last_name,
            "DateOfBirth": dob,
            "Gender": gender,
            "Email": email
        })
    return pd.DataFrame(data)

def rebuild_database(db_path, rda_path):
    print(f"Loading data from {rda_path}...")
    if not os.path.exists(rda_path):
        print(f"Error: File not found: {rda_path}")
        return

    parsed = rdata.parser.parse_file(rda_path)
    converted = rdata.conversion.convert(parsed)
    df_name = list(converted.keys())[0]
    raw_df = converted[df_name]
    
    # Clean column names
    raw_df.columns = [c.replace('.', '_') for c in raw_df.columns]
    print(f"Loaded {len(raw_df)} rows from R data.")

    # 1. Create Patients Table
    print("Creating Patients table...")
    unique_mrns = raw_df['mrn'].unique()
    patients_df = pd.DataFrame({'mrn': unique_mrns})
    patients_df['PatientID'] = range(1, len(patients_df) + 1)
    
    # Generate demographics
    demographics_df = generate_demographics(len(patients_df))
    patients_df = pd.concat([patients_df, demographics_df], axis=1)
    
    # 2. Create Visits Table
    print("Creating Visits table...")
    # Map MRN to PatientID for visits
    visits_df = raw_df[['visit_id', 'mrn', 'visit_start_date_time']].copy()
    visits_df = visits_df.merge(patients_df[['mrn', 'PatientID']], on='mrn', how='left')
    
    visits_df['VisitID'] = range(1, len(visits_df) + 1)
    visits_df.rename(columns={'visit_start_date_time': 'VisitDate'}, inplace=True)
    
    # Add dummy Reason/Diagnosis if not present
    visits_df['Reason'] = 'Routine Checkup'
    visits_df['Diagnosis'] = 'General Observation'
    
    # Select final columns for Visits
    visits_final = visits_df[['VisitID', 'PatientID', 'VisitDate', 'Reason', 'Diagnosis']]
    
    # 3. Update healthyR_data Table
    print("Updating healthyR_data table...")
    healthyr_final = raw_df.merge(patients_df[['mrn', 'PatientID']], on='mrn', how='left')
    
    # 4. Write to Database
    print(f"Writing to {db_path}...")
    conn = sqlite3.connect(db_path)
    
    # Patients (exclude mrn from schema if strictly following previous schema, 
    # but keeping it might be useful. The prompt asked to link by mrn AND PatientID, 
    # so we should probably keep mrn in Patients or just use PatientID as the link.
    # Standard practice: PatientID is PK, MRN is a field in Patients.
    # The user said "link together by mrn and PatientID". 
    # I will keep MRN in Patients table.)
    patients_df.to_sql('Patients', conn, if_exists='replace', index=False)
    
    visits_final.to_sql('Visits', conn, if_exists='replace', index=False)
    
    healthyr_final.to_sql('healthyR_data', conn, if_exists='replace', index=False)
    
    # Create Indices
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_patients_mrn ON Patients(mrn)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_visits_patientid ON Visits(PatientID)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_healthyr_patientid ON healthyR_data(PatientID)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_healthyr_mrn ON healthyR_data(mrn)")
    
    conn.commit()
    conn.close()
    print("Database rebuild complete.")

if __name__ == "__main__":
    rebuild_database("demo.db", "data/healthyR_data.rda")
