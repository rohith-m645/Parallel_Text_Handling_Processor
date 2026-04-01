"""
============================================================
 SHARED STYLE MODULE
 Call apply_theme() at the top of every page file.
============================================================
"""

import streamlit as st

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

:root {
    --accent:  #7c6cfa;
    --green:   #3ecfaa;
    --red:     #fa6c6c;
    --amber:   #f5a623;
    --blue:    #5baef7;
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

/* Background */
.stApp { background: #0a0a0f !important; }
.main .block-container { padding: 2rem 2.5rem !important; max-width: 1200px; }

/* Hide default streamlit page nav completely */
section[data-testid="stSidebar"] nav,
section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"],
section[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebarNavLink"] { display: none !important; }

/* Sidebar shell */
section[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 0.5px solid rgba(255,255,255,0.07) !important;
    min-width: 220px !important;
    max-width: 220px !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.2rem 0.8rem !important;
}

/* Headings */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: #f0eff8 !important;
    letter-spacing: -0.3px !important;
}
h1 { font-size: 1.5rem !important; font-weight: 700 !important; }
h2 { font-size: 1.15rem !important; font-weight: 600 !important; }
h3 { font-size: 1rem !important; font-weight: 600 !important; }

/* Hide metric delta arrows entirely */
[data-testid="stMetricDelta"] { display: none !important; }

/* Metric cards — coloured left border per card */
[data-testid="metric-container"] {
    background: #16161f !important;
    border: 0.5px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}
[data-testid="metric-container"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.08em !important;
    color: #7a7990 !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    color: #f0eff8 !important;
    letter-spacing: -1px !important;
}

/* Coloured metric cards using nth-child */
[data-testid="column"]:nth-child(1) [data-testid="metric-container"] {
    border-left: 2px solid #7c6cfa !important;
}
[data-testid="column"]:nth-child(2) [data-testid="metric-container"] {
    border-left: 2px solid #3ecfaa !important;
}
[data-testid="column"]:nth-child(3) [data-testid="metric-container"] {
    border-left: 2px solid #f5a623 !important;
}
[data-testid="column"]:nth-child(4) [data-testid="metric-container"] {
    border-left: 2px solid #5baef7 !important;
}

/* Buttons */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    border: 0.5px solid rgba(255,255,255,0.14) !important;
    background: transparent !important;
    color: #f0eff8 !important;
    transition: all 0.15s !important;
    width: 100%;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.28) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"] {
    background: #7c6cfa !important;
    border-color: #7c6cfa !important;
    color: #fff !important;
}
.stButton > button[kind="primary"]:hover { background: #6a5ae0 !important; }

/* Sidebar nav buttons — full width, flat */
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 9px 14px !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 400 !important;
    color: #7a7990 !important;
    background: transparent !important;
    border: 0.5px solid transparent !important;
    border-radius: 8px !important;
    margin-bottom: 2px;
    transform: none !important;
    letter-spacing: 0 !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.04) !important;
    color: #f0eff8 !important;
    transform: none !important;
    border-color: transparent !important;
}

/* Download button */
.stDownloadButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    background: rgba(62,207,170,0.1) !important;
    color: #3ecfaa !important;
    border: 0.5px solid rgba(62,207,170,0.3) !important;
    border-radius: 8px !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    background: rgba(62,207,170,0.18) !important;
    transform: translateY(-1px) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #16161f !important;
    border: 1.5px dashed rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    transition: all 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7c6cfa !important;
    background: rgba(124,108,250,0.05) !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #16161f !important;
    border: 0.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #f0eff8 !important;
}

