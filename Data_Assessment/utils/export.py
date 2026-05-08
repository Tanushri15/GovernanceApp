"""CSV export helpers."""
import io
import csv
import pandas as pd
from datetime import datetime


def generate_csv_bytes(user: dict, questions_df: pd.DataFrame) -> bytes:
    """
    Generate a CSV file for a user's answers.

    Columns:
        Domain | Question ID | Question | Answer | Saved At
    """
    answers = user.get("answers", {})

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "Domain",
        "Question ID",
        "Question",
        "Answer",
        "Saved At",
    ])

    for _, row in questions_df.iterrows():
        domain = row["domain"]
        qid    = str(row["QuestionID"])
        qtext  = row["QuestionText"]

        domain_data = answers.get(domain, {})
        responses   = domain_data.get("responses", {})
        saved_at    = domain_data.get("saved_at", "")

        answer = responses.get(qid, "Not Answered")
        writer.writerow([domain, qid, qtext, answer, saved_at])

    return output.getvalue().encode("utf-8")


def get_export_filename(user: dict) -> str:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M")
    company = user.get("company", "company").replace(" ", "_")
    name    = user.get("name", "user").replace(" ", "_")
    return f"{company}_{name}_assessment_{ts}.csv"
