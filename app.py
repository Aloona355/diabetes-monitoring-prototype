import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import base64
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import io

# ReportLab imports
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    HRFlowable, Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

st.set_page_config(page_title="AI Diabetes Monitor", layout="wide")

LOGO = "IMG_5991.png"

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def get_base64_logo():
    try:
        with open(LOGO, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""


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
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.tick_params(axis='x', labelsize=8)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf


def generate_meal_chart():
    categories = ["Healthy", "High Carb", "High Fat", "Balanced"]
    values = [8, 5, 3, 5]
    bar_colors = ['#059669', '#f59e0b', '#ef4444', '#0891b2']

    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(categories, values, color=bar_colors, width=0.5, edgecolor='white', linewidth=1.5)
    ax.set_ylabel("Meals", fontsize=10)
    ax.set_title("Meal Quality – Last 7 Days", fontsize=12, fontweight='bold', color='#0b2f4a')
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.tick_params(axis='x', labelsize=9)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                str(val), ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0b2f4a')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf


def create_pdf_report(patient, glucose, foot_risk, retinal_status):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=2*cm
    )

    navy   = colors.HexColor("#0b2f4a")
    teal   = colors.HexColor("#0891b2")
    slate  = colors.HexColor("#475569")
    light  = colors.HexColor("#f1f5f9")
    teal_light = colors.HexColor("#e0f2fe")
    green  = colors.HexColor("#059669")
    green_light = colors.HexColor("#d1fae5")
    amber  = colors.HexColor("#f59e0b")
    amber_light = colors.HexColor("#fef3c7")
    white  = colors.white

    def style(name, **kw):
        return ParagraphStyle(name, **kw)

    title_style   = style("T1", fontName="Helvetica-Bold",    fontSize=16, textColor=white,  alignment=TA_CENTER, spaceAfter=2)
    sub_style     = style("T2", fontName="Helvetica",          fontSize=11, textColor=colors.HexColor("#bae6fd"), alignment=TA_CENTER, spaceAfter=0)
    date_style    = style("T3", fontName="Helvetica",          fontSize=9,  textColor=colors.HexColor("#93c5fd"), alignment=TA_CENTER, spaceAfter=0)
    section_style = style("S1", fontName="Helvetica-Bold",     fontSize=12, textColor=navy,  spaceBefore=12, spaceAfter=5,
                          borderPad=4, leftIndent=0)
    body_style    = style("B1", fontName="Helvetica",          fontSize=10, textColor=slate, leading=16)
    small_style   = style("SM", fontName="Helvetica-Oblique",  fontSize=8,  textColor=slate, alignment=TA_CENTER)
    rec_style     = style("RC", fontName="Helvetica",          fontSize=10, textColor=colors.HexColor("#1e3a5f"), leading=18)

    story = []
    W = A4[0] - 4*cm        # ~15.1 cm usable width
    CH = W * 0.32           # chart height — compact enough to fit with header

    # ── HEADER BANNER ───────────────────────────────────
    header_data = [[Paragraph("Intelligent Diabetes Monitoring System", title_style)]]
    header_table = Table(header_data, colWidths=[W])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), navy),
        ("TOPPADDING",   (0,0), (-1,-1), 20),
        ("BOTTOMPADDING",(0,0), (-1,-1), 20),
        ("LEFTPADDING",  (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
    ]))

    sub_data = [[
        Paragraph("Health Summary Report", sub_style),
        Paragraph(datetime.now().strftime("%A, %B %d %Y  |  %I:%M %p"), date_style),
    ]]
    sub_table = Table(sub_data, colWidths=[W*0.5, W*0.5])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), teal),
        ("TOPPADDING",   (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0), (-1,-1), 10),
        ("LEFTPADDING",  (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
        ("ALIGN",        (1,0), (1,0),   "RIGHT"),
    ]))

    story.append(KeepTogether([header_table, Spacer(1, 6), sub_table, Spacer(1, 16)]))

    # ── PATIENT INFO ────────────────────────────────────
    def section_header(text):
        data = [[Paragraph(text, style("SH", fontName="Helvetica-Bold", fontSize=11,
                                       textColor=white, spaceAfter=0))]]
        t = Table(data, colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), teal),
            ("TOPPADDING",   (0,0), (-1,-1), 6),
            ("BOTTOMPADDING",(0,0), (-1,-1), 6),
            ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ]))
        return t

    info_data = [
        [Paragraph("<b>Name</b>",   style("i", fontName="Helvetica-Bold", fontSize=10, textColor=navy)),
         Paragraph(patient.get("name","—"),   style("i", fontName="Helvetica", fontSize=10, textColor=slate)),
         Paragraph("<b>Gender</b>", style("i", fontName="Helvetica-Bold", fontSize=10, textColor=navy)),
         Paragraph(patient.get("gender","—"), style("i", fontName="Helvetica", fontSize=10, textColor=slate))],
        [Paragraph("<b>Email</b>",  style("i", fontName="Helvetica-Bold", fontSize=10, textColor=navy)),
         Paragraph(patient.get("email","—"),  style("i", fontName="Helvetica", fontSize=10, textColor=slate)),
         Paragraph("<b>Age</b>",    style("i", fontName="Helvetica-Bold", fontSize=10, textColor=navy)),
         Paragraph(str(patient.get("age","—")), style("i", fontName="Helvetica", fontSize=10, textColor=slate))],
    ]
    info_table = Table(info_data, colWidths=[2.5*cm, 7.5*cm, 2.5*cm, 4.5*cm])
    info_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [light, white]),
        ("GRID",           (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",     (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 7),
        ("LEFTPADDING",    (0,0), (-1,-1), 10),
    ]))

    story.append(KeepTogether([
        section_header("Patient Information"),
        Spacer(1, 3),
        info_table,
        Spacer(1, 10),
    ]))

    # ── HEALTH OVERVIEW ─────────────────────────────────
    avg_glucose    = int(st.session_state.get("manual_glucose") or glucose)
    glucose_status = "slightly elevated" if avg_glucose >= 140 else "within normal range"
    summary_text   = (
        f"Over the past 7 days, the average glucose level was <b>{avg_glucose} mg/dL</b> — {glucose_status}. "
        f"Most recent reading: <b>{glucose} mg/dL</b>. "
        f"Meal analysis shows a combination of healthy and high-carbohydrate meals. "
        f"Foot health status: <b>{foot_risk} Risk</b>. "
        f"Retinal status: <b>{retinal_status}</b>."
    )
    summary_bg = amber_light if avg_glucose >= 140 else green_light
    summary_data = [[Paragraph(summary_text, style("SB", fontName="Helvetica", fontSize=10,
                                                    textColor=navy, leading=16))]]
    summary_table = Table(summary_data, colWidths=[W])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), summary_bg),
        ("TOPPADDING",   (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0), (-1,-1), 10),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("BOX",          (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]))

    story.append(KeepTogether([
        section_header("Health Overview"),
        Spacer(1, 4),
        summary_table,
        Spacer(1, 10),
    ]))

    # ── GLUCOSE & NUTRITION METRICS ─────────────────────
    # ── GLUCOSE METRICS ONLY ────────────────────────────
    def status_color(val):
        if val in ("Elevated", "High"):  return amber
        if val == "Normal":              return green
        return slate

    def status_bg(val):
        if val in ("Elevated", "High"):  return amber_light
        if val == "Normal":              return green_light
        return white

    metrics_data = [
        ["Metric", "Value", "Status"],
        ["Current Glucose",   f"{glucose} mg/dL",    "Elevated" if glucose >= 140 else "Normal"],
        ["7-Day Avg Glucose", f"{avg_glucose} mg/dL", "Elevated" if avg_glucose >= 140 else "Normal"],
    ]
    ts = [
        ("BACKGROUND",    (0,0), (-1,0),  navy),
        ("TEXTCOLOR",     (0,0), (-1,0),  white),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("FONTNAME",      (0,1), (0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1), (0,-1),  navy),
        ("FONTNAME",      (1,1), (1,-1),  "Helvetica"),
        ("TEXTCOLOR",     (1,1), (1,-1),  slate),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [light, white]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("ALIGN",         (0,0), (-1,-1), "LEFT"),
    ]
    for row_idx, row in enumerate(metrics_data[1:], start=1):
        ts.append(("TEXTCOLOR",  (2, row_idx), (2, row_idx), status_color(row[2])))
        ts.append(("FONTNAME",   (2, row_idx), (2, row_idx), "Helvetica-Bold"))
        ts.append(("BACKGROUND", (2, row_idx), (2, row_idx), status_bg(row[2])))
    metrics_table = Table(metrics_data, colWidths=[6*cm, 5.5*cm, 5.5*cm])
    metrics_table.setStyle(TableStyle(ts))

    story.append(KeepTogether([
        section_header("Glucose Metrics"),
        Spacer(1, 3),
        metrics_table,
        Spacer(1, 10),
    ]))

    # ── GLUCOSE CHART ───────────────────────────────────
    g_buf = generate_glucose_chart()
    story.append(KeepTogether([
        section_header("Glucose Trend – Last 7 Days"),
        Spacer(1, 4),
        RLImage(g_buf, width=W, height=CH),
        Spacer(1, 10),
    ]))

    # ── MEAL CHART ──────────────────────────────────────
    m_buf = generate_meal_chart()
    story.append(KeepTogether([
        section_header("Meal Quality – Last 7 Days"),
        Spacer(1, 4),
        RLImage(m_buf, width=W * 0.6, height=CH),
        Spacer(1, 10),
    ]))

    # ── CLINICAL ASSESSMENTS ────────────────────────────
    foot_c  = green       if foot_risk == "Low"                      else amber
    foot_bg = green_light if foot_risk == "Low"                      else amber_light
    ret_c   = green       if retinal_status == "No warning detected" else amber
    ret_bg  = green_light if retinal_status == "No warning detected" else amber_light

    assess_data = [
        ["Assessment",     "Result",            "Detail"],
        ["Foot Health",    f"{foot_risk} Risk", "No ulcer indicators detected"],
        ["Retinal Health",  retinal_status,      "Based on glucose pattern & retinal scan"],
    ]
    assess_ts = [
        ("BACKGROUND",    (0,0), (-1,0),  navy),
        ("TEXTCOLOR",     (0,0), (-1,0),  white),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("FONTNAME",      (0,1), (0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1), (0,-1),  navy),
        ("TEXTCOLOR",     (2,1), (2,-1),  slate),
        ("FONTNAME",      (2,1), (2,-1),  "Helvetica"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [light, white]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("TEXTCOLOR",  (1,1), (1,1), foot_c),  ("FONTNAME", (1,1), (1,1), "Helvetica-Bold"),
        ("BACKGROUND", (1,1), (1,1), foot_bg),
        ("TEXTCOLOR",  (1,2), (1,2), ret_c),   ("FONTNAME", (1,2), (1,2), "Helvetica-Bold"),
        ("BACKGROUND", (1,2), (1,2), ret_bg),
    ]
    assess_table = Table(assess_data, colWidths=[4.5*cm, 5*cm, 7.5*cm])
    assess_table.setStyle(TableStyle(assess_ts))

    story.append(KeepTogether([
        section_header("Clinical Assessments"),
        Spacer(1, 3),
        assess_table,
        Spacer(1, 14),
    ]))

    # ── FOOTER ──────────────────────────────────────────
    footer_data = [[Paragraph(
        "This report is generated by an AI-assisted prototype and is not a substitute for "
        "professional medical advice. Always consult a qualified healthcare provider for diagnosis and treatment.",
        small_style
    )]]
    footer_table = Table(footer_data, colWidths=[W])
    footer_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), light),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("BOX",          (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(footer_table)

    doc.build(story)
    buf.seek(0)
    return buf.read()


# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
.stApp { background: #f8fbfd; color: #0B2F4A; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1280px; }

.hero-title {
    font-size: 48px; font-weight: 850; color: #075985;
    text-align: center; line-height: 1.2; margin-top: 10px; margin-bottom: 28px;
}
.section-title { font-size: 30px; font-weight: 850; color: #075985; margin-bottom: 6px; }
.auth-subtitle { text-align: center; color: #64748b; font-size: 15px; margin-bottom: 24px; }
.small-center-text { text-align: center; color: #64748b; margin-top: 18px; margin-bottom: 5px; }

.card {
    background: white; padding: 22px; border-radius: 16px;
    border: 1px solid #e2e8f0; box-shadow: 0 6px 18px rgba(11,47,74,0.06); margin-bottom: 20px;
}
.card-title { font-size: 19px; font-weight: 800; color: #0B2F4A; margin-bottom: 14px; }

.metric-card {
    background: #ffffff; border-radius: 22px; padding: 32px 20px;
    text-align: center; box-shadow: 0 8px 22px rgba(15,23,42,0.08); min-height: 170px; color: #0b2f4a;
}
.metric-title  { font-size: 16px; font-weight: 800; margin-bottom: 18px; color: #0b2f4a; }
.metric-value  { font-size: 42px; font-weight: 900; line-height: 1.1; color: #0b2f4a; }
.metric-unit   { font-size: 18px; font-weight: 700; margin-top: 12px; color: #475569; }

.section-card {
    background: #ffffff; border-radius: 22px; padding: 30px;
    box-shadow: 0 8px 22px rgba(15,23,42,0.08); color: #0b2f4a; margin-bottom: 25px;
}
.section-heading { font-size: 26px; font-weight: 850; color: #0b2f4a; margin-bottom: 18px; }

.dashboard-title   { font-size: 34px; font-weight: 850; color: #0b2f4a; margin-bottom: 8px; }
.dashboard-welcome { font-size: 18px; font-weight: 650; color: #0b2f4a; margin-bottom: 25px; }

/* fix st.metric label + value color */
[data-testid="stMetricLabel"] p { color: #0b2f4a !important; font-weight: 700 !important; }
[data-testid="stMetricValue"]  { color: #0b2f4a !important; font-weight: 800 !important; }

/* fix checkbox label color */
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] p,
[data-baseweb="checkbox"] span {
    color: #0b2f4a !important;
    font-weight: 600 !important;
}

label { color: #0B2F4A !important; font-weight: 700 !important; }
.stTextInput input, .stNumberInput input {
    background-color: white !important; color: #0B2F4A !important;
    border: 1px solid #b7dce5 !important; border-radius: 12px !important;
}
.stSelectbox div[data-baseweb="select"] {
    background-color: white !important; color: #0B2F4A !important;
    border: 1px solid #b7dce5 !important; border-radius: 12px !important;
}
.stButton > button {
    background: linear-gradient(90deg, #0369a1, #0f766e);
    color: white; border: none; border-radius: 12px;
    padding: 0.7rem 1rem; font-weight: 700;
}
.stButton > button:hover { background: linear-gradient(90deg, #075985, #115e59); color: white; }

[data-testid="stSidebar"] { background: linear-gradient(180deg, #06263d 0%, #031827 100%); }
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.18); }

@media (max-width: 768px) { .hero-title { font-size: 36px; } }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Session state
# --------------------------------------------------
for key, default in [
    ("logged_in", False), ("page", "login"),
    ("patient", {}), ("auth_mode", "login"),
    ("retinal_img", None), ("manual_glucose", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
def render_sidebar():
    with st.sidebar:
        logo_b64 = get_base64_logo()
        if logo_b64:
            st.markdown(
                f'<div style="text-align:center;padding-top:25px;padding-bottom:35px;">'
                f'<img src="data:image/png;base64,{logo_b64}" width="230"></div>',
                unsafe_allow_html=True
            )

        selected = option_menu(
            menu_title=None,
            options=["Home", "Retinal Scan", "Reports", "History", "Profile", "Settings", "Logout"],
            icons=["house", "eye", "file-earmark-text", "clock-history", "person", "gear", "box-arrow-left"],
            default_index=0,
            styles={
                "container":        {"padding": "0px", "background-color": "#06263d"},
                "icon":             {"color": "white", "font-size": "20px"},
                "nav-link":         {
                    "background-color": "#06263d", "color": "white",
                    "font-size": "16px", "font-weight": "600",
                    "text-align": "left", "margin": "0px",
                    "padding": "14px 18px", "border-radius": "0px",
                    "--hover-color": "rgba(255,255,255,0.08)",
                },
                "nav-link-selected": {
                    "background-color": "rgba(255,255,255,0.08)",
                    "color": "white", "border-left": "4px solid #22d3ee", "font-weight": "700",
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
    _, logo_center, _ = st.columns([1, 1.4, 1])
    with logo_center:
        try:
            st.image(LOGO, width=430)
        except:
            pass

    st.markdown('<div class="hero-title">Intelligent Diabetes Monitoring System</div>', unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.15, 1])
    with center:
        if st.session_state.auth_mode == "login":
            st.markdown('<div class="section-title" style="text-align:center;">Welcome Back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Sign in to continue monitoring your health insights.</div>', unsafe_allow_html=True)

            email    = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            st.checkbox("Remember me", label_visibility="visible")

            if st.button("Sign In", use_container_width=True):
                if not email.strip():
                    st.error("Enter your email address to continue.")
                elif not password.strip():
                    st.error("Enter your password to continue.")
                else:
                    st.session_state.patient = {"name": "Patient", "email": email, "age": "N/A", "gender": "N/A"}
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

            name     = st.text_input("Full Name")
            email    = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            age      = st.number_input("Age", min_value=1, max_value=120, value=None, placeholder="Enter your age")
            gender   = st.selectbox("Gender", ["Female", "Male"])

            if st.button("Create Account and Continue", use_container_width=True):
                if not name.strip():
                    st.error("Enter your name to continue.")
                elif not email.strip():
                    st.error("Enter your email address to continue.")
                elif not password.strip():
                    st.error("Create a password to continue.")
                elif age is None:
                    st.error("Enter your age to continue.")
                else:
                    st.session_state.patient = {"name": name, "email": email, "age": age, "gender": gender}
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

    if selected == "Retinal Scan": retinal_scan_page(); return
    if selected == "Reports":      reports_page();      return
    if selected == "History":      history_page();      return
    if selected == "Profile":      profile_page();      return
    if selected == "Settings":     settings_page();     return

    st.markdown(
        '<div class="section-title">Upload Health Data</div>'
        '<div style="color:#475569;font-size:16px;margin-bottom:20px;">'
        'Upload your health files to generate the diabetes monitoring summary.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card"><div class="card-title">Meal Image</div>'
                    '<div style="color:#475569;margin-bottom:15px;">Upload a clear meal image for nutrition analysis.</div>',
                    unsafe_allow_html=True)
        food_img = st.file_uploader("", type=["jpg","jpeg","png"], key="food_upload", label_visibility="hidden")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">Foot Assessment Image</div>'
                    '<div style="color:#475569;margin-bottom:15px;">Upload a foot image for risk assessment. This can be done periodically.</div>',
                    unsafe_allow_html=True)
        foot_img = st.file_uploader("", type=["jpg","jpeg","png"], key="foot_upload", label_visibility="hidden")
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.food_img = food_img
    st.session_state.foot_img = foot_img

    st.markdown("<br>", unsafe_allow_html=True)

    if food_img or foot_img:
        if st.button("Start AI Analysis", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    else:
        st.info("Upload your files to get started.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Go to Dashboard →", use_container_width=False):
        st.session_state.page = "dashboard"
        st.rerun()


# --------------------------------------------------
# Dashboard
# --------------------------------------------------
def dashboard_page():
    selected_page = render_sidebar()

    if selected_page == "Retinal Scan": retinal_scan_page(); return
    if selected_page == "Reports":      reports_page();      return
    if selected_page == "History":      history_page();      return
    if selected_page == "Profile":      profile_page();      return
    if selected_page == "Settings":     settings_page();     return

    food_img     = st.session_state.get("food_img") or None
    foot_img     = st.session_state.get("foot_img") or None
    retinal_img  = st.session_state.get("retinal_img") or None

    calories, carbs, protein, fat = 550, 65, 28, 18
    glucose   = int(st.session_state.get("manual_glucose") or 145)
    foot_risk = "Low"

    st.markdown(
        f"""
        <div style="margin-bottom:10px;">
            <div class="dashboard-title">Your Health Analysis Summary</div>
            <div class="dashboard-welcome">Hello, {st.session_state.patient.get("name","Patient")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Build metrics dynamically based on what was uploaded
    metric_items = [("Predicted Glucose", glucose, "mg/dL")]
    if foot_img is not None:
        metric_items.append(("Foot Risk", foot_risk, "No ulcer detected"))
    if food_img is not None:
        metric_items.append(("Meal Carbs", carbs, "g"))

    cols = st.columns(len(metric_items))
    for col, (title, value, unit) in zip(cols, metric_items):
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-title">{title}</div>'
                f'<div class="metric-value">{value}</div>'
                f'<div class="metric-unit">{unit}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        if food_img:
            st.markdown(f'''
            <div class="section-card">
                <div class="section-heading">Dietary Analysis</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:10px;">
                    <div style="background:#f1f5f9; border-radius:12px; padding:16px;">
                        <div style="font-size:13px; font-weight:700; color:#475569;">Calories</div>
                        <div style="font-size:26px; font-weight:900; color:#0b2f4a;">{calories} <span style="font-size:14px;">kcal</span></div>
                    </div>
                    <div style="background:#f1f5f9; border-radius:12px; padding:16px;">
                        <div style="font-size:13px; font-weight:700; color:#475569;">Carbohydrates</div>
                        <div style="font-size:26px; font-weight:900; color:#0b2f4a;">{carbs} <span style="font-size:14px;">g</span></div>
                    </div>
                    <div style="background:#f1f5f9; border-radius:12px; padding:16px;">
                        <div style="font-size:13px; font-weight:700; color:#475569;">Protein</div>
                        <div style="font-size:26px; font-weight:900; color:#0b2f4a;">{protein} <span style="font-size:14px;">g</span></div>
                    </div>
                    <div style="background:#f1f5f9; border-radius:12px; padding:16px;">
                        <div style="font-size:13px; font-weight:700; color:#475569;">Fat</div>
                        <div style="font-size:26px; font-weight:900; color:#0b2f4a;">{fat} <span style="font-size:14px;">g</span></div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            st.image(Image.open(food_img), use_container_width=True)

    with right:
        st.markdown('<div class="section-card"><div class="section-heading">Wearable Data Analysis</div>', unsafe_allow_html=True)
        now = datetime.now()

        # Use manual glucose if entered, else default
        default_glucose = 145
        display_glucose = st.session_state.get("manual_glucose") or default_glucose
        display_glucose = int(display_glucose)

        auto_data = pd.DataFrame({
            "Time": [
                now.replace(hour=max(0, now.hour - 2), minute=0).strftime("%I:%M %p"),
                now.replace(hour=max(0, now.hour - 1), minute=0).strftime("%I:%M %p"),
                now.strftime("%I:%M %p"),
            ],
            "Heart Rate":       [72, 80, 76],
            "Glucose Estimate": [132, 138, display_glucose]
        })
        st.dataframe(auto_data, use_container_width=True)
        st.line_chart([120, 132, 138, display_glucose])

        # Manual entry toggle
        with st.expander("Not sure about the readings? Enter manually"):
            manual_val = st.number_input(
                "Enter your current glucose reading (mg/dL)",
                min_value=40, max_value=600,
                value=int(display_glucose),
                step=1,
                key="manual_glucose_input"
            )
            if st.button("Update Reading", key="update_glucose_btn"):
                st.session_state.manual_glucose = manual_val
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if foot_img:
            st.markdown('<div class="section-card"><div class="section-heading">Foot Assessment</div>', unsafe_allow_html=True)
            st.image(Image.open(foot_img), width=350)
            st.success("Low Risk – No ulcer indicators found.")
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card"><div class="section-heading">Retinal Health</div>', unsafe_allow_html=True)
        if glucose >= 180:
            st.warning("Elevated glucose levels detected. Retinal screening is recommended. Please consult an ophthalmologist.")
        else:
            st.success("No retinal risk warning detected at this time.")
        st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Retinal Scan Page
# --------------------------------------------------
def retinal_scan_page():
    st.markdown('<div class="section-title">Retinal Scan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#475569;font-size:16px;margin-bottom:20px;">'
        'Upload a retinal image for diabetic retinopathy risk assessment.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card"><div class="card-title">Retinal Image Upload</div>'
                '<div style="color:#475569;margin-bottom:15px;">'
                'Upload a clear retinal scan image. Supported formats: JPG, JPEG, PNG.</div>',
                unsafe_allow_html=True)

    retinal_img = st.file_uploader("", type=["jpg","jpeg","png"], key="retinal_upload", label_visibility="hidden")
    st.markdown('</div>', unsafe_allow_html=True)

    if retinal_img:
        st.session_state.retinal_img = retinal_img
        st.image(Image.open(retinal_img), caption="Uploaded Retinal Image", use_container_width=True)
        st.success("Retinal image uploaded successfully.")
    else:
        if st.session_state.retinal_img is None:
            pass  # no message needed


# --------------------------------------------------
# Reports Page
# --------------------------------------------------
def reports_page():
    st.markdown('<div class="section-title">Health Report</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#475569;font-size:16px;margin-bottom:24px;">'
        'Your complete health summary — ready to view or download.</div>',
        unsafe_allow_html=True
    )

    glucose        = int(st.session_state.get("manual_glucose") or 145)
    foot_risk      = "Low"
    retinal_img    = st.session_state.get("retinal_img")
    retinal_status = "No warning detected" if (not retinal_img or glucose < 180) else "Further screening recommended"
    avg_glucose    = glucose
    food_img       = st.session_state.get("food_img")
    foot_img       = st.session_state.get("foot_img")

    # ── inline report ──────────────────────────────
    st.markdown(f"""
    <div style="background:white; border-radius:18px; padding:32px 36px;
                box-shadow:0 6px 24px rgba(11,47,74,0.08); margin-bottom:24px;">

        <div style="background:#0b2f4a; border-radius:10px; padding:18px 20px; margin-bottom:4px;">
            <div style="color:white; font-size:18px; font-weight:800; text-align:center;">
                Intelligent Diabetes Monitoring System
            </div>
        </div>
        <div style="background:#0891b2; border-radius:0 0 10px 10px; padding:8px 20px;
                    display:flex; justify-content:space-between; margin-bottom:20px;">
            <span style="color:#e0f2fe; font-size:13px;">Health Summary Report</span>
            <span style="color:#bae6fd; font-size:13px;">{datetime.now().strftime("%A, %B %d %Y  |  %I:%M %p")}</span>
        </div>

        <div style="font-size:13px; font-weight:700; color:white; background:#0891b2;
                    padding:7px 12px; border-radius:6px; margin-bottom:8px;">Patient Information</div>
        <table style="width:100%; border-collapse:collapse; margin-bottom:16px; font-size:13px;">
            <tr style="background:#f1f5f9;">
                <td style="padding:8px 10px; font-weight:700; color:#0b2f4a; width:15%;">Name</td>
                <td style="padding:8px 10px; color:#475569; width:40%;">{st.session_state.patient.get("name","—")}</td>
                <td style="padding:8px 10px; font-weight:700; color:#0b2f4a; width:15%;">Gender</td>
                <td style="padding:8px 10px; color:#475569;">{st.session_state.patient.get("gender","—")}</td>
            </tr>
            <tr style="background:white;">
                <td style="padding:8px 10px; font-weight:700; color:#0b2f4a;">Email</td>
                <td style="padding:8px 10px; color:#475569;">{st.session_state.patient.get("email","—")}</td>
                <td style="padding:8px 10px; font-weight:700; color:#0b2f4a;">Age</td>
                <td style="padding:8px 10px; color:#475569;">{st.session_state.patient.get("age","—")}</td>
            </tr>
        </table>

        <div style="font-size:13px; font-weight:700; color:white; background:#0891b2;
                    padding:7px 12px; border-radius:6px; margin-bottom:8px;">Health Overview</div>
        <div style="background:{"#fef3c7" if avg_glucose >= 140 else "#d1fae5"};
                    border-radius:8px; padding:12px 16px; margin-bottom:16px;
                    font-size:13px; color:#0b2f4a; line-height:1.7;">
            Over the past 7 days, the average glucose level was <b>{avg_glucose} mg/dL</b> —
            {"slightly elevated" if avg_glucose >= 140 else "within normal range"}.
            Foot health status: <b>{foot_risk} Risk</b>.
            Retinal status: <b>{retinal_status}</b>.
        </div>

        <div style="font-size:13px; font-weight:700; color:white; background:#0891b2;
                    padding:7px 12px; border-radius:6px; margin-bottom:8px;">Glucose Metrics</div>
        <table style="width:100%; border-collapse:collapse; margin-bottom:16px; font-size:13px;">
            <tr style="background:#0b2f4a;">
                <td style="padding:8px 10px; color:white; font-weight:700;">Metric</td>
                <td style="padding:8px 10px; color:white; font-weight:700;">Value</td>
                <td style="padding:8px 10px; color:white; font-weight:700;">Status</td>
            </tr>
            <tr style="background:#f1f5f9;">
                <td style="padding:8px 10px; font-weight:700; color:#0b2f4a;">Current Glucose</td>
                <td style="padding:8px 10px; color:#475569;">{glucose} mg/dL</td>
                <td style="padding:8px 10px; font-weight:700;
                    color:{"#f59e0b" if glucose >= 140 else "#059669"};
                    background:{"#fef3c7" if glucose >= 140 else "#d1fae5"};">
                    {"Elevated" if glucose >= 140 else "Normal"}
                </td>
            </tr>
            <tr style="background:white;">
                <td style="padding:8px 10px; font-weight:700; color:#0b2f4a;">7-Day Avg Glucose</td>
                <td style="padding:8px 10px; color:#475569;">{avg_glucose} mg/dL</td>
                <td style="padding:8px 10px; font-weight:700;
                    color:{"#f59e0b" if avg_glucose >= 140 else "#059669"};
                    background:{"#fef3c7" if avg_glucose >= 140 else "#d1fae5"};">
                    {"Elevated" if avg_glucose >= 140 else "Normal"}
                </td>
            </tr>
        </table>

        <div style="font-size:13px; font-weight:700; color:white; background:#0891b2;
                    padding:7px 12px; border-radius:6px; margin-bottom:8px;">Clinical Assessments</div>
        <table style="width:100%; border-collapse:collapse; font-size:13px;">
            <tr style="background:#0b2f4a;">
                <td style="padding:8px 10px; color:white; font-weight:700;">Assessment</td>
                <td style="padding:8px 10px; color:white; font-weight:700;">Result</td>
                <td style="padding:8px 10px; color:white; font-weight:700;">Detail</td>
            </tr>
            <tr style="background:#f1f5f9;">
                <td style="padding:8px 10px; font-weight:700; color:#0b2f4a;">Foot Health</td>
                <td style="padding:8px 10px; font-weight:700; color:#059669; background:#d1fae5;">{foot_risk} Risk</td>
                <td style="padding:8px 10px; color:#475569;">No ulcer indicators detected</td>
            </tr>
            <tr style="background:white;">
                <td style="padding:8px 10px; font-weight:700; color:#0b2f4a;">Retinal Health</td>
                <td style="padding:8px 10px; font-weight:700;
                    color:{"#059669" if retinal_status == "No warning detected" else "#f59e0b"};
                    background:{"#d1fae5" if retinal_status == "No warning detected" else "#fef3c7"};">
                    {retinal_status}
                </td>
                <td style="padding:8px 10px; color:#475569;">Based on glucose pattern & retinal scan</td>
            </tr>
        </table>

    </div>
    """, unsafe_allow_html=True)

    # ── charts inline ──────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="font-size:13px;font-weight:700;color:#0b2f4a;margin-bottom:6px;">Glucose Trend – Last 7 Days</div>', unsafe_allow_html=True)
        g_buf = generate_glucose_chart()
        st.image(g_buf, use_container_width=True)
    with c2:
        st.markdown('<div style="font-size:13px;font-weight:700;color:#0b2f4a;margin-bottom:6px;">Meal Quality – Last 7 Days</div>', unsafe_allow_html=True)
        m_buf = generate_meal_chart()
        st.image(m_buf, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── download button ────────────────────────────
    if st.button("Download as PDF", use_container_width=True):
        with st.spinner("Generating PDF..."):
            pdf_bytes = create_pdf_report(
                st.session_state.patient,
                glucose, foot_risk, retinal_status
            )
        st.download_button(
            label="Click to Download",
            data=pdf_bytes,
            file_name=f"Health_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# --------------------------------------------------
# Other Pages
# --------------------------------------------------
def history_page():
    st.markdown('<div class="section-title">History</div>', unsafe_allow_html=True)
    st.info("No previous analysis records are available yet.")


def profile_page():
    patient = st.session_state.patient
    st.markdown('<div class="section-title">Profile</div>', unsafe_allow_html=True)
    st.write(f"Name: {patient.get('name','Patient')}")
    st.write(f"Email: {patient.get('email','N/A')}")
    st.write(f"Age: {patient.get('age','N/A')}")
    st.write(f"Gender: {patient.get('gender','N/A')}")


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
