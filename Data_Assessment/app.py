import streamlit as st
from utils.auth import check_session
from utils.styles import inject_global_styles

st.set_page_config(
    page_title="Assessment Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_styles()

# Route based on session state
if "user" not in st.session_state or st.session_state.user is None:
    from pages.auth_page import render_auth
    render_auth()
elif st.session_state.get("current_page") == "dashboard":
    from pages.dashboard_page import render_dashboard
    render_dashboard()
elif st.session_state.get("current_page") == "questions":
    from pages.questions_page import render_questions
    render_questions()
else:
    st.session_state.current_page = "dashboard"
    st.rerun()
