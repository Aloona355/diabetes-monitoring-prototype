import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime
import base64
from streamlit_option_menu import option_menu

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(page_title="AI Diabetes Monitor", layout="wide")

LOGO = "IMG_5991.png"


# --------------------------------------------------
# Convert logo to base64
# --------------------------------------------------
def get_base64_logo():
    with open(LOGO, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: #f7fbfc;
    color: #0B2F4A;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: #075985;
    text-align: center;
    line-height: 1.2;
    margin-top: 10px;
    margin-bottom: 28px;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #075985;
    margin-bottom: 8px;
}

.auth-subtitle {
    text-align: center;
    color: #475569;
    font-size: 15px;
    margin-bottom: 24px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(11,47,74,0.06);
    margin-bottom: 20px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(11,47,74,0.06);
}

.metric-title {
    font-size: 14px;
    color: #334155;
    font-weight: 700;
}

.metric-value {
    font-size: 34px;
    color: #0B2F4A;
    font-weight: 850;
    margin-top: 8px;
}

label {
    color: #0B2F4A !important;
    font-weight: 700 !important;
}

.stTextInput input,
.stNumberInput input {
    background-color: white !important;
    color: #0B2F4A !important;
    border: 1px solid #b7dce5 !important;
    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
    color: #0B2F4A !important;
    border: 1px solid #b7dce5 !important;
    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] span {
    color: #0B2F4A !important;
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

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06263d 0%, #031827 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.18);
}

/* Sidebar logout */
[data-testid="stSidebar"] .stButton > button {
    background: transparent;
    color: white !important;
    border: none;
    border-radius: 12px;
    text-align: left;
    justify-content: flex-start;
    font-size: 16px;
    font-weight: 600;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.10);
}

/* Upload box improvement */
[data-testid="stFileUploader"] {
    background: transparent;
}

.small-center-text {
    text-align: center;
    color: #475569;
    margin-top: 18px;
    margin-bottom: 5px;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 38px;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Session state
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "patient" not in st.session_state:
    st.session_state.patient = {}

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"


# --------------------------------------------------
# PDF report
# --------------------------------------------------
def create_pdf_report(patient, risk_score):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Intelligent Diabetes Monitoring System Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    data = {
        "Generated on": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Name": patient.get("name", "N/A"),
        "Email Address": patient.get("email", "N/A"),
        "Age": patient.get("age", "N/A"),
        "Gender": patient.get("gender", "N/A"),
        "Diabetes Type": patient.get("type", "N/A"),
        "Estimated Calories": "550 kcal",
        "Estimated Carbohydrates": "65 g",
        "Estimated Glucose": "145 mg/dL",
        "Foot Health Status": "Low Risk",
        "Overall Risk Score": f"{risk_score}/100",
        "Recommendation": (
            "Maintain regular glucose monitoring, review dietary carbohydrate intake, "
            "and schedule retinal screening if glucose instability persists."
        )
    }

    for key, value in data.items():
        pdf.cell(0, 9, f"{key}: {value}", ln=True)

    return pdf.output(dest="S").encode("latin-1")


# --------------------------------------------------
# Sidebar with Bootstrap icons
# --------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:18px; padding-bottom:22px;">
                <img src="data:image/png;base64,{get_base64_logo()}" width="190">
                <h2 style="color:white; margin-top:8px; font-weight:800;">IDMS</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        selected = option_menu(
            menu_title=None,
            options=[
                "Overview",
                "Dietary Analysis",
                "Wearable Analysis",
                "Foot Assessment",
                "Retinal Awareness",
                "Risk Summary",
                "Reports",
                "History",
                "Profile",
                "Settings",
            ],
            icons=[
                "house",
                "basket",
                "smartwatch",
                "activity",
                "eye",
                "clipboard-pulse",
                "file-earmark-text",
                "clock-history",
                "person",
                "gear",
            ],
            default_index=0,
            styles={
                "container": {
                    "padding": "0px",
                    "background-color": "transparent",
                },
                "icon": {
                    "color": "white",
                    "font-size": "20px",
                },
                "nav-link": {
                    "color": "white",
                    "font-size": "16px",
                    "font-weight": "600",
                    "text-align": "left",
                    "margin": "6px 0px",
                    "padding": "12px 14px",
                    "border-radius": "12px",
                    "--hover-color": "rgba(255,255,255,0.10)",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(90deg, #0891b2, #14b8a6)",
                    "color": "white",
                    "font-weight": "700",
                },
            }
        )

        st.markdown("---")

        if st.button("↪  Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.session_state.auth_mode = "login"
            st.rerun()

    return selected


# --------------------------------------------------
# Login / Create Account page
# --------------------------------------------------
def login_page():
    logo_left, logo_center, logo_right = st.columns([1, 1.4, 1])
    with logo_center:
        st.image(LOGO, width=430)

st.markdown("""
<div class="hero-title">
Intelligent Diabetes Monitoring System
</div>
""", unsafe_allow_html=True)
