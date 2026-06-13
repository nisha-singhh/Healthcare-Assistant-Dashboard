import streamlit as st


def render_dashboard(df_history):

    # Header Greetings Row
    st.markdown("""
        <div style='margin-bottom: 25px;'>
            <h1 style='margin: 0; font-size: 38px; font-weight: 700; color: #0F172A !important;'>Welcome back,</h1>
            <h3 style='margin: 5px 0 0 0; font-size: 24px; font-weight: 500; color: #475569 !important;'>Nisha Sharma 👋</h3>
            <p style='color: #64748B !important; font-size: 13px; margin: 5px 0 0 0;'>Take care of your health and let AI assist you.</p>
        </div>
    """, unsafe_allow_html=True)

    # Statistics Cards
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            "<div class='dashboard-card'><p class='sub-text'>📅 Appointments</p><h2 style='margin:5px 0; font-size:26px;'>5</h2><span style='color:#0D9488 !important; font-size:12px; font-weight:500;'>Total Booked</span></div>",
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            "<div class='dashboard-card'><p class='sub-text'>📄 Reports</p><h2 style='margin:5px 0; font-size:26px;'>8</h2><span style='color:#0D9488 !important; font-size:12px; font-weight:500;'>Total Reports</span></div>",
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            "<div class='dashboard-card'><p class='sub-text'>🦠 Last Disease</p><h2 style='margin:5px 0; font-size:24px; color:#EF4444 !important;'>Typhoid</h2><span style='color:#EF4444 !important; font-size:12px; font-weight:500;'>15 May 2025</span></div>",
            unsafe_allow_html=True
        )

    with m4:
        st.markdown(
            "<div class='dashboard-card'><p class='sub-text'>❤️ Health Score</p><h2 style='margin:5px 0; font-size:26px;'>86%</h2><span style='color:#3B82F6 !important; font-size:12px; font-weight:500;'>Good Condition</span></div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Actions
    st.markdown(
        "<h3 style='font-size: 18px; font-weight: 600; margin: 15px 0 10px 0;'>⚡ Quick Actions</h3>",
        unsafe_allow_html=True
    )

    qa1, qa2, qa3, qa4 = st.columns(4)

    with qa1:
        st.markdown(
            "<div class='action-box'><b>Core Predict</b><p style='font-size:11px; color:#64748B; margin:4px 0;'>Run diagnosis</p></div>",
            unsafe_allow_html=True
        )

        if st.button("Predict Now", key="qa_p", use_container_width=True):
            st.session_state.current_page = "🩺 Predict Disease"
            st.rerun()

    with qa2:
        st.markdown(
            "<div class='action-box'><b>AI Assistant</b><p style='font-size:11px; color:#64748B; margin:4px 0;'>Consult engine</p></div>",
            unsafe_allow_html=True
        )

        if st.button("Chat Now", key="qa_c", use_container_width=True):
            st.session_state.current_page = "💬 AI Chatbot"
            st.rerun()

    with qa3:
        st.markdown(
            "<div class='action-box'><b>Book Slot</b><p style='font-size:11px; color:#64748B; margin:4px 0;'>Find specialist</p></div>",
            unsafe_allow_html=True
        )

        if st.button("Book Now", key="qa_b", use_container_width=True):
            st.session_state.current_page = "📆 Book Appointment"
            st.rerun()

    with qa4:
        st.markdown(
            "<div class='action-box'><b>Reports Desk</b><p style='font-size:11px; color:#64748B; margin:4px 0;'>Download logs</p></div>",
            unsafe_allow_html=True
        )

        if st.button("Open Desk", key="qa_r", use_container_width=True):
            st.session_state.current_page = "📄 Reports"
            st.rerun()

    # Recent History
    st.markdown(
        "<h3 style='font-size: 18px; font-weight: 600; margin-bottom: 12px;'>📜 Recent History</h3>",
        unsafe_allow_html=True
    )

    st.dataframe(
        df_history,
        use_container_width=True,
        hide_index=True
    )