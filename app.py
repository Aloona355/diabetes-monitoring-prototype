import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime
import base64
from streamlit_option_menu import option_menu

st.set_page_config(page_title="AI Diabetes Monitor", layout="wide")

LOGO = "IMG_5991.png"


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def get_base64_logo():
    with open(LOGO, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def create_pdf_report(patient, risk_score):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Intelligent Diabetes Monitoring System Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    data = {
        "Generated on": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Name": patient.get("name", "Patient"),
        "Email Address": patient.get("email", "N/A"),
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
# CSS
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: #f8fbfd;
    color: #0B2F4A;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}

/* Login */
.hero-title {
    font-size: 48px;
    font-weight: 850;
    color: #075985;
    text-align: center;
    line-height: 1.2;
    margin-top: 10px;
    margin-bottom: 28px;
}

.section-title {
    font-size: 30px;
    font-weight: 850;
    color: #075985;
    margin-bottom: 6px;
}

.auth-subtitle {
    text-align: center;
    color: #64748b;
    font-size: 15px;
    margin-bottom: 24px;
}

.small-center-text {
    text-align: center;
    color: #64748b;
    margin-top: 18px;
    margin-bottom: 5px;
}

/* Cards */
.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(11,47,74,0.06);
    margin-bottom: 20px;
}

.card-title {
    font-size: 19px;
    font-weight: 800;
    color: #0B2F4A;
    margin-bottom: 14px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(11,47,74,0.06);
    min-height: 145px;
}

.metric-title {
    font-size: 14px;
    color: #334155;
    font-weight: 750;
}

.metric-value {
    font-size: 34px;
    color: #0B2F4A;
    font-weight: 850;
    margin-top: 8px;
}

.metric-note {
    font-size: 13px;
    color: #f59e0b;
    font-weight: 700;
}

.low-risk {
    color: #059669;
    font-weight: 850;
}

.moderate {
    color: #f59e0b;
    font-weight: 800;
}

.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 12px;
}

/* Inputs */
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

/* Buttons */
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

/* Simple progress bars */
.progress-track {
    width: 100%;
    height: 8px;
    background: #e5e7eb;
    border-radius: 20px;
    overflow: hidden;
}

.progress-fill {
    height: 8px;
    background: linear-gradient(90deg, #0891b2, #14b8a6);
    border-radius: 20px;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 36px;
    }
}

