import streamlit as st
import database


# ============================================================
# AI-DENTAL PRO
# Intelligent Dental & Orthodontic Clinic Management System
# ============================================================
# Developed by: Rashpreet Kaur Arora
# BCA 2nd Year
# ============================================================


st.set_page_config(
    page_title="AI-Dental Pro",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE
# ============================================================

database.initialize_database()


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #eef9ff 0%,
        #f8f3ff 50%,
        #fff4f8 100%
    );
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 5px;
}

.developer {
    text-align: center;
    font-size: 14px;
    margin-bottom: 30px;
}

.card {
    padding: 22px;
    border-radius: 20px;
    background: white;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 20px;
}

.card-title {
    font-size: 18px;
    font-weight: 700;
}

.card-number {
    font-size: 32px;
    font-weight: 800;
}

.section-title {
    font-size: 28px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 20px;
}

.patient-card {
    padding: 20px;
    border-radius: 18px;
    background: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07);
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🦷 AI-DENTAL PRO</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent Dental & Orthodontic Clinic Management System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="developer">'
    'Developed by <b>Rashpreet Kaur Arora</b> | BCA 2nd Year'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🦷 AI-Dental Pro")

st.sidebar.markdown(
    "**Rashpreet Kaur Arora**"
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
# DASHBOARD
# ============================================================

if menu == "🏠 Dashboard":

    patients = database.get_patients()

    total_patients = len(patients)

    st.markdown(
        '<div class="section-title">'
        'Welcome to AI-Dental Pro 👋'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "A unified platform for dental care, orthodontic management, "
        "patient records, clinic operations and AI-assisted analysis."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">👥 Patients</div>
            <div class="card-number">{total_patients}</div>
            <div>Registered</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">📅 Appointments</div>
            <div class="card-number">0</div>
            <div>Today</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">🦷 Treatments</div>
            <div class="card-number">0</div>
            <div>Active Cases</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card">
            <div class="card-title">🤖 AI</div>
            <div class="card-number">4</div>
            <div>AI Services</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">✨ Quick Actions</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button(
            "👤 Register Patient",
            use_container_width=True
        ):
            st.info(
                "Open 👤 Patients → Register New Patient"
            )

    with q2:
        if st.button(
            "📅 Book Appointment",
            use_container_width=True
        ):
            st.info(
                "Appointment module will be added next."
            )

    with q3:
        if st.button(
            "🤖 Open AI Center",
            use_container_width=True
        ):
            st.info(
                "Hugging Face AI will be connected later."
            )


# ============================================================
# PATIENT MANAGEMENT
# ============================================================

elif menu == "👤 Patients":

    st.markdown(
        '<div class="section-title">'
        '👤 Patient Management'
        '</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs([
        "➕ Register Patient",
        "🔍 Search Patient",
        "📋 All Patients"
    ])


    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    with tab1:

        st.subheader("➕ New Patient Registration")

        with st.form("patient_form"):

            col1, col2 = st.columns(2)

            with col1:

                full_name = st.text_input(
                    "Full Name *"
                )

                date_of_birth = st.date_input(
                    "Date of Birth"
                )

                gender = st.selectbox(
                    "Gender",
                    [
                        "Female",
                        "Male",
                        "Other"
                    ]
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

            with col2:

                emergency_contact = st.text_input(
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
                        "Please enter the patient's name."
                    )

                else:

                    patient_id = database.add_patient(
                        full_name,
                        str(date_of_birth),
                        gender,
                        phone,
                        email,
                        emergency_contact,
                        dental_history,
                        allergies,
                        address,
                        blood_group
                    )

                    st.success(
                        f"✅ Patient registered successfully! "
                        f"Patient ID: {patient_id}"
                    )

                    st.balloons()


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    with tab2:

        st.subheader("🔍 Search Patient")

        search_text = st.text_input(
            "Search by Patient ID, Name or Phone"
        )

        if search_text:

            results = database.search_patients(
                search_text
            )

            if results:

                for patient in results:

                    st.markdown(
                        f"""
                        <div class="patient-card">
                        <h3>👤 {patient[1]}</h3>

                        <b>Patient ID:</b> {patient[0]}<br>
                        <b>Date of Birth:</b> {patient[2]}<br>
                        <b>Gender:</b> {patient[3]}<br>
                        <b>Phone:</b> {patient[4]}<br>
                        <b>Email:</b> {patient[5]}<br>
                        <b>Blood Group:</b> {patient[6]}<br>
                        <b>Registered:</b> {patient[7]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.warning(
                    "No patient found."
                )


    # --------------------------------------------------------
    # ALL PATIENTS
    # --------------------------------------------------------

    with tab3:

        st.subheader("📋 Registered Patients")

        patients = database.get_patients()

        if patients:

            import pandas as pd

            df = pd.DataFrame(
                patients,
                columns=[
                    "Patient ID",
                    "Name",
                    "Date of Birth",
                    "Gender",
                    "Phone",
                    "Email",
                    "Blood Group",
                    "Registration Date"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No patients have been registered yet."
            )


# ============================================================
# OTHER MODULES
# ============================================================

elif menu == "📅 Appointments":

    st.title("📅 Appointment Management")

    st.info(
        "Appointment module is the next development stage."
    )


elif menu == "🦷 Orthodontics":

    st.title("🦷 Orthodontic Management")

    st.info(
        "Braces, aligners, retainers and treatment "
        "tracking will be added."
    )


elif menu == "🪥 Dental Care":

    st.title("🪥 Dental Care")

    st.info(
        "Dental assessment and oral-hygiene features "
        "will be added."
    )


elif menu == "🔔 Reminders":

    st.title("🔔 Smart Reminders")

    st.info(
        "Smart reminders will be connected to appointments "
        "and dental-care records."
    )


elif menu == "💳 Billing":

    st.title("💳 Billing & Payments")

    st.info(
        "Billing and payment tracking will be added."
    )


elif menu == "📦 Inventory":

    st.title("📦 Clinic Inventory")

    st.info(
        "Inventory and equipment management will be added."
    )


elif menu == "🤖 AI Care Center":

    st.title("🤖 AI Care Center")

    st.info(
        "Hugging Face AI-assisted features will be "
        "integrated after the core database system."
    )


elif menu == "📊 Reports":

    st.title("📊 Reports & Analytics")

    st.info(
        "Clinic analytics and reports will be connected "
        "to the database."
    )


elif menu == "⚙️ Administration":

    st.title("⚙️ Administration")

    st.info(
        "Administrative controls will be added later."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    '🦷 AI-Dental Pro | Developed by '
    '<b>Rashpreet Kaur Arora</b>'
    '<br>'
    'Academic Prototype — AI-assisted analysis only'
    '</div>',
    unsafe_allow_html=True
)
