import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import tutor_logic as tl

st.set_page_config(page_title="Office Hours — AI Tutor", page_icon="§", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');

:root{
    --paper:#F6F1E7;
    --card:#FFFDF8;
    --ink:#1C1B19;
    --ink-soft:#4A4742;
    --ink-faint:#8C877D;
    --rule:#DDD5C4;
    --brick:#8B4A3B;
    --weak:#A8452F;
    --weak-bg:#F6E3DD;
    --medium:#96692A;
    --medium-bg:#F4EAD6;
    --strong:#3E6B4E;
    --strong-bg:#E4EEE3;
}

html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
}

.stApp{
    background:var(--paper);
}

section[data-testid="stSidebar"]{
    background:var(--card);
    border-right:1px solid var(--rule);
}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3{
    font-family:'Fraunces', serif;
    font-weight:500;
    color:var(--ink);
}

h1{
    font-family:'Fraunces', serif !important;
    font-weight:500 !important;
    color:var(--ink) !important;
    letter-spacing:-0.01em;
}
h2, h3{
    font-family:'Fraunces', serif !important;
    font-weight:500 !important;
    color:var(--ink) !important;
}

[data-testid="stCaptionContainer"]{
    color:var(--ink-faint) !important;
    font-size:14px !important;
}

p, li, span, label{
    color:var(--ink-soft);
}

hr{
    border-color:var(--rule) !important;
    margin:2rem 0 !important;
}

[data-testid="stMetric"]{
    background:var(--card);
    border:1px solid var(--rule);
    border-radius:6px;
    padding:14px 18px;
}
[data-testid="stMetricLabel"]{
    color:var(--ink-faint) !important;
    font-size:12px !important;
    text-transform:uppercase;
    letter-spacing:0.04em;
}
[data-testid="stMetricValue"]{
    font-family:'Fraunces', serif !important;
    color:var(--ink) !important;
}

.stButton button{
    font-family:'Inter', sans-serif;
    font-weight:600;
    border-radius:3px;
    border:1.5px solid var(--brick);
    background:var(--brick);
    color:#FDF9F3;
    transition:all 0.15s ease;
}
.stButton button:hover{
    background:#6E3A2E;
    border-color:#6E3A2E;
    color:#FDF9F3;
}

[data-testid="stAlert"]{
    border-radius:6px;
    border:1px solid var(--rule);
    font-family:'Inter', sans-serif;
}

[data-testid="stDataFrame"]{
    border:1px solid var(--rule);
    border-radius:6px;
}

section[data-testid="stSidebar"] .stRadio label{
    font-family:'Inter', sans-serif;
    color:var(--ink-soft);
}

.stSlider label{
    color:var(--ink-soft) !important;
    font-size:13px;
}

[data-testid="stExpander"]{
    border:1px solid var(--rule);
    border-radius:6px;
    background:var(--card);
}

.verdict-box{
    background:var(--ink);
    color:#F4F1EA;
    padding:28px 32px;
    border-radius:8px;
    margin-bottom:8px;
}
.verdict-kicker{
    font-size:11px;
    font-weight:600;
    letter-spacing:0.08em;
    text-transform:uppercase;
    color:#C99A8A;
    margin-bottom:12px;
}
.verdict-title{
    font-family:'Fraunces', serif;
    font-weight:500;
    font-size:26px;
    line-height:1.35;
    margin-bottom:14px;
}
.verdict-title em{
    font-style:italic;
    color:#E8B8A4;
}
.verdict-body{
    font-size:14.5px;
    line-height:1.65;
    color:#D8D5CC;
    max-width:640px;
}

.practice-row{
    display:flex;
    gap:12px;
    padding:10px 0;
    border-bottom:1px solid var(--rule);
    font-size:14px;
    color:var(--ink-soft);
    line-height:1.5;
}
.practice-row:last-child{ border-bottom:none; }
.practice-num{
    font-family:'Fraunces', serif;
    font-style:italic;
    color:var(--brick);
    flex-shrink:0;
}

