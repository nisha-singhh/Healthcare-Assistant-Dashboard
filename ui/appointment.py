import streamlit as st


def render_appointment(df_appointments):

    st.markdown(
        """
        <h2 style='font-size: 24px; font-weight: 600; margin-bottom: 15px;'>
            📆 Book Slots & Active Appointments
        </h2>
        """,
        unsafe_allow_html=True
    )

    if not df_appointments.empty:

        st.dataframe(
            df_appointments,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No active appointments booked yet. Use the right side panel to book one!"
        )