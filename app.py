import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Glucovision AI", layout="wide", initial_sidebar_state="expanded")

LOGO = "PHOTO-2026-02-17-21-43-19.jpeg"

# --- التنسيق الجمالي الاحترافي (Premium UI) ---
st.markdown(f"""
<style>
    /* جعل اللوقو شفافاً وإزالة الخلفية البيضاء منه */
    [data-testid="stSidebarNav"] + div img {{
        mix-blend-mode: multiply;
        filter: contrast(110%);
    }}

    /* القائمة الجانبية الكحلية الفاخرة */
    [data-testid="stSidebar"] {{
        background-color: #0B2F4A !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* إخفاء الخطوط البيضاء والمستطيلات غير المرغوبة */
    .stDeployButton {{display:none;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* تنسيق البطاقات */
    .card {{
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
        margin-bottom: 20px;
        color: #1e293b;
    }}

    .medical-status {{
        font-size: 14px;
        font-weight: 600;
        padding: 8px 12px;
        border-radius: 8px;
        display: inline-block;
    }}
</style>
""", unsafe_allow_html=True)

# إدارة البيانات
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "history" not in st.session_state: st.session_state.history = []

# --- وظيفة التقرير PDF ---
def generate_pdf(patient, glucose, carbs, advice):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "Official Medical Monitoring Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    details = {
        "Patient Name": patient['name'], "ID": patient['id'], "Age": patient['age'],
        "Glucose Prediction": f"{glucose} mg/dL", "Carbohydrate Intake": f"{carbs} g",
        "Clinical Advice": advice
    }
    for k, v in details.items(): pdf.cell(0, 10, f"{k}: {v}", ln=True)
    return pdf.output(dest="S").encode("latin-1")

# --- صفحة الدخول (Centered & Clean) ---
def login_page():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("") # فضاء
        # كود لجعل اللوقو في النص شفاف
        st.markdown(f'<div style="text-align: center;"><img src="data:image/jpeg;base64,{base64.b64encode(open(LOGO, "rb").read()).decode()}" style="width:250px; mix-blend-mode: multiply;"></div>', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #0B2F4A;'>Glucovision AI</h1>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        name = st.text_input("Patient Full Name")
        p_id = st.text_input("Medical ID (e.g. 445XXXX)")
        age = st.number_input("Age", 1, 100, 23)
        d_type = st.selectbox("Diabetes Diagnosis", ["Type 1", "Type 2", "Prediabetes"])
        if st.button("Access Dashboard", use_container_width=True):
            if name and p_id:
                st.session_state.patient = {"name": name, "id": p_id, "age": age, "type": d_type}
                st.session_state.logged_in = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- لوحة التحكم ---
def dashboard_page():
    with st.sidebar:
        # اللوقو الشفاف في الجنب
        st.image(LOGO, width=120)
        st.markdown(f"### Profile: {st.session_state.patient['name']}")
        st.write(f"ID: {st.session_state.patient['id']}")
        st.write(f"Age: {st.session_state.patient['age']}")
        
        st.markdown("---")
        st.markdown("### 🕒 Records History")
        if st.session_state.history:
            for h in st.session_state.history[-4:]: st.caption(f"• {h}")
        else: st.caption("No history recorded yet.")
        
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown(f"<h2 style='color:#0B2F4A;'>Clinical Intelligence Dashboard</h2>", unsafe_allow_html=True)
    
    # قسم الرفع
    with st.expander("Upload Patient Data Modalities", expanded=True):
        c1, c2, c3 = st.columns(3)
        f_file = c1.file_uploader("Meal Image", type=['jpg', 'png'])
        w_file = c2.file_uploader("Wearable CSV", type=['csv'])
        ft_file = c3.file_uploader("Foot Image", type=['jpg', 'png'])

    if f_file and w_file and ft_file:
        # محاكاة ذكية للنتائج
        glucose = 155
        carbs = 75
        
        st.markdown("---")
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Dietary & Glucose Insights")
            st.image(f_file, use_container_width=True)
            if carbs > 60:
                st.error(f"⚠️ Clinical Insight: This meal is high in carbohydrates ({carbs}g). We recommend reducing portion sizes in your next meal to stabilize glucose levels.")
            else:
                st.success("Meal analysis: Carbohydrate levels are within the safe daily target.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Complication Screening")
            st.image(ft_file, width=280)
            st.success("Foot Assessment: Healthy tissue detected. Continue daily inspections.")
            
            # منطق الشبكية الذكي
            if glucose > 140:
                st.warning(f"⚠️ Critical Alert: Your current glucose trend ({glucose} mg/dL) shows persistent instability. You are REQUIRED to schedule a Retinal Screening with your specialist to prevent microvascular damage.")
            else:
                st.info("Retinal Health: Current glycemic stability does not indicate an immediate need for extra screening.")
            st.markdown('</div>', unsafe_allow_html=True)

        # التقرير
        if st.button("Generate Professional PDF Report"):
            advice = "High glucose trend detected. Immediate dietary adjustment and retinal screening advised." if glucose > 140 else "Glucose stable. Routine monitoring only."
            st.session_state.history.append(f"Analyzed on {datetime.now().strftime('%H:%M')}")
            pdf_bytes = generate_pdf(st.session_state.patient, glucose, carbs, advice)
            st.download_button("Download Official Medical Report", pdf_bytes, "Glucovision_Report.pdf", "application/pdf")

import base64
if not st.session_state.logged_in: login_page()
else: dashboard_page()
