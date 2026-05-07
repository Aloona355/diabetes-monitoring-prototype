import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(page_title="AI Diabetes Monitor", layout="wide")

# Use a transparent PNG logo if possible
LOGO = "IMG_5991.png"


# --------------------------------------------------
# Custom CSS styling
# --------------------------------------------------
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
    padding: 35px 20px 10px 20px;
}

.hero img {
    display: block;
    margin: 0 auto;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: #075985;
    margin-top: 18px;
    text-align: center;
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


# --------------------------------------------------
# Session state initialization
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "patient" not in st.session_state:
    st.session_state.patient = {}


# --------------------------------------------------
# PDF report generator
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
        "Patient ID": patient.get("id", "N/A"),
        "Age": patient.get("age", "N/A"),
        "Gender": patient.get("gender", "N/A"),
        "Diabetes Type": patient.get("type", "N/A"),
        "Estimated Calories": "550 kcal",
        "Estimated Carbohydrates": "65 g",
        "Predicted Glucose": "145 mg/dL",
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
# Sidebar navigation
# --------------------------------------------------
def render_sidebar():
    st.sidebar.image(LOGO, width=130)
    st.sidebar.markdown("## IDMS")

    selected = st.sidebar.radio(
        "Navigation",
        [
            "Overview",
            "Dietary Analysis",
            "Wearable Analysis",
            "Foot Assessment",
            "Retinal Awareness",
            "Risk Summary",
            "Reports",
            "History",
            "Profile",
            "Settings"
        ],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("Back to Upload", use_container_width=True):
        st.session_state.page = "upload"
        st.rerun()

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    return selected


# --------------------------------------------------
# Login page
# --------------------------------------------------
def login_page():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.image(LOGO, width=320)
    st.markdown(
        '<div class="hero-title">Intelligent Diabetes Monitoring System</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Login form without white card background
    left, center, right = st.columns([1, 1.2, 1])

    with center:
        st.markdown(
            '<div class="section-title" style="text-align:center;">Patient Information</div>',
            unsafe_allow_html=True
        )

        name = st.text_input("Full Name")
        patient_id = st.text_input("Patient ID")
        age = st.number_input("Age", min_value=1, max_value=100, value=23)
        gender = st.selectbox("Gender", ["Female", "Male"])
        diabetes_type = st.selectbox(
            "Diabetes Type",
            ["Type 1 Diabetes", "Type 2 Diabetes", "Prediabetes"]
        )

        if st.button("Continue to Data Upload", use_container_width=True):
            if name.strip() == "":
                st.error("Enter your name to continue.")
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


# --------------------------------------------------
# Upload page
# --------------------------------------------------
def upload_page():
    st.sidebar.image(LOGO, width=120)
    st.sidebar.markdown("### Patient Profile")
    st.sidebar.write(f"Name: {st.session_state.patient.get('name')}")
    st.sidebar.write(f"Age: {st.session_state.patient.get('age')}")
    st.sidebar.write(f"Type: {st.session_state.patient.get('type')}")

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    st.image(LOGO, width=160)
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
# Main overview page
# --------------------------------------------------
def overview_page():
    food_img = st.session_state.get("food_img")
    wearable_csv = st.session_state.get("wearable_csv")
    foot_img = st.session_state.get("foot_img")

    selected_page = render_sidebar()

    # Fixed demo values for prototype display
    calories = 550
    carbs = 65
    protein = 28
    fat = 18
    glucose = 145
    foot_risk = "Low Risk"
    risk_score = 46

    top1, top2 = st.columns([1, 5])

    with top1:
        st.image(LOGO, width=120)

    with top2:
        st.markdown('<div class="section-title">Integrated Health Overview</div>', unsafe_allow_html=True)
        st.write(f"Analysis summary for {st.session_state.patient.get('name')}")

    st.markdown("---")

    # Top health indicators
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-title">Estimated Glucose</div>
                <div class="metric-value">{glucose}</div>
                <div>mg/dL</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-title">Integrated Risk Score</div>
                <div class="metric-value">{risk_score}</div>
                <div>/100</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-title">Foot Health Status</div>
                <div class="metric-value">{foot_risk}</div>
                <div>No visible ulcer indicators</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m4:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-title">Estimated Meal Carbohydrates</div>
                <div class="metric-value">{carbs}</div>
                <div>g</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown("---")

    left, right = st.columns(2)

    # Dietary analysis section
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Meal Nutrition Analysis")
        st.image(Image.open(food_img), caption="Uploaded Meal Image", use_container_width=True)

        c1, c2 = st.columns(2)
        c1.metric("Calories", f"{calories} kcal")
        c1.metric("Protein", f"{protein} g")
        c2.metric("Carbohydrates", f"{carbs} g")
        c2.metric("Fat", f"{fat} g")

        # Personalized food recommendation based on carbohydrates
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

    # Wearable analysis section
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

    # Foot assessment section
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Diabetic Foot Assessment")
        st.image(Image.open(foot_img), caption="Uploaded Foot Image", width=350)
        st.success("Low Risk: No visible ulcer indicators detected in the uploaded image.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Retinal awareness section
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Retinal Health Awareness")

        # Retinal warning only appears when patient data indicates poor glucose status
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

    # Integrated risk summary
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

    # PDF report download
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
# Page routing
# --------------------------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.page == "upload":
        upload_page()
    else:
        overview_page()