.method-note{
    font-size:13.5px;
    color:var(--ink-soft);
    line-height:1.6;
}
</style>
""", unsafe_allow_html=True)

COLOR_MAP = {"Weak": "#A8452F", "Medium": "#96692A", "Strong": "#3E6B4E"}
PLOTLY_TEMPLATE = dict(
    plot_bgcolor="#FFFDF8",
    paper_bgcolor="#FFFDF8",
    font=dict(family="Inter, sans-serif", color="#1C1B19"),
)

st.markdown('<div style="font-size:12px; font-weight:600; letter-spacing:0.08em; '
            'text-transform:uppercase; color:#8B4A3B; margin-bottom:6px;">office hours</div>',
            unsafe_allow_html=True)
st.title("Your AI Study Mentor")
st.caption("Rule-based scoring + K-means clustering — tells you which subject needs your attention most, and why.")

st.sidebar.header("Your marksheet")

input_method = st.sidebar.radio(
    "How do you want to enter your subjects?",
    ["Use Demo Data", "Upload CSV", "Enter Manually"],
)

df_input = None

if input_method == "Use Demo Data":
    df_input = tl.load_data("data/student_data.csv")
    st.sidebar.success("Demo data loaded — 5 sample subjects.")

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
    st.sidebar.write("Add your subjects in the table on the right.")
    if "manual_df" not in st.session_state:
        st.session_state.manual_df = pd.DataFrame({
            "subject": ["Math", "Physics", "English"],
            "quiz_score": [50, 70, 85],
            "hours_studied": [2, 3, 1],
            "attempts": [3, 1, 1],
        })
    df_input = st.session_state.manual_df

st.sidebar.header("Settings")
weak_threshold = st.sidebar.slider("Where should \"weak\" start?", 0, 100, 60, help="Scores below this line are treated as struggling.")
weak_fraction = st.sidebar.slider("Fraction flagged weak (rule-based)", 0.1, 0.8, 0.4, help="Used only for the evaluation comparison below.")

run_button = st.sidebar.button("Ask for my recommendation", type="primary", use_container_width=True)

st.subheader("Your marksheet")

if input_method == "Enter Manually":
    edited_df = st.data_editor(
        df_input,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "quiz_score": st.column_config.NumberColumn("Quiz score (%)", min_value=0, max_value=100),
            "hours_studied": st.column_config.NumberColumn("Hours studied", min_value=0.0),
            "attempts": st.column_config.NumberColumn("Attempts", min_value=1, step=1),
        },
    )
    st.session_state.manual_df = edited_df
    df_input = edited_df
elif df_input is not None:
    st.dataframe(df_input, use_container_width=True, hide_index=True)
else:
    st.info("Choose an input method from the sidebar to get started.")

if run_button:
    if df_input is None or df_input.empty:
        st.error("No data available. Please upload, load demo data, or enter subjects manually.")
    else:
        errors = tl.validate_data(df_input)
        if errors:
            st.error("Please fix the following before continuing:")
            for e in errors:
                st.write(f"- {e}")
        else:
            with st.spinner("Reading through your subjects..."):
                result = tl.run_full_pipeline(df_input)

            df_ranked = result["df_ranked"]
            top = result["top_subject"]
            evaluation = result["evaluation"]

            st.markdown("---")
            st.markdown(f"""
            <div class="verdict-box">
                <div class="verdict-kicker">my read on things</div>
                <div class="verdict-title">You should put your next session into <em>{top['subject']}</em>.</div>
                <div class="verdict-body">{result['explanation']}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Score", f"{top['quiz_score']:.0f}%")
            col2.metric("Attempts", int(top["attempts"]))
            col3.metric("Hours studied", f"{top['hours_studied']:.1f}h")
            col4.metric("Priority", f"{top['priority_score']}")

            st.markdown("---")
            st.subheader("Where to start")
            practice_html = "".join(
                f'<div class="practice-row"><span class="practice-num">{i+1}</span><span>{q}</span></div>'
                for i, q in enumerate(result["questions"])
            )
            st.markdown(practice_html, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("Everything, ranked")
            display_df = df_ranked[[
                "subject", "quiz_score", "hours_studied", "attempts",
                "priority_score", "performance_level"
            ]].rename(columns={
                "subject": "Subject",
                "quiz_score": "Score (%)",
                "hours_studied": "Hours studied",
                "attempts": "Attempts",
                "priority_score": "Priority",
                "performance_level": "Level",
            })
            st.dataframe(
                display_df.style.apply(
                    lambda row: [f"background-color: {COLOR_MAP[row['Level']]}22"] * len(row),
                    axis=1,
                ),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("---")
            st.subheader("The shape of it")

            chart_col1, chart_col2 = st.columns([1.3, 1])

            with chart_col1:
                fig1 = px.bar(
                    df_ranked, x="subject", y="priority_score",
                    color="performance_level", color_discrete_map=COLOR_MAP,
                    text="priority_score",
                    labels={"priority_score": "Priority score", "subject": ""},
                )
                fig1.update_traces(textposition="outside")
                fig1.update_layout(**PLOTLY_TEMPLATE, showlegend=True, legend_title_text="",
                                    title=dict(text="Priority ranking", font=dict(family="Fraunces, serif", size=16)))
                st.plotly_chart(fig1, use_container_width=True)

            with chart_col2:
                level_counts = df_ranked["performance_level"].value_counts().reset_index()
                level_counts.columns = ["performance_level", "count"]
                fig3 = px.pie(
                    level_counts, names="performance_level", values="count",
                    color="performance_level", color_discrete_map=COLOR_MAP,
                    hole=0.45,
                )
                fig3.update_layout(**PLOTLY_TEMPLATE, showlegend=True,
                                    title=dict(text="Distribution", font=dict(family="Fraunces, serif", size=16)))
                st.plotly_chart(fig3, use_container_width=True)

            fig2 = px.bar(
                df_ranked, x="subject", y="quiz_score",
                color="performance_level", color_discrete_map=COLOR_MAP,
                labels={"quiz_score": "Quiz score (%)", "subject": ""},
            )
            fig2.add_hline(y=weak_threshold, line_dash="dash", line_color="#A8452F",
                            annotation_text=f"weak threshold ({weak_threshold}%)")
            fig2.update_yaxes(range=[0, 100])
            fig2.update_layout(**PLOTLY_TEMPLATE, showlegend=True, legend_title_text="",
                                title=dict(text="Quiz scores by subject", font=dict(family="Fraunces, serif", size=16)))
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown("---")
            st.subheader("How sure am I")

            ecol1, ecol2, ecol3 = st.columns(3)
            ecol1.metric("Flagged by the rule", len(evaluation["rule_based_weak"]))
            ecol2.metric("Flagged by clustering", len(evaluation["ml_weak"]))
            ecol3.metric("Agreement", f"{evaluation['agreement_rate']}%")

            st.write("**The rule says weak:**", ", ".join(evaluation["rule_based_weak"]) or "none")
            st.write("**Clustering says weak:**", ", ".join(evaluation["ml_weak"]) or "none")
            st.write("**Both agree on:**", ", ".join(evaluation["agreement"]) or "none")

            with st.expander("Why clustering, not a decision tree?"):
                st.markdown("""
                <p class="method-note">
                A decision tree needs many past labeled examples to learn from — hundreds of
                prior students marked "weak" or "strong". With just one student's handful of
                subjects, there's nowhere near enough data for that. Clustering doesn't need
                labels at all — it just looks at score, hours, and attempts together and groups
                your subjects by how similar they are. That works fine even with only a few entries.
                </p>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Office Hours — rule-based scoring + K-means clustering · lab project")