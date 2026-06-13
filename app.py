import streamlit as st
import joblib
import pandas as pd
import sqlite3
from datetime import datetime

from config import get_connection

from ui.styles import load_css
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard
from ui.chatbot import render_chatbot
from ui.appointment import render_appointment
from ui.right_panel import render_right_panel

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="HealthCare Assistant",
    page_icon="🏥",
    layout="wide"
)

# ==============================================================================
# LOAD CSS
# ==============================================================================
load_css()

# ==============================================================================
# MODEL & DATASET LOAD
# ==============================================================================
model = joblib.load("model.pkl")
symptom_columns = list(pd.read_csv("datasets/Training.csv").drop("prognosis", axis=1).columns)

# ==============================================================================
# DATABASE FUNCTIONS
# ==============================================================================
def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disease_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            symptoms TEXT,
            disease TEXT,
            confidence TEXT,
            date_predicted TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_name TEXT,
            appointment_date TEXT,
            appointment_time TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_name TEXT,
            specialization TEXT,
            hospital TEXT,
            rating TEXT,
            reviews TEXT,
            disease_specialty TEXT
        )
    """)
    conn.commit()
    conn.close()

init_database()

def fetch_recent_history():
    conn = get_connection()
    try:
        query = """
        SELECT date_predicted AS Date, symptoms AS Symptoms, disease AS [Predicted Disease], confidence AS Confidence
        FROM disease_history ORDER BY id DESC LIMIT 5
        """
        df = pd.read_sql_query(query, conn)
    except Exception:
        df = pd.DataFrame(columns=["Date", "Symptoms", "Predicted Disease", "Confidence"])
    finally:
        conn.close()
    return df

def fetch_appointments():
    conn = get_connection()
    try:
        query = """
        SELECT id AS [ID], doctor_name AS [Doctor Name], appointment_date AS [Date], appointment_time AS [Time Slot]
        FROM appointments ORDER BY id DESC
        """
        df = pd.read_sql_query(query, conn)
    except Exception:
        df = pd.DataFrame(columns=["ID", "Doctor Name", "Date", "Time Slot"])
    finally:
        conn.close()
    return df

def save_appointment(doc_name, app_date, app_time):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO appointments (doctor_name, appointment_date, appointment_time)
            VALUES (?, ?, ?)
        """, (doc_name, str(app_date), app_time))
        conn.commit()
    except Exception as e:
        st.error(f"Failed to book appointment: {e}")
    finally:
        conn.close()

def save_prediction(symptoms, disease, confidence):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Aaj ki date formatted tarike se nikalte hain (Jaise mockup mein h: 15 May 2025)
        current_date = datetime.now().strftime("%d %b %Y")
        
        cursor.execute("""
            INSERT INTO disease_history (patient_name, symptoms, disease, confidence, date_predicted)
            VALUES (?, ?, ?, ?, ?)
        """, ("Nisha Sharma", symptoms, disease, confidence, current_date))
        
        conn.commit()
    except Exception as e:
        st.error(f"Failed to save prediction history: {e}")
    finally:
        conn.close()

# --- Sahi aur Clean Doctor Function ---
def fetch_recommended_doctor(disease_name):
    # Bilkul saaf fallback data bina kisi HTML ke
    default_doctor = {
        "doctor_name": "Dr. Raj Sharma",
        "specialization": "General Physician",
        "hospital": "Max Hospital, Delhi, India",
        "rating": "4.8",
        "reviews": "120"
    }
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT doctor_name, specialization, hospital, rating, reviews FROM doctors WHERE disease_specialty = ?", (disease_name,))
        row = cursor.fetchone()
        if row:
            return {
                "doctor_name": row[0],
                "specialization": row[1],
                "hospital": row[2],
                "rating": row[3],
                "reviews": row[4]
            }
    except Exception:
        return default_doctor
    finally:
        conn.close()
        
    return default_doctor

# ==============================================================================
# STATE & DATA LOADING
# ==============================================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "📅 Dashboard"

#  [DYNAMIC REFRESHEABLE DATA FLOW]
df_history = fetch_recent_history()
df_appointments = fetch_appointments()

# ==============================================================================
# LAYOUT RENDERING
# ==============================================================================
selected_page = render_sidebar()
main_center_flow, main_right_flow = st.columns([65, 35])

with main_center_flow:
    if selected_page == "📅 Dashboard":
        render_dashboard(df_history)
    elif selected_page == "💬 AI Chatbot":
        render_chatbot()
    elif selected_page == "📆 Book Appointment":
        render_appointment(df_appointments)
    elif selected_page == "🩺 Predict Disease":
        st.markdown("<h2>🩺 Predict Disease Engine</h2>", unsafe_allow_html=True)
        st.info("Please use the right panel to input symptoms.")

with main_right_flow:
    # Humne model, symptom_columns aur save_prediction function ko right panel mein bhej diya
    render_right_panel(
        df_history=df_history,
        fetch_recommended_doctor=fetch_recommended_doctor,
        save_appointment=save_appointment,
        model=model,
        symptom_columns=symptom_columns,
        save_prediction=save_prediction
    )