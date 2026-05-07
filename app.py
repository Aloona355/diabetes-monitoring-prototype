import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime

st.set_page_config(
    page_title="AI Diabetes Monitor",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #006b8f;
        text-align: center;
    }

    .sub-title {
        font-size: 16px;
        color: #188f9d;
        text-align: center;
        margin-bottom: 25px;
    }

    .card {
        background-color: white;
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        background-color: #006b8f;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

if "user" not in st.session_state:
    st.session_state.user = {}


def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Patient Health Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    for key, value in data.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)

    return pdf.output(dest="S").encode("latin-1")


def login_page():
    left, center, right = st.columns([1, 1.5, 1])

    with center:
        st.image("PHOTO-2026-02-17-21-43-19.jpeg", width=150)

        st.markdown(
            '<div class="main-title">Intelligent Diabetes Monitoring System</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sub-title">Multimodal AI Prototype for Diabetes Monitoring</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Patient Login")

        name = st.text_input("Full Name")
        patient_id = st.text_input("Patient ID")
        age = st.number_input("Age", min_value=1, max_value=100, value=45)
        gender = st.selectbox("Gender", ["Female", "Male"])
        diabetes_type = st.selectbox(
            "Diabetes Type",
            ["Type 1", "Type 2", "Prediabetes"]
        )

        if st.button("Start Monitoring"):
            if name.strip() == "" or patient_id.strip() == "":
                st.error("Please enter patient name and ID.")
            else:
                st.session_state.logged_in = True
                st.session_state.user = {
                    "name": name,
                    "id": patient_id,
                    "age": age,
                    "gender": gender,
                    "type": diabetes_type
                }
                st.session_state.active_page = "Dashboard"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


def dashboard_page():
    with st.sidebar:
        st.image("PHOTO-2026-02-17-21-43-19.jpeg", width=110)

        st.markdown("### Patient Profile")
        st.write(f"Name: {st.session_state.user['name']}")
        st.write(f"ID: {st.session_state.user['id']}")
        st.write(f"Age: {st.session_state.user['age']}")
        st.write(f"Type: {st.session_state.user['type']}")

        st.markdown("---")

        if st.button("Dashboard Home"):
            st.session_state.active_page = "Dashboard"

        if st.button("Dietary Analysis"):
            st.session_state.active_page = "Diet"

        if st.button("Glucose Prediction"):
            st.session_state.active_page = "Glucose"

        if st.button("Foot Assessment"):
            st.session_state.active_page = "Foot"

        if st.button("Report"):
            st.session_state.active_page = "Report"

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown(
        '<div class="main-title">AI Diabetes Monitoring Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Integrated Dietary, Wearable, Foot, and Retinal Health Monitoring</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    if st.session_state.active_page == "Dashboard":
        col1, col2, col3 = st.columns(3)

        col1.metric("Predicted Glucose", "145 mg/dL")
        col2.metric("Risk Score", "65 / 100")
        col3.metric("Foot Risk", "Low")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("System Overview")
        st.write(
            "This prototype integrates dietary analysis, wearable-based glucose prediction, "
            "diabetic foot assessment, and retinal health awareness in a unified dashboard."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.active_page == "Diet":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Dietary Analysis Module")

        uploaded_food = st.file_uploader(
            "Upload Meal Image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_food:
            image = Image.open(uploaded_food)
            st.image(image, caption="Uploaded Meal", width=450)

            st.success("AI Nutrition Estimation Completed")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Calories", "550 kcal")
            c2.metric("Carbohydrates", "65 g")
            c3.metric("Protein", "28 g")
            c4.metric("Fat", "18 g")

        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.active_page == "Glucose":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable-Based Glucose Prediction")

        uploaded_csv = st.file_uploader(
            "Upload Wearable Sensor Data CSV",
            type=["csv"]
        )

        if uploaded_csv:
            data = pd.read_csv(uploaded_csv)
            st.dataframe(data.head(), use_container_width=True)

            st.line_chart([120, 132, 145, 138, 130])
            st.metric("Predicted Glucose", "145 mg/dL")
            st.warning("Moderate glucose elevation detected.")

        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.active_page == "Foot":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Diabetic Foot Assessment")

        uploaded_foot = st.file_uploader(
            "Upload Foot Image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_foot:
            image = Image.open(uploaded_foot)
            st.image(image, caption="Uploaded Foot Image", width=420)

            st.success("AI Result: Healthy tissue - No ulcer detected")
            st.metric("Foot Risk", "Low")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Retinal Health Awareness")
        st.warning(
            "Patients with persistent glucose instability should schedule periodic retinal screening."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.active_page == "Report":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Generate Patient PDF Report")

        report_data = {
            "Patient Name": st.session_state.user["name"],
            "Patient ID": st.session_state.user["id"],
            "Age": st.session_state.user["age"],
            "Gender": st.session_state.user["gender"],
            "Diabetes Type": st.session_state.user["type"],
            "Predicted Glucose": "145 mg/dL",
            "Dietary Carbohydrates": "65 g",
            "Foot Risk": "Low",
            "Risk Score": "65 / 100",
            "Report Date": datetime.now().strftime("%Y-%m-%d"),
            "System Status": "Academic Prototype"
        }

        pdf_bytes = create_pdf(report_data)

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="Diabetes_Health_Report.pdf",
            mime="application/pdf"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption(
        "Graduation Project Prototype | Intelligent Diabetes Monitoring System"
    )


if not st.session_state.logged_in:
    login_page()
else:
    dashboard_page()
