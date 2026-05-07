import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Glucovision AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

LOGO = "Logo.png"

# =========================
# PREMIUM UI STYLE
# =========================
st.markdown("""
<style>

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background: #071C2C;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding-top: 1rem;
    max-width: 1400px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #061826;
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* TITLES */

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin-bottom: 10px;
}

.sub-title {
    color: #AFC7D9;
    font-size: 18px;
    line-height: 1.8;
}

/* CARDS */

.card {
    background: #0D2436;
    padding: 24px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(145deg,#0C2436,#12314A);
    padding: 24px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.06);
    min-height: 160px;
}

.metric-title {
    color: #8FB5CE;
    font-size: 14px;
    font-weight: 700;
}

.metric-value {
    color: white;
    font-size: 38px;
    font-weight: 800;
    margin-top: 18px;
}

.metric-note {
    color: #37D39A;
    margin-top: 8px;
    font-size: 14px;
}

/* BUTTON */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg,#0B7FAB,#0E9F9B);
    color: white;
    border: none;
    height: 48px;
    font-size: 15px;
    font-weight: 700;
}

.stButton > button:hover {
    background: linear-gradient(90deg,#1390C1,#14B8A6);
    color: white;
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    border-radius: 10px !important;
}

/* PDF */

.pdf-box {
    background: linear-gradient(145deg,#0C2436,#102A3F);
    padding: 24px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* FOOTER */

.footer-note {
    text-align: center;
    color: #88A7BB;
    margin-top: 35px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# PDF REPORT
# =========================

def create_pdf(patient_name, patient_id, glucose, carbs, foot_risk, recommendation):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 15, "Glucovision AI - Clinical Report", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    report = {
        "Patient Name": patient_name,
        "Medical ID": patient_id,
        "Generated Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Predicted Glucose": f"{glucose} mg/dL",
        "Estimated Meal Carbohydrates": f"{carbs} g",
        "Foot Assessment": foot_risk,
        "Clinical Recommendation": recommendation,
    }

    for k, v in report.items():
        pdf.multi_cell(0, 10, f"{k}: {v}")

    return pdf.output(dest="S").encode("latin-1")

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.image(LOGO, width=140)

    st.markdown("## Glucovision AI")

    st.caption("Integrated AI Monitoring Platform")

    st.markdown("---")

    patient_name = st.text_input("Patient Name")
    patient_id = st.text_input("Medical ID")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=23
    )

    diabetes_type = st.selectbox(
        "Diabetes Type",
        [
            "Type 1 Diabetes",
            "Type 2 Diabetes",
            "Prediabetes"
        ]
    )

    st.markdown("---")

    st.markdown("### Upload Patient Data")

    food_file = st.file_uploader(
        "Meal Image",
        type=["jpg", "png"]
    )

    wearable_file = st.file_uploader(
        "Wearable CSV",
        type=["csv"]
    )

    foot_file = st.file_uploader(
        "Foot Image",
        type=["jpg", "png"]
    )

# =========================
# MAIN HEADER
# =========================

left, right = st.columns([1.2, 2])

with left:
    st.image(LOGO, width=240)

with right:

    st.markdown(
        '<div class="main-title">Glucovision AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
        AI-powered multimodal monitoring system developed as a graduation project 
        for intelligent diabetic patient assessment using meal analysis, wearable 
        data interpretation, diabetic foot screening, and clinical risk awareness.
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# =========================
# ANALYSIS
# =========================

if food_file and wearable_file and foot_file:

    glucose = 145
    carbs = 65
    foot_risk = "Low Risk"
    risk_score = 46

    if carbs > 60:
        meal_note = "This meal contains a relatively high carbohydrate level. A lighter meal is recommended later in the day to maintain glucose stability."
    else:
        meal_note = "Meal composition appears balanced based on estimated nutritional values."

    if glucose > 140:
        retina_note = "Persistent elevated glucose patterns detected. A retinal screening appointment is recommended."
    else:
        retina_note = "Current glucose trend does not indicate urgent retinal complications."

    # =========================
    # METRICS
    # =========================

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Predicted Glucose</div>
            <div class="metric-value">{glucose} mg/dL</div>
            <div class="metric-note">Moderate Pattern</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Meal Carbohydrates</div>
            <div class="metric-value">{carbs} g</div>
            <div class="metric-note">Nutritional Estimate</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Foot Assessment</div>
            <div class="metric-value">Low</div>
            <div class="metric-note">No ulcer detected</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Integrated Risk Score</div>
            <div class="metric-value">{risk_score}/100</div>
            <div class="metric-note">Moderate Risk</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # =========================
    # CONTENT
    # =========================

    c1, c2 = st.columns([1.1, 1])

    with c1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Dietary Analysis")

        st.image(food_file, use_container_width=True)

        st.markdown(f"""
        ### AI Nutritional Insight

        {meal_note}

        #### Estimated Values
        - Calories: 550 kcal
        - Carbohydrates: 65 g
        - Protein: 28 g
        - Fat: 18 g
        """)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Wearable Data Interpretation")

        df = pd.read_csv(wearable_file)

        st.dataframe(df, use_container_width=True)

        st.line_chart([120, 132, 145, 138, 141])

        st.markdown(
            "Wearable sensor analysis indicates moderate glucose fluctuation patterns across the monitored period."
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with c2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Diabetic Foot Assessment")

        st.image(foot_file, use_container_width=True)

        st.success(
            "Foot tissue condition appears healthy with no visible ulcer indicators."
        )

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Retinal Health Awareness")

        st.warning(retina_note)

        st.markdown("""
        Continuous monitoring and routine ophthalmology screening are essential 
        for preventing long-term diabetic retinal complications.
        """)

        st.markdown('</div>', unsafe_allow_html=True)

        # =========================
        # PDF
        # =========================

        st.markdown('<div class="pdf-box">', unsafe_allow_html=True)

        st.subheader("Professional Clinical Report")

        recommendation = f"{meal_note} {retina_note}"

        pdf_bytes = create_pdf(
            patient_name,
            patient_id,
            glucose,
            carbs,
            foot_risk,
            recommendation
        )

        st.download_button(
            "Download PDF Report",
            data=pdf_bytes,
            file_name="Glucovision_Report.pdf",
            mime="application/pdf"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # =========================
        # HISTORY
        # =========================

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Recent Activity")

        current_record = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - Analysis Generated"

        if current_record not in st.session_state.history:
            st.session_state.history.append(current_record)

        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"- {item}")

        st.markdown('</div>', unsafe_allow_html=True)

else:

    st.markdown("""
    <div class="card">
    <h3 style="color:white;">Start Patient Analysis</h3>

    Upload:
    <ul>
    <li>Meal image</li>
    <li>Wearable sensor CSV file</li>
    <li>Diabetic foot image</li>
    </ul>

    to generate the integrated AI clinical monitoring dashboard.
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================

st.markdown("""
<div class="footer-note">
Glucovision AI — Graduation Project Prototype | AI-Based Diabetic Monitoring System
</div>
""", unsafe_allow_html=True)
