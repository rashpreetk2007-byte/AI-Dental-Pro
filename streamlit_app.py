import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
from pathlib import Path

# ============================================================
# AI-DENTAL PRO
# Intelligent Dental & Orthodontic Clinic Management System
#
# Developed by: Rashpreet Kaur Arora
# BCA 2nd Year
#
# Academic Prototype
# AI provides assistance/analysis only.
# It is NOT a medical diagnosis or treatment-prescription system.
# ============================================================

st.set_page_config(
    page_title="AI-Dental Pro",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_NAME = "dental_clinic.db"


# ============================================================
# DATABASE
# ============================================================

def db():
    return sqlite3.connect(DB_NAME)


def initialize_database():

    conn = db()
    cur = conn.cursor()

    tables = [

        """
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
        """,

        """
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id TEXT UNIQUE,
            patient_id TEXT,
            doctor_name TEXT,
            appointment_type TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            token_number INTEGER,
            status TEXT DEFAULT 'Scheduled',
            notes TEXT,
            created_at TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            treatment_id TEXT UNIQUE,
            patient_id TEXT,
            treatment_type TEXT,
            treatment_name TEXT,
            treatment_date TEXT,
            dentist_name TEXT,
            cost REAL DEFAULT 0,
            notes TEXT,
            status TEXT DEFAULT 'Active'
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS orthodontic_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT UNIQUE,
            patient_id TEXT,
            treatment_type TEXT,
            start_date TEXT,
            expected_end_date TEXT,
            progress INTEGER DEFAULT 0,
            current_stage TEXT,
            notes TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS followups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            followup_id TEXT UNIQUE,
            patient_id TEXT,
            followup_date TEXT,
            treatment_stage TEXT,
            progress INTEGER DEFAULT 0,
            notes TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_id TEXT UNIQUE,
            patient_id TEXT,
            prescription_date TEXT,
            medicine TEXT,
            instructions TEXT,
            dentist_name TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS xray_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            xray_id TEXT UNIQUE,
            patient_id TEXT,
            xray_date TEXT,
            xray_type TEXT,
            file_name TEXT,
            notes TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder_id TEXT UNIQUE,
            patient_id TEXT,
            reminder_type TEXT,
            reminder_date TEXT,
            message TEXT,
            status TEXT DEFAULT 'Pending'
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id TEXT UNIQUE,
            patient_id TEXT,
            bill_date TEXT,
            description TEXT,
            total_amount REAL DEFAULT 0,
            paid_amount REAL DEFAULT 0,
            balance REAL DEFAULT 0,
            status TEXT DEFAULT 'Pending'
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT UNIQUE,
            bill_id TEXT,
            patient_id TEXT,
            payment_date TEXT,
            amount REAL DEFAULT 0,
            payment_method TEXT,
            notes TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS insurance_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim_id TEXT UNIQUE,
            patient_id TEXT,
            insurance_company TEXT,
            policy_number TEXT,
            claim_amount REAL DEFAULT 0,
            claim_date TEXT,
            status TEXT DEFAULT 'Pending',
            notes TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT UNIQUE,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            minimum_stock INTEGER DEFAULT 5,
            unit_price REAL DEFAULT 0,
            supplier TEXT,
            last_updated TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id TEXT UNIQUE,
            equipment_name TEXT NOT NULL,
            category TEXT,
            purchase_date TEXT,
            last_maintenance TEXT,
            next_maintenance TEXT,
            status TEXT DEFAULT 'Operational',
            notes TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_id TEXT UNIQUE,
            patient_id TEXT,
            rating INTEGER,
            feedback_text TEXT,
            sentiment TEXT,
            feedback_date TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id TEXT UNIQUE,
            patient_id TEXT,
            analysis_type TEXT,
            file_name TEXT,
            result TEXT,
            confidence REAL,
            analysis_date TEXT
        )
        """
    ]

    for table in tables:
        cur.execute(table)

    conn.commit()
    conn.close()


initialize_database()


# ============================================================
# DATABASE HELPERS
# ============================================================

def execute(query, params=(), fetch=False, many=False):

    conn = db()
    cur = conn.cursor()

    if many:
        cur.executemany(query, params)
    else:
        cur.execute(query, params)

    result = cur.fetchall() if fetch else None

    conn.commit()
    conn.close()

    return result


def scalar(query, params=()):

    conn = db()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()[0]
    conn.close()

    return result


def generate_id(prefix, table, column):

    number = scalar(
        f"SELECT COUNT(*) FROM {table}"
    )

    return f"{prefix}{1001 + number}"


def patient_names():

    rows = execute(
        """
        SELECT patient_id, full_name
        FROM patients
        ORDER BY full_name
        """,
        fetch=True
    )

    return rows


def patient_label(patient):

    return f"{patient[0]} — {patient[1]}"


# ============================================================
# CUSTOM UI
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        linear-gradient(
            135deg,
            #eefaff 0%,
            #f8f2ff 50%,
            #fff3f7 100%
        );
    }

    [data-testid="stSidebar"] {
        background:
        linear-gradient(
            180deg,
            #ffffff,
            #f2f8ff
        );
    }

    .hero {
        padding: 28px;
        border-radius: 24px;
        background: white;
        box-shadow: 0 8px 25px rgba(0,0,0,.08);
        text-align: center;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
    }

    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 5px 18px rgba(0,0,0,.07);
    }

    .metric-number {
        font-size: 34px;
        font-weight: 800;
    }

    .section {
        font-size: 28px;
        font-weight: 800;
        margin: 15px 0 20px 0;
    }

    .info-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,.06);
        margin-bottom: 15px;
    }

    .footer {
        margin-top: 45px;
        padding: 20px;
        text-align: center;
        border-radius: 18px;
        background: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <h1 style="text-align:center;">🦷</h1>
    <h2 style="text-align:center;">AI-Dental Pro</h2>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<p style='text-align:center;'><b>Rashpreet Kaur Arora</b></p>",
    unsafe_allow_html=True
)

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Patients",
        "📅 Appointments",
        "🦷 Orthodontics",
        "🪥 Dental Care",
        "🔔 Reminders",
        "💳 Billing",
        "📦 Inventory",
        "🤖 AI Care Center",
        "📊 Reports",
        "⚙️ Administration"
    ]
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🦷 AI-DENTAL PRO</h1>
        <p>
        Intelligent Dental & Orthodontic Clinic Management System
        </p>
        <p>
        <b>Developed by Rashpreet Kaur Arora | BCA 2nd Year</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="section">📊 Clinic Dashboard</div>',
        unsafe_allow_html=True
    )

    total_patients = scalar(
        "SELECT COUNT(*) FROM patients"
    )

    total_appointments = scalar(
        "SELECT COUNT(*) FROM appointments"
    )

    active_treatments = scalar(
        "SELECT COUNT(*) FROM treatments WHERE status='Active'"
    )

    orthodontic_cases = scalar(
        "SELECT COUNT(*) FROM orthodontic_cases"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div>👥 Patients</div>
                <div class="metric-number">
                    {total_patients}
                </div>
                <small>Registered</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div>📅 Appointments</div>
                <div class="metric-number">
                    {total_appointments}
                </div>
                <small>Total</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div>🦷 Treatments</div>
                <div class="metric-number">
                    {active_treatments}
                </div>
                <small>Active Cases</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div>😁 Orthodontics</div>
                <div class="metric-number">
                    {orthodontic_cases}
                </div>
                <small>Cases</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("✨ Quick Actions")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.info("👤 Register patients from the Patients section.")

    with q2:
        st.info("📅 Schedule dental appointments.")

    with q3:
        st.info("🦷 Track braces and aligner cases.")

    with q4:
        st.info("🤖 Use AI-assisted educational analysis.")

    st.subheader("📅 Recent Appointments")

    recent = execute(
        """
        SELECT
            appointment_id,
            patient_id,
            doctor_name,
            appointment_type,
            appointment_date,
            appointment_time,
            status
        FROM appointments
        ORDER BY id DESC
        LIMIT 10
        """,
        fetch=True
    )

    if recent:

        df = pd.DataFrame(
            recent,
            columns=[
                "Appointment ID",
                "Patient ID",
                "Doctor",
                "Type",
                "Date",
                "Time",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No appointments recorded yet.")


# ============================================================
# PATIENT MANAGEMENT
# ============================================================

elif menu == "👤 Patients":

    st.markdown(
        '<div class="section">👤 Patient Management</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "➕ Register",
            "🔍 Search",
            "📋 All Patients",
            "👁️ Patient Profile"
        ]
    )

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    with tab1:

        st.subheader("➕ New Patient Registration")

        with st.form("patient_registration"):

            c1, c2 = st.columns(2)

            with c1:

                full_name = st.text_input(
                    "Full Name *"
                )

                dob = st.date_input(
                    "Date of Birth",
                    value=date(2000, 1, 1)
                )

                gender = st.selectbox(
                    "Gender",
                    ["Female", "Male", "Other"]
                )

                phone = st.text_input(
                    "Phone Number"
                )

                email = st.text_input(
                    "Email"
                )

                blood_group = st.selectbox(
                    "Blood Group",
                    [
                        "Unknown",
                        "A+",
                        "A-",
                        "B+",
                        "B-",
                        "AB+",
                        "AB-",
                        "O+",
                        "O-"
                    ]
                )

            with c2:

                emergency = st.text_input(
                    "Emergency Contact"
                )

                address = st.text_area(
                    "Address"
                )

                dental_history = st.text_area(
                    "Dental History"
                )

                allergies = st.text_area(
                    "Allergies"
                )

            submitted = st.form_submit_button(
                "💾 Register Patient",
                use_container_width=True
            )

            if submitted:

                if not full_name.strip():

                    st.error(
                        "Patient name is required."
                    )

                else:

                    patient_id = generate_id(
                        "DP",
                        "patients",
                        "patient_id"
                    )

                    execute(
                        """
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
                        """,
                        (
                            patient_id,
                            full_name,
                            str(dob),
                            gender,
                            phone,
                            email,
                            emergency,
                            dental_history,
                            allergies,
                            address,
                            blood_group,
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        )
                    )

                    st.success(
                        f"✅ Patient registered successfully!"
                    )

                    st.code(
                        f"Patient ID: {patient_id}"
                    )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    with tab2:

        st.subheader("🔍 Search Patient")

        search = st.text_input(
            "Search by Patient ID, Name or Phone"
        )

        if search:

            results = execute(
                """
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
                """,
                (
                    f"%{search}%",
                    f"%{search}%",
                    f"%{search}%"
                ),
                fetch=True
            )

            if results:

                df = pd.DataFrame(
                    results,
                    columns=[
                        "Patient ID",
                        "Name",
                        "DOB",
                        "Gender",
                        "Phone",
                        "Email",
                        "Blood Group",
                        "Registered"
                    ]
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.warning(
                    "No patient found."
                )

    # --------------------------------------------------------
    # ALL PATIENTS
    # --------------------------------------------------------

    with tab3:

        patients = execute(
            """
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
            """,
            fetch=True
        )

        if patients:

            df = pd.DataFrame(
                patients,
                columns=[
                    "Patient ID",
                    "Name",
                    "DOB",
                    "Gender",
                    "Phone",
                    "Email",
                    "Blood Group",
                    "Registered"
                ]
            )
