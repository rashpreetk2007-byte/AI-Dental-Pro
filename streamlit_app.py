import streamlit as st
import sqlite3
import pandas as pd
import requests
from datetime import datetime, date, timedelta
from pathlib import Path

# ============================================================
# AI-DENTAL PRO
# 99-FEATURE DENTAL & ORTHODONTIC CLINIC SYSTEM
# Developed by Rashpreet Kaur Arora | BCA 2nd Year
# Academic prototype - AI is assistance/analysis only.
# ============================================================

st.set_page_config(
    page_title="AI-Dental Pro",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_NAME = "dental_clinic.db"

# ------------------------- DATABASE -------------------------

def db():
    return sqlite3.connect(DB_NAME)

def execute(query, params=(), fetch=False):
    conn = db()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result

def scalar(query, params=()):
    conn = db()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def initialize_database():
    conn = db()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT UNIQUE, full_name TEXT NOT NULL,
        date_of_birth TEXT, gender TEXT, phone TEXT, email TEXT,
        emergency_contact TEXT, dental_history TEXT, allergies TEXT,
        address TEXT, blood_group TEXT, registration_date TEXT,
        occupation TEXT, guardian_name TEXT, notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id TEXT UNIQUE, patient_id TEXT, doctor_name TEXT,
        appointment_type TEXT, appointment_date TEXT,
        appointment_time TEXT, token_number INTEGER,
        status TEXT DEFAULT 'Scheduled', notes TEXT, created_at TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS treatments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        treatment_id TEXT UNIQUE, patient_id TEXT, treatment_type TEXT,
        treatment_name TEXT, treatment_date TEXT, dentist_name TEXT,
        cost REAL DEFAULT 0, notes TEXT, status TEXT DEFAULT 'Active')""")

    cur.execute("""CREATE TABLE IF NOT EXISTS orthodontic_cases(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT UNIQUE, patient_id TEXT, treatment_type TEXT,
        start_date TEXT, expected_end_date TEXT, progress INTEGER DEFAULT 0,
        current_stage TEXT, notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS followups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        followup_id TEXT UNIQUE, patient_id TEXT, followup_date TEXT,
        treatment_stage TEXT, progress INTEGER DEFAULT 0, notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS prescriptions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prescription_id TEXT UNIQUE, patient_id TEXT,
        prescription_date TEXT, medicine TEXT, instructions TEXT,
        dentist_name TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS xray_records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        xray_id TEXT UNIQUE, patient_id TEXT, xray_date TEXT,
        xray_type TEXT, file_name TEXT, notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS reminders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reminder_id TEXT UNIQUE, patient_id TEXT, reminder_type TEXT,
        reminder_date TEXT, message TEXT, status TEXT DEFAULT 'Pending')""")

    cur.execute("""CREATE TABLE IF NOT EXISTS bills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id TEXT UNIQUE, patient_id TEXT, bill_date TEXT,
        description TEXT, total_amount REAL DEFAULT 0,
        paid_amount REAL DEFAULT 0, balance REAL DEFAULT 0,
        status TEXT DEFAULT 'Pending')""")

    cur.execute("""CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_id TEXT UNIQUE, bill_id TEXT, patient_id TEXT,
        payment_date TEXT, amount REAL DEFAULT 0,
        payment_method TEXT, notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS insurance_claims(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        claim_id TEXT UNIQUE, patient_id TEXT, insurance_company TEXT,
        policy_number TEXT, claim_amount REAL DEFAULT 0,
        claim_date TEXT, status TEXT DEFAULT 'Pending', notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id TEXT UNIQUE, item_name TEXT NOT NULL, category TEXT,
        quantity INTEGER DEFAULT 0, minimum_stock INTEGER DEFAULT 5,
        unit_price REAL DEFAULT 0, supplier TEXT, last_updated TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS equipment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipment_id TEXT UNIQUE, equipment_name TEXT NOT NULL,
        category TEXT, purchase_date TEXT, last_maintenance TEXT,
        next_maintenance TEXT, status TEXT DEFAULT 'Operational',
        notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feedback_id TEXT UNIQUE, patient_id TEXT, rating INTEGER,
        feedback_text TEXT, sentiment TEXT, feedback_date TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS ai_analysis(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id TEXT UNIQUE, patient_id TEXT, analysis_type TEXT,
        file_name TEXT, result TEXT, confidence REAL,
        analysis_date TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS hygiene_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT, log_date TEXT, brushing INTEGER DEFAULT 0,
        flossing INTEGER DEFAULT 0, mouthwash INTEGER DEFAULT 0,
        notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS health_assessments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id TEXT UNIQUE, patient_id TEXT, assessment_date TEXT,
        pain_level INTEGER, sensitivity TEXT, bleeding TEXT,
        swelling TEXT, tobacco TEXT, sugary_frequency TEXT,
        brushing_frequency TEXT, risk_level TEXT, notes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS diet_plans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id TEXT UNIQUE, patient_id TEXT, plan_date TEXT,
        goal TEXT, recommendations TEXT, restrictions TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_id TEXT UNIQUE, expense_date TEXT, category TEXT,
        description TEXT, amount REAL DEFAULT 0)""")

    conn.commit()
    conn.close()

initialize_database()

def new_id(prefix, table):
    n = scalar(f"SELECT COUNT(*) FROM {table}")
    return f"{prefix}{1001+n}"

def patients():
    return execute(
        "SELECT patient_id, full_name FROM patients ORDER BY full_name",
        fetch=True
    )

def label_patient(x):
    return f"{x[0]} — {x[1]}"

def patient_name(pid):
    r = execute("SELECT full_name FROM patients WHERE patient_id=?", (pid,), True)
    return r[0][0] if r else "Unknown"

def safe_insert(query, params):
    try:
        execute(query, params)
        return True, ""
    except sqlite3.IntegrityError as e:
        return False, str(e)

# --------------------------- STYLE ---------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#eafaff 0%,#f7f0ff 48%,#fff1f6 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#ffffff,#edf7ff);
}
.hero {
    padding:28px;
    border-radius:26px;
    background:linear-gradient(135deg,#ffffff,#f8f3ff);
    box-shadow:0 8px 28px rgba(0,0,0,.08);
    text-align:center;
    margin-bottom:22px;
    border:1px solid #eee;
}
.hero h1 {font-size:42px;margin:0 0 6px 0;}
.hero p {font-size:17px;}
.card {
    background:white;padding:20px;border-radius:20px;
    box-shadow:0 5px 18px rgba(0,0,0,.07);margin-bottom:14px;
}
.metric {
    background:white;padding:20px;border-radius:20px;
    text-align:center;box-shadow:0 5px 18px rgba(0,0,0,.07);
}
.metric b {font-size:32px;}
.section {font-size:28px;font-weight:800;margin:8px 0 20px;}
.small {font-size:13px;color:#666;}
</style>
""", unsafe_allow_html=True)

