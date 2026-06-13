import streamlit as st


def render_chatbot():

    st.markdown(
        """
        <h3 style='font-size: 18px; font-weight: 600; margin-bottom: 12px;'>
            💬 AI Health Chatbot
        </h3>
        """,
        unsafe_allow_html=True
    )

    with st.container():

        with st.chat_message("user"):
            st.write("I have fever and cough.")

        with st.chat_message("assistant"):
            st.write(
                "Please consult a physician. It could be a viral infection or flu. Stay hydrated."
            )

        st.chat_input(
            "Ask your health related query...",
            key="main_stream_chat_input"
        )