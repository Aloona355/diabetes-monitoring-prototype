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
        # إزالة الخلفية البيضاء من اللوجو ودمجه مع الكحلي
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:25px; padding-bottom:35px;">
                <img src="data:image/png;base64,{get_base64_logo()}" width="230" style="mix-blend-mode: multiply;">
            </div>
            """,
            unsafe_allow_html=True
        )

        # كود CSS جبار لإخفاء البوكس الرمادي نهائياً
        st.markdown("""
            <style>
                /* استهداف الحاوية الخارجية للمنيو وإزالة الحدود والظلال */
                div[data-testid="stVerticalBlock"] div[style*="flex-direction: column"] > div {
                    background-color: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                }
                /* التأكد من أن المنيو نفسه شفاف */
                .nav-link {
                    background-color: transparent !important;
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
                    "background-color": "transparent!important", # شفافية مطلقة
                    "border": "none!important",                # إلغاء الحدود تماماً
                    "box-shadow": "none!important",
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
                },
                "nav-link-selected": {
                    "background-color": "rgba(255,255,255,0.08)", # ظل خفيف جداً للاختيار الحالي
                    "color": "white",
                    "border-left": "4px solid #22d3ee",         # الخط السماوي المميز
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
def overview_page():
    selected_section = render_sidebar()

    food_img = st.session_state.get("food_img")
    wearable_csv = st.session_state.get("wearable_csv")
    foot_img = st.session_state.get("foot_img")

    calories = 550
    carbs = 65
    protein = 28
    fat = 18
    glucose = 145
    risk_score = 46

    # Header
    top_left, top_right = st.columns([4, 1])

    with top_left:
        st.markdown('<div class="section-title">Home</div>', unsafe_allow_html=True)
        st.write(f"Welcome back, {st.session_state.patient.get('name', 'Patient')}")

    with top_right:
        st.write(datetime.now().strftime("%b %d, %Y"))
        st.write(st.session_state.patient.get("name", "Patient"))

    st.markdown("---")

    # Top metrics
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Estimated Glucose</div>
            <div class="metric-value">{glucose} <span style="font-size:16px;">mg/dL</span></div>
            <div class="metric-note">Moderate</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Risk Score</div>
            <div class="metric-value">{risk_score} <span style="font-size:16px;">/100</span></div>
            <div class="metric-note">Moderate Risk</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Foot Risk</div>
            <div class="metric-value low-risk">Low</div>
            <div class="metric-note" style="color:#64748b;">No ulcer detected</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Last Meal Carbs</div>
            <div class="metric-value">{carbs} <span style="font-size:16px;">g</span></div>
            <div class="metric-note" style="color:#64748b;">Today</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Dietary and wearable sections
    left, right = st.columns([1, 1.45])

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Dietary Analysis</div>', unsafe_allow_html=True)

        if food_img:
            st.image(Image.open(food_img), use_container_width=True)
        else:
            st.info("No meal image uploaded.")

        c1, c2 = st.columns(2)
        c1.metric("Calories", f"{calories} kcal")
        c1.metric("Protein", f"{protein} g")
        c2.metric("Carbohydrates", f"{carbs} g")
        c2.metric("Fat", f"{fat} g")

        if carbs >= 70:
            st.warning("This meal is high in carbohydrates. Consider reducing starchy portions.")
        elif carbs >= 45:
            st.info("This meal contains a moderate amount of carbohydrates. Monitor your glucose response.")
        else:
            st.success("This meal appears to be a suitable low-carbohydrate choice.")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Wearable Data Analysis</div>', unsafe_allow_html=True)

        if wearable_csv:
            data = pd.read_csv(wearable_csv)
            st.dataframe(data.head(), use_container_width=True)
        else:
            sample_data = pd.DataFrame({
                "Time": ["10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM", "02:00 PM"],
                "Heart Rate (bpm)": [78, 82, 76, 80, 83],
                "Steps": [1200, 1450, 1800, 2100, 2300],
                "Sleep (h)": [7.2, 7.2, 7.2, 7.1, 7.1],
                "Glucose (Est.)": ["138 mg/dL", "142 mg/dL", "145 mg/dL", "147 mg/dL", "149 mg/dL"]
            })
            st.dataframe(sample_data, use_container_width=True)

        st.markdown(
            f"""
            <div style="margin-top:12px;">
                <b>Estimated Glucose Level</b><br>
                <span style="font-size:32px; font-weight:850; color:#0B2F4A;">{glucose}</span>
                <span>mg/dL</span>
                <span class="moderate" style="margin-left:18px;">Moderate</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # Foot and retinal sections
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Foot Assessment</div>', unsafe_allow_html=True)

        img_col, result_col = st.columns([1, 1])

        with img_col:
            if foot_img:
                st.image(Image.open(foot_img), use_container_width=True)
            else:
                st.info("No foot image uploaded.")

        with result_col:
            st.markdown("""
            <div style="border:1px solid #e2e8f0; border-radius:14px; padding:18px;">
                <b>Result</b><br>
                <span class="low-risk" style="font-size:24px;">Low Risk</span><br>
                <span style="font-size:13px; color:#64748b;">No ulcer detected</span>
            </div>
            <br>
            <span style="font-size:12px; color:#64748b;">Model: EfficientNet</span>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Retinal Health Awareness</div>', unsafe_allow_html=True)

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

    # Risk and report sections
    risk_col, report_col = st.columns([1.45, 1])

    with risk_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Integrated Risk Score</div>', unsafe_allow_html=True)

        score_col, factors_col = st.columns([1, 1.3])

        with score_col:
            st.markdown(f"""
            <div style="text-align:center;">
                <div style="font-size:46px; font-weight:900; color:#0B2F4A;">{risk_score}</div>
                <div style="font-size:16px;">/100</div>
                <div class="moderate">Moderate Risk</div>
            </div>
            """, unsafe_allow_html=True)

        with factors_col:
            st.write("Risk Factors Contribution")

            st.write("Diet")
            st.markdown('<div class="progress-track"><div class="progress-fill" style="width:40%;"></div></div>', unsafe_allow_html=True)
            st.caption("40%")

            st.write("Glucose")
            st.markdown('<div class="progress-track"><div class="progress-fill" style="width:60%;"></div></div>', unsafe_allow_html=True)
            st.caption("60%")

            st.write("Foot Health")
            st.markdown('<div class="progress-track"><div class="progress-fill" style="width:20%;"></div></div>', unsafe_allow_html=True)
            st.caption("20%")

        st.markdown('</div>', unsafe_allow_html=True)

    with report_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Download Report</div>', unsafe_allow_html=True)
        st.write("Download your health report in PDF format.")

        pdf = create_pdf_report(st.session_state.patient, risk_score)

        st.download_button(
            label="Download PDF Report",
            data=pdf,
            file_name="Diabetes_Health_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="footer-note">This system is an academic prototype and is not intended for clinical diagnosis.</div>',
        unsafe_allow_html=True
    )


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
