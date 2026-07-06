"""
tutor_logic.py
--------------
All AI logic for the AI Tutor app: data validation, rule-based priority
scoring, KMeans clustering, recommendation generation, and evaluation.

Keeping this separate from app.py (the UI) follows the "modular code"
requirement — logic and interface are independent of each other.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


# ---------------------------------------------------------------------------
# 1. DATA LOADING
# ---------------------------------------------------------------------------
def load_data(path):
    """Load student marksheet data from a CSV file."""
    df = pd.read_csv(path)
    return df


def load_data_from_dict(data_dict):
    """Build a DataFrame directly from form input (dict of lists)."""
    return pd.DataFrame(data_dict)


# ---------------------------------------------------------------------------
# 2. VALIDATION
# ---------------------------------------------------------------------------
def validate_data(df):
    """Check the dataframe for missing/invalid values. Returns list of error strings."""
    errors = []

    required_cols = {"subject", "quiz_score", "hours_studied", "attempts"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        return errors  # can't validate further without columns

    if df.empty:
        errors.append("No data provided. Add at least one subject.")
        return errors

    if df["subject"].isnull().any():
        errors.append("Every row must have a subject name.")

    if df["quiz_score"].isnull().any() or not df["quiz_score"].between(0, 100).all():
        errors.append("quiz_score must be a number between 0 and 100.")

    if df["hours_studied"].isnull().any() or (df["hours_studied"] < 0).any():
        errors.append("hours_studied cannot be negative or empty.")

    if df["attempts"].isnull().any() or (df["attempts"] < 1).any():
        errors.append("attempts must be at least 1.")

    return errors


# ---------------------------------------------------------------------------
# 3. PREPROCESSING
# ---------------------------------------------------------------------------
def preprocess_data(df):
    """Clean and ensure correct types."""
    df = df.copy()
    df["subject"] = df["subject"].astype(str).str.strip()
    df["quiz_score"] = df["quiz_score"].astype(float)
    df["hours_studied"] = df["hours_studied"].astype(float)
    df["attempts"] = df["attempts"].astype(int)
    return df


# ---------------------------------------------------------------------------
# 4. RULE-BASED AI — PRIORITY SCORE
# ---------------------------------------------------------------------------
def calculate_priority_score(row, weight_score=0.5, weight_attempts=8, weight_hours=3):
    """
    priority_score = (100 - quiz_score) * weight_score
                    + attempts * weight_attempts
                    + hours_studied * weight_hours

    Higher priority score => subject needs more attention.
    """
    score_gap = (100 - row["quiz_score"]) * weight_score
    attempt_penalty = row["attempts"] * weight_attempts
    effort_penalty = row["hours_studied"] * weight_hours
    return round(score_gap + attempt_penalty + effort_penalty, 2)


def run_rule_based(df):
    """Apply rule-based priority scoring to the whole dataframe."""
    df = df.copy()
    df["priority_score"] = df.apply(calculate_priority_score, axis=1)
    return df.sort_values("priority_score", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 5. MACHINE LEARNING — KMEANS CLUSTERING
# ---------------------------------------------------------------------------
def run_kmeans_clustering(df, n_clusters=3, random_state=42):
    """
    Groups subjects into Weak / Medium / Strong clusters using KMeans,
    based on quiz_score, hours_studied, and attempts.

    KMeans (unsupervised) is used instead of a supervised model like a
    Decision Tree because we only have a handful of subjects for ONE
    student — not enough labeled examples to train/test a supervised
    classifier properly. KMeans finds natural groupings without needing
    labeled training data, which fits small, single-student datasets.
    """
    df = df.copy()
    n_clusters = max(1, min(n_clusters, len(df)))

    features = df[["quiz_score", "hours_studied", "attempts"]]
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    df["cluster"] = model.fit_predict(scaled)

    # Label clusters by average quiz_score: lowest score avg = "Weak"
    cluster_avg = df.groupby("cluster")["quiz_score"].mean().sort_values()
    label_names = ["Weak", "Medium", "Strong"][:n_clusters]
    cluster_to_label = {cid: label for label, cid in zip(label_names, cluster_avg.index)}

    df["performance_level"] = df["cluster"].map(cluster_to_label)
    return df


# ---------------------------------------------------------------------------
# 6. RECOMMENDATION + EXPLAINABILITY
# ---------------------------------------------------------------------------
def generate_explanation(top_row):
    """Generate a plain-language explanation for the top-priority subject."""
    explanation = (
        f"Recommended focus: {top_row['subject']}\n\n"
        f"Reason: Score is {top_row['quiz_score']:.0f}% "
        f"(classified as '{top_row['performance_level']}' performance). "
        f"You attempted this {int(top_row['attempts'])} time(s) and studied it for "
        f"{top_row['hours_studied']:.1f} hour(s). "
        f"This combination gives it the highest priority score of {top_row['priority_score']}, "
        f"meaning effort spent here isn't yet matching results compared to your other subjects."
    )
    return explanation


def get_recommendation(df_ranked):
    """Return the top-priority row (Series) as the recommended subject."""
    return df_ranked.iloc[0]


def generate_practice_questions(subject):
    """Return simple placeholder practice questions for the recommended subject."""
    templates = [
        f"Review the core definitions and key terms in {subject}.",
        f"Attempt 5 practice problems focused on {subject} fundamentals.",
        f"Re-watch or re-read the lesson material for {subject} and summarise it in your own words.",
    ]
    return templates


# ---------------------------------------------------------------------------
# 7. EVALUATION — COMPARE RULE-BASED VS ML
# ---------------------------------------------------------------------------
def evaluate_approaches(df_ranked, weak_fraction=0.4):
    """
    Compares which subjects each approach flags as 'weak' and computes
    an agreement rate between the two independent methods.
    """
    n_weak = max(1, int(len(df_ranked) * weak_fraction))
    rule_based_weak = set(df_ranked.nlargest(n_weak, "priority_score")["subject"])
    ml_weak = set(df_ranked[df_ranked["performance_level"] == "Weak"]["subject"])

    agreement = rule_based_weak.intersection(ml_weak)
    agreement_rate = len(agreement) / max(len(rule_based_weak), 1) * 100

    return {
        "rule_based_weak": rule_based_weak,
        "ml_weak": ml_weak,
        "agreement": agreement,
        "agreement_rate": round(agreement_rate, 1),
    }


# ---------------------------------------------------------------------------
# 8. FULL PIPELINE (convenience wrapper)
# ---------------------------------------------------------------------------
def run_full_pipeline(df):
    """Runs validation -> preprocessing -> rule-based -> clustering -> evaluation."""
    errors = validate_data(df)
    if errors:
        return {"errors": errors}

    df = preprocess_data(df)
    df_ranked = run_rule_based(df)
    df_ranked = run_kmeans_clustering(df_ranked)
    top = get_recommendation(df_ranked)
    explanation = generate_explanation(top)
    questions = generate_practice_questions(top["subject"])
    evaluation = evaluate_approaches(df_ranked)

    return {
        "errors": [],
        "df_ranked": df_ranked,
        "top_subject": top,
        "explanation": explanation,
        "questions": questions,
        "evaluation": evaluation,
    }
