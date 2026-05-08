import streamlit as st
from utils.db import fetch_questions
from utils.auth import save_answers
from utils.export import generate_csv_bytes, get_export_filename


def render_questions():
    user   = st.session_state.user
    name   = user.get("name", "User")
    company = user.get("company", "")
    initials = "".join(p[0].upper() for p in name.split()[:2])
    domain = st.session_state.get("active_domain", "")

    # ── Top Nav ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="az-topbar">
        <div class="az-topbar-logo">
            <svg width="22" height="22" viewBox="0 0 96 96" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M48 4L92 76H4L48 4Z" fill="#0078d4"/>
                <path d="M48 24L76 72H20L48 24Z" fill="#50a0e0"/>
                <path d="M48 44L64 72H32L48 44Z" fill="#9dc8f0"/>
            </svg>
            Assessment Portal
        </div>
        <div class="az-topbar-divider"></div>
        <span class="az-topbar-title">{company}</span>
        <div class="az-topbar-actions">
            <div class="az-topbar-user">
                <div class="az-avatar">{initials}</div>
                {name}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Load questions ─────────────────────────────────────────────────────────
    questions_df = fetch_questions()
    domain_qs    = questions_df[questions_df["domain"] == domain].reset_index(drop=True)

    existing_answers = user.get("answers", {}).get(domain, {}).get("responses", {})

    st.markdown('<div class="az-page">', unsafe_allow_html=True)

    # Breadcrumb
    st.markdown(f"""
    <div class="az-breadcrumb">
        🏠 Home &rsaquo;
        <a href="#" onclick="return false;">Assessment Dashboard</a>
        &rsaquo; {domain}
    </div>
    """, unsafe_allow_html=True)

    # Page header
    st.markdown(f"""
    <div class="az-page-header">
        <div class="az-page-icon">📝</div>
        <div>
            <div class="az-page-title">{domain}</div>
            <div class="az-page-subtitle">
                {len(domain_qs)} questions · Answer Yes or No for each control
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Command bar ────────────────────────────────────────────────────────────
    back_col, save_col, export_col, spacer = st.columns([1, 1, 1.2, 5])
    with back_col:
        if st.button("← Dashboard", key="back_btn", type="secondary", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()

    # ── Banner ─────────────────────────────────────────────────────────────────
    done_count = len(existing_answers)
    total_count = len(domain_qs)
    if done_count > 0:
        st.markdown(f"""
        <div class="az-banner">
            ℹ️ You have previously answered <b>{done_count}</b> of <b>{total_count}</b> questions
            in this domain. Your saved responses are pre-filled below.
        </div>
        """, unsafe_allow_html=True)

    # ── Questions ──────────────────────────────────────────────────────────────
    st.markdown('<div class="az-section-label">Questions</div>', unsafe_allow_html=True)

    current_answers = dict(existing_answers)  # copy

    OPTIONS = ["Yes", "No"]

    with st.form(key=f"questions_form_{domain}"):
        for idx, row in domain_qs.iterrows():
            qid   = str(row["QuestionID"])
            qtext = row["QuestionText"]
            saved = existing_answers.get(qid)

            st.markdown(f"""
            <div class="az-question-card">
                <div class="az-question-num">Question {idx + 1} of {total_count}</div>
                <div class="az-question-text">{qtext}</div>
            </div>
            """, unsafe_allow_html=True)

            default_idx = OPTIONS.index(saved) if saved in OPTIONS else None

            answer = st.radio(
                label=f"q_{qid}",
                options=OPTIONS,
                index=default_idx,
                horizontal=True,
                key=f"radio_{qid}",
                label_visibility="collapsed",
            )

            if answer:
                current_answers[qid] = answer

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        save_submitted = st.form_submit_button(
            "💾  Save Answers",
            use_container_width=False,
            type="primary",
        )

    if save_submitted:
        # Only save questions that were actually answered
        to_save = {k: v for k, v in current_answers.items() if v in OPTIONS}
        save_answers(user["_key"], domain, to_save)
        # Refresh user in session
        from utils.auth import load_user_answers
        st.session_state.user["answers"] = load_user_answers(user["_key"])
        answered = len(to_save)
        st.success(f"✓ Saved {answered} answer(s) for **{domain}**.")
        if answered == total_count:
            st.balloons()

    # Export button below form
    with export_col:
        csv_bytes = generate_csv_bytes(st.session_state.user, questions_df)
        st.download_button(
            label="⬇ Export CSV",
            data=csv_bytes,
            file_name=get_export_filename(user),
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)  # az-page
