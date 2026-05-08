# 🛡️ Assessment Portal — Streamlit App

A client-facing security assessment tool with an **Azure Portal–style UI**.
Users sign in, answer Yes/No questions per domain, track progress on a dashboard,
and download a per-client CSV of all responses.

---

## 📁 Project Structure

```
assessment_app/
├── app.py                        ← Entry point (run this)
├── requirements.txt
├── .gitignore
├── users.json                    ← Auto-created; stores user accounts & answers
│
├── .streamlit/
│   ├── config.toml               ← Theme & server settings
│   └── secrets.toml.template     ← Copy → secrets.toml and fill in credentials
│
├── pages/
│   ├── auth_page.py              ← Sign In / Sign Up page
│   ├── dashboard_page.py         ← Domain progress dashboard
│   └── questions_page.py         ← Yes/No question answering
│
└── utils/
    ├── styles.py                 ← Azure-style global CSS
    ├── db.py                     ← Databricks connection + question fetch
    ├── auth.py                   ← User registration, login, answer persistence
    └── export.py                 ← CSV generation
```

---

## ⚡ Quick Start (Step by Step)

### Step 1 — Prerequisites

Make sure you have **Python 3.10+** installed:

```bash
python --version   # should print 3.10 or higher
```

### Step 2 — Clone / Download the project

If you downloaded the zip, extract it. Then open a terminal in the project folder:

```bash
cd assessment_app
```

### Step 3 — Create a virtual environment

```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Configure Databricks credentials

1. Copy the secrets template:

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

2. Open `.streamlit/secrets.toml` and fill in your values:

```toml
DATABRICKS_HOST      = "adb-1234567890.12.azuredatabricks.net"
DATABRICKS_TOKEN     = "dapi..."
DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/abc123"
DATABRICKS_CATALOG   = "john_smith"     # your personal catalog name
DATABRICKS_SCHEMA    = "assessment"     # schema where questions table lives
QUESTIONS_TABLE      = "questions"      # table name
```

> **Where to find these values in Databricks:**
> - `DATABRICKS_HOST` → Your workspace URL (without `https://`)
> - `DATABRICKS_TOKEN` → User Settings → Developer → Access Tokens → Generate
> - `DATABRICKS_HTTP_PATH` → SQL Warehouses → your warehouse → Connection details

### Step 6 — Prepare the Questions Table in Databricks

Your questions table must have (at minimum) these columns:

| Column         | Type    | Description                     |
|----------------|---------|---------------------------------|
| `question_id`  | INT     | Unique question identifier      |
| `domain`       | STRING  | Domain / category name          |
| `question_text`| STRING  | The question shown to the user  |

Example DDL to create the table:

```sql
CREATE TABLE IF NOT EXISTS john_smith.assessment.questions (
    question_id   INT,
    domain        STRING,
    question_text STRING
);

-- Insert sample rows
INSERT INTO john_smith.assessment.questions VALUES
(1, 'Identity & Access Management', 'Do you enforce MFA for all privileged accounts?'),
(2, 'Network Security', 'Are network segments isolated using VLANs?');
```

### Step 7 — Run the app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 🔌 Offline / Development Mode

If Databricks is not configured or unreachable, the app automatically falls back
to **30 built-in sample questions** across 6 domains so you can test the full
flow immediately. A yellow warning banner will appear in the app.

---

## 👤 User Accounts & Data Persistence

- User accounts are stored in `users.json` (auto-created on first sign-up).
- Answers are persisted inside `users.json` per user, per domain.
- When a user signs back in, their previous answers are pre-filled.
- **For production** replace `users.json` with a proper database
  (PostgreSQL, Azure SQL, Databricks Delta table, etc.).

---

## 📄 CSV Export

Each user can download their responses at any time via the **Export CSV** button
on both the Dashboard and the Questions pages.

CSV columns:

```
Domain | Question ID | Question | Answer | Saved At
```

Filename format: `CompanyName_UserName_assessment_YYYYMMDD_HHMM.csv`

---

## 🎨 UI Design

The app follows **Microsoft Azure Portal design conventions**:
- Top navigation bar with logo, company name, and user avatar
- Breadcrumb navigation
- Stat tiles and progress bars on the dashboard
- Card-based layout with Azure blue (`#0078d4`) accents
- Clean form inputs matching Fluent UI styling

---

## 🔒 Security Notes

| Topic | Recommendation |
|-------|---------------|
| `secrets.toml` | Never commit to git (already in `.gitignore`) |
| Passwords | Stored as SHA-256 hashes (upgrade to bcrypt for production) |
| `users.json` | Move to a proper database for multi-server deployments |
| Databricks Token | Use a service principal token with minimal permissions in production |
| HTTPS | Use Streamlit Cloud or put an HTTPS reverse proxy in front for production |

---

## 🚀 Deploying to Streamlit Community Cloud

1. Push your project to a **private** GitHub repo
   (make sure `secrets.toml` is in `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app.
3. Select your repo and set **Main file path** to `app.py`.
4. Under **Advanced settings → Secrets**, paste the contents of your
   `secrets.toml`.
5. Click **Deploy**.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: databricks` | Run `pip install databricks-sql-connector` |
| `RuntimeError: Databricks credentials missing` | Check `.streamlit/secrets.toml` |
| App shows sample data | Databricks is unreachable; verify host, token, HTTP path |
| Questions table not found | Verify catalog/schema/table names in secrets.toml |
| `users.json` permission error | Ensure the directory is writable |

---

## 📞 Support

Contact your portal administrator or raise an issue in the project repository.
