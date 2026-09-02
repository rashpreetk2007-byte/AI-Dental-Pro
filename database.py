import sqlite3
from datetime import datetime

DB_NAME = "dental_clinic.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE,
            full_name TEXT NOT NULL,
            date_of_birth TEXT,
            gender TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            emergency_contact TEXT,
            allergies TEXT,
            dental_history TEXT,
            medical_history TEXT,
            treatment_history TEXT,
            prescription_notes TEXT,
            xray_notes TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def generate_patient_id():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]

    conn.close()

    return f"DP{1001 + count}"


def add_patient(
    full_name,
    date_of_birth,
    gender,
    phone,
    email,
    address,
    emergency_contact,
    allergies,
    dental_history,
    medical_history,
    treatment_history,
    prescription_notes,
    xray_notes
):
    conn = get_connection()
    cursor = conn.cursor()

    patient_id = generate_patient_id()

    cursor.execute("""
        INSERT INTO patients (
            patient_id,
            full_name,
            date_of_birth,
            gender,
            phone,
            email,
            address,
            emergency_contact,
            allergies,
            dental_history,
            medical_history,
            treatment_history,
            prescription_notes,
            xray_notes,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        full_name,
        date_of_birth,
        gender,
        phone,
        email,
        address,
        emergency_contact,
        allergies,
        dental_history,
        medical_history,
        treatment_history,
        prescription_notes,
        xray_notes,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return patient_id


def get_patients():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            full_name,
            gender,
            phone,
            email,
            created_at
        FROM patients
        ORDER BY id DESC
    """)

    patients = cursor.fetchall()

    conn.close()

    return patients


def search_patients(search_text):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            full_name,
            gender,
            phone,
            email,
            created_at
        FROM patients
        WHERE patient_id LIKE ?
           OR full_name LIKE ?
           OR phone LIKE ?
        ORDER BY id DESC
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    patients = cursor.fetchall()

    conn.close()

    return patients


def get_patient(patient_id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    conn.close()

    return patient


def delete_patient(patient_id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    conn.commit()
    conn.close()
  
    return patient
