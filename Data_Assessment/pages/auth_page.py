import streamlit as st
from utils.auth import register_user, login_user


def render_auth():
    # ── Tab state ────────────────────────────────────────────────────────────
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "signin"

    # ── Full-page gradient shell ──────────────────────────────────────────────
    st.markdown('<div class="az-auth-shell">', unsafe_allow_html=True)

    # We use a centred column to approximate the auth box
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        # Logo
        st.markdown("""
        <div class="az-auth-logo">
            <svg width="28" height="28" viewBox="0 0 96 96" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M48 4L92 76H4L48 4Z" fill="#0078d4"/>
                <path d="M48 24L76 72H20L48 24Z" fill="#50a0e0"/>
                <path d="M48 44L64 72H32L48 44Z" fill="#9dc8f0"/>
            </svg>
            <span class="az-auth-logo-text">Assessment Portal</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="az-auth-heading">Sign in to your account</div>', unsafe_allow_html=True)
        st.markdown('<div class="az-auth-sub">Complete your organisation\'s security assessment</div>', unsafe_allow_html=True)

        # ── Tab switch ─────────────────────────────────────────────────────────
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("Sign In", use_container_width=True,
                         type="primary" if st.session_state.auth_tab == "signin" else "secondary"):
                st.session_state.auth_tab = "signin"
                st.rerun()
        with tab_col2:
            if st.button("Create Account", use_container_width=True,
                         type="primary" if st.session_state.auth_tab == "signup" else "secondary"):
                st.session_state.auth_tab = "signup"
                st.rerun()

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # ── Sign In Form ───────────────────────────────────────────────────────
        if st.session_state.auth_tab == "signin":
            with st.form("signin_form", clear_on_submit=False):
                name     = st.text_input("Full Name *", placeholder="John Smith")
                company  = st.text_input("Company *", placeholder="Contoso Ltd.")
                password = st.text_input("Password *", type="password")

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

            if submitted:
                if not name or not company or not password:
                    st.error("Please fill in all fields.")
                else:
                    ok, msg, user = login_user(name, company, password)
                    if ok:
                        st.session_state.user = user
                        st.session_state.current_page = "dashboard"
                        st.rerun()
                    else:
                        st.error(msg)

        # ── Sign Up Form ───────────────────────────────────────────────────────
        else:
            with st.form("signup_form", clear_on_submit=False):
                name     = st.text_input("Full Name *", placeholder="John Smith")
                email    = st.text_input("Work Email *", placeholder="john@contoso.com")
                company  = st.text_input("Company *", placeholder="Contoso Ltd.")
                password = st.text_input("Password *", type="password",
                                         help="Minimum 8 characters")
                password2 = st.text_input("Confirm Password *", type="password")

                st.markdown("""
                <div style="font-size:11px;color:#605e5c;margin-top:4px;line-height:1.5;">
                By creating an account you agree to our Terms of Service and Privacy Policy.
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Create Account →", use_container_width=True, type="primary")

            if submitted:
                errors = []
                if not name:     errors.append("Full Name is required.")
                if not email:    errors.append("Email is required.")
                if not company:  errors.append("Company is required.")
                if not password: errors.append("Password is required.")
                if password and len(password) < 8:
                    errors.append("Password must be at least 8 characters.")
                if password != password2:
                    errors.append("Passwords do not match.")
                if "@" not in email:
                    errors.append("Please enter a valid email address.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    ok, msg = register_user(name, email, company, password)
                    if ok:
                        st.success(f"✓ {msg} You can now sign in.")
                        st.session_state.auth_tab = "signin"
                        st.rerun()
                    else:
                        st.error(msg)

        # Footer
        st.markdown("""
        <div style="margin-top:32px;font-size:11px;color:#8a8886;text-align:center;">
            © 2025 Assessment Portal. All rights reserved.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
