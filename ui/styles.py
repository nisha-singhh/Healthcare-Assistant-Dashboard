import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* Global Canvas Setup */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        .stApp {
            background-color: #F8FAFC !important;
        }
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            font-family: 'Inter', sans-serif !important;
            color: #0F172A !important;
        }

        /* Premium Dashboard Card Blocks */
        .dashboard-card {
            background: #FFFFFF !important;
            padding: 20px !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            margin-bottom: 16px !important;
        }

        /* Accurate Custom Typography */
        .teal-accent {
            color: #0D9488 !important;
            font-weight: 600 !important;
        }
        .sub-text {
            color: #64748B !important;
            font-size: 13px !important;
        }

        /* Sidebar Container Overhaul */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }

        /* Sidebar Radio Group Options Configuration */
        [data-testid="stSidebar"] div.stRadio div[role="radiogroup"] {
            gap: 6px !important;
            padding: 10px 0px;
        }

        [data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label {
            background-color: transparent !important;
            border: none !important;
            padding: 12px 16px !important;
            border-radius: 10px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            color: #475569 !important;
            transition: all 0.2s ease-in-out;
            margin: 0 !important;
            width: 100% !important;
            cursor: pointer;
        }

        /* Hover Navigation Style */
        [data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:hover {
            background-color: #F1F5F9 !important;
            color: #0F172A !important;
        }

        /* =====================================================================
           FIX: FORCE SIDEBAR TEXT COLOR & ACTIVE VISIBILITY 
           ===================================================================== */
        /* Default State Text Formatting */
        div[data-testid="stSidebarUserContent"] div.stRadio div[role="radiogroup"] label p {
            color: #475569 !important;
            font-weight: 500 !important;
        }

        /* Hover State Text Formatting */
        div[data-testid="stSidebarUserContent"] div.stRadio div[role="radiogroup"] label:hover p {
            color: #0F172A !important;
        }

        /* Strict Active Tab Structural Target - Isse white text tight bind rahega */
        div[data-testid="stSidebarUserContent"] div.stRadio div[role="radiogroup"] div[data-testid="stWidgetListItem"] input[type="radio"]:checked + div label {
            background-color: #0D9488 !important;
            box-shadow: 0 4px 10px rgba(13, 148, 136, 0.2) !important;
        }

        div[data-testid="stSidebarUserContent"] div.stRadio div[role="radiogroup"] div[data-testid="stWidgetListItem"] input[type="radio"]:checked + div label p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* Hiding Streamlit's Default Selection Radio Circles Completely */
        [data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label div[data-testid="stMarker"] {
            display: none !important;
        }

        /* Universal Native Buttons Remapping to Match UI Mockup */
        div.stButton > button {
            background-color: #0D9488 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }

        div.stButton > button:hover {
            background-color: #0F766E !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25) !important;
        }
        
        div.stButton > button:active {
            background-color: #115E59 !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            background-color: #0F172A !important;
            color: #FFFFFF !important;
            border-color: #0F172A !important;
            box-shadow: none !important;
        }
        /* Predict Disease button alag dikhna chahiye chips se */
        div.stButton > button[kind="primary"] {
            background-color: #0D9488 !important;
            color: #FFFFFF !important;
        }

        /* Quick Action Internal Card Framework Layout */
        .action-box {
            background-color: #FFFFFF !important;
            padding: 16px !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            margin-bottom: 10px !important;
        }

        /* Fix selectbox dropdown - remove red selected option highlight */
        div[data-baseweb="select"] ul li[aria-selected="true"],
        div[data-baseweb="popover"] ul li[aria-selected="true"] {
            background-color: #F1F5F9 !important;
            color: #0F172A !important;
        }

        div[data-baseweb="select"] ul li:hover,
        div[data-baseweb="popover"] ul li:hover {
            background-color: #E2E8F0 !important;
            color: #0F172A !important;
        }

        /* Remove red focus ring on selectbox */
        div[data-baseweb="select"] > div:focus-within,
        div[data-baseweb="select"] > div {
            border-color: #CBD5E1 !important;
            box-shadow: none !important;
        }

        div[data-baseweb="select"] > div:focus-within {
            border-color: #0D9488 !important;
            box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.15) !important;
        }
        /* Chip default - light grey */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            background-color: #F1F5F9 !important;
            color: #475569 !important;
            border: 1.5px solid #E2E8F0 !important;
            font-size: 12px !important;
            font-weight: 500 !important;
            box-shadow: none !important;
        }

        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            background-color: #E2E8F0 !important;
            color: #0F172A !important;
            box-shadow: none !important;
        }     
        /* Active chip button hide karo - sirf dark HTML div dikhega */
        button[kind="secondary"][data-testid*="chip_"]:has(span:contains("✓")) {
            opacity: 0 !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            pointer-events: auto !important;
            position: absolute !important;
        }   

    </style>
    """, unsafe_allow_html=True)