/* Text input */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 0.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #f0eff8 !important;
    padding: 10px 14px !important;
    transition: border-color 0.15s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #7c6cfa !important;
    background: rgba(124,108,250,0.05) !important;
    box-shadow: none !important;
}
[data-testid="stTextInput"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.05em !important;
    color: #7a7990 !important;
    text-transform: uppercase !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 0.5px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Alerts */
div[data-testid="stInfo"]    { background: rgba(124,108,250,0.08) !important; border-color: rgba(124,108,250,0.4) !important; }
div[data-testid="stSuccess"] { background: rgba(62,207,170,0.08) !important;  border-color: rgba(62,207,170,0.4) !important; }
div[data-testid="stWarning"] { background: rgba(245,166,35,0.08) !important;  border-color: rgba(245,166,35,0.4) !important; }
div[data-testid="stError"]   { background: rgba(250,108,108,0.08) !important; border-color: rgba(250,108,108,0.4) !important; }

/* Progress bar */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #7c6cfa, #3ecfaa) !important;
    border-radius: 4px !important;
}
[data-testid="stProgressBar"] > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 4px !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.5rem 0 !important; }

/* Pyplot charts */
.stPyplot { background: transparent !important; }
</style>
"""

SIDEBAR_HTML = """
<style>
/* Logo */
.sp-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 4px 6px 20px 6px;
    border-bottom: 0.5px solid rgba(255,255,255,0.07);
    margin-bottom: 14px;
}
.sp-logo-icon {
    width: 34px; height: 34px; flex-shrink: 0;
    background: linear-gradient(135deg, #7c6cfa, #3ecfaa);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
}
.sp-logo-name {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 14px !important;
    color: #f0eff8 !important; line-height: 1.2 !important;
}
.sp-logo-tag {
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important; color: #7a7990 !important;
    letter-spacing: 0.05em !important;
}

/* Nav section label */
.sp-nav-label {
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important; letter-spacing: 0.1em !important;
    color: #44435a !important; padding: 0 6px; margin-bottom: 6px;
    text-transform: uppercase;
}

/* Active nav item highlight */
.sp-nav-active > div > button,
.sp-nav-active .stButton > button {
    background: rgba(124,108,250,0.12) !important;
    color: #a89cfc !important;
    border-color: rgba(124,108,250,0.25) !important;
}

/* Status pill */
.sp-status {
    display: flex; align-items: center; gap: 7px;
    padding: 8px 10px; margin-top: 14px;
    border-top: 0.5px solid rgba(255,255,255,0.06);
}
.sp-status-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #3ecfaa; flex-shrink: 0;
    box-shadow: 0 0 5px #3ecfaa;
}
.sp-status-text {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important; color: #7a7990 !important;
}
</style>

<div class="sp-logo">
    <div class="sp-logo-icon">🔷</div>
    <div>
        <div class="sp-logo-name">SentimentPro</div>
        <div class="sp-logo-tag">Analytics Suite</div>
    </div>
</div>
<div class="sp-nav-label">Navigation</div>
"""

SIDEBAR_FOOTER_HTML = """
<div class="sp-status">
    <div class="sp-status-dot"></div>
    <div class="sp-status-text">pipeline ready</div>
</div>
"""


def apply_theme():
    """Inject global CSS. Call at the very top of every page, before any st. call."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def render_sidebar(active: str = ""):
    """
    Render the full styled sidebar with nav buttons.
    active: one of 'upload', 'results', 'insights', 'email'
    """
    st.sidebar.markdown(SIDEBAR_HTML, unsafe_allow_html=True)

    pages = [
        ("upload",   "📂", "Upload"),
        ("results",  "📊", "Results"),
        ("insights", "📈", "Insights"),
        ("email",    "📧", "Email"),
    ]

    for key, icon, label in pages:
        # Wrap in a div that can be highlighted if active
        is_active = (active == key)
        css_class = "sp-nav-active" if is_active else ""
        st.sidebar.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if st.sidebar.button(f"{icon}  {label}", key=f"nav_{key}"):
            st.switch_page(f"pages/{['1_Upload','2_Results','3_Insights','4_Email'][[p[0] for p in pages].index(key)]}.py")
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown(SIDEBAR_FOOTER_HTML, unsafe_allow_html=True)
