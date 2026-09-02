import sqlite3
from datetime import datetime

DB_NAME = "dental_clinic.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # PATIENTS
    # =========================

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

    # =========================
    # APPOINTMENTS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            doctor_name TEXT,
            appointment_type TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            token_number INTEGER,
            status TEXT DEFAULT 'Scheduled',
            notes TEXT,
            created_at TEXT,
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # TREATMENTS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            treatment_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            treatment_type TEXT,
            treatment_name TEXT,
            treatment_date TEXT,
            dentist_name TEXT,
            cost REAL DEFAULT 0,
            notes TEXT,
            status TEXT DEFAULT 'Active',
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # ORTHODONTIC CASES
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orthodontic_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            treatment_type TEXT,
            start_date TEXT,
            expected_end_date TEXT,
            progress INTEGER DEFAULT 0,
            current_stage TEXT,
            notes TEXT,
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # FOLLOW UPS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS followups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            followup_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            followup_date TEXT,
            treatment_stage TEXT,
            progress INTEGER DEFAULT 0,
            notes TEXT,
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # PRESCRIPTIONS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            prescription_date TEXT,
            medicine TEXT,
            instructions TEXT,
            dentist_name TEXT,
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # X-RAYS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xray_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            xray_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            xray_date TEXT,
            xray_type TEXT,
            file_name TEXT,
            notes TEXT,
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # REMINDERS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            reminder_type TEXT,
            reminder_date TEXT,
            message TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # BILLING
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            bill_date TEXT,
            description TEXT,
            total_amount REAL DEFAULT 0,
            paid_amount REAL DEFAULT 0,
            balance REAL DEFAULT 0,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # PAYMENTS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT UNIQUE NOT NULL,
            bill_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            payment_date TEXT,
            amount REAL DEFAULT 0,
            payment_method TEXT,
            notes TEXT,
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # INSURANCE
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insurance_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            insurance_company TEXT,
            policy_number TEXT,
            claim_amount REAL DEFAULT 0,
            claim_date TEXT,
            status TEXT DEFAULT 'Pending',
            notes TEXT,
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # INVENTORY
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT UNIQUE NOT NULL,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            minimum_stock INTEGER DEFAULT 5,
            unit_price REAL DEFAULT 0,
            supplier TEXT,
            last_updated TEXT
        )
    """)

    # =========================
    # EQUIPMENT
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id TEXT UNIQUE NOT NULL,
            equipment_name TEXT NOT NULL,
            category TEXT,
            purchase_date TEXT,
            last_maintenance TEXT,
            next_maintenance TEXT,
            status TEXT DEFAULT 'Operational',
            notes TEXT
        )
    """)

    # =========================
    # FEEDBACK
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            rating INTEGER,
            feedback_text TEXT,
            sentiment TEXT,
            feedback_date TEXT,
            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        )
    """)

    # =========================
    # AI ANALYSIS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id TEXT UNIQUE NOT NULL,
            patient_id TEXT,
            analysis_type TEXT,
            file_name TEXT,
            result TEXT,
            confidence REAL,
            analysis_date TEXT
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# PATIENT FUNCTIONS
# ============================================================

def generate_patient_id():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM patients"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return f"DP{1001 + count}"


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
            date_of_birth,
            gender,
            phone,
            email,
            blood_group,
            registration_date
        FROM patients
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


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

    data = cursor.fetchall()

    conn.close()

    return data


def get_patient(patient_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    data = cursor.fetchone()

    conn.close()

    return data


# ============================================================
# DASHBOARD COUNTS
# ============================================================

def count_patients():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM patients"
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result


def count_appointments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM appointments"
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result


def count_treatments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM treatments WHERE status = 'Active'"
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result
