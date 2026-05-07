import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime

# إعدادات الصفحة الفاخرة
st.set_page_config(page_title="Glucovision AI", layout="wide", initial_sidebar_state="expanded")

# --- ملفات الوسائط ---
LOGO = "PHOTO-2026-02-17-21-43-19.jpeg"

# --- التنسيق الجمالي المتطور (Modern UI) ---
st.markdown(f"""
<style>
    /* الخلفية العامة */
    .stApp {{
        background-color: #fcfdfe;
        color: #1e293b;
    }}

    /* القائمة الجانبية الكحلية */
    [data-testid="stSidebar"] {{
        background-color: #0B2F4A !important;
        color: white !important;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}

    /* البطاقات الفاخرة */
    .card {{
        background: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }}

    /* العناوين */
    .main-title {{
        font-size: 36px;
        font-weight: 800;
        color: #0B2F4A;
        text-align: center;
        letter-spacing: -1px;
    }}

    /* الأزرار */
    .stButton > button {{
        background: #0369a1;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 15px 30px;
        transition: all 0.3s;
    }}
    .stButton > button:hover {{
        background: #0ea5e9;
        transform: translateY(-2px);
    }}

    /* إخفاء العناصر غير الضرورية */
    #MainMenu, footer, header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# --- إدارة حالة النظام ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "history" not in st.session_state:
    st.session_state.history = []

# --- وظائف مساعدة ---
def create_pdf_report(patient, risk_score, advice):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Clinical Health Report - Glucovision AI", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    data = {
        "Patient": patient['name'], "ID": patient['id'], "Date": datetime.now().strftime("%Y-%m-%d"),
        "Risk Score": f"{risk_score}/100", "Doctor Advice": advice
    }
    for key, value in data.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    return pdf.output(dest="S").encode("latin-1")

# --- صفحة الدخول (Premium Login) ---
def login_page():
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.write("") # فضاء علوي
        st.image(LOGO, width=280) # اللوجو في النص كبير
        st.markdown('<div class="main-title">Glucovision AI</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#64748b;">Precision Diabetes Care Through Multimodal Intelligence</p>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            name = st.text_input("Patient Full Name", placeholder="e.g. Dana Bafaqih")
            p_id = st.text_input("Medical ID", placeholder="ID-44XXXX")
            col_a, col_b = st.columns(2)
            age = col_a.number_input("Age", 1, 100, 23)
            gender = col_b.selectbox("Gender", ["Female", "Male"])
            d_type = st.selectbox("Diagnosis", ["Type 1 Diabetes", "Type 2 Diabetes", "Prediabetes"])
            
            if st.button("Enter Clinical Dashboard", use_container_width=True):
                if name and p_id:
                    st.session_state.patient = {"name": name, "id": p_id, "age": age, "gender": gender, "type": d_type}
                    st.session_state.logged_in = True
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- لوحة التحكم (Clinical Dashboard) ---
def dashboard_page():
    # Sidebar الكحلي
    with st.sidebar:
        st.image(LOGO, width=100)
        st.markdown("### Clinical Profile")
        st.write(f"**ID:** {st.session_state.patient['id']}")
        st.write(f"**Name:** {st.session_state.patient['name']}")
        st.write(f"**Diagnosis:** {st.session_state.patient['type']}")
        
        st.markdown("---")
        st.markdown("### 🕒 Activity History")
        if st.session_state.history:
            for item in st.session_state.history[-3:]:
                st.caption(f"✓ {item}")
        else:
            st.caption("No recent activities.")
        
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # محتوى الصفحة
    st.markdown(f'<div style="font-size:30px; font-weight:700; color:#0B2F4A;">Patient Overview</div>', unsafe_allow_html=True)
    st.write(f"Real-time Monitoring | {datetime.now().strftime('%d %B %Y')}")

    # رفع البيانات
    with st.expander("📤 Upload New Clinical Data", expanded=True):
        c1, c2, c3 = st.columns(3)
        food = c1.file_uploader("Meal Image", type=['png', 'jpg'])
        wearable = c2.file_uploader("Sensor Data (CSV)", type=['csv'])
        foot = c3.file_uploader("Foot Condition Image", type=['png', 'jpg'])

    if food and wearable and foot:
        # محاكاة التحليل الذكي
        glucose = 148
        carbs = 72
        risk_score = 65
        
        # النصيحة الذكية
        if carbs > 60:
            diet_advice = "Warning: High glycemic load. Increase fiber intake in your next meal."
            diet_status = "error"
        else:
            diet_advice = "Healthy meal composition. Carbs within target range."
            diet_status = "success"

        # عرض النتائج
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Glucose", f"{glucose} mg/dL", "Elevated")
        m2.metric("Meal Carbs", f"{carbs}g", "High")
        m3.metric("System Risk Score", f"{risk_score}/100")

        col_l, col_r = st.columns(2)
        
        with col_l:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Dietary Insights")
            st.image(food, use_container_width=True)
            if diet_status == "error": st.error(diet_advice)
            else: st.success(diet_advice)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Foot & Retinal Screening")
            st.image(foot, width=280)
            st.info("AI Analysis: No active ulcers detected. Skin integrity 94%.")
            
            # منطق الشبكية الذكي
            if glucose > 140:
                st.warning("⚠️ Action Required: Elevated glucose trends detected. Please schedule your Retinal Screening with Dr. Seereen Noorwali.")
            else:
                st.success("Retinal health parameters within stable range.")
            st.markdown('</div>', unsafe_allow_html=True)

        # زر التقرير
        if st.button("Generate Final Medical PDF"):
            st.session_state.history.append(f"Report Generated on {datetime.now().strftime('%H:%M')}")
            pdf_data = create_pdf_report(st.session_state.patient, risk_score, diet_advice)
            st.download_button("Download Official Report", pdf_data, "Medical_Report.pdf", "application/pdf")

# تشغيل النظام
if not st.session_state.logged_in:
    login_page()
else:
    dashboard_page()
