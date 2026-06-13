import streamlit as st
import pandas as pd

def render_right_panel(
    df_history,
    fetch_recommended_doctor,
    save_appointment,
    model=None,
    symptom_columns=None,
    save_prediction=None
):

    latest_disease = "Typhoid"
    if not df_history.empty:
        latest_disease = df_history.iloc[0]["Predicted Disease"]

    doc_data = fetch_recommended_doctor(latest_disease)

    st.markdown("<h3 style='margin-top: 0; font-size: 18px; color: #0F172A;'>Predict Disease</h3>", unsafe_allow_html=True)
    
    symptom_col, result_col = st.columns([55, 45])

    with symptom_col:
        st.markdown("<p style='font-size: 13px; font-weight: 500; margin-bottom: 4px; color: #475569;'>Search & Select Symptoms</p>", unsafe_allow_html=True)
        
        available_options = ["-- Select Symptom --"] + sorted(symptom_columns) if symptom_columns else ["-- Select Symptom --"]
        
        chosen_symptom = st.selectbox(
            label="Search Symptoms",
            options=available_options,
            label_visibility="collapsed",
            key="clean_symptom_dropdown"
        )
        
        if "selected_from_search" not in st.session_state:
            st.session_state.selected_from_search = []
            
        if chosen_symptom != "-- Select Symptom --" and chosen_symptom not in st.session_state.selected_from_search:
            st.session_state.selected_from_search.append(chosen_symptom)
            st.rerun()
            
        selected_from_search = st.session_state.selected_from_search
        
        st.write("")

        st.markdown("<p style='font-size: 13px; font-weight: 500; margin-bottom: 8px; color: #475569;'>Active & Suggested Symptoms</p>", unsafe_allow_html=True)
        
        base_defaults = ["fever", "vomiting", "cough", "fatigue", "headache", "body_pain"]
        
        final_slots = []
        if selected_from_search:
            final_slots = list(selected_from_search)[:6]
            
        if len(final_slots) < 6:
            for d in base_defaults:
                if d not in final_slots and len(final_slots) < 6:
                    final_slots.append(d)
                    
        if len(final_slots) < 6 and symptom_columns:
            for s in symptom_columns:
                if s not in final_slots and len(final_slots) < 6:
                    final_slots.append(s)

        if "active_chips" not in st.session_state:
            st.session_state.active_chips = set()

        for sym in selected_from_search:
            st.session_state.active_chips.add(sym)

        active_toggles_state = {}

        # Render 3 rows of 2 chips each using columns
        pairs = [(final_slots[i], final_slots[i+1] if i+1 < len(final_slots) else None) for i in range(0, len(final_slots), 2)]

        for left_sym, right_sym in pairs:
            col_l, col_r = st.columns(2)

            for sym_id, col in [(left_sym, col_l), (right_sym, col_r)]:
                if sym_id is None:
                    active_toggles_state[sym_id] = False
                    continue
                    
                clean_label = str(sym_id).replace("_", " ").title()
                is_active = sym_id in st.session_state.active_chips

                if is_active:
                    bg = "#0F172A"
                    color = "#FFFFFF"
                    border = "#0F172A"
                else:
                    bg = "#F1F5F9"
                    color = "#64748B"
                    border = "#E2E8F0"

                with col:
                    st.markdown(f"""
                    <div style='background:{bg}; color:{color}; border:1.5px solid {border};
                                border-radius:8px; padding:10px 8px; font-size:12px; font-weight:500;
                                text-align:center; height:42px; display:flex; align-items:center;
                                justify-content:center; box-sizing:border-box;
                                overflow:hidden; white-space:nowrap; text-overflow:ellipsis;
                                margin-bottom:2px;'>
                        {clean_label}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(clean_label, key=f"chip_{sym_id}", use_container_width=True):
                        if is_active:
                            st.session_state.active_chips.discard(sym_id)
                            if sym_id in st.session_state.selected_from_search:
                                st.session_state.selected_from_search.remove(sym_id)
                        else:
                            st.session_state.active_chips.add(sym_id)
                        st.rerun()

                active_toggles_state[sym_id] = is_active

        # Hide real buttons but keep them clickable
        st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            opacity: 0 !important;
            height: 38px !important;
            min-height: 38px !important;
            margin-top: -46px !important;
            position: relative !important;
            z-index: 999 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            opacity: 0 !important;
            height: 38px !important;
            min-height: 38px !important;
            margin-top: -46px !important;
            position: relative !important;
            z-index: 999 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        /* Predict button restore */
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] div.stButton > button {
            opacity: 1 !important;
            height: auto !important;
            min-height: 38px !important;
            margin-top: 0px !important;
            position: static !important;
            background-color: #0D9488 !important;
            color: #FFFFFF !important;
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        predict_clicked = st.button("Predict Disease", key="right_predict_btn", use_container_width=True)
    


    with result_col:
        disease_display = "No Diagnosis"
        confidence_display = "--%"
        
        active_symptoms = [sym for sym, is_on in active_toggles_state.items() if is_on]

        if predict_clicked:
            if active_symptoms and (model is not None) and (symptom_columns is not None):
                try:
                    input_vector = [0] * len(symptom_columns)
                    for sym in active_symptoms:
                        if sym in symptom_columns:
                            idx = symptom_columns.index(sym)
                            input_vector[idx] = 1
                    
                    df_input = pd.DataFrame([input_vector], columns=symptom_columns)
                    prediction = model.predict(df_input)[0]
                    disease_display = str(prediction)
                    
                    if hasattr(model, "predict_proba"):
                        proba = model.predict_proba(df_input)
                        confidence_display = f"{int(max(proba[0]) * 100)}%"
                    else:
                        confidence_display = "92%"
                    
                    if save_prediction:
                        save_prediction(", ".join(active_symptoms), disease_display, confidence_display)
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Prediction Error: {e}")
            else:
                st.warning("Please select at least one symptom!")

        if not df_history.empty and disease_display == "No Diagnosis":
            disease_display = df_history.iloc[0]["Predicted Disease"]
            confidence_display = df_history.iloc[0]["Confidence"]

        st.markdown(f"""
        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); height: 100%;'>
            <div style='font-size: 32px; margin-bottom: 4px;'>📋</div>
            <p style='font-size: 12px; font-weight: 600; color: #475569; margin: 0;'>Prediction Result</p>
            <h3 style='color: #0D9488; font-size: 22px; font-weight: 700; margin: 8px 0 2px 0;'>{disease_display}</h3>
            <p style='font-size: 11px; color: #64748B; margin: 0;'>Confidence</p>
            <p style='font-size: 16px; font-weight: 700; color: #0F172A; margin: 2px 0 10px 0;'>{confidence_display}</p>
            <p style='font-size: 10px; color: #94A3B8; line-height: 1.3; margin: 0;'>Please consult with the doctor for better treatment.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='margin: 24px 0; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 18px; color: #0F172A; margin-top: 15px;'>👨‍⚕️ Recommended Doctor</h3>", unsafe_allow_html=True)
    
    latest_disease = "Typhoid"
    if not df_history.empty:
        latest_disease = df_history.iloc[0]["Predicted Disease"]
    doc_data = fetch_recommended_doctor(latest_disease)

    doctor_html = f"""
    <div class='dashboard-card' style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px;'>
        <h4 style='margin: 0 0 4px 0; font-size: 16px; color: #0F172A;'><b>{doc_data['doctor_name']}</b></h4>
        <p style='margin: 0 0 8px 0; font-size: 13px; color: #0D9488; font-weight: 600;'>{doc_data['specialization']}</p>
        <p style='margin: 4px 0; font-size: 12px; color: #64748B;'>🏥 {doc_data['hospital']}</p>
        <p style='margin: 4px 0; font-size: 12px; color: #0F172A;'>⭐ <b>{doc_data.get('rating', '4.8')}</b> ({doc_data.get('reviews', '120')} Patient Reviews)</p>
    </div>
    """
    st.markdown(doctor_html, unsafe_allow_html=True)

    tab_book, tab_report = st.tabs(["📅 Book Slot", "📄 Report Summary"])

    with tab_book:
        appointment_date = st.date_input("Select Date", key="r_date")
        appointment_time = st.selectbox("Select Time", ["10:00 AM", "11:30 AM", "02:00 PM"], key="r_time")

        if st.button("Confirm Appointment", key="r_confirm_btn", use_container_width=True):
            save_appointment(doc_data["doctor_name"], appointment_date, appointment_time)
            st.success(f"🎉 Appointment Booked successfully with {doc_data['doctor_name']} for {appointment_date}!")

    with tab_report:
        st.write("**Patient:** Nisha Sharma")
        st.write(f"**Case:** {latest_disease} Verified (AI Flagged)")
        st.button("📥 Download PDF Report", key="r_pdf_btn", use_container_width=True)