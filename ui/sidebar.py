import streamlit as st


def render_sidebar():

    with st.sidebar:

        # Logo Section
        st.markdown("""
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 25px; margin-top: -10px;'>
                <div style='background-color: #E6F4F1; padding: 8px; border-radius: 10px; display: flex; align-items: center; justify-content: center;'>
                    <span style='font-size: 24px;'>💚</span>
                </div>
                <div>
                    <h3 style='margin: 0; font-size: 18px; font-weight: 700; color: #0F172A !important; line-height: 1.2;'>
                        HealthCare<br>
                        <span style='color: #0D9488 !important; font-size: 12px; letter-spacing: 1px; font-weight: 600;'>
                            ASSISTANT
                        </span>
                    </h3>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Menu Options
        menu_options = [
            "📅 Dashboard",
            "🩺 Predict Disease",
            "💬 AI Chatbot",
            "📆 Book Appointment",
            "📄 Reports",
            "👤 Profile",
            "🚪 Logout"
        ]

        default_index = menu_options.index(
            st.session_state.current_page
        )

        selected_page = st.radio(
            "Navigate Menu",
            menu_options,
            index=default_index,
            label_visibility="collapsed"
        )

        st.session_state.current_page = selected_page

        st.markdown("---")

        # Need Help Box
        st.markdown("""
            <div style='background-color: #F1F5F9; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #E2E8F0; margin-top: 20px;'>
                <p style='margin: 0; font-weight: 600; font-size: 14px; color: #0F172A !important;'>
                    Need Help?
                </p>
                <p style='margin: 4px 0 12px 0; font-size: 12px; color: #64748B !important;'>
                    Talk to our AI Assistant
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.button(
            "Chat Now",
            key="sidebar_chat_action"
        )

    return selected_page