# -------------------------- SIDEBAR --------------------------

st.sidebar.markdown("<h1 style='text-align:center'>🦷</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align:center'>AI-Dental Pro</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center'><b>Rashpreet Kaur Arora</b><br>BCA 2nd Year</p>", unsafe_allow_html=True)
st.sidebar.divider()

menu = st.sidebar.radio("Navigation", [
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
])

st.markdown("""
<div class="hero">
<h1>🦷 AI-DENTAL PRO</h1>
<p>Intelligent Dental & Orthodontic Clinic Management System</p>
<p><b>Developed by Rashpreet Kaur Arora | BCA 2nd Year</b></p>
<p class="small">Academic Prototype • AI-assisted analysis only • Not a diagnosis or prescription system</p>
</div>
""", unsafe_allow_html=True)

# =========================== DASHBOARD ===========================

if menu == "🏠 Dashboard":
    st.markdown('<div class="section">📊 Clinic Dashboard</div>', unsafe_allow_html=True)

    vals = [
        ("👥 Patients", scalar("SELECT COUNT(*) FROM patients"), "Registered"),
        ("📅 Appointments", scalar("SELECT COUNT(*) FROM appointments WHERE appointment_date=?", (str(date.today()),)), "Today"),
        ("🦷 Active Treatments", scalar("SELECT COUNT(*) FROM treatments WHERE status='Active'"), "Cases"),
        ("😁 Orthodontics", scalar("SELECT COUNT(*) FROM orthodontic_cases"), "Cases"),
        ("💰 Revenue", scalar("SELECT COALESCE(SUM(amount),0) FROM payments"), "Payments"),
        ("⚠️ Low Stock", scalar("SELECT COUNT(*) FROM inventory WHERE quantity<=minimum_stock"), "Items"),
    ]
    cols = st.columns(3)
    for i,(a,b,c) in enumerate(vals):
        with cols[i%3]:
            st.markdown(f"<div class='metric'><div>{a}</div><b>{b}</b><div>{c}</div></div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📅 Today's Appointments")
    rows = execute("""SELECT a.appointment_id,a.patient_id,p.full_name,a.doctor_name,
                     a.appointment_type,a.appointment_time,a.token_number,a.status
                     FROM appointments a LEFT JOIN patients p ON a.patient_id=p.patient_id
                     WHERE a.appointment_date=? ORDER BY a.appointment_time""",
                   (str(date.today()),), True)
    if rows:
        st.dataframe(pd.DataFrame(rows,columns=["ID","Patient ID","Patient","Doctor","Type","Time","Token","Status"]),
                     use_container_width=True,hide_index=True)
    else:
        st.info("No appointments scheduled for today.")

# =========================== PATIENTS ===========================

