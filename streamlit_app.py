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
st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No patients registered yet."
            )

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    with tab4:

        patients = patient_names()

        if patients:

            selected = st.selectbox(
                "Select Patient",
                patients,
                format_func=patient_label
            )

            patient_id = selected[0]

            patient = execute(
                """
                SELECT *
                FROM patients
                WHERE patient_id = ?
                """,
                (patient_id,),
                fetch=True
            )

            if patient:

                p = patient[0]

                c1, c2 = st.columns(2)

                with c1:

                    st.subheader(
                        f"👤 {p[2]}"
                    )

                    st.write(
                        f"**Patient ID:** {p[1]}"
                    )

                    st.write(
                        f"**Date of Birth:** {p[3]}"
                    )

                    st.write(
                        f"**Gender:** {p[4]}"
                    )

                    st.write(
                        f"**Phone:** {p[5]}"
                    )

                    st.write(
                        f"**Email:** {p[6]}"
                    )

                    st.write(
                        f"**Blood Group:** {p[12]}"
                    )

                with c2:

                    st.write(
                        f"**Emergency Contact:** {p[7]}"
                    )

                    st.write(
                        f"**Address:** {p[10]}"
                    )

                    st.write(
                        f"**Dental History:** {p[8]}"
                    )

                    st.write(
                        f"**Allergies:** {p[9]}"
                    )

                    st.write(
                        f"**Registration:** {p[13]}"
                    )

        else:

            st.warning(
                "Register a patient first."
            )
            # ============================================================
# APPOINTMENTS
# ============================================================

