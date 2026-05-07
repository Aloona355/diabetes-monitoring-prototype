import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime

st.set_page_config(
    page_title="Glucovision AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

LOGO = "Logo.png"

st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}

.stApp {
    background: #f4efe7;
    color: #0b2f4a;
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1250px;
}

.login-wrapper {
    background: white;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 10px 35px rgba(0,0,0,0.10);
    min-height: 650px;
}

.login-left {
    background: linear-gradient(160deg, #062a44, #0b5f6f);
    padding: 55px 45px;
    color: white;
    min-height: 650px;
}

.login-title {
    font-size: 38px;
    font-weight: 800;
    line-height: 1.15;
    margin-top: 120px;
}

.login-sub {
    color: #d8eef1;
    font-size: 15px;
    margin-top: 18px;
    line-height: 1.7;
}

.login-stats {
    display: flex;
    gap: 32px;
    margin-top: 38px;
}

.stat-num {
    font-size: 25px;
    font-weight: 800;
}

.stat-label {
    font-size: 11px;
    color: #b7d6dc;
}

.login-right {
    background: #faf6ef;
    padding: 75px 60px;
    min-height: 650px;
}

.form-title {
    font-size: 30px;
    font-weight: 800;
    color: #0b2f4a;
}

.form-sub {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 25px;
}

.stButton > button {
    background: #082f49;
    color: white;
    border-radius: 8px;
    border: none;
    height: 44px;
    font-weight: 700;
}

.stButton > button:hover {
    background: #0b5f6f;
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #062a44, #073b5a);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-card {
    background: rgba(255,255,255,0.08);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 18px;
}

.page-title {
    font-size: 36px;
    font-weight: 850;
    color: #0b2f4a;
    line-height: 1.2;
}

.page-subtitle {
    color: #64748b;
    margin-top: 5px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #eadfce;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #eadfce;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    min-height: 140px;
}

.metric-label {
    font-size: 13px;
    color: #64748b;
    font-weight: 700;
    text-transform: uppercase;
}

.metric-value {
    font-size: 34px;
    color: #0b2f4a;
    font-weight: 850;
    margin-top: 14px;
}

.metric-note {
    font-size: 13px;
    color: #0f766e;
    margin-top: 4px;
}

.upload-box {
    border: 1px dashed #94a3b8;
    border-radius: 14px;
    padding: 18px;
    background: #fbfdff;
}

.status-good {
    color: #047857;
    font-weight: 800;
}

.status-warning {
    color: #d97706;
    font-weight: 800;
}

.small-muted {
    color: #64748b;
    font-size: 13px;
}

.footer-note {
    color: #94a3b8;
    text-align: center;
    font-size: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "history" not in st.session_state:
    st.session_state.history = []

if "patient" not in st.session_state:
    st.session_state.patient = {}


def create_pdf(patient, glucose, carbs, foot_risk, risk_score, advice):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 17)
    pdf.cell(0, 12, "Glucovision AI - Patient Health Report", ln=True, align="C")

    pdf.ln(8)
    pdf.set_font("Arial", size=11)

    report_items = {
        "Generated On": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Patient Name": patient.get("name", "N/A"),
        "Patient ID": patient.get("id", "N/A"),
        "Age": patient.get("age", "N/A"),
        "Diabetes Type": patient.get("type", "N/A"),
        "Predicted Glucose": f"{glucose} mg/dL",
        "Estimated Carbohydrates": f"{carbs} g",
        "Foot Risk": foot_risk,
        "Overall Risk Score": f"{risk_score}/100",
        "Clinical Recommendation": advice,
        "System Note": "Academic prototype only. Not intended for clinical diagnosis."
    }

    for key, value in report_items.items():
        pdf.multi_cell(0, 9, f"{key}: {value}")

    return pdf.output(dest="S").encode("latin-1")


def login_page():
    left, right = st.columns([1.1, 1])

    with left:
        st.markdown('<div class="login-left">', unsafe_allow_html=True)
        st.image(LOGO, width=85)
        st.markdown('<div class="login-title">Predict today’s risks,<br>before they become complications.</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="login-sub">An AI-powered multimodal diabetes monitoring system combining dietary analysis, wearable data, foot assessment, and retinal health awareness.</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="login-stats">
            <div>
                <div class="stat-num">4</div>
                <div class="stat-label">AI MODULES</div>
            </div>
            <div>
                <div class="stat-num">24/7</div>
                <div class="stat-label">MONITORING</div>
            </div>
            <div>
                <div class="stat-num">PDF</div>
                <div class="stat-label">REPORTS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="login-right">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Welcome back</div>', unsafe_allow_html=True)
        st.markdown('<div class="form-sub">Enter patient details to access the monitoring dashboard.</div>', unsafe_allow_html=True)

        name = st.text_input("Patient full name")
        patient_id = st.text_input("Medical ID")
        age = st.number_input("Age", min_value=1, max_value=100, value=23)
        diabetes_type = st.selectbox("Diabetes type", ["Type 1 Diabetes", "Type 2 Diabetes", "Prediabetes"])

        if st.button("Sign in to dashboard", use_container_width=True):
            if not name.strip():
                st.error("Please enter patient name.")
            else:
                st.session_state.patient = {
                    "name": name,
                    "id": patient_id,
                    "age": age,
                    "type": diabetes_type
                }
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                st.rerun()

        st.markdown('<p class="small-muted">This system is for academic demonstration only.</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def sidebar():
    with st.sidebar:
        st.image(LOGO, width=95)
        st.markdown("## Glucovision AI")

        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.write(f"Patient: {st.session_state.patient.get('name', 'N/A')}")
        st.write(f"Age: {st.session_state.patient.get('age', 'N/A')}")
        st.write(f"Type: {st.session_state.patient.get('type', 'N/A')}")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("Data Upload"):
            st.session_state.page = "upload"
            st.rerun()

        if st.button("Records History"):
            st.session_state.page = "history"
            st.rerun()

        if st.button("Report"):
            st.session_state.page = "report"
            st.rerun()

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()


def upload_page():
    sidebar()

    st.markdown('<div class="page-title">Upload Patient Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Submit patient modalities for integrated AI analysis.</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Food Image")
        food_img = st.file_uploader("Upload meal image", type=["jpg", "jpeg", "png"])
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable Data")
        wearable_csv = st.file_uploader("Upload CSV file", type=["csv"])
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Foot Image")
        foot_img = st.file_uploader("Upload foot image", type=["jpg", "jpeg", "png"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.food_img = food_img
    st.session_state.wearable_csv = wearable_csv
    st.session_state.foot_img = foot_img

    if food_img and wearable_csv and foot_img:
        if st.button("Analyze patient data", use_container_width=True):
            st.session_state.history.append(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - New multimodal analysis completed"
            )
            st.session_state.page = "dashboard"
            st.rerun()
    else:
        st.info("Upload all required files to enable full analysis.")


def dashboard_page():
    sidebar()

    st.markdown('<div class="page-title">Health Intelligence Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Integrated overview of dietary intake, glucose estimation, complication awareness, and patient risk.</div>', unsafe_allow_html=True)

    st.markdown("---")

    food_img = st.session_state.get("food_img", None)
    wearable_csv = st.session_state.get("wearable_csv", None)
    foot_img = st.session_state.get("foot_img", None)

    glucose = 145
    carbs = 65
    calories = 550
    protein = 28
    fat = 18
    foot_risk = "Low"
    risk_score = 46

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Predicted Glucose</div>
            <div class="metric-value">{glucose}</div>
            <div class="metric-note">mg/dL - Moderate</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Risk Score</div>
            <div class="metric-value">{risk_score}/100</div>
            <div class="metric-note">Moderate Risk</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Foot Risk</div>
            <div class="metric-value">{foot_risk}</div>
            <div class="metric-note">No ulcer detected</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Meal Carbs</div>
            <div class="metric-value">{carbs} g</div>
            <div class="metric-note">Today</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Dietary Analysis")

        if food_img:
            st.image(Image.open(food_img), use_container_width=True)
        else:
            st.info("No meal image uploaded yet.")

        st.write(f"Calories: {calories} kcal")
        st.write(f"Carbohydrates: {carbs} g")
        st.write(f"Protein: {protein} g")
        st.write(f"Fat: {fat} g")

        if carbs > 60:
            st.warning("Meal advisory: This meal is high in carbohydrates. Consider reducing portion size or balancing it with protein and fiber.")
        else:
            st.success("Meal advisory: Carbohydrate level is within a safer range.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable Data Analysis")

        if wearable_csv:
            data = pd.read_csv(wearable_csv)
            st.dataframe(data.head(), use_container_width=True)
        else:
            st.info("No wearable CSV uploaded yet.")

        st.metric("Predicted Glucose Level", f"{glucose} mg/dL")

        if glucose > 180:
            st.error("Glucose advisory: High glucose pattern detected. Medical consultation is recommended.")
        elif glucose > 140:
            st.warning("Glucose advisory: Moderate elevation detected. Monitor meals and activity closely.")
        else:
            st.success("Glucose advisory: Current trend appears stable.")

        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Foot Assessment")

        if foot_img:
            st.image(Image.open(foot_img), width=350)
        else:
            st.info("No foot image uploaded yet.")

        st.markdown('<p class="status-good">Result: Low Risk</p>', unsafe_allow_html=True)
        st.write("No visible ulcer indicators detected in this prototype assessment.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Retinal Health Awareness")

        if glucose > 140:
            st.warning("Retinal recommendation: Glucose instability may increase long-term retinal risk. Schedule a retinal check-up with a specialist.")
        else:
            st.success("Retinal recommendation: No urgent retinal alert based on current prototype indicators.")

        st.write("This module supports long-term complication awareness.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    colr1, colr2 = st.columns([2, 1])

    with colr1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Integrated Risk Score")
        st.progress(risk_score / 100)
        st.write(f"Overall Risk Score: {risk_score}/100")
        st.warning("Overall Risk Level: Moderate")
        st.markdown("</div>", unsafe_allow_html=True)

    with colr2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Download Report")
        advice = "Monitor glucose trend, adjust carbohydrate intake, and schedule retinal screening."
        pdf = create_pdf(st.session_state.patient, glucose, carbs, foot_risk, risk_score, advice)
        st.download_button(
            "Download PDF Report",
            data=pdf,
            file_name="Glucovision_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)


def history_page():
    sidebar()
    st.markdown('<div class="page-title">Records History</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Recent patient analysis sessions.</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.history:
        for item in reversed(st.session_state.history):
            st.write(item)
    else:
        st.info("No records available yet.")

    st.markdown("</div>", unsafe_allow_html=True)


def report_page():
    sidebar()
    st.markdown('<div class="page-title">Patient Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate and download the latest health report.</div>', unsafe_allow_html=True)
    st.markdown("---")

    glucose = 145
    carbs = 65
    foot_risk = "Low"
    risk_score = 46
    advice = "Monitor glucose trend, adjust carbohydrate intake, and schedule retinal screening."

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("Report is ready for download.")
    pdf = create_pdf(st.session_state.patient, glucose, carbs, foot_risk, risk_score, advice)
    st.download_button(
        "Download PDF Report",
        data=pdf,
        file_name="Glucovision_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)


if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.page == "dashboard":
        dashboard_page()
    elif st.session_state.page == "upload":
        upload_page()
    elif st.session_state.page == "history":
        history_page()
    elif st.session_state.page == "report":
        report_page()
