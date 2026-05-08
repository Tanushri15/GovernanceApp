"""
Authentication helpers.
Users are stored in a local JSON file (users.json) for portability.
Swap with a database-backed store in production.
"""
import json
import hashlib
import os
import streamlit as st
from datetime import datetime

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "users.json")
ANSWERS_DIR = os.path.join(os.path.dirname(__file__), "..", "answers")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def _user_key(name: str, company: str) -> str:
    return f"{name.strip().lower()}|{company.strip().lower()}"


# ── Public API ─────────────────────────────────────────────────────────────────

def register_user(name: str, email: str, company: str, password: str) -> tuple[bool, str]:
    """Register a new user. Returns (success, message)."""
    users = _load_users()
    key = _user_key(name, company)
    if key in users:
        return False, "An account with this name and company already exists. Please sign in."
    users[key] = {
        "name": name.strip(),
        "email": email.strip(),
        "company": company.strip(),
        "password_hash": _hash(password),
        "created_at": datetime.utcnow().isoformat(),
        "last_login": None,
        "answers": {},
    }
    _save_users(users)
    return True, "Account created successfully."


def login_user(name: str, company: str, password: str) -> tuple[bool, str, dict | None]:
    """Authenticate user. Returns (success, message, user_dict | None)."""
    users = _load_users()
    key = _user_key(name, company)
    if key not in users:
        return False, "No account found for this name and company. Please sign up.", None
    user = users[key]
    if user["password_hash"] != _hash(password):
        return False, "Incorrect password. Please try again.", None
    # Update last login
    users[key]["last_login"] = datetime.utcnow().isoformat()
    _save_users(users)
    return True, "Welcome back!", {**user, "_key": key}


def save_answers(user_key: str, domain: str, answers: dict):
    """Persist answers for a user under a specific domain."""
    users = _load_users()
    if user_key not in users:
        return
    if "answers" not in users[user_key]:
        users[user_key]["answers"] = {}
    users[user_key]["answers"][domain] = {
        "responses": answers,
        "saved_at": datetime.utcnow().isoformat(),
    }
    _save_users(users)
    # Also update session state
    if "user" in st.session_state and st.session_state.user:
        st.session_state.user["answers"] = users[user_key]["answers"]


def load_user_answers(user_key: str) -> dict:
    """Return the full answers dict for a user."""
    users = _load_users()
    return users.get(user_key, {}).get("answers", {})


def check_session() -> bool:
    """Return True if a valid session exists."""
    return "user" in st.session_state and st.session_state.user is not None


def logout():
    st.session_state.user = None
    st.session_state.current_page = None
    st.session_state.pop("active_domain", None)