elif menu == "📅 Appointments":

    st.markdown(
        '<div class="section">📅 Appointment Management</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Book Appointment",
            "📋 Appointment List",
            "🎫 Queue"
        ]
    )

    patients = patient_names()

    with tab1:

        if not patients:

            st.warning(
                "Please register a patient before booking."
            )

        else:

            with st.form("appointment_form"):

                selected = st.selectbox(
                    "Patient",
                    patients,
                    format_func=patient_label
                )

                doctor = st.text_input(
                    "Dentist / Orthodontist Name"
                )

                appointment_type = st.selectbox(
                    "Appointment Type",
                    [
                        "Dental Consultation",
                        "Dental Cleaning",
                        "Toothache Consultation",
                        "Dental Follow-up",
                        "Orthodontic Consultation",
                        "Braces Follow-up",
                        "Aligner Follow-up",
                        "Retainer Check",
                        "Emergency Guidance"
                    ]
                )

                c1, c2 = st.columns(2)

                with c1:

                    appointment_date = st.date_input(
                        "Appointment Date",
                        value=date.today()
                    )

                with c2:

                    appointment_time = st.time_input(
                        "Appointment Time"
                    )

                notes = st.text_area(
                    "Notes"
                )

                submit = st.form_submit_button(
                    "📅 Book Appointment",
                    use_container_width=True
                )

                if submit:

                    appointment_id = generate_id(
                        "AP",
                        "appointments",
                        "appointment_id"
                    )

                    token = scalar(
                        """
                        SELECT COUNT(*)
                        FROM appointments
                        WHERE appointment_date = ?
                        """,
                        (str(appointment_date),)
                    ) + 1

                    execute(
                        """
                        INSERT INTO appointments (
                            appointment_id,
                            patient_id,
                            doctor_name,
                            appointment_type,
                            appointment_date,
                            appointment_time,
                            token_number,
                            status,
                            notes,
                            created_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            appointment_id,
                            selected[0],
                            doctor,
                            appointment_type,
                            str(appointment_date),
                            str(appointment_time),
                            token,
                            "Scheduled",
                            notes,
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        )
                    )

                    st.success(
                        "✅ Appointment booked successfully."
                    )

                    st.code(
                        f"Appointment ID: {appointment_id}\n"
                        f"Token Number: {token}"
                    )

    with tab2:

        appointments = execute(
            """
            SELECT
                appointment_id,
                patient_id,
                doctor_name,
                appointment_type,
                appointment_date,
                appointment_time,
                token_number,
                status
            FROM appointments
            ORDER BY appointment_date DESC,
                     appointment_time DESC
            """,
            fetch=True
        )
        if appointments:

            df = pd.DataFrame(
                appointments,
                columns=[
                    "Appointment ID",
                    "Patient ID",
                    "Doctor",
                    "Type",
                    "Date",
                    "Time",
                    "Token",
                    "Status"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            appointment_ids = [
                x[0] for x in appointments
            ]

            selected_ap = st.selectbox(
                "Select Appointment to Update",
                appointment_ids
            )

            new_status = st.selectbox(
                "New Status",
                [
                    "Scheduled",
                    "Confirmed",
                    "Completed",
                    "Cancelled",
                    "No Show"
                ]
            )

            if st.button(
                "🔄 Update Appointment Status"
            ):

                execute(
                    """
                    UPDATE appointments
                    SET status = ?
                    WHERE appointment_id = ?
                    """,
                    (
                        new_status,
                        selected_ap
                    )
                )

                st.success(
                    "Appointment status updated."
                )

        else:

            st.info(
                "No appointments available."
            )

    with tab3:

        today = str(date.today())

        queue = execute(
            """
            SELECT
                token_number,
                patient_id,
                doctor_name,
                appointment_type,
                appointment_time,
                status
            FROM appointments
            WHERE appointment_date = ?
            ORDER BY token_number
            """,
            (today,),
            fetch=True
        )

        st.subheader(
            f"🎫 Today's Queue — {today}"
        )

        if queue:

            df = pd.DataFrame(
                queue,
                columns=[
                    "Token",
                    "Patient ID",
                    "Doctor",
                    "Type",
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

            st.info(
                "No appointments in today's queue."
            )
            # ============================================================
# ORTHODONTICS
# ============================================================

elif menu == "🦷 Orthodontics":

    st.markdown(
        '<div class="section">🦷 Orthodontic Management</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ New Case",
            "📈 Progress",
            "🔄 Follow-up"
        ]
    )

    patients = patient_names()

    with tab1:

        if not patients:

            st.warning(
                "Register a patient first."
            )

        else:

            with st.form("ortho_case"):

                selected = st.selectbox(
                    "Patient",
                    patients,
                    format_func=patient_label
                )

                treatment_type = st.selectbox(
                    "Treatment",
                    [
                        "Metal Braces",
                        "Ceramic Braces",
                        "Clear Aligners",
                        "Retainer",
                        "Orthodontic Observation"
                    ]
                )

                start = st.date_input(
                    "Start Date",
                    value=date.today()
                )

                expected = st.date_input(
                    "Expected End Date",
                    value=date.today() + timedelta(days=365)
                )

                progress = st.slider(
                    "Initial Progress %",
                    0,
                    100,
                    0
                )

                stage = st.selectbox(
                    "Current Stage",
                    [
                        "Consultation",
                        "Planning",
                        "Initial Treatment",
                        "Active Treatment",
                        "Adjustment",
                        "Retention",
                        "Completed"
                    ]
                )

                notes = st.text_area(
                    "Clinical/Progress Notes"
                )

                submit = st.form_submit_button(
                    "💾 Save Orthodontic Case",
                    use_container_width=True
                )

                if submit:

                    case_id = generate_id(
                        "OC",
                        "orthodontic_cases",
                        "case_id"
                    )

                    execute(
                        """
                        INSERT INTO orthodontic_cases (
                            case_id,
                            patient_id,
                            treatment_type,
                            start_date,
                            expected_end_date,
                            progress,
                            current_stage,
                            notes
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            case_id,
                            selected[0],
                            treatment_type,
                            str(start),
                            str(expected),
                            progress,
                            stage,
                            notes
                        )
                    )

                    st.success(
                        f"Orthodontic case {case_id} saved."
                    )

    with tab2:

        cases = execute(
            """
            SELECT
                case_id,
                patient_id,
                treatment_type,
                start_date,
                expected_end_date,
                progress,
                current_stage,
                notes
            FROM orthodontic_cases
            ORDER BY id DESC
            """,
            fetch=True
        )

        if cases:

            df = pd.DataFrame(
                cases,
                columns=[
                    "Case ID",
                    "Patient ID",
                    "Treatment",
                    "Start",
                    "Expected End",
                    "Progress %",
                    "Stage",
                    "Notes"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            selected_case = st.selectbox(
                "Select Case",
                [x[0] for x in cases]
            )

            progress = st.slider(
                "Update Progress",
                0,
                100,
                50
            )

            stage = st.selectbox(
                "Update Stage",
                [
                    "Consultation",
                    "Planning",
                    "Initial Treatment",
                    "Active Treatment",
                    "Adjustment",
                    "Retention",
                    "Completed"
                ]
            )

            if st.button(
                "📈 Update Progress"
            ):

                execute(
                    """
                    UPDATE orthodontic_cases
                    SET progress = ?,
                        current_stage = ?
                    WHERE case_id = ?
                    """,
                    (
                        progress,
                        stage,
                        selected_case
                    )
                )

                st.success(
                    "Orthodontic progress updated."
                )

    with tab3:

        if patients:

            selected = st.selectbox(
                "Patient",
                patients,
                format_func=patient_label,
                key="follow_patient"
            )

            follow_date = st.date_input(
                "Follow-up Date",
                value=date.today()
            )

            stage = st.text_input(
                "Treatment Stage"
            )

            progress = st.slider(
                "Progress %",
                0,
                100,
                50
            )

            notes = st.text_area(
                "Follow-up Notes"
            )

            if st.button(
                "💾 Save Follow-up"
            ):

                follow_id = generate_id(
                    "FU",
                    "followups",
                    "followup_id"
                )

                execute(
                    """
                    INSERT INTO followups (
                        followup_id,
                        patient_id,
                        followup_date,
                        treatment_stage,
                        progress,
                        notes
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        follow_id,
                        selected[0],
                        str(follow_date),
                        stage,
                        progress,
                        notes
                    )
                )

                st.success(
                    f"Follow-up {follow_id} saved."
                )
                # ============================================================
# DENTAL CARE
# ============================================================

elif menu == "🪥 Dental Care":

    st.markdown(
        '<div class="section">🪥 Dental Care Center</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📝 Assessment",
            "🥗 Diet Guide",
            "🚨 Emergency Guidance",
            "🧠 Dental Quiz"
        ]
    )

    with tab1:

        st.subheader(
            "📝 Oral Health Questionnaire"
        )

        q1 = st.radio(
            "Do you brush your teeth twice a day?",
            ["Yes", "No"]
        )

        q2 = st.radio(
            "Do you regularly floss/interdental clean?",
            ["Yes", "No", "Sometimes"]
        )

        q3 = st.radio(
            "Do you experience tooth sensitivity?",
            ["Yes", "No"]
        )

        q4 = st.radio(
            "Do you frequently consume sugary foods/drinks?",
            ["Yes", "No", "Sometimes"]
        )

        q5 = st.radio(
            "Have you visited a dentist recently?",
            ["Yes", "No"]
        )

        if st.button(
            "📊 Calculate Educational Risk Score"
        ):

            score = 0

            if q1 == "No":
                score += 2

            if q2 == "No":
                score += 2

            if q3 == "Yes":
                score += 2

            if q4 == "Yes":
                score += 2

            if q5 == "No":
                score += 2

            if score <= 2:

                level = "Lower educational risk"

            elif score <= 5:

                level = "Moderate educational risk"

            else:

                level = "Higher educational risk"

            st.metric(
                "Educational Score",
                f"{score}/10"
            )

            st.info(
                f"Assessment result: {level}. "
                "This is an educational screening tool, "
                "not a medical diagnosis."
            )

    with tab2:

        st.subheader(
            "🥗 Dental Diet Recommendations"
        )

        st.success(
            "Prefer balanced meals, water, vegetables, "
            "calcium-rich foods and limited added sugar."
        )

        st.warning(
            "For braces, avoid very hard, sticky or chewy "
            "foods that may damage orthodontic appliances."
        )

    with tab3:

        st.subheader(
            "🚨 Dental Emergency Guidance"
        )

        situation = st.selectbox(
            "Select situation",
            [
                "Severe tooth pain",
                "Dental injury",
                "Bleeding",
                "Swelling",
                "Broken dental appliance",
                "Knocked-out tooth"
            ]
        )

        st.info(
            f"""
            General educational guidance for: {situation}

            Seek professional dental care promptly,
            especially when pain, swelling, bleeding,
            trauma or other serious symptoms are present.

            If the situation appears life-threatening,
            seek emergency medical assistance.
            """
        )

    with tab4:

        st.subheader(
            "🧠 Dental Health Quiz"
        )

        answer = st.radio(
            "How often is brushing generally recommended?",
            [
                "Once a week",
                "Twice daily",
                "Once a month",
                "Only when pain occurs"
            ]
        )

        if st.button(
            "Check Answer"
        ):

            if answer == "Twice daily":

                st.success(
                    "✅ Correct!"
                )

            else:

                st.error(
                    "❌ Incorrect. The expected educational answer is twice daily."
                )
                # ============================================================
# REMINDERS
# ============================================================

elif menu == "🔔 Reminders":

    st.markdown(
        '<div class="section">🔔 Smart Dental Reminders</div>',
        unsafe_allow_html=True
    )

    patients = patient_names()

    if patients:

        selected = st.selectbox(
            "Patient",
            patients,
            format_func=patient_label
        )

        reminder_type = st.selectbox(
            "Reminder Type",
            [
                "Appointment",
                "Dental Cleaning",
                "Toothbrush Replacement",
                "Oral Hygiene",
                "Braces Care",
                "Aligner Wear",
                "Retainer Usage",
                "Follow-up"
            ]
        )

        reminder_date = st.date_input(
            "Reminder Date",
            value=date.today()
        )

        message = st.text_area(
            "Reminder Message"
        )

        if st.button(
            "🔔 Save Reminder"
        ):

            reminder_id = generate_id(
                "RM",
                "reminders",
                "reminder_id"
            )

            execute(
                """
                INSERT INTO reminders (
                    reminder_id,
                    patient_id,
                    reminder_type,
                    reminder_date,
                    message,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    reminder_id,
                    selected[0],
                    reminder_type,
                    str(reminder_date),
                    message,
                    "Pending"
                )
            )

            st.success(
                f"Reminder {reminder_id} created."
            )

    reminders = execute(
        """
        SELECT
            reminder_id,
            patient_id,
            reminder_type,
            reminder_date,
            message,
            status
        FROM reminders
        ORDER BY reminder_date
        """,
        fetch=True
    )

    if reminders:

        st.subheader("📋 Reminder List")

        df = pd.DataFrame(
            reminders,
            columns=[
                "Reminder ID",
                "Patient ID",
                "Type",
                "Date",
                "Message",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# BILLING
# ============================================================

elif menu == "💳 Billing":

    st.markdown(
        '<div class="section">💳 Billing & Payments</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "🧾 Create Bill",
            "💰 Payment",
            "📋 Billing History"
        ]
    )

    patients = patient_names()

    with tab1:

        if patients:

            selected = st.selectbox(
                "Patient",
                patients,
                format_func=patient_label
            )

            description = st.text_input(
                "Treatment / Service"
            )

            total = st.number_input(
                "Total Amount",
                min_value=0.0,
                step=100.0
            )

            paid = st.number_input(
                "Initial Paid Amount",
                min_value=0.0,
                max_value=total,
                step=100.0
            )

            if st.button(
                "🧾 Generate Bill"
            ):

                bill_id = generate_id(
                    "BL",
                    "bills",
                    "bill_id"
                )

                balance = total - paid

                status = (
                    "Paid"
                    if balance == 0
                    else "Partially Paid"
                    if paid > 0
                    else "Pending"
                )

                execute(
                    """
                    INSERT INTO bills (
                        bill_id,
                        patient_id,
                        bill_date,
                        description,
                        total_amount,
                        paid_amount,
                        balance,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        bill_id,
                        selected[0],
                        str(date.today()),
                        description,
                        total,
                        paid,
                        balance,
                        status
                    )
                )

                st.success(
                    f"Bill {bill_id} generated."
                )

                st.metric(
                    "Balance",
                    f"₹{balance:,.2f}"
                )

    with tab2:

        bills = execute(
            """
            SELECT bill_id, patient_id, balance
            FROM bills
            WHERE balance > 0
            ORDER BY id DESC
            """,
            fetch=True
        )

        if bills:

            selected_bill = st.selectbox(
                "Bill",
                bills,
                format_func=lambda x:
                    f"{x[0]} — {x[1]} — ₹{x[2]:,.2f}"
            )

            amount = st.number_input(
                "Payment Amount",
                min_value=0.0,
                max_value=float(selected_bill[2]),
                step=100.0
            )

            method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Card",
                    "Bank Transfer"
                ]
            )

            if st.button(
                "💰 Record Payment"
            ):
                payment_id = generate_id(
                    "PY",
                    "payments",
                    "payment_id"
                )

                execute(
                    """
                    INSERT INTO payments (
                        payment_id,
                        bill_id,
                        patient_id,
                        payment_date,
                        amount,
                        payment_method,
                        notes
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        payment_id,
                        selected_bill[0],
                        selected_bill[1],
                        str(date.today()),
                        amount,
                        method,
                        ""
                    )
                )

                new_balance = selected_bill[2] - amount

                new_status = (
                    "Paid"
                    if new_balance <= 0
                    else "Partially Paid"
                )

                execute(
                    """
                    UPDATE bills
                    SET paid_amount =
                        paid_amount + ?,
                        balance = ?,
                        status = ?
                    WHERE bill_id = ?
                    """,
                    (
                        amount,
                        new_balance,
                        new_status,
                        selected_bill[0]
                    )
                )

                st.success(
                    f"Payment {payment_id} recorded."
                )

        else:

            st.info(
                "No outstanding bills."
            )

    with tab3:

        bills = execute(
            """
            SELECT
                bill_id,
                patient_id,
                bill_date,
                description,
                total_amount,
                paid_amount,
                balance,
                status
            FROM bills
            ORDER BY id DESC
            """,
            fetch=True
        )

        if bills:

            df = pd.DataFrame(
                bills,
                columns=[
                    "Bill ID",
                    "Patient ID",
                    "Date",
                    "Description",
                    "Total",
                    "Paid",
                    "Balance",
                    "Status"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# INVENTORY
# ============================================================

elif menu == "📦 Inventory":

    st.markdown(
        '<div class="section">📦 Clinic Inventory</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        [
            "➕ Add Item",
            "📋 Inventory"
        ]
    )

    with tab1:

        with st.form("inventory_form"):

            item_name = st.text_input(
                "Item Name"
            )

            category = st.text_input(
                "Category"
            )

            quantity = st.number_input(
                "Quantity",
                min_value=0,
                step=1
            )

            minimum = st.number_input(
                "Minimum Stock Level",
                min_value=0,
                value=5,
                step=1
            )

            unit_price = st.number_input(
                "Unit Price",
                min_value=0.0,
                step=10.0
            )

            supplier = st.text_input(
                "Supplier"
            )

            submit = st.form_submit_button(
                "📦 Save Item",
                use_container_width=True
            )

            if submit:

                if item_name.strip():

                    item_id = generate_id(
                        "IN",
                        "inventory",
                        "item_id"
                    )

                    execute(
                        """
                        INSERT INTO inventory (
                            item_id,
                            item_name,
                            category,
                            quantity,
                            minimum_stock,
                            unit_price,
                            supplier,
                            last_updated
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            item_id,
                            item_name,
                            category,
                            quantity,
                            minimum,
                            unit_price,
                            supplier,
                            str(datetime.now())
                        )
                    )

                    st.success(
                        f"Inventory item {item_id} saved."
                    )

    with tab2:

        items = execute(
            """
            SELECT
                item_id,
                item_name,
                category,
                quantity,
                minimum_stock,
                unit_price,
                supplier
            FROM inventory
            ORDER BY id DESC
            """,
            fetch=True
        )
        # ============================================================
# AI CARE CENTER
# ============================================================

elif menu == "🤖 AI Care Center":

    st.markdown(
        '<div class="section">🤖 AI Care Center</div>',
        unsafe_allow_html=True
    )

    st.info(
        "AI-assisted educational analysis only. "
        "This prototype does not provide medical diagnosis "
        "or treatment prescriptions."
    )

    try:

        hf_token = st.secrets["HF_TOKEN"]

    except Exception:

        hf_token = None

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "💬 Dental AI Assistant",
            "😁 Smile Analysis",
            "🦷 Progress Analysis",
            "💬 Feedback Analysis"
        ]
    )

    # --------------------------------------------------------
    # TEXT AI
    # --------------------------------------------------------

    with tab1:

        if hf_token:

            st.success(
                "🟢 Hugging Face token detected."
            )

        else:

            st.warning(
                "🟡 HF_TOKEN is not configured in Streamlit Secrets."
            )

        question = st.text_area(
            "Ask an educational dental question",
            placeholder=(
                "Example: What are good oral hygiene habits?"
            )
        )

        if st.button(
            "🤖 Ask Hugging Face AI",
            use_container_width=True
        ):

            if not hf_token:

                st.error(
                    "Add HF_TOKEN to Streamlit Secrets first."
                )

            elif not question.strip():

                st.warning(
                    "Enter a question."
                )

            else:

                try:

                    from huggingface_hub import InferenceClient

                    client = InferenceClient(
                        api_key=hf_token
                    )

                    model = st.secrets.get(
                        "HF_MODEL",
                        "Qwen/Qwen2.5-7B-Instruct"
                    )

                    with st.spinner(
                        "AI is preparing an educational response..."
                    ):

                        response = client.chat_completion(
                            model=model,
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are an educational dental "
                                        "information assistant. "
                                        "Do not diagnose medical or "
                                        "dental conditions. "
                                        "Do not prescribe medication. "
                                        "Provide general educational "
                                        "information and recommend "
                                        "consulting a qualified "
                                        "dental professional when "
                                        "appropriate."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": question
                                }
                            ],
                            max_tokens=500
                        )

                    answer = (
                        response.choices[0]
                        .message.content
                    )

                    st.markdown("### 🤖 AI Response")

                    st.write(answer)

                except Exception as e:

                    st.error(
                        "Hugging Face request failed."
                    )

                    st.code(
                        str(e)
                    )
                    # --------------------------------------------------------
    # SMILE IMAGE
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "😁 AI Smile Analysis Assistant"
        )

        image = st.file_uploader(
            "Upload Smile Image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            key="smile_image"
        )

        if image:

            st.image(
                image,
                caption="Uploaded Smile Image",
                use_container_width=True
            )

            st.info(
                "Vision-model integration can be used for "
                "educational image analysis. The output must "
                "not be presented as a dental diagnosis."
            )

    # --------------------------------------------------------
    # ORTHODONTIC IMAGE
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "🦷 Orthodontic Progress Analyzer"
        )

        before = st.file_uploader(
            "Initial / Before Image",
            type=["jpg", "jpeg", "png"],
            key="before_image"
        )

        after = st.file_uploader(
            "Follow-up / After Image",
            type=["jpg", "jpeg", "png"],
            key="after_image"
        )

        if before and after:

            c1, c2 = st.columns(2)

            with c1:

                st.image(
                    before,
                    caption="Initial Image",
                    use_container_width=True
                )
                with c2:

                st.image(
                    after,
                    caption="Follow-up Image",
                    use_container_width=True
                )

            st.success(
                "Images uploaded successfully."
            )

            st.info(
                "The production version can connect these "
                "images to a suitable computer-vision model "
                "for educational progress comparison."
            )

    # --------------------------------------------------------
    # FEEDBACK AI
    # --------------------------------------------------------

    with tab4:

        st.subheader(
            "💬 AI Feedback Analysis"
        )

        feedback_text = st.text_area(
            "Enter patient feedback"
        )

        if st.button(
            "Analyze Feedback"
        ):

            text = feedback_text.lower()

            positive_words = [
                "good",
                "excellent",
                "happy",
                "great",
                "nice",
                "satisfied"
            ]

            negative_words = [
                "bad",
                "poor",
                "unhappy",
                "slow",
                "worst",
                "dissatisfied"
            ]

            positive = sum(
                word in text
                for word in positive_words
            )

            negative = sum(
                word in text
                for word in negative_words
            )

            if positive > negative:

                sentiment = "Positive 😊"

            elif negative > positive:

                sentiment = "Negative 😟"

            else:

                sentiment = "Neutral 😐"

            st.metric(
                "Detected Sentiment",
                sentiment
            )
            # ============================================================
# REPORTS
# ============================================================

elif menu == "📊 Reports":

    st.markdown(
        '<div class="section">📊 Clinic Reports & Analytics</div>',
        unsafe_allow_html=True
    )

    patients = scalar(
        "SELECT COUNT(*) FROM patients"
    )

    appointments = scalar(
        "SELECT COUNT(*) FROM appointments"
    )

    treatments = scalar(
        "SELECT COUNT(*) FROM treatments"
    )

    cases = scalar(
        "SELECT COUNT(*) FROM orthodontic_cases"
    )

    revenue = scalar(
        "SELECT COALESCE(SUM(paid_amount),0) FROM bills"
    )

    outstanding = scalar(
        "SELECT COALESCE(SUM(balance),0) FROM bills"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "👥 Patients",
            patients
        )

    with c2:
        st.metric(
            "📅 Appointments",
            appointments
        )

    with c3:
        st.metric(
            "🦷 Treatments",
            treatments
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        st.metric(
            "😁 Orthodontic Cases",
            cases
        )

    with c5:
        st.metric(
            "💰 Collected",
            f"₹{revenue:,.2f}"
        )

    with c6:
        st.metric(
            "⚠️ Outstanding",
            f"₹{outstanding:,.2f}"
        )

    st.subheader(
        "📈 Appointment Status"
    )

    appointment_status = execute(
        """
        SELECT status, COUNT(*)
        FROM appointments
        GROUP BY status
        """,
        fetch=True
    )

    if appointment_status:

        df = pd.DataFrame(
            appointment_status,
            columns=[
                "Status",
                "Count"
            ]
        )

        st.bar_chart(
            df.set_index("Status")
        )

    st.subheader(
        "💳 Revenue Summary"
    )

    revenue_data = execute(
        """
        SELECT
            bill_date,
            SUM(total_amount),
            SUM(paid_amount),
            SUM(balance)
        FROM bills
        GROUP BY bill_date
        ORDER BY bill_date
        """,
        fetch=True
    )

    if revenue_data:

        df = pd.DataFrame(
            revenue_data,
            columns=[
                "Date",
                "Total",
                "Paid",
                "Balance"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        # ============================================================
# ADMINISTRATION
# ============================================================

elif menu == "⚙️ Administration":

    st.markdown(
        '<div class="section">⚙️ Administration</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "🏥 Clinic Information"
    )

    clinic_name = st.text_input(
        "Clinic Name",
        "AI-Dental Pro Academic Clinic"
    )

    dentist = st.text_input(
        "Primary Dentist / Orthodontist"
    )

    phone = st.text_input(
        "Clinic Contact Number"
    )

    address = st.text_area(
        "Clinic Address"
    )

    if st.button(
        "💾 Save Clinic Information"
    ):

        st.success(
            "Clinic information saved for this session."
        )

    st.divider()

    st.subheader(
        "🛠️ System Information"
    )

    st.write(
        "**Application:** AI-Dental Pro"
    )

    st.write(
        "**Developer:** Rashpreet Kaur Arora"
    )

    st.write(
        "**Course:** BCA 2nd Year"
    )

    st.write(
        "**Platform:** Streamlit"
    )

    st.write(
        "**Database:** SQLite"
    )

    st.write(
        "**AI:** Hugging Face"
    )

    st.write(
        "**Purpose:** Academic Prototype"
    )

    st.warning(
        "AI outputs are for educational assistance and "
        "analysis only. They should not be treated as "
        "professional medical advice."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🦷 <b>AI-Dental Pro</b><br>
        Intelligent Dental & Orthodontic Clinic Management System<br><br>
        Developed by <b>Rashpreet Kaur Arora</b> | BCA 2nd Year<br>
        Academic Prototype — AI-assisted analysis only
    </div>
    """,
    unsafe_allow_html=True
)
                    