elif menu == "👤 Patients":
    st.markdown('<div class="section">👤 Patient Management</div>', unsafe_allow_html=True)
    t1,t2,t3,t4 = st.tabs(["➕ Register","🔍 Search","📋 All Patients","👁️ Profile"])

    with t1:
        with st.form("register_patient"):
            c1,c2 = st.columns(2)
            with c1:
                name=st.text_input("Full Name *")
                dob=st.date_input("Date of Birth",date(2000,1,1))
                gender=st.selectbox("Gender",["Female","Male","Other"])
                phone=st.text_input("Phone")
                email=st.text_input("Email")
                blood=st.selectbox("Blood Group",["Unknown","A+","A-","B+","B-","AB+","AB-","O+","O-"])
                occupation=st.text_input("Occupation")
            with c2:
                guardian=st.text_input("Guardian / Parent")
                emergency=st.text_input("Emergency Contact")
                address=st.text_area("Address")
                history=st.text_area("Dental History")
                allergies=st.text_area("Allergies")
                notes=st.text_area("Additional Notes")
            submit=st.form_submit_button("💾 Register Patient",use_container_width=True)
        if submit:
            if not name.strip():
                st.error("Full name is required.")
            else:
                pid=new_id("DP","patients")
                ok,err=safe_insert("""INSERT INTO patients
                (patient_id,full_name,date_of_birth,gender,phone,email,emergency_contact,
                 dental_history,allergies,address,blood_group,registration_date,occupation,guardian_name,notes)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                 (pid,name,str(dob),gender,phone,email,emergency,history,allergies,address,blood,
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),occupation,guardian,notes))
                if ok:
                    st.success(f"Patient registered: {pid}")
                else: st.error(err)

    with t2:
        q=st.text_input("Search by ID, name or phone")
        if q:
            rows=execute("""SELECT patient_id,full_name,date_of_birth,gender,phone,email,blood_group,registration_date
                            FROM patients WHERE patient_id LIKE ? OR full_name LIKE ? OR phone LIKE ?
                            ORDER BY id DESC""",(f"%{q}%",f"%{q}%",f"%{q}%"),True)
            if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Name","DOB","Gender","Phone","Email","Blood","Registered"]),use_container_width=True,hide_index=True)
            else: st.warning("No patient found.")

    with t3:
        rows=execute("""SELECT patient_id,full_name,date_of_birth,gender,phone,email,blood_group,registration_date
                        FROM patients ORDER BY id DESC""",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Name","DOB","Gender","Phone","Email","Blood","Registered"]),use_container_width=True,hide_index=True)
        else: st.info("No patients registered yet.")

    with t4:
        ps=patients()
        if not ps: st.info("Register a patient first.")
        else:
            p=st.selectbox("Select patient",ps,format_func=label_patient,key="profile_patient")
            pid=p[0]
            row=execute("""SELECT full_name,date_of_birth,gender,phone,email,emergency_contact,
                           dental_history,allergies,address,blood_group,registration_date,occupation,guardian_name,notes
                           FROM patients WHERE patient_id=?""",(pid,),True)[0]
            st.markdown(f"<div class='card'><h2>👤 {row[0]}</h2><b>ID:</b> {pid}<br><b>DOB:</b> {row[1]}<br><b>Gender:</b> {row[2]}<br><b>Phone:</b> {row[3]}<br><b>Email:</b> {row[4]}<br><b>Emergency:</b> {row[5]}<br><b>Blood:</b> {row[9]}<br><b>Occupation:</b> {row[11]}<br><b>Guardian:</b> {row[12]}</div>",unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                st.subheader("🦷 Dental History")
                st.write(row[6] or "None recorded")
                st.subheader("⚠️ Allergies")
                st.write(row[7] or "None recorded")
            with c2:
                st.subheader("📍 Address")
                st.write(row[8] or "None recorded")
                st.subheader("📝 Notes")
                st.write(row[13] or "None recorded")

# ========================= APPOINTMENTS =========================

elif menu == "📅 Appointments":
    st.markdown('<div class="section">📅 Appointment & Queue Management</div>',unsafe_allow_html=True)
    t1,t2,t3,t4=st.tabs(["➕ Schedule","📋 List","🎫 Queue","❌ Manage"])
    ps=patients()

    with t1:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("appointment"):
                p=st.selectbox("Patient",ps,format_func=label_patient)
                c1,c2=st.columns(2)
                with c1:
                    doctor=st.text_input("Dentist / Orthodontist")
                    typ=st.selectbox("Appointment Type",["Dental Consultation","Dental Cleaning","Dental Treatment","Orthodontic Consultation","Braces Follow-up","Clear Aligner Follow-up","Retainer Check-up","Emergency Dental Visit","General Follow-up"])
                    ad=st.date_input("Date",date.today())
                with c2:
                    at=st.time_input("Time")
                    token=st.number_input("Queue Token",1,999,1)
                    notes=st.text_area("Notes")
                ok=st.form_submit_button("📅 Schedule",use_container_width=True)
            if ok:
                aid=new_id("APT","appointments")
                duplicate=scalar("""SELECT COUNT(*) FROM appointments WHERE appointment_date=? AND appointment_time=? AND doctor_name=? AND status NOT IN ('Cancelled','Completed')""",(str(ad),str(at),doctor))
                if duplicate: st.error("Doctor already has an active appointment at this time.")
                else:
                    good,err=safe_insert("""INSERT INTO appointments(appointment_id,patient_id,doctor_name,appointment_type,appointment_date,appointment_time,token_number,status,notes,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                    (aid,p[0],doctor,typ,str(ad),str(at),int(token),"Scheduled",notes,datetime.now().isoformat()))
                    if good: st.success(f"Scheduled {aid}")
                    else: st.error(err)

    with t2:
        d=st.date_input("Filter date",date.today(),key="appt_filter")
        rows=execute("""SELECT a.appointment_id,a.patient_id,p.full_name,a.doctor_name,a.appointment_type,
                        a.appointment_date,a.appointment_time,a.token_number,a.status,a.notes
                        FROM appointments a LEFT JOIN patients p ON a.patient_id=p.patient_id
                        WHERE a.appointment_date=? ORDER BY a.appointment_time""",(str(d),),True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Patient ID","Patient","Doctor","Type","Date","Time","Token","Status","Notes"]),use_container_width=True,hide_index=True)
        else: st.info("No appointments.")

    with t3:
        rows=execute("""SELECT a.appointment_id,a.token_number,p.full_name,a.appointment_type,a.appointment_time,a.doctor_name,a.status
                        FROM appointments a LEFT JOIN patients p ON a.patient_id=p.patient_id
                        WHERE a.appointment_date=? ORDER BY a.token_number""",(str(date.today()),),True)
        if not rows: st.info("Today's queue is empty.")
        for r in rows:
            st.markdown(f"<div class='card'><h3>🎫 Token #{r[1]} — {r[2]}</h3><b>Type:</b> {r[3]} &nbsp; <b>Time:</b> {r[4]} &nbsp; <b>Doctor:</b> {r[5]}<br><b>Status:</b> {r[6]}</div>",unsafe_allow_html=True)
            if r[6] in ("Scheduled","In Progress"):
                c1,c2=st.columns(2)
                with c1:
                    if st.button("▶️ Start",key="start_"+r[0]):
                        execute("UPDATE appointments SET status='In Progress' WHERE appointment_id=?",(r[0],)); st.rerun()
                with c2:
                    if st.button("✅ Complete",key="done_"+r[0]):
                        execute("UPDATE appointments SET status='Completed' WHERE appointment_id=?",(r[0],)); st.rerun()

    with t4:
        rows=execute("SELECT appointment_id,patient_id,appointment_date,appointment_time,status FROM appointments ORDER BY id DESC LIMIT 200",fetch=True)
        if rows:
            opts=[f"{r[0]} | {r[1]} | {r[2]} {r[3]} | {r[4]}" for r in rows]
            sel=st.selectbox("Appointment",opts)
            r=rows[opts.index(sel)]
            status=st.selectbox("New Status",["Scheduled","In Progress","Completed","Cancelled","No Show"])
            reason=st.text_area("Reason / note")
            if st.button("💾 Update Status",use_container_width=True):
                execute("UPDATE appointments SET status=?,notes=? WHERE appointment_id=?",(status,reason,r[0]))
                st.success("Appointment updated.")
                st.rerun()
        else: st.info("No appointments.")

# ========================= ORTHODONTICS =========================

elif menu == "🦷 Orthodontics":
    st.markdown('<div class="section">🦷 Orthodontic Treatment Center</div>',unsafe_allow_html=True)
    t1,t2,t3,t4=st.tabs(["➕ Case","📈 Progress","🔄 Follow-ups","📋 Timeline"])
    ps=patients()

    with t1:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("ortho_case"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="ortho_patient")
                typ=st.selectbox("Treatment",["Braces","Clear Aligners","Retainer","Orthodontic Observation"])
                sd=st.date_input("Start Date",date.today())
                ed=st.date_input("Expected End Date",date.today()+timedelta(days=365))
                progress=st.slider("Progress %",0,100,0)
                stage=st.selectbox("Current Stage",["Assessment","Planning","Active Treatment","Adjustment","Retention","Completed"])
                notes=st.text_area("Case Notes")
                save=st.form_submit_button("💾 Create Case",use_container_width=True)
            if save:
                cid=new_id("ORTH","orthodontic_cases")
                good,err=safe_insert("""INSERT INTO orthodontic_cases(case_id,patient_id,treatment_type,start_date,expected_end_date,progress,current_stage,notes) VALUES(?,?,?,?,?,?,?,?)""",(cid,p[0],typ,str(sd),str(ed),progress,stage,notes))
                if good: st.success(f"Case created: {cid}")
                else: st.error(err)

    with t2:
        rows=execute("""SELECT o.case_id,o.patient_id,p.full_name,o.treatment_type,o.progress,o.current_stage,o.expected_end_date
                        FROM orthodontic_cases o LEFT JOIN patients p ON o.patient_id=p.patient_id ORDER BY o.id DESC""",fetch=True)
        if rows:
            st.dataframe(pd.DataFrame(rows,columns=["Case","Patient ID","Patient","Treatment","Progress %","Stage","Expected End"]),use_container_width=True,hide_index=True)
            opts=[f"{r[0]} — {r[2]}" for r in rows]
            sel=st.selectbox("Update case",opts)
            r=rows[opts.index(sel)]
            np=st.slider("New Progress %",0,100,int(r[4]),key="new_ortho_progress")
            ns=st.selectbox("New Stage",["Assessment","Planning","Active Treatment","Adjustment","Retention","Completed"],index=["Assessment","Planning","Active Treatment","Adjustment","Retention","Completed"].index(r[5]))
            if st.button("💾 Update Orthodontic Progress"):
                execute("UPDATE orthodontic_cases SET progress=?,current_stage=? WHERE case_id=?",(np,ns,r[0]))
                st.success("Progress updated.")
                st.rerun()
        else: st.info("No orthodontic cases.")

    with t3:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("followup"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="follow_patient")
                fd=st.date_input("Follow-up Date",date.today())
                stage=st.text_input("Treatment Stage")
                prog=st.slider("Progress %",0,100,0,key="follow_progress")
                notes=st.text_area("Follow-up Notes")
                save=st.form_submit_button("💾 Save Follow-up",use_container_width=True)
            if save:
                fid=new_id("FUP","followups")
                good,err=safe_insert("INSERT INTO followups(followup_id,patient_id,followup_date,treatment_stage,progress,notes) VALUES(?,?,?,?,?,?)",(fid,p[0],str(fd),stage,prog,notes))
                if good: st.success(f"Follow-up saved: {fid}")
                else: st.error(err)
        rows=execute("""SELECT f.followup_id,f.patient_id,p.full_name,f.followup_date,f.treatment_stage,f.progress,f.notes
                        FROM followups f LEFT JOIN patients p ON f.patient_id=p.patient_id ORDER BY f.id DESC""",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Patient ID","Patient","Date","Stage","Progress %","Notes"]),use_container_width=True,hide_index=True)

    with t4:
        if ps:
            p=st.selectbox("Patient",ps,format_func=label_patient,key="timeline_patient")
            pid=p[0]
            rows=execute("""SELECT treatment_date,treatment_name,treatment_type,status FROM treatments WHERE patient_id=?
                            UNION ALL SELECT followup_date,treatment_stage,'Orthodontic Follow-up','Recorded' FROM followups WHERE patient_id=?
                            ORDER BY 1 DESC""",(pid,pid),True)
            if rows: st.dataframe(pd.DataFrame(rows,columns=["Date","Event","Type","Status"]),use_container_width=True,hide_index=True)
            else: st.info("No treatment timeline yet.")

# =========================== DENTAL CARE ===========================

elif menu == "🪥 Dental Care":
    st.markdown('<div class="section">🪥 Dental Care & Oral Health</div>',unsafe_allow_html=True)
    t1,t2,t3,t4,t5=st.tabs(["📝 Assessment","🦷 Treatments","💊 Prescriptions","🩻 X-Ray Records","🥗 Diet & Education"])
    ps=patients()

    with t1:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("assessment"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="assessment_patient")
                pain=st.slider("Pain level",0,10,0)
                sensitivity=st.selectbox("Tooth sensitivity",["No","Occasional","Frequent"])
                bleeding=st.selectbox("Gum bleeding",["No","Sometimes","Frequent"])
                swelling=st.selectbox("Swelling",["No","Yes"])
                tobacco=st.selectbox("Tobacco exposure",["No","Yes","Prefer not to say"])
                sugar=st.selectbox("Sugary food/drink frequency",["Low","Moderate","High"])
                brushing=st.selectbox("Brushing frequency",["Less than once daily","Once daily","Twice daily","More than twice daily"])
                notes=st.text_area("Notes")
                save=st.form_submit_button("📊 Save Assessment",use_container_width=True)
            if save:
                risk="Low"
                score=pain
                if sensitivity=="Frequent": score+=2
                if bleeding=="Frequent": score+=2
                if swelling=="Yes": score+=2
                if tobacco=="Yes": score+=2
                if sugar=="High": score+=1
                if score>=7: risk="High"
                elif score>=4: risk="Moderate"
                aid=new_id("ASM","health_assessments")
                execute("""INSERT INTO health_assessments(assessment_id,patient_id,assessment_date,pain_level,sensitivity,bleeding,swelling,tobacco,sugary_frequency,brushing_frequency,risk_level,notes)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",(aid,p[0],str(date.today()),pain,sensitivity,bleeding,swelling,tobacco,sugar,brushing,risk,notes))
                st.success(f"Assessment saved. Educational risk category: {risk}")

    with t2:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("treatment"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="treatment_patient")
                typ=st.selectbox("Treatment Type",["Preventive","Restorative","Cleaning","Orthodontic","Cosmetic","Emergency","General"])
                name=st.text_input("Treatment Name")
                td=st.date_input("Treatment Date",date.today())
                dentist=st.text_input("Dentist")
                cost=st.number_input("Cost (₹)",0.0,1000000.0,0.0)
                notes=st.text_area("Notes")
                status=st.selectbox("Status",["Active","Completed","Planned","Cancelled"])
                save=st.form_submit_button("💾 Save Treatment",use_container_width=True)
            if save:
                if not name.strip(): st.error("Treatment name required.")
                else:
                    tid=new_id("TRT","treatments")
                    execute("INSERT INTO treatments(treatment_id,patient_id,treatment_type,treatment_name,treatment_date,dentist_name,cost,notes,status) VALUES(?,?,?,?,?,?,?,?,?)",(tid,p[0],typ,name,str(td),dentist,cost,notes,status))
                    st.success(f"Treatment saved: {tid}")
            rows=execute("""SELECT t.treatment_id,t.patient_id,p.full_name,treatment_type,treatment_name,treatment_date,dentist_name,cost,status
                            FROM treatments t LEFT JOIN patients p ON t.patient_id=p.patient_id ORDER BY t.id DESC""",fetch=True)
            if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Patient ID","Patient","Type","Treatment","Date","Dentist","Cost","Status"]),use_container_width=True,hide_index=True)

    with t3:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("prescription"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="rx_patient")
                med=st.text_input("Medicine / Product name")
                instr=st.text_area("Instructions")
                dentist=st.text_input("Dentist",key="rx_dentist")
                save=st.form_submit_button("💾 Save Record",use_container_width=True)
            if save:
                rid=new_id("RX","prescriptions")
                execute("INSERT INTO prescriptions(prescription_id,patient_id,prescription_date,medicine,instructions,dentist_name) VALUES(?,?,?,?,?,?)",(rid,p[0],str(date.today()),med,instr,dentist))
                st.success(f"Prescription record saved: {rid}")
                st.caption("Record keeping only; this prototype does not prescribe medicines.")
            rows=execute("""SELECT r.prescription_id,r.patient_id,p.full_name,r.prescription_date,r.medicine,r.instructions,r.dentist_name
                            FROM prescriptions r LEFT JOIN patients p ON r.patient_id=p.patient_id ORDER BY r.id DESC""",fetch=True)
            if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Patient ID","Patient","Date","Medicine","Instructions","Dentist"]),use_container_width=True,hide_index=True)

    with t4:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("xray"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="xray_patient")
                xd=st.date_input("X-Ray Date",date.today())
                xt=st.selectbox("X-Ray Type",["Panoramic","Intraoral","Cephalometric","Other"])
                fn=st.text_input("File name / reference")
                notes=st.text_area("Notes")
                save=st.form_submit_button("💾 Save X-Ray Record",use_container_width=True)
            if save:
                xid=new_id("XR","xray_records")
                execute("INSERT INTO xray_records(xray_id,patient_id,xray_date,xray_type,file_name,notes) VALUES(?,?,?,?,?,?)",(xid,p[0],str(xd),xt,fn,notes))
                st.success(f"X-Ray record saved: {xid}")
            rows=execute("""SELECT x.xray_id,x.patient_id,p.full_name,x.xray_date,x.xray_type,x.file_name,x.notes
                            FROM xray_records x LEFT JOIN patients p ON x.patient_id=p.patient_id ORDER BY x.id DESC""",fetch=True)
            if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Patient ID","Patient","Date","Type","File","Notes"]),use_container_width=True,hide_index=True)

    with t5:
        st.subheader("🥗 Educational Dental Diet & Hygiene Guide")
        st.info("Educational information only. Individual dietary or medical decisions should be discussed with a qualified dental professional.")
        st.markdown("""
        **General oral-health habits**
        - Brush twice daily with fluoride toothpaste.
        - Clean between teeth regularly.
        - Limit frequent sugary snacks and drinks.
        - Drink water regularly.
        - Follow the cleaning and follow-up schedule given by your dental professional.

        **Braces / aligner care**
        - Follow the orthodontic provider's instructions.
        - Avoid foods that the provider specifically restricts.
        - Keep appliances clean.
        - Do not make treatment changes based on this application.
        """)

        if ps:
            with st.form("diet_plan"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="diet_patient")
                goal=st.selectbox("Goal",["General Oral Hygiene","Braces Care","Aligner Care","Healthy Eating"])
                rec=st.text_area("Recommendations")
                restrictions=st.text_area("Food / habit restrictions")
                save=st.form_submit_button("💾 Save Education Plan")
            if save:
                did=new_id("DIET","diet_plans")
                execute("INSERT INTO diet_plans(plan_id,patient_id,plan_date,goal,recommendations,restrictions) VALUES(?,?,?,?,?,?)",(did,p[0],str(date.today()),goal,rec,restrictions))
                st.success(f"Education plan saved: {did}")

# =========================== REMINDERS ===========================

elif menu == "🔔 Reminders":
    st.markdown('<div class="section">🔔 Smart Reminder Center</div>',unsafe_allow_html=True)
    t1,t2=st.tabs(["➕ Create Reminder","📋 Reminder List"])
    ps=patients()

    with t1:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("reminder"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="reminder_patient")
                rt=st.selectbox("Reminder Type",["Appointment","Dental Cleaning","Toothbrush Replacement","Oral Hygiene","Braces Care","Aligner Wear","Retainer Usage","Follow-up","Payment"])
                rd=st.date_input("Reminder Date",date.today()+timedelta(days=1))
                msg=st.text_area("Message")
                save=st.form_submit_button("🔔 Create Reminder",use_container_width=True)
            if save:
                rid=new_id("REM","reminders")
                execute("INSERT INTO reminders(reminder_id,patient_id,reminder_type,reminder_date,message,status) VALUES(?,?,?,?,?,?)",(rid,p[0],rt,str(rd),msg,"Pending"))
                st.success(f"Reminder created: {rid}")

    with t2:
        rows=execute("""SELECT r.reminder_id,r.patient_id,p.full_name,r.reminder_type,r.reminder_date,r.message,r.status
                        FROM reminders r LEFT JOIN patients p ON r.patient_id=p.patient_id ORDER BY r.reminder_date""",fetch=True)
        if rows:
            st.dataframe(pd.DataFrame(rows,columns=["ID","Patient ID","Patient","Type","Date","Message","Status"]),use_container_width=True,hide_index=True)
            opts=[f"{r[0]} — {r[2]} — {r[4]}" for r in rows]
            sel=st.selectbox("Update reminder",opts)
            r=rows[opts.index(sel)]
            ns=st.selectbox("Status",["Pending","Completed","Cancelled"])
            if st.button("💾 Update Reminder"):
                execute("UPDATE reminders SET status=? WHERE reminder_id=?",(ns,r[0]))
                st.success("Updated.")
                st.rerun()
        else: st.info("No reminders.")

# ============================ BILLING ============================

elif menu == "💳 Billing":
    st.markdown('<div class="section">💳 Billing, Payments & Insurance</div>',unsafe_allow_html=True)
    t1,t2,t3,t4=st.tabs(["🧾 Bills","💵 Payments","📊 Installments","🛡️ Insurance"])
    ps=patients()

    with t1:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("bill"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="bill_patient")
                desc=st.text_input("Bill Description")
                total=st.number_input("Total Amount (₹)",0.0,10000000.0,0.0)
                paid=st.number_input("Initial Paid Amount (₹)",0.0,10000000.0,0.0)
                save=st.form_submit_button("🧾 Create Bill",use_container_width=True)
            if save:
                if paid>total: st.error("Paid amount cannot exceed total.")
                else:
                    bid=new_id("BILL","bills")
                    bal=total-paid
                    status="Paid" if bal==0 else ("Partially Paid" if paid>0 else "Pending")
                    execute("INSERT INTO bills(bill_id,patient_id,bill_date,description,total_amount,paid_amount,balance,status) VALUES(?,?,?,?,?,?,?,?)",(bid,p[0],str(date.today()),desc,total,paid,bal,status))
                    st.success(f"Bill created: {bid}")

            rows=execute("""SELECT b.bill_id,b.patient_id,p.full_name,b.bill_date,b.description,b.total_amount,b.paid_amount,b.balance,b.status
                            FROM bills b LEFT JOIN patients p ON b.patient_id=p.patient_id ORDER BY b.id DESC""",fetch=True)
            if rows: st.dataframe(pd.DataFrame(rows,columns=["Bill","Patient ID","Patient","Date","Description","Total","Paid","Balance","Status"]),use_container_width=True,hide_index=True)

    with t2:
        bills=execute("SELECT bill_id,patient_id FROM bills WHERE balance>0 ORDER BY id DESC",fetch=True)
        if not bills: st.info("No outstanding bills.")
        else:
            opts=[f"{r[0]} — {r[1]}" for r in bills]
            sel=st.selectbox("Bill",opts)
            b=bills[opts.index(sel)]
            amount=st.number_input("Payment Amount (₹)",0.0,10000000.0,0.0)
            method=st.selectbox("Payment Method",["Cash","UPI","Card","Bank Transfer","Other"])
            notes=st.text_area("Payment Notes")
            if st.button("💵 Record Payment",use_container_width=True):
                balance=scalar("SELECT balance FROM bills WHERE bill_id=?",(b[0],))
                if amount<=0: st.error("Enter a payment amount.")
                elif amount>balance: st.error("Payment exceeds outstanding balance.")
                else:
                    payid=new_id("PAY","payments")
                    execute("INSERT INTO payments(payment_id,bill_id,patient_id,payment_date,amount,payment_method,notes) SELECT ?,bill_id,patient_id,?,?,?,?,? FROM bills WHERE bill_id=?",(payid,str(date.today()),amount,method,notes,b[0]))
                    # Correct the bill using a direct update.
                    new_paid=scalar("SELECT paid_amount FROM bills WHERE bill_id=?",(b[0],))+amount
                    new_balance=balance-amount
                    status="Paid" if new_balance<=0 else "Partially Paid"
                    execute("UPDATE bills SET paid_amount=?,balance=?,status=? WHERE bill_id=?",(new_paid,new_balance,status,b[0]))
                    st.success(f"Payment recorded: {payid}")
                    st.rerun()

    with t3:
        rows=execute("""SELECT b.bill_id,b.patient_id,p.full_name,b.total_amount,b.paid_amount,b.balance,b.status
                        FROM bills b LEFT JOIN patients p ON b.patient_id=p.patient_id ORDER BY b.id DESC""",fetch=True)
        if rows:
            st.subheader("Installment / Balance Tracking")
            st.dataframe(pd.DataFrame(rows,columns=["Bill","Patient ID","Patient","Total","Paid","Balance","Status"]),use_container_width=True,hide_index=True)
        else: st.info("No bills.")

    with t4:
        if not ps: st.warning("Register a patient first.")
        else:
            with st.form("insurance"):
                p=st.selectbox("Patient",ps,format_func=label_patient,key="insurance_patient")
                company=st.text_input("Insurance Company")
                policy=st.text_input("Policy Number")
                amount=st.number_input("Claim Amount (₹)",0.0,10000000.0,0.0)
                status=st.selectbox("Claim Status",["Pending","Submitted","Approved","Rejected","Settled"])
                notes=st.text_area("Notes")
                save=st.form_submit_button("🛡️ Save Claim",use_container_width=True)
            if save:
                cid=new_id("CLM","insurance_claims")
              execute("INSERT INTO insurance_claims(claim_id,patient_id,insurance_company,policy_number,claim_amount,claim_date,status,notes) VALUES(?,?,?,?,?,?,?,?)",(cid,p[0],company,policy,amount,str(date.today()),status,notes))
                st.success(f"Claim saved: {cid}")
            rows=execute("""SELECT c.claim_id,c.patient_id,p.full_name,c.insurance_company,c.policy_number,c.claim_amount,c.claim_date,c.status
                            FROM insurance_claims c LEFT JOIN patients p ON c.patient_id=p.patient_id ORDER BY c.id DESC""",fetch=True)
            if rows: st.dataframe(pd.DataFrame(rows,columns=["Claim","Patient ID","Patient","Company","Policy","Amount","Date","Status"]),use_container_width=True,hide_index=True)

# ============================ INVENTORY ============================

elif menu == "📦 Inventory":
    st.markdown('<div class="section">📦 Inventory & Equipment</div>',unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["📦 Stock","⚠️ Low Stock","🛠️ Equipment"])
    with t1:
        with st.form("inventory"):
            c1,c2=st.columns(2)
            with c1:
                name=st.text_input("Item Name")
                cat=st.selectbox("Category",["Dental Consumable","Orthodontic","Cleaning","Office","Other"])
                qty=st.number_input("Quantity",0,100000,0)
                minimum=st.number_input("Minimum Stock",0,100000,5)
            with c2:
                price=st.number_input("Unit Price (₹)",0.0,1000000.0,0.0)
                supplier=st.text_input("Supplier")
            save=st.form_submit_button("💾 Add / Update Stock",use_container_width=True)
        if save:
            existing=execute("SELECT item_id,quantity FROM inventory WHERE item_name=?",(name,),True)
            if existing:
                execute("UPDATE inventory SET quantity=?,minimum_stock=?,unit_price=?,supplier=?,last_updated=? WHERE item_id=?",(qty,minimum,price,supplier,str(datetime.now()),existing[0][0]))
                st.success("Inventory item updated.")
            else:
                iid=new_id("INV","inventory")
                execute("INSERT INTO inventory(item_id,item_name,category,quantity,minimum_stock,unit_price,supplier,last_updated) VALUES(?,?,?,?,?,?,?,?)",(iid,name,cat,qty,minimum,price,supplier,str(datetime.now())))
                st.success(f"Inventory item added: {iid}")
        rows=execute("SELECT item_id,item_name,category,quantity,minimum_stock,unit_price,supplier,last_updated FROM inventory ORDER BY item_name",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Item","Category","Qty","Minimum","Unit Price","Supplier","Updated"]),use_container_width=True,hide_index=True)
    with t2:
        rows=execute("SELECT item_id,item_name,category,quantity,minimum_stock,supplier FROM inventory WHERE quantity<=minimum_stock ORDER BY quantity",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Item","Category","Qty","Minimum","Supplier"]),use_container_width=True,hide_index=True)
        else: st.success("No low-stock items.")
    with t3:
        with st.form("equipment"):
            name=st.text_input("Equipment Name")
            cat=st.selectbox("Equipment Category",["Dental Chair","X-Ray","Sterilizer","Scanner","Computer","Other"])
            purchase=st.date_input("Purchase Date",date.today())
            last=st.date_input("Last Maintenance",date.today())
            nxt=st.date_input("Next Maintenance",date.today()+timedelta(days=180))
            status=st.selectbox("Status",["Operational","Maintenance Due","Under Maintenance","Out of Service"])
            notes=st.text_area("Notes")
            save=st.form_submit_button("🛠️ Save Equipment",use_container_width=True)
        if save:
            eid=new_id("EQ","equipment")
            execute("INSERT INTO equipment(equipment_id,equipment_name,category,purchase_date,last_maintenance,next_maintenance,status,notes) VALUES(?,?,?,?,?,?,?,?)",(eid,name,cat,str(purchase),str(last),str(nxt),status,notes))
            st.success(f"Equipment saved: {eid}")
        rows=execute("SELECT equipment_id,equipment_name,category,purchase_date,last_maintenance,next_maintenance,status,notes FROM equipment ORDER BY id DESC",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["ID","Equipment","Category","Purchase","Last Maintenance","Next Maintenance","Status","Notes"]),use_container_width=True,hide_index=True)

# ========================= AI CARE CENTER =========================

elif menu == "🤖 AI Care Center":
    st.markdown('<div class="section">🤖 AI Care Center</div>',unsafe_allow_html=True)
    st.info("AI-assisted educational analysis only. This prototype does not diagnose conditions or prescribe treatment.")

    try:
        hf_token=st.secrets["HF_TOKEN"]
    except Exception:
        hf_token=None

    t1,t2,t3,t4=st.tabs(["💬 Dental AI Assistant","😁 Smile Analysis","🦷 Progress Analysis","💬 Feedback Analysis"])

    with t1:
        question=st.text_area("Ask an educational dental-care question",placeholder="Example: What are general oral hygiene habits?")
        if st.button("🤖 Ask AI",key="ask_ai"):
            if not question.strip():
                st.warning("Enter a question.")
            elif not hf_token:
                st.warning("HF_TOKEN is not configured in Streamlit Secrets. The local educational fallback will be used.")
                st.write("General guidance: maintain regular oral hygiene, limit frequent sugary foods/drinks, and consult a qualified dental professional for personal concerns.")
            else:
                try:
                    headers={"Authorization":f"Bearer {hf_token}"}
                    payload={"inputs":question,"parameters":{"max_new_tokens":180}}
                    url="https://api-inference.huggingface.co/models/google/flan-t5-base"
                    r=requests.post(url,headers=headers,json=payload,timeout=45)
                    if r.ok:
                        data=r.json()
                        if isinstance(data,list) and data:
                            text=data[0].get("generated_text","")
                        elif isinstance(data,dict):
                            text=data.get("generated_text",str(data))
                        else: text=str(data)
                        st.success("AI response")
                        st.write(text)
                        st.caption("Educational AI output; verify important information with a qualified professional.")
                    else:
                        st.error(f"Hugging Face request failed: {r.status_code}")
                except Exception as e:
                    st.error(f"AI connection error: {e}")

    with t2:
        st.subheader("😁 Smile Analysis Assistant")
        st.write("This prototype records an image-analysis request and provides non-diagnostic visual workflow information.")
        img=st.file_uploader("Upload smile image (optional)",type=["jpg","jpeg","png"],key="smile_img")
        if img:
            st.image(img,use_container_width=True)
            st.success("Image uploaded successfully.")
            st.write("Suggested analysis categories: image quality, visible alignment appearance, smile symmetry appearance, and before/after comparison.")
            st.warning("This does not diagnose dental or orthodontic conditions.")
            if st.button("💾 Save Smile Analysis",key="save_smile"):
                aid=new_id("AI","ai_analysis")
                execute("INSERT INTO ai_analysis(analysis_id,analysis_type,file_name,result,confidence,analysis_date) VALUES(?,?,?,?,?,?)",(aid,"Smile Analysis",img.name,"Educational visual review workflow recorded.",0.0,str(datetime.now())))
                st.success(f"Saved: {aid}")

    with t3:
        st.subheader("🦷 Orthodontic Progress Analyzer")
        ps=patients()
        if ps:
            p=st.selectbox("Patient",ps,format_func=label_patient,key="ai_progress_patient")
            rows=execute("""SELECT treatment_type,progress,current_stage,start_date,expected_end_date
                            FROM orthodontic_cases WHERE patient_id=? ORDER BY id DESC""",(p[0],),True)
            if rows:
                avg=sum(x[1] for x in rows)/len(rows)
                st.metric("Recorded Progress",f"{avg:.0f}%")
                st.progress(min(max(avg/100,0),1))
                st.dataframe(pd.DataFrame(rows,columns=["Treatment","Progress %","Stage","Start","Expected End"]),use_container_width=True,hide_index=True)
                st.info("This is a summary of recorded progress values. It is not a clinical prediction.")
            else: st.info("No orthodontic case recorded for this patient.")
        else: st.warning("Register a patient first.")

    with t4:
        text=st.text_area("Patient feedback")
        rating=st.slider("Rating",1,5,5)
        if st.button("🔎 Analyze Feedback"):
            low=text.lower()
            positive=sum(w in low for w in ["good","great","excellent","happy","helpful","clean","friendly","satisfied"])
            negative=sum(w in low for w in ["bad","poor","slow","unhappy","rude","expensive","wait"])
            sentiment="Positive" if positive>negative else ("Negative" if negative>positive else "Neutral")
            st.metric("Rule-based sentiment",sentiment)
            if st.button("💾 Save Feedback",key="save_feedback"):
                fid=new_id("FDB","feedback")
                execute("INSERT INTO feedback(feedback_id,patient_id,rating,feedback_text,sentiment,feedback_date) VALUES(?,?,?,?,?,?)",(fid,None,rating,text,sentiment,str(date.today())))
                st.success(f"Feedback saved: {fid}")

# ============================ REPORTS ============================

elif menu == "📊 Reports":
    st.markdown('<div class="section">📊 Reports & Analytics</div>',unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["📈 Clinic","👥 Patients","💰 Finance"])

    with t1:
        data={
            "Patients":scalar("SELECT COUNT(*) FROM patients"),
            "Appointments":scalar("SELECT COUNT(*) FROM appointments"),
            "Treatments":scalar("SELECT COUNT(*) FROM treatments"),
            "Orthodontic Cases":scalar("SELECT COUNT(*) FROM orthodontic_cases"),
            "Reminders":scalar("SELECT COUNT(*) FROM reminders"),
            "AI Analyses":scalar("SELECT COUNT(*) FROM ai_analysis"),
        }
        st.bar_chart(pd.Series(data))
        rows=execute("SELECT status,COUNT(*) FROM appointments GROUP BY status",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["Appointment Status","Count"]),use_container_width=True,hide_index=True)

    with t2:
        rows=execute("SELECT gender,COUNT(*) FROM patients GROUP BY gender",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["Gender","Patients"]),use_container_width=True,hide_index=True)
        rows=execute("SELECT blood_group,COUNT(*) FROM patients GROUP BY blood_group",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["Blood Group","Patients"]),use_container_width=True,hide_index=True)

    with t3:
        revenue=scalar("SELECT COALESCE(SUM(amount),0) FROM payments")
        billed=scalar("SELECT COALESCE(SUM(total_amount),0) FROM bills")
        outstanding=scalar("SELECT COALESCE(SUM(balance),0) FROM bills")
        c1,c2,c3=st.columns(3)
        c1.metric("💵 Payments",f"₹{revenue:,.2f}")
        c2.metric("🧾 Billed",f"₹{billed:,.2f}")
        c3.metric("⏳ Outstanding",f"₹{outstanding:,.2f}")
        rows=execute("SELECT payment_date,payment_method,SUM(amount) FROM payments GROUP BY payment_date,payment_method ORDER BY payment_date DESC",fetch=True)
        if rows: st.dataframe(pd.DataFrame(rows,columns=["Date","Method","Amount"]),use_container_width=True,hide_index=True)

# ========================= ADMINISTRATION =========================

elif menu == "⚙️ Administration":
    st.markdown('<div class="section">⚙️ Administration</div>',unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["📋 System Status","🗃️ Data Tools","ℹ️ About"])

    with t1:
        tables=["patients","appointments","treatments","orthodontic_cases","followups","prescriptions","xray_records","reminders","bills","payments","insurance_claims","inventory","equipment","feedback","ai_analysis","hygiene_logs","health_assessments","diet_plans","expenses"]
        rows=[(x,scalar(f"SELECT COUNT(*) FROM {x}")) for x in tables]
        st.dataframe(pd.DataFrame(rows,columns=["Table","Records"]),use_container_width=True,hide_index=True)
        st.success("Database connection: Active")
        st.success("Application: Operational")

    with t2:
        st.warning("Use exports for academic demonstration. Avoid deleting records unless you have a backup.")
        table=st.selectbox("Export table",["patients","appointments","treatments","orthodontic_cases","followups","prescriptions","xray_records","reminders","bills","payments","insurance_claims","inventory","equipment","feedback","ai_analysis","health_assessments","diet_plans"])
        rows=execute(f"SELECT * FROM {table}",fetch=True)
        conn=db()
        columns=[d[1] for d in conn.execute(f"PRAGMA table_info({table})").fetchall()]
        conn.close()
        df=pd.DataFrame(rows,columns=columns)
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.download_button("⬇️ Download CSV",df.to_csv(index=False).encode("utf-8"),f"{table}.csv","text/csv")

    with t3:
        st.markdown("""
        ### 🦷 AI-Dental Pro
        **Developed by Rashpreet Kaur Arora — BCA 2nd Year**

        This academic prototype demonstrates:
        - patient and clinic record management
        - appointments and queue handling
        - orthodontic case and progress tracking
        - dental-care records and educational guidance
        - reminders
        - billing, payments and insurance records
        - inventory and equipment maintenance
        - AI-assisted educational workflows
        - reports and CSV export

        **AI Safety:** AI outputs are assistance/analysis only. The application must not be presented as a reliable medical diagnosis or treatment-prescription system.
        """)

# --------------------------- FOOTER ---------------------------

st.markdown("""
<div class="card" style="text-align:center;margin-top:35px;">
<b>🦷 AI-Dental Pro</b><br>
Developed by <b>Rashpreet Kaur Arora</b> | BCA 2nd Year<br>
<span class="small">Academic Prototype — AI-assisted analysis only</span>
</div>
""",unsafe_allow_html=True)

            if st.button("💾 Update Status",use_container_width=True):
                execute("UPDATE appointments SET status=?,notes=? WHERE appointment_id=?",(
