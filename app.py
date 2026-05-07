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

def clean_pdf_text(text):
    return str(text).encode("latin-1", "ignore").decode("latin-1")


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
        "Recommendation": "Maintain regular glucose monitoring and schedule retinal screening if needed."
    }

    for key, value in data.items():
        line = clean_pdf_text(f"{key}: {value}")
        pdf.cell(0, 9, line, ln=True)

    return pdf.output(dest="S").encode("latin-1", "ignore")


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
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:25px; padding-bottom:35px;">
                <img src="data:image/png;base64,{get_base64_logo()}" width="230">
            </div>
            """,
            unsafe_allow_html=True
        )

        selected = option_menu(
            menu_title=None,
            options=["Home", "Reports", "History", "Profile", "Settings", "Logout"],
            icons=["house", "file-earmark-text", "clock-history", "person", "gear", "box-arrow-left"],
            default_index=0,
            styles={
                "container": {"padding": "0px", "background-color": "#06263d"},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {
                    "background-color": "#06263d",
                    "color": "white",
                    "font-size": "16px",
                    "font-weight": "600",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "14px 18px",
                    "border-radius": "0px",
                    "--hover-color": "rgba(255,255,255,0.08)",
                },
                "nav-link-selected": {
                    "background-color": "rgba(255,255,255,0.08)",
                    "color": "white",
                    "border-left": "4px solid #22d3ee",
                    "font-weight": "700",
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

    selected = render_sidebar()

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:10px;">
            <div>
                <div class="section-title">Upload Health Data</div>
                <div style="color:#475569; font-size:16px;">
                    Upload your health files to generate the diabetes monitoring summary.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="card-title">Meal Image</div>
        <div style="color:#475569; margin-bottom:15px;">
            Upload a clear meal image for nutrition analysis.
        </div>
        """, unsafe_allow_html=True)

        food_img = st.file_uploader(
            "",
            type=["jpg", "jpeg", "png"],
            key="food_upload",
            label_visibility="hidden"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="card-title">Wearable Device Data</div>
        <div style="color:#475569; margin-bottom:15px;">
            Upload wearable data in CSV format.
        </div>
        """, unsafe_allow_html=True)

        wearable_csv = st.file_uploader(
            "",
            type=["csv"],
            key="wearable_upload",
            label_visibility="hidden"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="card-title">Foot Assessment Image</div>
        <div style="color:#475569; margin-bottom:15px;">
            Upload a clear foot image for risk assessment.
        </div>
        """, unsafe_allow_html=True)

        foot_img = st.file_uploader(
            "",
            type=["jpg", "jpeg", "png"],
            key="foot_upload",
            label_visibility="hidden"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.food_img = food_img
    st.session_state.wearable_csv = wearable_csv
    st.session_state.foot_img = foot_img

    st.markdown("<br>", unsafe_allow_html=True)

    if food_img and wearable_csv and foot_img:

        st.success("All files uploaded successfully.")

        if st.button("Start AI Analysis", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    else:
        st.info("Upload the meal image, wearable data file, and foot image to continue.")

# --------------------------------------------------
# Dashboard / Overview page
# --------------------------------------------------
def dashboard_page():
    # 1. جلب البيانات والصفحة المختارة
    selected_page = render_sidebar()
    food_img = st.session_state.get("food_img")
    wearable_csv = st.session_state.get("wearable_csv")
    foot_img = st.session_state.get("foot_img")

    # بيانات المحاكاة
    calories, carbs, protein, fat = 550, 65, 28, 18
    glucose, risk_score, foot_risk = 145, 70, "Low"

    # 2. توجيه الصفحات الجانبية
    if selected_page == "Reports":
        reports_page(risk_score)
        return
    elif selected_page == "History":
        history_page()
        return
    elif selected_page == "Profile":
        profile_page()
        return
    elif selected_page == "Settings":
        settings_page()
        return

    # 3. الستايل (يجب أن يكون داخل الدالة ليعمل عند استدعائها)
    st.markdown("""
    <style>
    .block-container { max-width: 1180px; padding-top: 2rem; }
    .dashboard-title { font-size: 34px; font-weight: 850; color: #0b2f4a; margin-bottom: 8px; }
    .dashboard-welcome { font-size: 18px; font-weight: 650; color: #0b2f4a; }
    .metric-card { background: #ffffff; border-radius: 22px; padding: 32px 20px; text-align: center; box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08); min-height: 170px; color: #0b2f4a; }
    .metric-title { font-size: 16px; font-weight: 800; margin-bottom: 18px; }
    .metric-value { font-size: 42px; font-weight: 900; line-height: 1.1; }
    .metric-unit { font-size: 18px; font-weight: 700; margin-top: 12px; }
    .section-card { background: #ffffff; border-radius: 22px; padding: 30px; box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08); color: #0b2f4a; margin-bottom: 25px; }
    .section-heading { font-size: 30px; font-weight: 850; color: #0b2f4a; margin-bottom: 18px; }
    .recommendation { background: #f8fafc; border-left: 5px solid #0f766e; padding: 15px; border-radius: 12px; margin-top: 15px; color: #0b2f4a; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

    # 4. محتوى الهيدر (Header)
    st.markdown('<div class="dashboard-title">Your Health Analysis Summary</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dashboard-welcome">Hello, {st.session_state.patient.get("name", "Patient")}</div>', unsafe_allow_html=True)
    st.markdown("---")

    # 5. المؤشرات العلوية (Metrics)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Predicted Glucose</div><div class="metric-value">{glucose}</div><div class="metric-unit">mg/dL</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Risk Score</div><div class="metric-value">{risk_score}</div><div class="metric-unit">/100</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Foot Risk</div><div class="metric-value">{foot_risk}</div><div class="metric-unit">No ulcer detected</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Meal Carbs</div><div class="metric-value">{carbs}</div><div class="metric-unit">g</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # 6. الأقسام التفصيلية (Dietary & Wearable)
  # 6. الأقسام التفصيلية (Dietary & Wearable)
left, right = st.columns(2)

with left:
    st.markdown(
        '<div class="section-card"><div class="section-heading">Dietary Analysis</div>',
        unsafe_allow_html=True
    )

    if food_img:
        st.image(Image.open(food_img), use_container_width=True)

    st.metric("Calories", f"{calories} kcal")
    st.metric("Carbohydrates", f"{carbs} g")

    st.markdown(
        '<div class="recommendation">This meal is high in carbs. Consider balancing it with fiber.</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Wearable Data Analysis</div>',
        unsafe_allow_html=True
    )

    if wearable_csv:
        st.dataframe(
            pd.read_csv(wearable_csv).head(),
            use_container_width=True
        )

    st.line_chart([120, 132, 145, 138, 149])

    st.markdown(
        '<div class="recommendation">Moderate glucose elevation detected.</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---", unsafe_allow_html=True)

    # 7. التقييمات الإضافية (Foot & Retina)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card"><div class="section-heading">Foot Assessment</div>', unsafe_allow_html=True)
        if foot_img: st.image(Image.open(foot_img), width=350)
        st.success("Low Risk: No ulcer indicators found")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card"><div class="section-heading">Retinal Health Awareness</div>', unsafe_allow_html=True)
        if risk_score >= 70:
            st.warning("Schedule a retinal check-up")
        else:
            st.success("No retinal risk detected.")
        st.markdown('</div>', unsafe_allow_html=True)
# --------------------------------------------------
# Sidebar Pages
# --------------------------------------------------
def reports_page(risk_score):
    st.markdown('<div class="section-title">Reports</div>', unsafe_allow_html=True)
    st.write("Download your health report in PDF format.")

    pdf = create_pdf_report(st.session_state.patient, risk_score)

    st.download_button(
        label="Download PDF Report",
        data=pdf,
        file_name="Diabetes_Health_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )


def history_page():
    st.markdown('<div class="section-title">History</div>', unsafe_allow_html=True)
    st.info("No previous analysis records are available yet.")


def profile_page():
    patient = st.session_state.patient

    st.markdown('<div class="section-title">Profile</div>', unsafe_allow_html=True)
    st.write(f"Name: {patient.get('name', 'Patient')}")
    st.write(f"Email: {patient.get('email', 'N/A')}")
    st.write(f"Age: {patient.get('age', 'N/A')}")
    st.write(f"Gender: {patient.get('gender', 'N/A')}")
    st.write(f"Diabetes Type: {patient.get('type', 'N/A')}")


def settings_page():
    st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)
    st.info("Settings can be expanded in future versions of this prototype.")

# --------------------------------------------------
# Routing
# --------------------------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.page == "upload":
        upload_page()
    else:
        dashboard_page()
