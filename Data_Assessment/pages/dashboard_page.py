import streamlit as st
import pandas as pd
from utils.db import fetch_questions
from utils.auth import logout
from utils.export import generate_csv_bytes, get_export_filename


DOMAIN_ICONS = {
    "Identity & Access Management": "🔐",
    "Network Security":             "🌐",
    "Data Protection":              "🛡️",
    "Incident Response":            "🚨",
    "Compliance & Governance":      "📋",
    "Cloud Security":               "☁️",
}
DEFAULT_ICON = "📁"


def render_dashboard():
    user     = st.session_state.user
    name     = user.get("name", "User")
    company  = user.get("company", "")
    initials = "".join(p[0].upper() for p in name.split()[:2])

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

    # ── Load Questions ─────────────────────────────────────────────────────────
    with st.spinner("Loading assessment data…"):
        questions_df = fetch_questions()

    answers = user.get("answers", {})
    domains = sorted(questions_df["domain"].unique())

    # ── Compute stats ──────────────────────────────────────────────────────────
    total_q     = len(questions_df)
    total_done  = sum(
        len(answers.get(d, {}).get("responses", {}))
        for d in domains
    )
    domains_done = sum(
        1 for d in domains
        if len(answers.get(d, {}).get("responses", {})) ==
           len(questions_df[questions_df["domain"] == d])
        and len(questions_df[questions_df["domain"] == d]) > 0
    )

    pct = int(total_done / total_q * 100) if total_q else 0

    # ── Page body ──────────────────────────────────────────────────────────────
    st.markdown('<div class="az-page">', unsafe_allow_html=True)

    # Breadcrumb
    st.markdown("""
    <div class="az-breadcrumb">
        🏠 Home &rsaquo; Assessment Dashboard
    </div>
    """, unsafe_allow_html=True)

    # Page header
    st.markdown(f"""
    <div class="az-page-header">
        <div class="az-page-icon">📊</div>
        <div>
            <div class="az-page-title">Assessment Dashboard</div>
            <div class="az-page-subtitle">Security Readiness Assessment — {company}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat tiles ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="az-stat-grid">
        <div class="az-stat-tile">
            <div class="az-stat-label">Overall Progress</div>
            <div class="az-stat-value az-stat-accent">{pct}%</div>
            <div class="az-stat-sub">{total_done} of {total_q} questions</div>
        </div>
        <div class="az-stat-tile">
            <div class="az-stat-label">Domains</div>
            <div class="az-stat-value">{len(domains)}</div>
            <div class="az-stat-sub">Assessment areas</div>
        </div>
        <div class="az-stat-tile">
            <div class="az-stat-label">Completed</div>
            <div class="az-stat-value" style="color:#107c10">{domains_done}</div>
            <div class="az-stat-sub">Domains finished</div>
        </div>
        <div class="az-stat-tile">
            <div class="az-stat-label">Remaining</div>
            <div class="az-stat-value">{total_q - total_done}</div>
            <div class="az-stat-sub">Questions left</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Overall progress bar
    st.markdown(f"""
    <div class="az-card" style="padding:16px 20px;margin-bottom:20px;">
        <div class="az-progress-label">
            <span>Overall Completion</span>
            <span><b>{pct}%</b></span>
        </div>
        <div class="az-progress-bar-bg">
            <div class="az-progress-bar-fill {'complete' if pct==100 else ''}"
                 style="width:{pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Command bar ────────────────────────────────────────────────────────────
    cmd1, cmd2, cmd3 = st.columns([1, 1, 6])
    with cmd1:
        csv_bytes = generate_csv_bytes(user, questions_df)
        st.download_button(
            label="⬇ Export CSV",
            data=csv_bytes,
            file_name=get_export_filename(user),
            mime="text/csv",
            use_container_width=True,
        )
    with cmd2:
        if st.button("🚪 Sign Out", use_container_width=True, type="secondary"):
            logout()
            st.rerun()

    # ── Domain list ────────────────────────────────────────────────────────────
    st.markdown('<div class="az-section-label">Assessment Domains</div>', unsafe_allow_html=True)

    for domain in domains:
        domain_qs   = questions_df[questions_df["domain"] == domain]
        total       = len(domain_qs)
        done_ids    = set(answers.get(domain, {}).get("responses", {}).keys())
        done        = len(done_ids)
        pct_d       = int(done / total * 100) if total else 0

        if done == total and total > 0:
            badge = '<span class="az-domain-badge az-badge-done">✓ Completed</span>'
        elif done > 0:
            badge = f'<span class="az-domain-badge az-badge-partial">{done}/{total} answered</span>'
        else:
            badge = '<span class="az-domain-badge az-badge-new">Not Started</span>'

        icon = DOMAIN_ICONS.get(domain, DEFAULT_ICON)

        st.markdown(f"""
        <div class="az-domain-row" id="domain-{domain.replace(' ','_')}">
            <div class="az-domain-icon">{icon}</div>
            <div class="az-domain-info">
                <div class="az-domain-name">{domain}</div>
                <div class="az-domain-progress">
                    <div class="az-progress-bar-bg" style="width:300px;max-width:100%;">
                        <div class="az-progress-bar-fill {'complete' if pct_d==100 else ''}"
                             style="width:{pct_d}%"></div>
                    </div>
                </div>
            </div>
            {badge}
            <div class="az-chevron">›</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Open → {domain}", key=f"open_{domain}", use_container_width=False):
            st.session_state.active_domain = domain
            st.session_state.current_page  = "questions"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # az-page
