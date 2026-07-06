"""
app.py
------
Streamlit web frontend for the AI Tutor App.
Run with:  streamlit run app.py

This file only handles UI/interaction. All AI logic lives in tutor_logic.py
(separation of concerns / modular code, as required by the lab guide).
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import tutor_logic as tl

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Tutor", page_icon="🎓", layout="wide")

st.title("🎓 AI Tutor — Personalized Study Recommendations")
st.caption("Rule-based scoring + KMeans clustering to find which subject needs your attention most.")

COLOR_MAP = {"Weak": "#E74C3C", "Medium": "#F5B041", "Strong": "#58D68D"}

# ---------------------------------------------------------------------------
# SIDEBAR — INPUT METHOD
# ---------------------------------------------------------------------------
st.sidebar.header("1. Provide Your Data")

input_method = st.sidebar.radio(
    "How do you want to enter your marksheet?",
    ["Use Demo Data", "Upload CSV", "Enter Manually"],
)

df_input = None

if input_method == "Use Demo Data":
    df_input = tl.load_data("data/student_data.csv")
    st.sidebar.success("Demo data loaded (5 sample subjects).")

elif input_method == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader(
        "Upload your marksheet CSV",
        type=["csv"],
        help="Columns required: subject, quiz_score, hours_studied, attempts",
    )
    if uploaded_file is not None:
        try:
            df_input = pd.read_csv(uploaded_file)
            st.sidebar.success("File uploaded successfully.")
        except Exception as e:
            st.sidebar.error(f"Could not read file: {e}")

elif input_method == "Enter Manually":
    st.sidebar.write("Add your subjects below (edit the table in the main panel).")
    if "manual_df" not in st.session_state:
        st.session_state.manual_df = pd.DataFrame({
            "subject": ["Math", "Physics", "English"],
            "quiz_score": [50, 70, 85],
            "hours_studied": [2, 3, 1],
            "attempts": [3, 1, 1],
        })
    df_input = st.session_state.manual_df

# ---------------------------------------------------------------------------
# SIDEBAR — PARAMETERS
# ---------------------------------------------------------------------------
st.sidebar.header("2. Settings")
weak_threshold = st.sidebar.slider("Weak score threshold (%)", 0, 100, 60)
weak_fraction = st.sidebar.slider("Fraction of subjects considered 'weak' for evaluation", 0.1, 0.8, 0.4)

run_button = st.sidebar.button("🚀 Analyse My Subjects", type="primary")

# ---------------------------------------------------------------------------
# MAIN PANEL — EDITABLE TABLE (for manual entry mode)
# ---------------------------------------------------------------------------
st.subheader("📋 Your Marksheet")

if input_method == "Enter Manually":
    edited_df = st.data_editor(
        df_input,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "quiz_score": st.column_config.NumberColumn("Quiz Score (%)", min_value=0, max_value=100),
            "hours_studied": st.column_config.NumberColumn("Hours Studied", min_value=0.0),
            "attempts": st.column_config.NumberColumn("Attempts", min_value=1, step=1),
        },
    )
    st.session_state.manual_df = edited_df
    df_input = edited_df
elif df_input is not None:
    st.dataframe(df_input, use_container_width=True)
else:
    st.info("👈 Choose an input method from the sidebar to get started.")

# ---------------------------------------------------------------------------
# RUN PIPELINE
# ---------------------------------------------------------------------------
if run_button:
    if df_input is None or df_input.empty:
        st.error("⚠️ No data available. Please upload, load demo data, or enter subjects manually.")
    else:
        errors = tl.validate_data(df_input)
        if errors:
            st.error("⚠️ Please fix the following issues:")
            for e in errors:
                st.write(f"- {e}")
        else:
            with st.spinner("Analysing your subjects..."):
                result = tl.run_full_pipeline(df_input)

            df_ranked = result["df_ranked"]
            top = result["top_subject"]
            evaluation = result["evaluation"]

            st.success("Analysis complete!")

            # -----------------------------------------------------------------
            # RESULT PANEL
            # -----------------------------------------------------------------
            st.markdown("---")
            st.subheader("🎯 Recommendation")

            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Priority Subject", top["subject"])
                st.metric("Quiz Score", f"{top['quiz_score']:.0f}%")
                st.metric("Performance Level", top["performance_level"])
            with col2:
                st.info(result["explanation"])
                st.markdown("**Suggested Practice:**")
                for q in result["questions"]:
                    st.write(f"- {q}")

            # -----------------------------------------------------------------
            # VISUAL 1: Priority score bar chart
            # -----------------------------------------------------------------
            st.markdown("---")
            st.subheader("📊 Subject Priority Ranking")

            fig1 = px.bar(
                df_ranked, x="subject", y="priority_score",
                color="performance_level", color_discrete_map=COLOR_MAP,
                text="priority_score",
                labels={"priority_score": "Priority Score", "subject": "Subject"},
                title="Higher score = needs more attention",
            )
            fig1.update_traces(textposition="outside")
            st.plotly_chart(fig1, use_container_width=True)

            # -----------------------------------------------------------------
            # VISUAL 2: Quiz scores with threshold line
            # -----------------------------------------------------------------
            col3, col4 = st.columns(2)

            with col3:
                fig2 = px.bar(
                    df_ranked, x="subject", y="quiz_score",
                    color="performance_level", color_discrete_map=COLOR_MAP,
                    labels={"quiz_score": "Quiz Score (%)"},
                    title="Quiz Scores by Subject",
                )
                fig2.add_hline(y=weak_threshold, line_dash="dash", line_color="red",
                                annotation_text=f"Weak threshold ({weak_threshold}%)")
                fig2.update_yaxes(range=[0, 100])
                st.plotly_chart(fig2, use_container_width=True)

            # -----------------------------------------------------------------
            # VISUAL 3: Performance level pie chart
            # -----------------------------------------------------------------
            with col4:
                level_counts = df_ranked["performance_level"].value_counts().reset_index()
                level_counts.columns = ["performance_level", "count"]
                fig3 = px.pie(
                    level_counts, names="performance_level", values="count",
                    color="performance_level", color_discrete_map=COLOR_MAP,
                    title="Distribution of Performance Levels",
                )
                st.plotly_chart(fig3, use_container_width=True)

            # -----------------------------------------------------------------
            # FULL RANKED TABLE
            # -----------------------------------------------------------------
            st.markdown("---")
            st.subheader("📄 Full Ranked Table")
            display_df = df_ranked[[
                "subject", "quiz_score", "hours_studied", "attempts",
                "priority_score", "performance_level"
            ]]
            st.dataframe(
                display_df.style.apply(
                    lambda row: [f"background-color: {COLOR_MAP[row['performance_level']]}33"] * len(row),
                    axis=1,
                ),
                use_container_width=True,
            )

            # -----------------------------------------------------------------
            # EVALUATION PANEL
            # -----------------------------------------------------------------
            st.markdown("---")
            st.subheader("✅ Evaluation — Rule-Based vs Machine Learning")

            ecol1, ecol2, ecol3 = st.columns(3)
            ecol1.metric("Rule-Based Flagged Weak", len(evaluation["rule_based_weak"]))
            ecol2.metric("KMeans Flagged Weak", len(evaluation["ml_weak"]))
            ecol3.metric("Agreement Rate", f"{evaluation['agreement_rate']}%")

            st.write("**Rule-based weak subjects:**", ", ".join(evaluation["rule_based_weak"]) or "None")
            st.write("**ML (KMeans) weak subjects:**", ", ".join(evaluation["ml_weak"]) or "None")
            st.write("**Subjects both methods agree on:**", ", ".join(evaluation["agreement"]) or "None")

            with st.expander("ℹ️ Why KMeans instead of a Decision Tree?"):
                st.write(
                    "Decision Trees are supervised models that need many pre-labeled "
                    "training examples. With only one student's small set of subjects, "
                    "there isn't enough data to properly train/test a supervised model. "
                    "KMeans is unsupervised — it finds natural groupings without needing "
                    "labeled data, making it suitable for small, single-student datasets."
                )

st.markdown("---")
st.caption("AI Tutor App — Lab Project | Rule-Based AI + KMeans Clustering | Built with Streamlit")
