import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime

st.set_page_config(
    page_title="AI Diabetes Monitor",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
# 🩺 Intelligent Diabetes Monitoring System
### Multimodal AI Prototype for Dietary Analysis, Wearable Data, Foot Assessment, and Retinal Awareness
""")

st.sidebar.title("📥 Patient Data Input")

food_img = st.sidebar.file_uploader("Upload Food Image", type=["jpg", "jpeg", "png"])
wearable_csv = st.sidebar.file_uploader("Upload Wearable Data CSV", type=["csv"])
foot_img = st.sidebar.file_uploader("Upload Foot Image", type=["jpg", "jpeg", "png"])

st.sidebar.markdown("---")
patient_name = st.sidebar.text_input("Patient Name", "Demo Patient")
age = st.sidebar.number_input("Age", min_value=1, max_value=100, value=45)

st.markdown("---")

# Default values
calories = 0
carbs = 0
protein = 0
fat = 0
predicted_glucose = 0
foot_risk = "Not assessed"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🍽️ Meal Carbs", f"{carbs} g")

with col2:
    st.metric("🩸 Predicted Glucose", f"{predicted_glucose} mg/dL")

with col3:
    st.metric("🦶 Foot Risk", foot_risk)

st.markdown("---")

left, right = st.columns(2)

with left:
    st.subheader("🍽️ Dietary Analysis Module")

    if food_img:
        image = Image.open(food_img)
        st.image(image, caption="Uploaded Food Image", use_container_width=True)

        calories = 550
        carbs = 65
        protein = 28
        fat = 18

        st.success("Food analysis completed")

        a, b, c, d = st.columns(4)
        a.metric("Calories", f"{calories} kcal")
        b.metric("Carbs", f"{carbs} g")
        c.metric("Protein", f"{protein} g")
        d.metric("Fat", f"{fat} g")

        st.caption("Prototype output: simulated AI-based nutrition estimation.")
    else:
        st.info("Upload a food image to estimate nutrition values.")

with right:
    st.subheader("⌚ Wearable-Based Glucose Estimation")

    if wearable_csv:
        data = pd.read_csv(wearable_csv)
        st.dataframe(data.head(), use_container_width=True)

        predicted_glucose = 145

        st.metric("Predicted Glucose Level", f"{predicted_glucose} mg/dL")

        if predicted_glucose > 180:
            st.error("High glucose pattern detected")
        elif predicted_glucose > 140:
            st.warning("Moderate glucose elevation detected")
        else:
            st.success("Glucose level appears normal")

        st.caption("Prototype output: simulated XGBoost glucose prediction.")
    else:
        st.info("Upload wearable CSV data to estimate glucose level.")

st.markdown("---")

col4, col5 = st.columns(2)

with col4:
    st.subheader("🦶 Diabetic Foot Assessment Module")

    if foot_img:
        foot_image = Image.open(foot_img)
        st.image(foot_image, caption="Uploaded Foot Image", width=350)

        foot_risk = "Low"
        st.success("AI Classification: No ulcer detected")
        st.caption("Prototype output: simulated EfficientNet-based foot assessment.")
    else:
        st.info("Upload a foot image for diabetic foot assessment.")

with col5:
    st.subheader("👁️ Retinal Health Awareness")

    st.warning(
        "Retinal Reminder: Patients with persistent glucose instability should schedule periodic retinal screening."
    )

    st.write(
        "This module supports long-term complication awareness and future retinal health integration."
    )

st.markdown("---")

st.subheader("📊 Integrated Risk Score")

risk_score = 0

if food_img:
    risk_score += 25
    if carbs > 60:
        risk_score += 15

if wearable_csv:
    risk_score += 25
    if predicted_glucose > 140:
        risk_score += 20

if foot_img:
    risk_score += 10

risk_score = min(risk_score, 100)

st.progress(risk_score / 100)
st.write(f"**Overall Risk Score:** {risk_score}/100")

if risk_score >= 70:
    st.error("Overall Risk Level: High")
elif risk_score >= 40:
    st.warning("Overall Risk Level: Moderate")
else:
    st.success("Overall Risk Level: Low")

st.markdown("---")

st.subheader("📄 Health Report")

report = f"""
AI Diabetes Monitoring Prototype Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Patient Name: {patient_name}
Age: {age}

Dietary Analysis:
Calories: {calories} kcal
Carbohydrates: {carbs} g
Protein: {protein} g
Fat: {fat} g

Wearable-Based Glucose Estimation:
Predicted Glucose Level: {predicted_glucose} mg/dL

Diabetic Foot Assessment:
Foot Risk: {foot_risk}

Retinal Health Awareness:
Periodic retinal screening is recommended for long-term complication monitoring.

Integrated Risk Score:
{risk_score}/100

System Note:
This prototype is for academic demonstration only and is not intended for clinical diagnosis.
"""

st.download_button(
    label="⬇️ Download Health Report",
    data=report,
    file_name="diabetes_health_report.txt",
    mime="text/plain"
)

st.markdown("---")
st.caption("Graduation Project Prototype | AI-based Multimodal Diabetes Monitoring System")
