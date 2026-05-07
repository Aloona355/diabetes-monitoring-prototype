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
# Sidebar
# --------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:18px; padding-bottom:22px;">
                <img src="data:image/png;base64,{get_base64_logo()}" width="210">
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

if st.button("⎋  Logout", use_container_width=True):
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

    st.markdown(
        '<div class="hero-title">Intelligent Diabetes Monitoring System</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.15, 1])

    with center:
        if st.session_state.auth_mode == "login":
            st.markdown(
                '<div class="section-title" style="text-align:center;">Welcome Back</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="auth-subtitle">Sign in to continue monitoring your health insights.</div>',
                unsafe_allow_html=True
            )

            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            remember = st.checkbox("Remember me")

            if st.button("Sign In", use_container_width=True):
                if email.strip() == "":
                    st.error("Enter your email address to continue.")
                elif password.strip() == "":
                    st.error("Enter your password to continue.")
                else:
                    st.session_state.patient = {
                        "name": "Patient",
                        "email": email,
                        "age": "N/A",
                        "gender": "N/A",
                        "type": "N/A"
                    }
                    st.session_state.logged_in = True
                    st.session_state.page = "upload"
                    st.rerun()

            st.markdown(
                '<div class="small-center-text">Don’t have an account?</div>',
                unsafe_allow_html=True
            )

            if st.button("Create Account", use_container_width=True):
                st.session_state.auth_mode = "create"
                st.rerun()

        else:
            st.markdown(
                '<div class="section-title" style="text-align:center;">Create Your Account</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="auth-subtitle">Create an account to start your diabetes monitoring journey.</div>',
                unsafe_allow_html=True
            )

            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            age = st.number_input("Age", min_value=1, max_value=100, value=23)
            gender = st.selectbox("Gender", ["Female", "Male"])
            diabetes_type = st.selectbox(
                "Diabetes Type",
                ["Type 1 Diabetes", "Type 2 Diabetes", "Prediabetes"]
            )

            if st.button("Create Account and Continue", use_container_width=True):
                if name.strip() == "":
                    st.error("Enter your name to continue.")
                elif email.strip() == "":
                    st.error("Enter your email address to continue.")
                elif password.strip() == "":
                    st.error("Create a password to continue.")
                else:
                    st.session_state.patient = {
                        "name": name,
                        "email": email,
                        "age": age,
                        "gender": gender,
                        "type": diabetes_type
                    }
                    st.session_state.logged_in = True
                    st.session_state.page = "upload"
                    st.rerun()

            st.markdown(
                '<div class="small-center-text">Already have an account?</div>',
                unsafe_allow_html=True
            )

            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()


# --------------------------------------------------
# Upload page
# --------------------------------------------------
def upload_page():
    render_sidebar()

    st.markdown('<div class="section-title">Upload Health Data</div>', unsafe_allow_html=True)
    st.write("Upload the required files to generate an integrated diabetes risk analysis.")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Meal Image")
        food_img = st.file_uploader(
            "Upload a clear image of your meal for nutritional analysis.",
            type=["jpg", "jpeg", "png"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable Device Data")
        wearable_csv = st.file_uploader(
            "Upload wearable sensor data in CSV format for glucose pattern estimation.",
            type=["csv"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Foot Assessment Image")
        foot_img = st.file_uploader(
            "Upload a clear foot image to support diabetic foot risk assessment.",
            type=["jpg", "jpeg", "png"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.food_img = food_img
    st.session_state.wearable_csv = wearable_csv
    st.session_state.foot_img = foot_img

    if food_img and wearable_csv and foot_img:
        if st.button("Generate Analysis", use_container_width=True):
            st.session_state.page = "overview"
            st.rerun()
    else:
        st.info("Upload the meal image, wearable data file, and foot image to continue.")


# --------------------------------------------------
# Overview page
# --------------------------------------------------
def overview_page():
    selected_page = render_sidebar()

    food_img = st.session_state.get("food_img")
    wearable_csv = st.session_state.get("wearable_csv")
    foot_img = st.session_state.get("foot_img")

    if selected_page != "Overview":
        st.markdown(f'<div class="section-title">{selected_page}</div>', unsafe_allow_html=True)
        st.info("This section is included in the prototype navigation and can be expanded in the next development phase.")
        return

    calories = 550
    carbs = 65
    protein = 28
    fat = 18
    glucose = 145
    foot_risk = "Low Risk"
    risk_score = 46

    st.markdown('<div class="section-title">Integrated Health Overview</div>', unsafe_allow_html=True)
    st.write(f"Analysis summary for {st.session_state.patient.get('name')}")

    st.markdown("---")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Estimated Glucose</div>
            <div class="metric-value">{glucose}</div>
            <div>mg/dL</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Integrated Risk Score</div>
            <div class="metric-value">{risk_score}</div>
            <div>/100</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Foot Health Status</div>
            <div class="metric-value">{foot_risk}</div>
            <div>No visible ulcer indicators</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Estimated Meal Carbohydrates</div>
            <div class="metric-value">{carbs}</div>
            <div>g</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Meal Nutrition Analysis")
        st.image(Image.open(food_img), caption="Uploaded Meal Image", use_container_width=True)

        c1, c2 = st.columns(2)
        c1.metric("Calories", f"{calories} kcal")
        c1.metric("Protein", f"{protein} g")
        c2.metric("Carbohydrates", f"{carbs} g")
        c2.metric("Fat", f"{fat} g")

        if carbs >= 70:
            st.warning(
                "This meal appears to contain a high amount of carbohydrates. "
                "Consider reducing starchy portions and monitoring your glucose level after eating."
            )
        elif carbs >= 45:
            st.info(
                "This meal contains a moderate amount of carbohydrates. "
                "Choose healthier carbohydrate sources and continue monitoring your glucose response."
            )
        else:
            st.success(
                "This meal appears to be a suitable choice with a relatively low carbohydrate amount."
            )

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable-Based Glucose Analysis")

        data = pd.read_csv(wearable_csv)
        st.dataframe(data.head(), use_container_width=True)

        st.metric("Estimated Glucose Level", f"{glucose} mg/dL")

        if glucose >= 180:
            st.warning("High glucose elevation pattern detected. Immediate monitoring is recommended.")
        elif glucose >= 140:
            st.warning("Moderate glucose elevation pattern detected. Continued monitoring is recommended.")
        else:
            st.success("Glucose pattern appears within an acceptable range.")

        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Diabetic Foot Assessment")
        st.image(Image.open(foot_img), caption="Uploaded Foot Image", width=350)
        st.success("Low Risk: No visible ulcer indicators detected in the uploaded image.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Retinal Health Awareness")

        if risk_score >= 70 or glucose >= 180:
            st.warning(
                "Persistent glucose instability may increase the risk of diabetic retinopathy. "
                "Periodic retinal screening is recommended."
            )
        else:
            st.info(
                "No high-risk retinal warning is detected at this time. "
                "Continue maintaining stable glucose levels and regular follow-up."
            )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    report_col1, report_col2 = st.columns([2, 1])

    with report_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Overall Diabetes Risk Summary")
        st.write("The integrated score combines nutritional, wearable, and foot assessment indicators.")
        st.progress(risk_score / 100)
        st.write(f"Overall Risk Score: {risk_score}/100")

        if risk_score >= 70:
            st.warning("Overall Risk Level: High")
        elif risk_score >= 40:
            st.warning("Overall Risk Level: Moderate")
        else:
            st.success("Overall Risk Level: Low")

        st.caption("This system is an academic prototype and is not intended for clinical diagnosis.")
        st.markdown('</div>', unsafe_allow_html=True)

    with report_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Generate Health Report")

        pdf = create_pdf_report(st.session_state.patient, risk_score)

        st.download_button(
            label="Download Report",
            data=pdf,
            file_name="Diabetes_Health_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Routing
# --------------------------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.page == "upload":
        upload_page()
    else:
        overview_page()
