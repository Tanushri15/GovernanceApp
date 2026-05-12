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
           (1, "Strategy & Funding", "Is there an enterprise data strategy approved by leadership?"),
    (2, "Strategy & Funding", "Is governance tied to business priorities (revenue, risk, compliance, CX, AI)?"),
    (3, "Strategy & Funding", "Is there a documented business case for data governance?"),
    (4, "Strategy & Funding", "Is funding allocated and sustained for governance capabilities?"),
    (5, "Strategy & Funding", "Are governance objectives embedded in executive goals?"),
    (6, "Strategy & Funding", "Are value metrics defined (e.g., incident reduction, trust, compliance readiness)?"),
    (7, "Strategy & Funding", "Is the data strategy reviewed on a defined cadence?"),
    (8, "Strategy & Funding", "Are tradeoffs between delivery speed and data control explicitly managed?"),

    (9, "Governance Operating Model", "Are data owners assigned for critical domains/data products?"),
    (10, "Governance Operating Model", "Are data stewards formally identified and active?"),
    (11, "Governance Operating Model", "Are governance decision rights clearly defined?"),
    (12, "Governance Operating Model", "Is there a governance council with decision authority?"),
    (13, "Governance Operating Model", "Are roles understood across business and technology?"),
    (14, "Governance Operating Model", "Are domain and enterprise governance forums aligned?"),
    (15, "Governance Operating Model", "Are escalation paths defined for unresolved issues?"),
    (16, "Governance Operating Model", "Are governance accountabilities included in performance expectations?"),

    (17, "Policy, Standards & Control Environment", "Are governance policies formally documented and approved?"),
    (18, "Policy, Standards & Control Environment", "Are enterprise data standards defined (naming, definitions, retention, access, quality)?"),
    (19, "Policy, Standards & Control Environment", "Are policies translated into operational controls?"),
    (20, "Policy, Standards & Control Environment", "Are control owners identified for critical controls?"),
    (21, "Policy, Standards & Control Environment", "Are policy exceptions formally approved and tracked?"),
    (22, "Policy, Standards & Control Environment", "Are controls tested or reviewed on a recurring basis?"),
    (23, "Policy, Standards & Control Environment", "Are control deficiencies remediated through workflows?"),
    (24, "Policy, Standards & Control Environment", "Is there evidence that standards are applied in delivery processes?"),

    (25, "Data Quality Management", "Are enterprise data quality dimensions defined?"),
    (26, "Data Quality Management", "Are data quality rules documented for critical elements?"),
    (27, "Data Quality Management", "Are expectations aligned to business usage and risk?"),
    (28, "Data Quality Management", "Are automated DQ checks in place for critical datasets?"),
    (29, "Data Quality Management", "Are DQ metrics visible to owners and stakeholders?"),
    (30, "Data Quality Management", "Is there a formal issue management process?"),
    (31, "Data Quality Management", "Are issues prioritized based on business impact?"),
    (32, "Data Quality Management", "Are remediation SLAs defined and monitored?"),
    (33, "Data Quality Management", "Are root causes analyzed and addressed?"),
    (34, "Data Quality Management", "Are preventive controls introduced after recurring failures?"),
    (35, "Data Quality Management", "Are quality thresholds embedded in pipelines/products?"),
    (36, "Data Quality Management", "Are quality trends monitored over time?"),

    (37, "KPI Alignment & Trusted Reporting", "Are critical KPIs formally defined and approved?"),
    (38, "KPI Alignment & Trusted Reporting", "Is there one authoritative definition per KPI?"),
    (39, "KPI Alignment & Trusted Reporting", "Are KPI formulas documented and accessible?"),
    (40, "KPI Alignment & Trusted Reporting", "Are source systems for each KPI identified?"),
    (41, "KPI Alignment & Trusted Reporting", "Do KPI values reconcile across reports and systems?"),
    (42, "KPI Alignment & Trusted Reporting", "Are KPI discrepancies tracked and resolved?"),
    (43, "KPI Alignment & Trusted Reporting", "Is ownership assigned for each KPI?"),
    (44, "KPI Alignment & Trusted Reporting", "Is KPI lineage traceable from source to report?"),
    (45, "KPI Alignment & Trusted Reporting", "Are KPI changes governed through a formal process?"),
    (46, "KPI Alignment & Trusted Reporting", "Do executives trust KPIs for decision-making?"),
    (47, "KPI Alignment & Trusted Reporting", "Are KPI definitions linked to the business glossary?"),
    (48, "KPI Alignment & Trusted Reporting", "Are KPI SLAs defined (freshness/accuracy/latency)?"),

    (49, "Metadata, Catalog & Glossary", "Is there a centralized metadata catalog?"),
    (50, "Metadata, Catalog & Glossary", "Are critical datasets registered in the catalog?"),
    (51, "Metadata, Catalog & Glossary", "Is a business glossary defined?"),
    (52, "Metadata, Catalog & Glossary", "Are business terms linked to physical data assets?"),
    (53, "Metadata, Catalog & Glossary", "Are metadata standards defined and enforced?"),
    (54, "Metadata, Catalog & Glossary", "Is ownership metadata maintained for assets?"),
    (55, "Metadata, Catalog & Glossary", "Are authoritative sources recorded?"),
    (56, "Metadata, Catalog & Glossary", "Is metadata captured automatically where possible?"),
    (57, "Metadata, Catalog & Glossary", "Can business users easily discover and understand data?"),
    (58, "Metadata, Catalog & Glossary", "Are catalog records kept current via workflows?"),

    (59, "Lineage, Traceability & Impact", "Is lineage documented for critical assets?"),
    (60, "Lineage, Traceability & Impact", "Is lineage documented for reports and KPIs?"),
    (61, "Lineage, Traceability & Impact", "Is both technical and business lineage available?"),
    (62, "Lineage, Traceability & Impact", "Can users trace data end-to-end?"),
    (63, "Lineage, Traceability & Impact", "Are dependencies (upstream/downstream) visible?"),
    (64, "Lineage, Traceability & Impact", "Can impact analysis be performed before changes?"),
    (65, "Lineage, Traceability & Impact", "Is lineage updated automatically/semi-automatically?"),
    (66, "Lineage, Traceability & Impact", "Are lineage gaps treated as governance issues?"),
    (67, "Lineage, Traceability & Impact", "Is lineage used during incident response?"),
    (68, "Lineage, Traceability & Impact", "Is lineage available for sensitive/regulated data?"),

    (69, "Architecture, Modeling & Integration", "Is enterprise data architecture aligned to business architecture?"),
    (70, "Architecture, Modeling & Integration", "Are conceptual/logical data models defined for key domains?"),
    (71, "Architecture, Modeling & Integration", "Are data models governed during solution design?"),
    (72, "Architecture, Modeling & Integration", "Are integration patterns standardized?"),
    (73, "Architecture, Modeling & Integration", "Are interfaces/data exchanges documented?"),
    (74, "Architecture, Modeling & Integration", "Are canonical models or shared definitions used?"),
    (75, "Architecture, Modeling & Integration", "Are schema changes controlled and communicated?"),
    (76, "Architecture, Modeling & Integration", "Are interoperability standards defined?"),
    (77, "Architecture, Modeling & Integration", "Are architecture decisions aligned to governance standards?"),
    (78, "Architecture, Modeling & Integration", "Are designs reviewed for control compliance?"),

    (79, "Master & Reference Data", "Are critical master/reference domains identified?"),
    (80, "Master & Reference Data", "Are authoritative sources assigned for each domain?"),
    (81, "Master & Reference Data", "Are golden record policies defined?"),
    (82, "Master & Reference Data", "Are duplicate/survivorship rules established?"),
    (83, "Master & Reference Data", "Is reference data standardized across systems?"),
    (84, "Master & Reference Data", "Are hierarchies governed and maintained?"),
    (85, "Master & Reference Data", "Are changes governed via workflow and approval?"),
    (86, "Master & Reference Data", "Are domain owners accountable for master data?"),
    (87, "Master & Reference Data", "Are downstream systems aligned to master/reference models?"),
    (88, "Master & Reference Data", "Is poor master data recognized as a root cause of issues?"),

    (89, "Access, Security, Privacy & Sovereignty", "Is sensitive data formally classified?"),
    (90, "Access, Security, Privacy & Sovereignty", "Is classification automated where possible?"),
    (91, "Access, Security, Privacy & Sovereignty", "Are RBAC/ABAC controls implemented?"),
    (92, "Access, Security, Privacy & Sovereignty", "Are entitlements reviewed and recertified regularly?"),
    (93, "Access, Security, Privacy & Sovereignty", "Are access approvals traceable to owners?"),
    (94, "Access, Security, Privacy & Sovereignty", "Are usage purposes defined for sensitive data sharing?"),
    (95, "Access, Security, Privacy & Sovereignty", "Are privacy impact assessments triggered where required?"),
    (96, "Access, Security, Privacy & Sovereignty", "Are encryption/security controls applied based on classification?"),
    (97, "Access, Security, Privacy & Sovereignty", "Are audit logs maintained for access/use?"),
    (98, "Access, Security, Privacy & Sovereignty", "Are cross-border movement/sovereignty requirements controlled?"),
    (99, "Access, Security, Privacy & Sovereignty", "Are privacy obligations mapped to jurisdictions?"),
    (100, "Access, Security, Privacy & Sovereignty", "Are data owners accountable for access decisions?"),    (1, "Strategy & Funding", "Is there an enterprise data strategy approved by leadership?"),
    (2, "Strategy & Funding", "Is governance tied to business priorities (revenue, risk, compliance, CX, AI)?"),
    (3, "Strategy & Funding", "Is there a documented business case for data governance?"),
    (4, "Strategy & Funding", "Is funding allocated and sustained for governance capabilities?"),
    (5, "Strategy & Funding", "Are governance objectives embedded in executive goals?"),
    (6, "Strategy & Funding", "Are value metrics defined (e.g., incident reduction, trust, compliance readiness)?"),
    (7, "Strategy & Funding", "Is the data strategy reviewed on a defined cadence?"),
    (8, "Strategy & Funding", "Are tradeoffs between delivery speed and data control explicitly managed?"),

    (9, "Governance Operating Model", "Are data owners assigned for critical domains/data products?"),
    (10, "Governance Operating Model", "Are data stewards formally identified and active?"),
    (11, "Governance Operating Model", "Are governance decision rights clearly defined?"),
    (12, "Governance Operating Model", "Is there a governance council with decision authority?"),
    (13, "Governance Operating Model", "Are roles understood across business and technology?"),
    (14, "Governance Operating Model", "Are domain and enterprise governance forums aligned?"),
    (15, "Governance Operating Model", "Are escalation paths defined for unresolved issues?"),
    (16, "Governance Operating Model", "Are governance accountabilities included in performance expectations?"),

    (17, "Policy, Standards & Control Environment", "Are governance policies formally documented and approved?"),
    (18, "Policy, Standards & Control Environment", "Are enterprise data standards defined (naming, definitions, retention, access, quality)?"),
    (19, "Policy, Standards & Control Environment", "Are policies translated into operational controls?"),
    (20, "Policy, Standards & Control Environment", "Are control owners identified for critical controls?"),
    (21, "Policy, Standards & Control Environment", "Are policy exceptions formally approved and tracked?"),
    (22, "Policy, Standards & Control Environment", "Are controls tested or reviewed on a recurring basis?"),
    (23, "Policy, Standards & Control Environment", "Are control deficiencies remediated through workflows?"),
    (24, "Policy, Standards & Control Environment", "Is there evidence that standards are applied in delivery processes?"),

    (25, "Data Quality Management", "Are enterprise data quality dimensions defined?"),
    (26, "Data Quality Management", "Are data quality rules documented for critical elements?"),
    (27, "Data Quality Management", "Are expectations aligned to business usage and risk?"),
    (28, "Data Quality Management", "Are automated DQ checks in place for critical datasets?"),
    (29, "Data Quality Management", "Are DQ metrics visible to owners and stakeholders?"),
    (30, "Data Quality Management", "Is there a formal issue management process?"),
    (31, "Data Quality Management", "Are issues prioritized based on business impact?"),
    (32, "Data Quality Management", "Are remediation SLAs defined and monitored?"),
    (33, "Data Quality Management", "Are root causes analyzed and addressed?"),
    (34, "Data Quality Management", "Are preventive controls introduced after recurring failures?"),
    (35, "Data Quality Management", "Are quality thresholds embedded in pipelines/products?"),
    (36, "Data Quality Management", "Are quality trends monitored over time?"),

    (37, "KPI Alignment & Trusted Reporting", "Are critical KPIs formally defined and approved?"),
    (38, "KPI Alignment & Trusted Reporting", "Is there one authoritative definition per KPI?"),
    (39, "KPI Alignment & Trusted Reporting", "Are KPI formulas documented and accessible?"),
    (40, "KPI Alignment & Trusted Reporting", "Are source systems for each KPI identified?"),
    (41, "KPI Alignment & Trusted Reporting", "Do KPI values reconcile across reports and systems?"),
    (42, "KPI Alignment & Trusted Reporting", "Are KPI discrepancies tracked and resolved?"),
    (43, "KPI Alignment & Trusted Reporting", "Is ownership assigned for each KPI?"),
    (44, "KPI Alignment & Trusted Reporting", "Is KPI lineage traceable from source to report?"),
    (45, "KPI Alignment & Trusted Reporting", "Are KPI changes governed through a formal process?"),
    (46, "KPI Alignment & Trusted Reporting", "Do executives trust KPIs for decision-making?"),
    (47, "KPI Alignment & Trusted Reporting", "Are KPI definitions linked to the business glossary?"),
    (48, "KPI Alignment & Trusted Reporting", "Are KPI SLAs defined (freshness/accuracy/latency)?"),

    (49, "Metadata, Catalog & Glossary", "Is there a centralized metadata catalog?"),
    (50, "Metadata, Catalog & Glossary", "Are critical datasets registered in the catalog?"),
    (51, "Metadata, Catalog & Glossary", "Is a business glossary defined?"),
    (52, "Metadata, Catalog & Glossary", "Are business terms linked to physical data assets?"),
    (53, "Metadata, Catalog & Glossary", "Are metadata standards defined and enforced?"),
    (54, "Metadata, Catalog & Glossary", "Is ownership metadata maintained for assets?"),
    (55, "Metadata, Catalog & Glossary", "Are authoritative sources recorded?"),
    (56, "Metadata, Catalog & Glossary", "Is metadata captured automatically where possible?"),
    (57, "Metadata, Catalog & Glossary", "Can business users easily discover and understand data?"),
    (58, "Metadata, Catalog & Glossary", "Are catalog records kept current via workflows?"),

    (59, "Lineage, Traceability & Impact", "Is lineage documented for critical assets?"),
    (60, "Lineage, Traceability & Impact", "Is lineage documented for reports and KPIs?"),
    (61, "Lineage, Traceability & Impact", "Is both technical and business lineage available?"),
    (62, "Lineage, Traceability & Impact", "Can users trace data end-to-end?"),
    (63, "Lineage, Traceability & Impact", "Are dependencies (upstream/downstream) visible?"),
    (64, "Lineage, Traceability & Impact", "Can impact analysis be performed before changes?"),
    (65, "Lineage, Traceability & Impact", "Is lineage updated automatically/semi-automatically?"),
    (66, "Lineage, Traceability & Impact", "Are lineage gaps treated as governance issues?"),
    (67, "Lineage, Traceability & Impact", "Is lineage used during incident response?"),
    (68, "Lineage, Traceability & Impact", "Is lineage available for sensitive/regulated data?"),

    (69, "Architecture, Modeling & Integration", "Is enterprise data architecture aligned to business architecture?"),
    (70, "Architecture, Modeling & Integration", "Are conceptual/logical data models defined for key domains?"),
    (71, "Architecture, Modeling & Integration", "Are data models governed during solution design?"),
    (72, "Architecture, Modeling & Integration", "Are integration patterns standardized?"),
    (73, "Architecture, Modeling & Integration", "Are interfaces/data exchanges documented?"),
    (74, "Architecture, Modeling & Integration", "Are canonical models or shared definitions used?"),
    (75, "Architecture, Modeling & Integration", "Are schema changes controlled and communicated?"),
    (76, "Architecture, Modeling & Integration", "Are interoperability standards defined?"),
    (77, "Architecture, Modeling & Integration", "Are architecture decisions aligned to governance standards?"),
    (78, "Architecture, Modeling & Integration", "Are designs reviewed for control compliance?"),

    (79, "Master & Reference Data", "Are critical master/reference domains identified?"),
    (80, "Master & Reference Data", "Are authoritative sources assigned for each domain?"),
    (81, "Master & Reference Data", "Are golden record policies defined?"),
    (82, "Master & Reference Data", "Are duplicate/survivorship rules established?"),
    (83, "Master & Reference Data", "Is reference data standardized across systems?"),
    (84, "Master & Reference Data", "Are hierarchies governed and maintained?"),
    (85, "Master & Reference Data", "Are changes governed via workflow and approval?"),
    (86, "Master & Reference Data", "Are domain owners accountable for master data?"),
    (87, "Master & Reference Data", "Are downstream systems aligned to master/reference models?"),
    (88, "Master & Reference Data", "Is poor master data recognized as a root cause of issues?"),

    (89, "Access, Security, Privacy & Sovereignty", "Is sensitive data formally classified?"),
    (90, "Access, Security, Privacy & Sovereignty", "Is classification automated where possible?"),
    (91, "Access, Security, Privacy & Sovereignty", "Are RBAC/ABAC controls implemented?"),
    (92, "Access, Security, Privacy & Sovereignty", "Are entitlements reviewed and recertified regularly?"),
    (93, "Access, Security, Privacy & Sovereignty", "Are access approvals traceable to owners?"),
    (94, "Access, Security, Privacy & Sovereignty", "Are usage purposes defined for sensitive data sharing?"),
    (95, "Access, Security, Privacy & Sovereignty", "Are privacy impact assessments triggered where required?"),
    (96, "Access, Security, Privacy & Sovereignty", "Are encryption/security controls applied based on classification?"),
    (97, "Access, Security, Privacy & Sovereignty", "Are audit logs maintained for access/use?"),
    (98, "Access, Security, Privacy & Sovereignty", "Are cross-border movement/sovereignty requirements controlled?"),
    (99, "Access, Security, Privacy & Sovereignty", "Are privacy obligations mapped to jurisdictions?"),
    (100, "Access, Security, Privacy & Sovereignty", "Are data owners accountable for access decisions?"),
    ]
    return pd.DataFrame(data, columns=["QuestionID", "domain", "QuestionText"])
