# generate_data.py
import mysql.connector
import random
from datetime import datetime, timedelta

# Connect to MySQL (CHANGE password if needed)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your password",  # CHANGE THIS
    database="pharmacy_optimizer"
)
cursor = conn.cursor()

# List of drugs
drugs = ['Paracetamol 500mg', 'Amoxicillin 250mg', 'Crocin', 'Dolo 650', 'Metformin']
start_date = datetime(2025, 1, 1)

print("Adding 50 records...")

for i in range(50):
    drug = random.choice(drugs)
    qty = random.randint(10, 50)
    days_offset = random.randint(0, 365)
    date = start_date + timedelta(days=days_offset)
    store = random.randint(1, 3)

    cursor.execute(
        "INSERT INTO sales (drug_name, quantity_sold, sale_date, store_id) VALUES (%s, %s, %s, %s)",
        (drug, qty, date.date(), store)
    )

conn.commit()
conn.close()
print("50 records added successfully!")
