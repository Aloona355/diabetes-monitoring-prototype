import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime

st.set_page_config(
    page_title="AI Diabetes Monitor",
    page_icon="logo",
    layout="wide"
)

# =========================
# Styling
# =========================

st.markdown("""
<style>
    .stApp {
        background-color: #f7fbfc;
        color: #0b2f4a;
    }

    [data-testid="stSidebar"] {
        background-color: #e9f4f6;
    }

    h1, h2, h3 {
        color: #0b5f8a;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #0b5f8a;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 20px;
        color: #188f9d;
        margin-top: 0px;
    }

    .card {
        background-color: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        border-left: 6px solid #188f9d;
        margin-bottom: 18px;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        text-align: center;
    }

    .risk-low {
        background-color: #e8f7ef;
        color: #0b6b3a;
        padding: 15px;
        border-radius: 12px;
        font-weight: 700;
    }

    .risk-medium {
        background-color: #fff7df;
        color: #9a6a00;
        padding: 15px;
        border-radius: 12px;
        font-weight: 700;
    }

    .risk-high {
        background-color: #fdecec;
        color: #b42318;
        padding: 15px;
        border-radius: 12px;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# Login Page
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

if "patient_age" not in st.session_state:
    st.session_state.patient_age = 45

if "diabetes_type" not in st.session_state:
    st.session_state.diabetes_type = "Type 2 Diabetes"


def login_page():
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("PHOTO-2026-02-17-21-43-19.jpeg", width=170)

    with col2:
        st.markdown('<div class="main-title">Intelligent Diabetes Monitoring System</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="subtitle">Multimodal AI Prototype for Diabetes Monitoring and Risk Awareness</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Patient Login")

        patient_name = st.text_input("Patient Name", placeholder="Enter patient name")
        patient_id = st.text_input("Patient ID", placeholder="Enter patient ID")
        patient_age = st.number_input("Age", min_value=1, max_value=100, value=45)
        gender = st.selectbox("Gender", ["Female", "Male"])
        diabetes_type = st.selectbox("Diabetes Type", ["Type 1 Diabetes", "Type 2 Diabetes", "Prediabetes"])

        start = st.button("Start Monitoring", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if start:
            if patient_name.strip() == "":
                st.error("Please enter patient name.")
            else:
                st.session_state.logged_in = True
                st.session_state.patient_name = patient_name
                st.session_state.patient_id = patient_id
                st.session_state.patient_age = patient_age
                st.session_state.gender = gender
                st.session_state.diabetes_type = diabetes_type
                st.rerun()


# =========================
# Dashboard Page
# =========================

def dashboard_page():

    # Header
    col1, col2, col3 = st.columns([1, 5, 1])

    with col1:
        st.image("PHOTO-2026-02-17-21-43-19.jpeg", width=110)

    with col2:
        st.markdown('<div class="main-title">Intelligent Diabetes Monitoring System</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="subtitle">Integrated Multimodal AI Dashboard</div>',
            unsafe_allow_html=True
        )

    with col3:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")

    # Sidebar
    st.sidebar.image("PHOTO-2026-02-17-21-43-19.jpeg", width=120)
    st.sidebar.title("Patient Data Input")

    st.sidebar.markdown("### Patient Profile")
    st.sidebar.write(f"Name: {st.session_state.patient_name}")
    st.sidebar.write(f"Age: {st.session_state.patient_age}")
    st.sidebar.write(f"Type: {st.session_state.diabetes_type}")

    st.sidebar.markdown("---")

    food_img = st.sidebar.file_uploader("Upload Food Image", type=["jpg", "jpeg", "png"])
    wearable_csv = st.sidebar.file_uploader("Upload Wearable Data CSV", type=["csv"])
    foot_img = st.sidebar.file_uploader("Upload Foot Image", type=["jpg", "jpeg", "png"])

    # Default values
    calories = 0
    carbs = 0
    protein = 0
    fat = 0
    predicted_glucose = 0
    foot_risk = "Not assessed"

    # Food analysis
    if food_img:
        calories = 550
        carbs = 65
        protein = 28
        fat = 18

    # Wearable analysis
    if wearable_csv:
        predicted_glucose = 145

    # Foot assessment
    if foot_img:
        foot_risk = "Low"

    # Metrics
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Meal Carbohydrates</h3>
            <h1>{carbs} g</h1>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Predicted Glucose</h3>
            <h1>{predicted_glucose} mg/dL</h1>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Foot Risk</h3>
            <h1>{foot_risk}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Dietary Analysis Module")

        if food_img:
            image = Image.open(food_img)
            st.image(image, caption="Uploaded Food Image", use_container_width=True)

            st.success("Food analysis completed")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Calories", f"{calories} kcal")
            c2.metric("Carbs", f"{carbs} g")
            c3.metric("Protein", f"{protein} g")
            c4.metric("Fat", f"{fat} g")

            st.caption("Prototype output: simulated AI-based nutrition estimation.")
        else:
            st.info("Upload a food image to estimate nutrition values.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable-Based Glucose Estimation")

        if wearable_csv:
            data = pd.read_csv(wearable_csv)
            st.dataframe(data.head(), use_container_width=True)

            st.metric("Predicted Glucose Level", f"{predicted_glucose} mg/dL")

            if predicted_glucose > 180:
                st.error("High glucose pattern detected.")
            elif predicted_glucose > 140:
                st.warning("Moderate glucose elevation detected.")
            else:
                st.success("Glucose level appears normal.")

            st.caption("Prototype output: simulated XGBoost glucose prediction.")
        else:
            st.info("Upload wearable CSV data to estimate glucose level.")

        st.markdown("</div>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Diabetic Foot Assessment Module")

        if foot_img:
            foot_image = Image.open(foot_img)
            st.image(foot_image, caption="Uploaded Foot Image", width=350)

            st.success("AI Classification: No ulcer detected.")
            st.caption("Prototype output: simulated EfficientNet-based foot assessment.")
        else:
            st.info("Upload a foot image for diabetic foot assessment.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Retinal Health Awareness")

        st.warning(
            "Patients with persistent glucose instability should schedule periodic retinal screening."
        )

        st.write(
            "This module supports long-term complication awareness and future retinal health integration."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Risk score
    st.markdown("---")
    st.subheader("Integrated Risk Score")

    risk_score = 0

    if food_img:
        risk_score += 25
        if carbs > 60:
            risk_score += 15

    if wearable_csv:
        risk_score += 25
        if predicted_glucose > 140:
            risk_score += 20

    if foot_img:
        risk_score += 10

    risk_score = min(risk_score, 100)

    st.progress(risk_score / 100)
    st.write(f"Overall Risk Score: {risk_score}/100")

    if risk_score >= 70:
        st.markdown('<div class="risk-high">Overall Risk Level: High</div>', unsafe_allow_html=True)
    elif risk_score >= 40:
        st.markdown('<div class="risk-medium">Overall Risk Level: Moderate</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="risk-low">Overall Risk Level: Low</div>', unsafe_allow_html=True)

    # Report
    st.markdown("---")
    st.subheader("Health Report")

    report = f"""
Intelligent Diabetes Monitoring System Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Patient Information:
Name: {st.session_state.patient_name}
Patient ID: {st.session_state.patient_id}
Age: {st.session_state.patient_age}
Gender: {st.session_state.gender}
Diabetes Type: {st.session_state.diabetes_type}

Dietary Analysis:
Calories: {calories} kcal
Carbohydrates: {carbs} g
Protein: {protein} g
Fat: {fat} g

Wearable-Based Glucose Estimation:
Predicted Glucose Level: {predicted_glucose} mg/dL

Diabetic Foot Assessment:
Foot Risk: {foot_risk}

Retinal Health Awareness:
Periodic retinal screening is recommended for long-term complication monitoring.

Integrated Risk Score:
{risk_score}/100

System Note:
This prototype is for academic demonstration only and is not intended for clinical diagnosis.
"""

    st.download_button(
        label="Download Health Report",
        data=report,
        file_name="diabetes_health_report.txt",
        mime="text/plain"
    )

    st.markdown(
        '<div class="footer">Graduation Project Prototype | AI-based Multimodal Diabetes Monitoring System</div>',
        unsafe_allow_html=True
    )


if not st.session_state.logged_in:
    login_page()
else:
    dashboard_page()
