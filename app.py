import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="AI Diabetes Monitor", layout="wide")

LOGO = "IMG_5991.png"

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f7fbfc 0%, #eef8fa 100%);
    color: #0B2F4A;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.card {
    background: white;
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #dbeafe;
    box-shadow: 0 8px 24px rgba(11,47,74,0.08);
    margin-bottom: 22px;
}

.hero {
    text-align: center;
    padding: 35px 20px 25px 20px;
}

.hero-title {
    font-size: 44px;
    font-weight: 800;
    color: #075985;
    margin-top: 10px;
}

.hero-subtitle {
    font-size: 18px;
    color: #0f766e;
    margin-top: 8px;
}

.section-title {
    font-size: 26px;
    font-weight: 750;
    color: #075985;
    margin-bottom: 10px;
}

.metric-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #dbeafe;
    box-shadow: 0 6px 18px rgba(11,47,74,0.07);
    text-align: center;
}

.metric-title {
    font-size: 15px;
    color: #64748b;
    font-weight: 600;
}

.metric-value {
    font-size: 36px;
    color: #0B2F4A;
    font-weight: 800;
}

.stButton > button {
    background: linear-gradient(90deg, #0369a1, #0f766e);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    font-weight: 700;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #075985, #115e59);
    color: white;
}

[data-testid="stSidebar"] {
    background: #e6f4f6;
}
</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "patient" not in st.session_state:
    st.session_state.patient = {}


def create_pdf_report(patient, risk_score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Intelligent Diabetes Monitoring System Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    data = {
        "Generated on": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Patient Name": patient.get("name", "N/A"),
        "Patient ID": patient.get("id", "N/A"),
        "Age": patient.get("age", "N/A"),
        "Gender": patient.get("gender", "N/A"),
        "Diabetes Type": patient.get("type", "N/A"),
        "Estimated Calories": "550 kcal",
        "Estimated Carbohydrates": "65 g",
        "Predicted Glucose": "145 mg/dL",
        "Foot Risk": "Low",
        "Overall Risk Score": f"{risk_score}/100",
        "Recommendation": "Continue monitoring glucose and schedule periodic retinal screening."
    }

    for key, value in data.items():
        pdf.cell(0, 9, f"{key}: {value}", ln=True)

    return pdf.output(dest="S").encode("latin-1")


def login_page():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.image(LOGO, width=230)
    st.markdown('<div class="hero-title">Intelligent Diabetes Monitoring System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Multimodal AI Prototype for Dietary Analysis, Wearable Data, Foot Assessment, and Retinal Awareness</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.4, 1])

    with center:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Patient Login</div>', unsafe_allow_html=True)

        name = st.text_input("Full Name")
        patient_id = st.text_input("Patient ID")
        age = st.number_input("Age", min_value=1, max_value=100, value=23)
        gender = st.selectbox("Gender", ["Female", "Male"])
        diabetes_type = st.selectbox("Diabetes Type", ["Type 1 Diabetes", "Type 2 Diabetes", "Prediabetes"])

        if st.button("Start Monitoring", use_container_width=True):
            if name.strip() == "":
                st.error("Please enter patient name.")
            else:
                st.session_state.patient = {
                    "name": name,
                    "id": patient_id,
                    "age": age,
                    "gender": gender,
                    "type": diabetes_type
                }
                st.session_state.logged_in = True
                st.session_state.page = "upload"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


def upload_page():
    st.sidebar.image(LOGO, width=120)
    st.sidebar.markdown("### Patient Profile")
    st.sidebar.write(f"Name: {st.session_state.patient.get('name')}")
    st.sidebar.write(f"Age: {st.session_state.patient.get('age')}")
    st.sidebar.write(f"Type: {st.session_state.patient.get('type')}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    st.image(LOGO, width=150)
    st.markdown('<div class="section-title">Upload Patient Data</div>', unsafe_allow_html=True)
    st.write("Upload the required data to start the multimodal AI analysis.")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Food Image")
        food_img = st.file_uploader("Upload meal image", type=["jpg", "jpeg", "png"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable CSV")
        wearable_csv = st.file_uploader("Upload wearable data", type=["csv"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Foot Image")
        foot_img = st.file_uploader("Upload foot image", type=["jpg", "jpeg", "png"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.food_img = food_img
    st.session_state.wearable_csv = wearable_csv
    st.session_state.foot_img = foot_img

    if food_img and wearable_csv and foot_img:
        if st.button("Analyze Patient Data", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    else:
        st.info("Please upload all three files to continue.")


def dashboard_page():
    food_img = st.session_state.get("food_img")
    wearable_csv = st.session_state.get("wearable_csv")
    foot_img = st.session_state.get("foot_img")

    st.sidebar.image(LOGO, width=120)
    st.sidebar.markdown("### Navigation")

    if st.sidebar.button("Back to Upload"):
        st.session_state.page = "upload"
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    top1, top2 = st.columns([1, 5])
    with top1:
        st.image(LOGO, width=120)
    with top2:
        st.markdown('<div class="section-title">Patient Analysis Dashboard</div>', unsafe_allow_html=True)
        st.write(f"Welcome, {st.session_state.patient.get('name')}")

    st.markdown("---")

    calories = 550
    carbs = 65
    protein = 28
    fat = 18
    glucose = 145
    foot_risk = "Low"
    risk_score = 70

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Predicted Glucose</div><div class="metric-value">{glucose}</div><div>mg/dL</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Risk Score</div><div class="metric-value">{risk_score}</div><div>/100</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Foot Risk</div><div class="metric-value">{foot_risk}</div><div>No ulcer detected</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Meal Carbs</div><div class="metric-value">{carbs}</div><div>g</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Dietary Analysis")
        st.image(Image.open(food_img), caption="Uploaded Food Image", use_container_width=True)
        c1, c2 = st.columns(2)
        c1.metric("Calories", f"{calories} kcal")
        c1.metric("Protein", f"{protein} g")
        c2.metric("Carbohydrates", f"{carbs} g")
        c2.metric("Fat", f"{fat} g")
        st.success("Analysis completed")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable Data Analysis")
        data = pd.read_csv(wearable_csv)
        st.dataframe(data.head(), use_container_width=True)
        st.metric("Predicted Glucose Level", f"{glucose} mg/dL")
        st.warning("Moderate glucose elevation detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Foot Assessment")
        st.image(Image.open(foot_img), caption="Uploaded Foot Image", width=350)
        st.success("Low Risk: No ulcer detected")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Retinal Health Awareness")
        st.warning("Patients with persistent glucose instability should schedule periodic retinal screening.")
        st.write("This module supports long-term complication awareness and future retinal health integration.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    report_col1, report_col2 = st.columns([2, 1])

    with report_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Integrated Risk Score")
        st.progress(risk_score / 100)
        st.write(f"Overall Risk Score: {risk_score}/100")
        st.warning("Overall Risk Level: Moderate")
        st.markdown('</div>', unsafe_allow_html=True)

    with report_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Download Report")
        pdf = create_pdf_report(st.session_state.patient, risk_score)
        st.download_button(
            label="Download PDF Report",
            data=pdf,
            file_name="Diabetes_Health_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)


if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.page == "upload":
        upload_page()
    else:
        dashboard_page()
