import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime
import base64
import random
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import io

st.set_page_config(page_title="AI Diabetes Monitor", layout="wide")

LOGO = "IMG_5991.png"


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def get_base64_logo():
    try:
        with open(LOGO, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return ""

def clean_pdf_text(text):
    return str(text).encode("latin-1", "ignore").decode("latin-1")


def generate_glucose_chart():
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    glucose_values = [132, 145, 138, 160, 142, 135, 145]

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(days, glucose_values, marker='o', color='#0891b2', linewidth=2.5, markersize=7)
    ax.axhline(y=140, color='#f59e0b', linestyle='--', linewidth=1.5, label='Target (140 mg/dL)')
    ax.fill_between(days, glucose_values, alpha=0.15, color='#0891b2')
    ax.set_ylabel("mg/dL", fontsize=10)
    ax.set_title("Glucose Levels – Last 7 Days", fontsize=12, fontweight='bold', color='#0b2f4a')
    ax.legend(fontsize=9)
    ax.set_facecolor('#f8fbfd')
    fig.patch.set_facecolor('#f8fbfd')
    ax.tick_params(axis='x', labelsize=8)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf


def generate_meal_chart():
    categories = ["Healthy\nMeals", "High Carb\nMeals", "High Fat\nMeals", "Balanced\nMeals"]
    values = [8, 5, 3, 5]
    colors = ['#059669', '#f59e0b', '#ef4444', '#0891b2']

    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(categories, values, color=colors, width=0.5, edgecolor='white', linewidth=1.5)
    ax.set_ylabel("Number of Meals", fontsize=10)
    ax.set_title("Meal Quality – Last 7 Days", fontsize=12, fontweight='bold', color='#0b2f4a')
    ax.set_facecolor('#f8fbfd')
    fig.patch.set_facecolor('#f8fbfd')
    ax.tick_params(axis='x', labelsize=8)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, str(val),
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0b2f4a')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf


def create_pdf_report(glucose, foot_risk, retinal_status):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(11, 47, 74)
    pdf.cell(0, 12, "Intelligent Diabetes Monitoring System", ln=True, align="C")
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 8, "Health Summary Report", ln=True, align="C")
    pdf.ln(4)

    pdf.set_font("Arial", size=10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 7, clean_pdf_text(f"Generated: {datetime.now().strftime('%Y-%m-%d  %H:%M')}"), ln=True, align="C")
    pdf.ln(6)

    # Divider
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Quick Summary
    avg_glucose = 142
    trend = "slightly elevated"
    summary = (
        f"Over the past 7 days, your average glucose level was {avg_glucose} mg/dL, which is {trend}. "
        f"Your meal pattern shows a mix of healthy and high-carbohydrate meals. "
        f"Foot health remains {foot_risk.lower()} risk. Retinal status: {retinal_status}."
    )
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(11, 47, 74)
    pdf.cell(0, 8, "Quick Summary", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(71, 85, 105)
    pdf.multi_cell(0, 6, clean_pdf_text(summary))
    pdf.ln(5)

    # Glucose Chart
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(11, 47, 74)
    pdf.cell(0, 8, "Glucose Trend – Last 7 Days", ln=True)
    glucose_buf = generate_glucose_chart()
    glucose_buf.seek(0)
    with open("/tmp/glucose_chart.png", "wb") as f:
        f.write(glucose_buf.read())
    pdf.image("/tmp/glucose_chart.png", x=15, w=175)
    pdf.ln(4)

    # Meal Chart
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(11, 47, 74)
    pdf.cell(0, 8, "Meal Quality – Last 7 Days", ln=True)
    meal_buf = generate_meal_chart()
    meal_buf.seek(0)
    with open("/tmp/meal_chart.png", "wb") as f:
        f.write(meal_buf.read())
    pdf.image("/tmp/meal_chart.png", x=40, w=120)
    pdf.ln(4)

    # Divider
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Foot & Retinal
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(11, 47, 74)
    pdf.cell(0, 8, "Clinical Assessments", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 7, clean_pdf_text(f"  Foot Health:    {foot_risk} Risk – No ulcer indicators detected."), ln=True)
    pdf.cell(0, 7, clean_pdf_text(f"  Retinal Health: {retinal_status}"), ln=True)
    pdf.ln(5)

    # Divider
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Recommendations
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(11, 47, 74)
    pdf.cell(0, 8, "Recommendations", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(71, 85, 105)

    recs = []
    if avg_glucose >= 140:
        recs.append("Glucose levels are slightly elevated. Consider reducing carbohydrate intake.")
    if foot_risk == "Low":
        recs.append("Continue regular foot care and daily self-inspection.")
    if retinal_status == "No warning detected":
        recs.append("Maintain routine annual retinal screening.")
    else:
        recs.append("Retinal screening is recommended. Please consult your ophthalmologist.")

    for rec in recs:
        pdf.cell(0, 7, clean_pdf_text(f"  - {rec}"), ln=True)

    pdf.ln(8)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 6, "This report is generated by an AI-assisted prototype and is not a substitute for professional medical advice.", ln=True, align="C")

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

.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 12px;
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
    background: linear-gradient(180deg, #06263d 0%, #031827 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.18);
}

.dashboard-title {
    font-size: 34px;
    font-weight: 850;
    color: #0b2f4a;
    margin-bottom: 8px;
}

.dashboard-welcome {
    font-size: 18px;
    font-weight: 650;
    color: #0b2f4a;
    margin-bottom: 25px;
}

.metric-card {
    background: #ffffff;
    border-radius: 22px;
    padding: 32px 20px;
    text-align: center;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
    min-height: 170px;
    color: #0b2f4a;
}

.metric-title {
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 18px;
}

.metric-value {
    font-size: 42px;
    font-weight: 900;
    line-height: 1.1;
}

.metric-unit {
    font-size: 18px;
    font-weight: 700;
    margin-top: 12px;
}

.section-card {
    background: #ffffff;
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
    color: #0b2f4a;
    margin-bottom: 25px;
}

.section-heading {
    font-size: 30px;
    font-weight: 850;
    color: #0b2f4a;
    margin-bottom: 18px;
}

@media (max-width: 768px) {
    .hero-title { font-size: 36px; }
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
        logo_b64 = get_base64_logo()
        if logo_b64:
            st.markdown(
                f"""
                <div style="text-align:center; padding-top:25px; padding-bottom:35px;">
                    <img src="data:image/png;base64,{logo_b64}" width="230">
                </div>
                """,
                unsafe_allow_html=True
            )

        selected = option_menu(
            menu_title=None,
            options=["Home", "Retinal Scan", "Reports", "History", "Profile", "Settings", "Logout"],
            icons=["house", "eye", "file-earmark-text", "clock-history", "person", "gear", "box-arrow-left"],
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
# Login / Create Account
# --------------------------------------------------
def login_page():
    logo_left, logo_center, logo_right = st.columns([1, 1.4, 1])
    with logo_center:
        try:
            st.image(LOGO, width=430)
        except:
            pass

    st.markdown(
        '<div class="hero-title">Intelligent Diabetes Monitoring System</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.15, 1])

    with center:
        if st.session_state.auth_mode == "login":
            st.markdown('<div class="section-title" style="text-align:center;">Welcome Back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Sign in to continue monitoring your health insights.</div>', unsafe_allow_html=True)

            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            st.checkbox("Remember me")

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
                    }
                    st.session_state.logged_in = True
                    st.session_state.page = "upload"
                    st.rerun()

            st.markdown('<div class="small-center-text">Don\'t have an account?</div>', unsafe_allow_html=True)

            if st.button("Create Account", use_container_width=True):
                st.session_state.auth_mode = "create"
                st.rerun()

        else:
            st.markdown('<div class="section-title" style="text-align:center;">Create Your Account</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Create an account to start your diabetes monitoring journey.</div>', unsafe_allow_html=True)

            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            age = st.number_input("Age", min_value=1, max_value=100, value=23)
            gender = st.selectbox("Gender", ["Female", "Male"])

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
                    }
                    st.session_state.logged_in = True
                    st.session_state.page = "upload"
                    st.rerun()

            st.markdown('<div class="small-center-text">Already have an account?</div>', unsafe_allow_html=True)

            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()


# --------------------------------------------------
# Upload page
# --------------------------------------------------
def upload_page():
    selected = render_sidebar()

    if selected == "Retinal Scan":
        retinal_scan_page()
        return
    elif selected == "Reports":
        reports_page()
        return
    elif selected == "History":
        history_page()
        return
    elif selected == "Profile":
        profile_page()
        return
    elif selected == "Settings":
        settings_page()
        return

    st.markdown(
        """
        <div style="margin-bottom:10px;">
            <div class="section-title">Upload Health Data</div>
            <div style="color:#475569; font-size:16px;">
                Upload your health files to generate the diabetes monitoring summary.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Current time display
    now = datetime.now()
    st.markdown(
        f"""
        <div style="background:white; border-radius:14px; padding:14px 20px; border:1px solid #e2e8f0;
                    box-shadow:0 4px 12px rgba(11,47,74,0.06); display:inline-block; margin-bottom:20px;">
            <span style="color:#64748b; font-size:14px; font-weight:600;">Current Date & Time &nbsp;</span>
            <span style="color:#0b2f4a; font-size:16px; font-weight:800;">
                {now.strftime("%A, %B %d %Y")} &nbsp;|&nbsp; {now.strftime("%I:%M %p")}
            </span>
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
        <div style="color:#475569; margin-bottom:15px;">Upload a clear meal image for nutrition analysis.</div>
        """, unsafe_allow_html=True)
        food_img = st.file_uploader("", type=["jpg", "jpeg", "png"], key="food_upload", label_visibility="hidden")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="card-title">Wearable Device Data</div>
        <div style="color:#475569; margin-bottom:15px;">Upload wearable data in CSV format.</div>
        """, unsafe_allow_html=True)
        wearable_csv = st.file_uploader("", type=["csv"], key="wearable_upload", label_visibility="hidden")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="card-title">Foot Assessment Image</div>
        <div style="color:#475569; margin-bottom:15px;">Upload a clear foot image for risk assessment.</div>
        """, unsafe_allow_html=True)
        foot_img = st.file_uploader("", type=["jpg", "jpeg", "png"], key="foot_upload", label_visibility="hidden")
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
# Dashboard
# --------------------------------------------------
def dashboard_page():
    selected_page = render_sidebar()

    if selected_page == "Retinal Scan":
        retinal_scan_page()
        return
    elif selected_page == "Reports":
        reports_page()
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

    food_img = st.session_state.get("food_img")
    wearable_csv = st.session_state.get("wearable_csv")
    foot_img = st.session_state.get("foot_img")

    calories, carbs, protein, fat = 550, 65, 28, 18
    glucose = 145
    foot_risk = "Low"

    now = datetime.now()

    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px; flex-wrap:wrap; gap:10px;">
            <div>
                <div class="dashboard-title">Your Health Analysis Summary</div>
                <div class="dashboard-welcome">Hello, {st.session_state.patient.get("name", "Patient")}</div>
            </div>
            <div style="background:white; border-radius:14px; padding:12px 20px; border:1px solid #e2e8f0;
                        box-shadow:0 4px 12px rgba(11,47,74,0.06); text-align:right;">
                <div style="color:#64748b; font-size:12px; font-weight:600;">Analysis Time</div>
                <div style="color:#0b2f4a; font-size:18px; font-weight:800;">{now.strftime("%I:%M %p")}</div>
                <div style="color:#64748b; font-size:12px;">{now.strftime("%A, %B %d %Y")}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Predicted Glucose</div>
                <div class="metric-value">{glucose}</div>
                <div class="metric-unit">mg/dL</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Foot Risk</div>
                <div class="metric-value">{foot_risk}</div>
                <div class="metric-unit">No ulcer detected</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Meal Carbs</div>
                <div class="metric-value">{carbs}</div>
                <div class="metric-unit">g</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-card"><div class="section-heading">Dietary Analysis</div>', unsafe_allow_html=True)
        if food_img:
            st.image(Image.open(food_img), use_container_width=True)
        else:
            st.info("No meal image uploaded.")
        st.metric("Calories", f"{calories} kcal")
        st.metric("Carbohydrates", f"{carbs} g")
        st.metric("Protein", f"{protein} g")
        st.metric("Fat", f"{fat} g")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card"><div class="section-heading">Wearable Data Analysis</div>', unsafe_allow_html=True)
        if wearable_csv:
            wearable_data = pd.read_csv(wearable_csv)
            st.dataframe(wearable_data.head(), use_container_width=True)
        else:
            sample_data = pd.DataFrame({
                "Time": ["10:00 AM", "11:00 AM", "12:00 PM"],
                "Heart Rate": [72, 80, 76],
                "Glucose Estimate": [120, 132, 145]
            })
            st.dataframe(sample_data, use_container_width=True)
        st.line_chart([120, 132, 145, 138, 149])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card"><div class="section-heading">Foot Assessment</div>', unsafe_allow_html=True)
        if foot_img:
            st.image(Image.open(foot_img), width=350)
        else:
            st.info("No foot image uploaded.")
        st.success("Low Risk: No ulcer indicators found.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card"><div class="section-heading">Retinal Health Awareness</div>', unsafe_allow_html=True)
        retinal_img = st.session_state.get("retinal_img")
        if retinal_img:
            st.image(Image.open(retinal_img), use_container_width=True)
            if glucose >= 180:
                st.warning("Your glucose pattern may indicate a higher retinal health risk. Please schedule a retinal check-up.")
            else:
                st.success("No retinal risk warning detected at this time.")
        else:
            st.info("No retinal image uploaded. Go to Retinal Scan in the sidebar to upload.")
        st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Retinal Scan Page
# --------------------------------------------------
def retinal_scan_page():
    st.markdown('<div class="section-title">Retinal Scan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#475569; font-size:16px; margin-bottom:20px;">Upload a retinal image for diabetic retinopathy risk assessment.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-title">Retinal Image Upload</div>
    <div style="color:#475569; margin-bottom:15px;">
        Upload a clear retinal scan image. Supported formats: JPG, JPEG, PNG.
    </div>
    """, unsafe_allow_html=True)

    retinal_img = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        key="retinal_upload",
        label_visibility="hidden"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if retinal_img:
        st.session_state.retinal_img = retinal_img
        st.image(Image.open(retinal_img), caption="Uploaded Retinal Image", use_container_width=True)
        st.success("Retinal image uploaded successfully. Analysis will appear on the dashboard.")
    else:
        st.session_state.retinal_img = None
        st.info("No retinal image uploaded yet.")


# --------------------------------------------------
# Reports Page
# --------------------------------------------------
def reports_page():
    st.markdown('<div class="section-title">Health Report</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#475569; font-size:16px; margin-bottom:20px;">Generate and download your health summary report as a PDF.</div>',
        unsafe_allow_html=True
    )

    glucose = 145
    foot_risk = "Low"
    retinal_img = st.session_state.get("retinal_img")
    retinal_status = "No warning detected" if not retinal_img or glucose < 180 else "Further screening recommended"

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-title">Report Contents</div>
    <ul style="color:#475569; font-size:15px; line-height:2;">
        <li>Quick health summary</li>
        <li>Glucose trend chart – last 7 days</li>
        <li>Meal quality chart – last 7 days</li>
        <li>Foot assessment result</li>
        <li>Retinal health status</li>
        <li>Recommendations</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Generate PDF Report", use_container_width=True):
        with st.spinner("Generating your report..."):
            pdf = create_pdf_report(glucose, foot_risk, retinal_status)
        st.download_button(
            label="Download PDF Report",
            data=pdf,
            file_name=f"Health_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# --------------------------------------------------
# Other Sidebar Pages
# --------------------------------------------------
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