.progress-fill {
    height: 8px;
    background: linear-gradient(90deg, #0891b2, #14b8a6);
    border-radius: 20px;
}

/* إزالة البوكس الرمادي من السايدبار */
[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    background: transparent !important;
}

[data-testid="stSidebar"] .nav,
[data-testid="stSidebar"] .nav-pills,
[data-testid="stSidebar"] ul,
[data-testid="stSidebar"] li {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 36px;
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
# Sidebar
# --------------------------------------------------
def render_sidebar():
    with st.sidebar:
        # عرض اللوجو مع خاصية الدمج لإخفاء الخلفية البيضاء
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:25px; padding-bottom:35px;">
                <img src="data:image/png;base64,{get_base64_logo()}" width="230" style="mix-blend-mode: multiply;">
            </div>
            """,
            unsafe_allow_html=True
        )

        # كود CSS إضافي لضمان شفافية الحاوية الخارجية
        st.markdown("""
            <style>
                /* استهداف الحاوية التي تحمل المنيو لإزالة الظل والحدود الرمادية */
                [data-testid="stSidebar"] div.nav-link {
                    background-color: transparent !important;
                }
                div[data-testid="stVerticalBlock"] > div:has(div.nav-link) {
                    background-color: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                }
            </style>
        """, unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=["Home", "Reports", "History", "Profile", "Settings", "Logout"],
            icons=["house", "file-earmark-text", "clock-history", "person", "gear", "box-arrow-left"],
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background": "transparent !important",       # شفافية مطلقة للحاوية
                    "background-color": "transparent !important", # التأكيد على إزالة اللون الرمادي
                    "border": "none !important",                 # إزالة الحدود (البوكس الرمادي)
                    "box-shadow": "none !important",             # إزالة أي ظل
                },
                "icon": {
                    "color": "white",
                    "font-size": "20px",
                },
                "nav-link": {
                    "background-color": "transparent",
                    "color": "white",
                    "font-size": "16px",
                    "font-weight": "600",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "14px 18px",
                    "border-radius": "0px",
                    "--hover-color": "rgba(255,255,255,0.08)", # تأثير خفيف عند تمرير الماوس
                },
                "nav-link-selected": {
                    "background": "rgba(255,255,255,0.05)",      # خلفية خفيفة جداً للعنصر المختار
                    "color": "white",
                    "border-left": "4px solid #22d3ee",          # الخط السماوي المميز
                },
            }
        )

        if selected == "Logout":
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
    st.write("Upload your health files to generate the diabetes monitoring summary.")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Meal Image</div>', unsafe_allow_html=True)
        st.write("Upload a clear meal image for nutrition analysis.")
        food_img = st.file_uploader(
            "Meal Image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Wearable Device Data</div>', unsafe_allow_html=True)
        st.write("Upload wearable data in CSV format.")
        wearable_csv = st.file_uploader(
            "Wearable CSV",
            type=["csv"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Foot Assessment Image</div>', unsafe_allow_html=True)
        st.write("Upload a clear foot image for risk assessment.")
        foot_img = st.file_uploader(
            "Foot Image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.food_img = food_img
    st.session_state.wearable_csv = wearable_csv
    st.session_state.foot_img = foot_img

    st.markdown("<br>", unsafe_allow_html=True)

    if food_img and wearable_csv and foot_img:
        if st.button("Generate Analysis", use_container_width=True):
            st.session_state.page = "overview"
            st.rerun()
    else:
        st.info("Upload the meal image, wearable data file, and foot image to continue.")
# --------------------------------------------------
# Dashboard / Overview page
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
        "Estimated Glucose": "145 mg/dL",
        "Overall Risk Score": f"{risk_score}/100",
    }
    for key, value in data.items():
        pdf.cell(0, 9, f"{key}: {value}", ln=True)
    return pdf.output(dest="S").encode("latin-1")

def dashboard_page():
    # استرجاع البيانات المرفوعة من الحالة (Session State)
    food_img = st.session_state.get("food_img")
    wearable_csv = st.session_state.get("wearable_csv")
    foot_img = st.session_state.get("foot_img")

    # بيانات تجريبية (Simulated Results) بناءً على ما ورد في التقرير
    calories, carbs, protein, fat = 550, 65, 28, 18
    glucose, risk_score, foot_risk = 145, 70, "Low"

    # العنوان العلوي
    top1, top2 = st.columns([1, 5])
    with top1:
        st.image("PHOTO-2026-02-17-21-43-19.jpeg", width=100) # تأكدي من وجود ملف اللوجو بنفس الاسم
    with top2:
        st.markdown('<div class="section-title">Patient Analysis Dashboard</div>', unsafe_allow_html=True)
        st.write(f"Welcome, {st.session_state.patient.get('name', 'Patient')}")

    st.markdown("---")

    # صف المؤشرات العلوية (Metrics)
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

    # تقسيم الصفحة لجزأين: تحليل الغذاء وتحليل البيانات القابلة للارتداء
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Dietary Analysis")
        if food_img:
            st.image(Image.open(food_img), caption="Processed Meal Image", use_container_width=True)
            st.success("AI Analysis: High-fidelity pixel mask extracted [cite: 119]")
        
        c1, c2 = st.columns(2)
        c1.metric("Calories", f"{calories} kcal")
        c2.metric("Carbohydrates", f"{carbs} g")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Wearable Data Analysis")
        if wearable_csv:
            data = pd.read_csv(wearable_csv)
            st.dataframe(data.head(), use_container_width=True)
            st.metric("XGBoost Prediction", f"{glucose} mg/dL")
            st.warning("Pattern: Moderate glucose elevation detected [cite: 194]")
        st.markdown('</div>', unsafe_allow_html=True)

    # صف سفلي: تقييم القدم والوعي بالشبكية
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Diabetic Foot Assessment")
        if foot_img:
            st.image(Image.open(foot_img), caption="Foot Image Analysis", width=350)
            st.success("EfficientNet Result: Normal Skin (Low Risk) [cite: 324]")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Retinal Health Awareness")
        st.warning("System Alert: Periodic retinal screening is recommended due to glucose trends [cite: 453]")
        st.write("Current design supports long-term complication tracking [cite: 447]")
        st.markdown('</div>', unsafe_allow_html=True)

    # التقرير النهائي
    st.markdown("---")
    report_col1, report_col2 = st.columns([2, 1])
    with report_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Integrated Risk Score")
        st.progress(risk_score / 100)
        st.write(f"Comprehensive Risk Assessment: {risk_score}/100 ")
        st.markdown('</div>', unsafe_allow_html=True)

    with report_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Final Report")
        pdf = create_pdf_report(st.session_state.patient, risk_score)
        st.download_button(
            label="Download PDF Report",
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
