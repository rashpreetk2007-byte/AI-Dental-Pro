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
            patient_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            date_of_birth TEXT,
            gender TEXT,
            phone TEXT,
            email TEXT,
            emergency_contact TEXT,
            dental_history TEXT,
            allergies TEXT,
            address TEXT,
            blood_group TEXT,
            registration_date TEXT
        )
    """)

    conn.commit()
    conn.close()


def generate_patient_id():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT MAX(id) FROM patients"
    )

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        number = 1001
    else:
        number = 1001 + result

    return f"DP{number}"


def add_patient(
    full_name,
    date_of_birth,
    gender,
    phone,
    email,
    emergency_contact,
    dental_history,
    allergies,
    address,
    blood_group
):

    conn = get_connection()
    cursor = conn.cursor()

    patient_id = generate_patient_id()

    registration_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO patients (
            patient_id,
            full_name,
            date_of_birth,
            gender,
            phone,
            email,
            emergency_contact,
            dental_history,
            allergies,
            address,
            blood_group,
            registration_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        full_name,
        date_of_birth,
        gender,
        phone,
        email,
        emergency_contact,
        dental_history,
        allergies,
        address,
        blood_group,
        registration_date
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
            date_of_birth,
            gender,
            phone,
            email,
            blood_group,
            registration_date
        FROM patients
        ORDER BY id DESC
    """)

    patients = cursor.fetchall()

    conn.close()

    return patients


def search_patients(search_text):

    conn = get_connection()
    cursor = conn.cursor()

    search = f"%{search_text}%"

    cursor.execute("""
        SELECT
            patient_id,
            full_name,
            date_of_birth,
            gender,
            phone,
            email,
            blood_group,
            registration_date
        FROM patients
        WHERE patient_id LIKE ?
           OR full_name LIKE ?
           OR phone LIKE ?
        ORDER BY id DESC
    """, (
        search,
        search,
        search
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
