"""
Databricks connection utility.
All Databricks credentials are loaded from environment variables / Streamlit secrets.
"""
import os
import streamlit as st
import pandas as pd

try:
    from databricks import sql as databricks_sql
    DATABRICKS_AVAILABLE = True
except ImportError:
    DATABRICKS_AVAILABLE = False


def get_databricks_connection():
    """Return a Databricks SQL connection using secrets or env vars."""
    host   = st.secrets.get("DATABRICKS_HOST",  os.getenv("DATABRICKS_HOST", ""))
    token  = st.secrets.get("DATABRICKS_TOKEN", os.getenv("DATABRICKS_TOKEN", ""))
    http   = st.secrets.get("DATABRICKS_HTTP_PATH", os.getenv("DATABRICKS_HTTP_PATH", ""))
    catalog = st.secrets.get("DATABRICKS_CATALOG", os.getenv("DATABRICKS_CATALOG", ""))
    schema  = st.secrets.get("DATABRICKS_SCHEMA",  os.getenv("DATABRICKS_SCHEMA",  "default"))

    if not DATABRICKS_AVAILABLE:
        raise RuntimeError(
            "databricks-sql-connector not installed. "
            "Run: pip install databricks-sql-connector"
        )
    if not host or not token or not http:
        raise RuntimeError(
            "Databricks credentials missing. "
            "Set DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_HTTP_PATH in .streamlit/secrets.toml."
        )

    conn = databricks_sql.connect(
        server_hostname=host,
        http_path=http,
        access_token=token,
        catalog=catalog,
        schema=schema,
    )
    return conn


@st.cache_data(ttl=300, show_spinner=False)
def fetch_questions() -> pd.DataFrame:
    """
    Fetch questions from Databricks.

    Expected table schema (your personal catalog):
        QuestionID   INT
        Domain        VARCHAR
        QuestionText VARCHAR
    """
    try:
        conn = get_databricks_connection()
        catalog = st.secrets.get("DATABRICKS_CATALOG", os.getenv("DATABRICKS_CATALOG", ""))
        schema  = st.secrets.get("DATABRICKS_SCHEMA",  os.getenv("DATABRICKS_SCHEMA", "default"))
        table   = st.secrets.get("QUESTIONS_TABLE", os.getenv("QUESTIONS_TABLE", "questions"))

        full_table = f"`{catalog}`.`{schema}`.`{table}`" if catalog else f"`{schema}`.`{table}`"

        query = f"""
            SELECT
                QuestionID,
                domain,
                QuestionText
            FROM {full_table}
            ORDER BY domain, QuestionID
        """
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]

        conn.close()
        return pd.DataFrame(rows, columns=cols)

    except Exception as e:
        # Fallback to sample data so the app still loads during development
        st.warning(f"⚠️ Could not connect to Databricks: {e}. Using sample data.")
        return _sample_questions()


def _sample_questions() -> pd.DataFrame:
    """Bundled sample questions for offline / development mode."""
    data = [
        # Identity & Access Management
        (1,  "Identity & Access Management", "Do you enforce Multi-Factor Authentication (MFA) for all privileged accounts?"),
        (2,  "Identity & Access Management", "Is role-based access control (RBAC) implemented across all systems?"),
        (3,  "Identity & Access Management", "Are access reviews conducted on a quarterly basis?"),
        (4,  "Identity & Access Management", "Do you have a formal offboarding process that revokes access within 24 hours?"),
        (5,  "Identity & Access Management", "Is Privileged Access Management (PAM) solution in place?"),
        # Network Security
        (6,  "Network Security", "Are network segments isolated using VLANs or micro-segmentation?"),
        (7,  "Network Security", "Is a next-generation firewall deployed at all ingress/egress points?"),
        (8,  "Network Security", "Are intrusion detection/prevention systems (IDS/IPS) actively monitored?"),
        (9,  "Network Security", "Is network traffic encrypted in transit using TLS 1.2 or higher?"),
        (10, "Network Security", "Do you perform regular penetration testing on network infrastructure?"),
        # Data Protection
        (11, "Data Protection", "Is data classified by sensitivity level across all repositories?"),
        (12, "Data Protection", "Are encryption keys managed using a dedicated key management service?"),
        (13, "Data Protection", "Is data-at-rest encryption enabled on all storage systems?"),
        (14, "Data Protection", "Do you have a formal data retention and disposal policy?"),
        (15, "Data Protection", "Is data loss prevention (DLP) tooling deployed?"),
        # Incident Response
        (16, "Incident Response", "Is there a documented and tested Incident Response Plan (IRP)?"),
        (17, "Incident Response", "Are security incidents tracked in a dedicated ticketing system?"),
        (18, "Incident Response", "Is a Security Operations Center (SOC) or MSSP engaged?"),
        (19, "Incident Response", "Are post-incident reviews conducted within 72 hours of resolution?"),
        (20, "Incident Response", "Is a communication plan defined for regulatory notifications?"),
        # Compliance & Governance
        (21, "Compliance & Governance", "Is an information security policy reviewed and approved annually?"),
        (22, "Compliance & Governance", "Are employees required to complete security awareness training?"),
        (23, "Compliance & Governance", "Do you maintain an up-to-date asset inventory?"),
        (24, "Compliance & Governance", "Are third-party vendors assessed for security risk annually?"),
        (25, "Compliance & Governance", "Is a risk register maintained and reviewed by leadership?"),
        # Cloud Security
        (26, "Cloud Security", "Are cloud resource configurations audited against CIS benchmarks?"),
        (27, "Cloud Security", "Is cloud access governed through a Cloud Access Security Broker (CASB)?"),
        (28, "Cloud Security", "Are cloud storage buckets/containers protected from public access?"),
        (29, "Cloud Security", "Is infrastructure-as-code (IaC) scanned for misconfigurations?"),
        (30, "Cloud Security", "Are cloud workloads protected by endpoint detection and response (EDR)?"),
    ]
    return pd.DataFrame(data, columns=["question_id", "domain", "question_text"])
