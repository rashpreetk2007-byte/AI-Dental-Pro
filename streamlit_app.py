import streamlit as st

# ============================================================
# AI-DENTAL PRO
# Intelligent Dental & Orthodontic Clinic Management System
# ============================================================
# Developed by: Rashpreet Kaur Arora
# Technology: Python + Streamlit
# ============================================================

st.set_page_config(
    page_title="AI-Dental Pro",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------

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
    margin-bottom: 25px;
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
    margin-top: 8px;
}

.section-title {
    font-size: 26px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    padding: 20px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------

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


# -----------------------------
# Sidebar
# -----------------------------

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


# -----------------------------
# Dashboard
# -----------------------------

if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">Welcome to AI-Dental Pro 👋</div>',
        unsafe_allow_html=True
    )

    st.write(
        "A unified platform for dental care, orthodontic management, "
        "patient records, clinic operations and AI-assisted analysis."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">👥 Patients</div>
            <div class="card-number">248</div>
            <div>Registered</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">📅 Appointments</div>
            <div class="card-number">18</div>
            <div>Today</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">🦷 Treatments</div>
            <div class="card-number">126</div>
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
        if st.button("👤 Register Patient", use_container_width=True):
            st.info("Patient registration module will be connected next.")

    with q2:
        if st.button("📅 Book Appointment", use_container_width=True):
            st.info("Appointment module will be connected next.")

    with q3:
        if st.button("🤖 Open AI Center", use_container_width=True):
            st.info("Hugging Face AI module will be connected later.")


# -----------------------------
# Other sections
# -----------------------------

elif menu == "👤 Patients":
    st.title("👤 Patient Management")
    st.info("Patient registration and records module — coming next.")

elif menu == "📅 Appointments":
    st.title("📅 Appointment Management")
    st.info("Appointment and queue module — coming next.")

elif menu == "🦷 Orthodontics":
    st.title("🦷 Orthodontic Management")
    st.info("Braces, aligners and treatment tracking — coming next.")

elif menu == "🪥 Dental Care":
    st.title("🪥 Dental Care")
    st.info("Dental health and hygiene module — coming next.")

elif menu == "🔔 Reminders":
    st.title("🔔 Smart Reminders")
    st.info("Appointment and dental-care reminders — coming next.")

elif menu == "💳 Billing":
    st.title("💳 Billing & Payments")
    st.info("Billing, invoices and installment tracking — coming next.")

elif menu == "📦 Inventory":
    st.title("📦 Clinic Inventory")
    st.info("Inventory and equipment management — coming next.")

elif menu == "🤖 AI Care Center":
    st.title("🤖 AI Care Center")
    st.info(
        "Hugging Face-powered AI-assisted analysis will be integrated "
        "after the core system is completed."
    )

elif menu == "📊 Reports":
    st.title("📊 Clinic Reports & Analytics")
    st.info("Reports and analytics will be connected next.")

elif menu == "⚙️ Administration":
    st.title("⚙️ Administration")
    st.info("Admin controls will be connected later.")


# -----------------------------
# Footer
# -----------------------------

st.markdown(
    '<div class="footer">'
    '🦷 AI-Dental Pro | Developed by '
    '<b>Rashpreet Kaur Arora</b>'
    '<br>'
    'Academic Prototype — AI-assisted analysis only'
    '</div>',
    unsafe_allow_html=True
)
