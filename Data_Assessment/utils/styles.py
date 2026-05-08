import streamlit as st

def inject_global_styles():
    st.markdown("""
    <style>
    /* ── Azure Portal Design System ── */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;500;600;700&display=swap');

    :root {
        --azure-blue:        #0078d4;
        --azure-blue-dark:   #005a9e;
        --azure-blue-light:  #deecf9;
        --azure-blue-hover:  #106ebe;
        --azure-teal:        #00b7c3;
        --azure-bg:          #f3f2f1;
        --azure-surface:     #ffffff;
        --azure-border:      #edebe9;
        --azure-border-dark: #c8c6c4;
        --azure-text:        #323130;
        --azure-text-muted:  #605e5c;
        --azure-text-subtle: #8a8886;
        --azure-success:     #107c10;
        --azure-warning:     #797673;
        --azure-error:       #a4262c;
        --azure-header:      #1b1a19;
        --azure-sidebar:     #201f1e;
        --font:              'Segoe UI', system-ui, -apple-system, sans-serif;
    }

    /* Reset Streamlit defaults */
    html, body, [class*="css"] {
        font-family: var(--font) !important;
        color: var(--azure-text) !important;
    }

    .stApp {
        background: var(--azure-bg) !important;
    }

    /* Hide default Streamlit UI chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }

    /* Remove default padding */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    .main > div { padding: 0 !important; }

    /* ── Top Navigation Bar ── */
    .az-topbar {
        background: var(--azure-header);
        color: #fff;
        height: 48px;
        display: flex;
        align-items: center;
        padding: 0 20px;
        gap: 16px;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,.3);
    }
    .az-topbar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 15px;
        font-weight: 600;
        color: #fff;
        text-decoration: none;
        letter-spacing: .2px;
    }
    .az-topbar-logo svg { width: 22px; height: 22px; }
    .az-topbar-divider {
        width: 1px;
        height: 20px;
        background: #4a4a4a;
        margin: 0 6px;
    }
    .az-topbar-title {
        font-size: 14px;
        color: #ccc;
        font-weight: 400;
    }
    .az-topbar-actions {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .az-topbar-user {
        font-size: 13px;
        color: #ccc;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .az-avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: var(--azure-blue);
        color: white;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* ── Page Content Wrapper ── */
    .az-page {
        padding: 24px 32px;
        min-height: calc(100vh - 48px);
    }

    /* ── Breadcrumb ── */
    .az-breadcrumb {
        font-size: 12px;
        color: var(--azure-text-subtle);
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .az-breadcrumb a {
        color: var(--azure-blue);
        text-decoration: none;
    }
    .az-breadcrumb a:hover { text-decoration: underline; }

    /* ── Page Header ── */
    .az-page-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--azure-border);
    }
    .az-page-icon {
        width: 48px;
        height: 48px;
        background: var(--azure-blue-light);
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
    .az-page-title { font-size: 22px; font-weight: 600; color: var(--azure-text); margin: 0; }
    .az-page-subtitle { font-size: 13px; color: var(--azure-text-muted); margin: 2px 0 0 0; }

    /* ── Cards ── */
    .az-card {
        background: var(--azure-surface);
        border: 1px solid var(--azure-border);
        border-radius: 4px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .az-card-header {
        font-size: 14px;
        font-weight: 600;
        color: var(--azure-text);
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--azure-border);
    }

    /* ── Stat Tiles (Dashboard) ── */
    .az-stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 12px;
        margin-bottom: 24px;
    }
    .az-stat-tile {
        background: var(--azure-surface);
        border: 1px solid var(--azure-border);
        border-radius: 4px;
        padding: 16px 20px;
        display: flex;
        flex-direction: column;
        gap: 4px;
        transition: box-shadow .15s;
    }
    .az-stat-tile:hover { box-shadow: 0 2px 8px rgba(0,0,0,.12); }
    .az-stat-label { font-size: 12px; color: var(--azure-text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: .4px; }
    .az-stat-value { font-size: 28px; font-weight: 300; color: var(--azure-text); }
    .az-stat-sub { font-size: 12px; color: var(--azure-text-subtle); }
    .az-stat-accent { color: var(--azure-blue); }

    /* ── Progress Bar ── */
    .az-progress-wrap { margin-bottom: 4px; }
    .az-progress-label {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        color: var(--azure-text-muted);
        margin-bottom: 4px;
    }
    .az-progress-bar-bg {
        height: 6px;
        background: var(--azure-border);
        border-radius: 3px;
        overflow: hidden;
    }
    .az-progress-bar-fill {
        height: 100%;
        background: var(--azure-blue);
        border-radius: 3px;
        transition: width .4s ease;
    }
    .az-progress-bar-fill.complete { background: var(--azure-success); }

    /* ── Domain Row ── */
    .az-domain-row {
        background: var(--azure-surface);
        border: 1px solid var(--azure-border);
        border-radius: 4px;
        padding: 16px 20px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: border-color .15s, box-shadow .15s;
        cursor: pointer;
    }
    .az-domain-row:hover {
        border-color: var(--azure-blue);
        box-shadow: 0 0 0 1px var(--azure-blue);
    }
    .az-domain-icon { font-size: 20px; min-width: 32px; text-align: center; }
    .az-domain-info { flex: 1; }
    .az-domain-name { font-size: 14px; font-weight: 600; color: var(--azure-text); margin-bottom: 6px; }
    .az-domain-progress { }
    .az-domain-badge {
        font-size: 12px;
        padding: 2px 10px;
        border-radius: 12px;
        font-weight: 500;
        white-space: nowrap;
    }
    .az-badge-done { background: #dff6dd; color: var(--azure-success); }
    .az-badge-partial { background: var(--azure-blue-light); color: var(--azure-blue-dark); }
    .az-badge-new { background: #f3f2f1; color: var(--azure-text-muted); border: 1px solid var(--azure-border-dark); }
    .az-chevron { color: var(--azure-text-subtle); font-size: 16px; }

    /* ── Auth Page ── */
    .az-auth-shell {
        min-height: 100vh;
        background: linear-gradient(135deg, #0078d4 0%, #005a9e 50%, #003966 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
    }
    .az-auth-box {
        background: #fff;
        border-radius: 4px;
        box-shadow: 0 8px 40px rgba(0,0,0,.25);
        width: 100%;
        max-width: 440px;
        padding: 40px;
    }
    .az-auth-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 32px;
    }
    .az-auth-logo-text {
        font-size: 18px;
        font-weight: 600;
        color: var(--azure-text);
    }
    .az-auth-heading {
        font-size: 20px;
        font-weight: 600;
        color: var(--azure-text);
        margin-bottom: 6px;
    }
    .az-auth-sub {
        font-size: 13px;
        color: var(--azure-text-muted);
        margin-bottom: 28px;
    }
    .az-auth-tabs {
        display: flex;
        border-bottom: 2px solid var(--azure-border);
        margin-bottom: 24px;
        gap: 0;
    }
    .az-auth-tab {
        padding: 8px 20px;
        font-size: 14px;
        font-weight: 500;
        color: var(--azure-text-muted);
        cursor: pointer;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
    }
    .az-auth-tab.active {
        color: var(--azure-blue);
        border-bottom-color: var(--azure-blue);
    }

    /* ── Form Elements ── */
    .az-field { margin-bottom: 16px; }
    .az-label {
        font-size: 13px;
        font-weight: 600;
        color: var(--azure-text);
        margin-bottom: 4px;
        display: block;
    }
    .az-label-required::after { content: ' *'; color: var(--azure-error); }

    /* Override Streamlit inputs */
    [data-testid="stTextInput"] > div > div > input,
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stTextArea"] textarea {
        border: 1px solid var(--azure-border-dark) !important;
        border-radius: 2px !important;
        font-family: var(--font) !important;
        font-size: 14px !important;
        color: var(--azure-text) !important;
        background: #fff !important;
        padding: 6px 8px !important;
        transition: border-color .1s !important;
    }
    [data-testid="stTextInput"] > div > div > input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--azure-blue) !important;
        box-shadow: 0 0 0 1px var(--azure-blue) !important;
        outline: none !important;
    }
    [data-testid="stTextInput"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stTextArea"] label {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: var(--azure-text) !important;
    }

    /* Streamlit Buttons */
    .stButton > button {
        font-family: var(--font) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border-radius: 2px !important;
        transition: background .15s, box-shadow .15s !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button:not([kind]) {
        background: var(--azure-blue) !important;
        color: #fff !important;
        border: 1px solid var(--azure-blue) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button:not([kind]):hover {
        background: var(--azure-blue-hover) !important;
        border-color: var(--azure-blue-hover) !important;
        box-shadow: 0 2px 6px rgba(0,120,212,.35) !important;
    }
    .stButton > button[kind="secondary"] {
        background: #fff !important;
        color: var(--azure-blue) !important;
        border: 1px solid var(--azure-blue) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: var(--azure-blue-light) !important;
    }

    /* Alert / info boxes */
    [data-testid="stAlert"] {
        border-radius: 2px !important;
        font-size: 13px !important;
        font-family: var(--font) !important;
    }

    /* Questions page */
    .az-question-card {
        background: var(--azure-surface);
        border: 1px solid var(--azure-border);
        border-radius: 4px;
        padding: 20px 24px;
        margin-bottom: 12px;
        transition: border-color .15s;
    }
    .az-question-card:hover { border-color: var(--azure-blue-dark); }
    .az-question-num {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        color: var(--azure-text-subtle);
        letter-spacing: .5px;
        margin-bottom: 6px;
    }
    .az-question-text {
        font-size: 14px;
        font-weight: 500;
        color: var(--azure-text);
        margin-bottom: 14px;
        line-height: 1.5;
    }
    .az-yn-row { display: flex; gap: 10px; }
    .az-yn-btn {
        padding: 5px 20px;
        border-radius: 2px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid;
        cursor: pointer;
        transition: all .15s;
    }
    .az-yn-yes { border-color: #107c10; color: #107c10; background: #fff; }
    .az-yn-yes.selected { background: #107c10; color: #fff; }
    .az-yn-no { border-color: #a4262c; color: #a4262c; background: #fff; }
    .az-yn-no.selected { background: #a4262c; color: #fff; }

    /* Status pills */
    .az-pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: .3px;
    }
    .az-pill-blue   { background: var(--azure-blue-light); color: var(--azure-blue-dark); }
    .az-pill-green  { background: #dff6dd; color: #107c10; }
    .az-pill-gray   { background: #f3f2f1; color: var(--azure-text-muted); border: 1px solid var(--azure-border-dark); }

    /* Command bar */
    .az-command-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 0;
        border-bottom: 1px solid var(--azure-border);
        margin-bottom: 20px;
    }

    /* Section label */
    .az-section-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        color: var(--azure-text-subtle);
        letter-spacing: .6px;
        margin: 24px 0 12px 0;
    }

    /* Divider */
    .az-divider { border-top: 1px solid var(--azure-border); margin: 20px 0; }

    /* Notification banner */
    .az-banner {
        background: var(--azure-blue-light);
        border-left: 3px solid var(--azure-blue);
        padding: 10px 16px;
        font-size: 13px;
        color: var(--azure-blue-dark);
        border-radius: 0 2px 2px 0;
        margin-bottom: 16px;
    }

    /* Export button row */
    .az-export-row {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 8px;
        margin-bottom: 20px;
    }

    /* Radio button override */
    [data-testid="stRadio"] label {
        font-size: 14px !important;
        font-family: var(--font) !important;
    }
    </style>
    """, unsafe_allow_html=True)
