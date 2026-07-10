import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import tutor_logic as tl

st.set_page_config(page_title="Office Hours — AI Tutor", page_icon="🎓", layout="wide")

# ----------------------------------------------------------------------------
# THEME
# ----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root{
    --bg:#F7F8FB;
    --card:#FFFFFF;
    --card-hover:#FBFBFE;
    --ink:#12131A;
    --ink-soft:#565C6B;
    --ink-faint:#9AA0AD;
    --border:#E7E9F0;
    --accent:#5B5BF6;
    --accent-soft:#EEEDFF;
    --accent-hover:#4747E0;
    --weak:#E1533F;
    --weak-bg:#FDECEA;
    --medium:#DB9A2A;
    --medium-bg:#FDF4E2;
    --strong:#22A66E;
    --strong-bg:#E6F7EF;
    --shadow:0 1px 2px rgba(18,19,26,0.04), 0 8px 24px -12px rgba(18,19,26,0.10);
}

html, body, [class*="css"]{
    font-family:'Plus Jakarta Sans', sans-serif;
}

.stApp{
    background:var(--bg);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{
    background:var(--card);
    border-right:1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3{
    font-weight:700;
    color:var(--ink);
    letter-spacing:-0.01em;
}
section[data-testid="stSidebar"] .stRadio label{
    font-family:'Plus Jakarta Sans', sans-serif;
    color:var(--ink-soft);
}

/* ---------- Typography ---------- */
h1{
    font-weight:800 !important;
    color:var(--ink) !important;
    letter-spacing:-0.02em;
}
h2, h3{
    font-weight:700 !important;
    color:var(--ink) !important;
    letter-spacing:-0.01em;
}
p, li, span, label{
    color:var(--ink-soft);
}
[data-testid="stCaptionContainer"]{
    color:var(--ink-faint) !important;
    font-size:14px !important;
}

hr{
    border-color:var(--border) !important;
    margin:1.75rem 0 !important;
}

/* ---------- Pill header ---------- */
.pill{
    display:inline-flex;
    align-items:center;
    gap:6px;
    background:var(--accent-soft);
    color:var(--accent);
    font-size:12px;
    font-weight:700;
    letter-spacing:0.04em;
    text-transform:uppercase;
    padding:5px 12px;
    border-radius:999px;
    margin-bottom:10px;
}

/* ---------- Metric cards ---------- */
[data-testid="stMetric"]{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:14px;
    padding:16px 20px;
    box-shadow:var(--shadow);
}
[data-testid="stMetricLabel"]{
    color:var(--ink-faint) !important;
    font-size:12px !important;
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:0.04em;
}
[data-testid="stMetricValue"]{
    font-weight:800 !important;
    color:var(--ink) !important;
}

/* ---------- Buttons ---------- */
.stButton button,
.stButton button:focus,
.stButton button:visited,
.stButton button p{
    font-family:'Plus Jakarta Sans', sans-serif !important;
    font-weight:700 !important;
    border-radius:10px !important;
    border:none !important;
    background:var(--accent) !important;
    color:#FFFFFF !important;
    padding:0.6rem 1rem !important;
    box-shadow:0 4px 14px -6px rgba(91,91,246,0.55);
    transition:all 0.15s ease;
}
.stButton button:hover,
.stButton button:hover p{
    background:var(--accent-hover) !important;
    color:#FFFFFF !important;
    transform:translateY(-1px);
}
.stButton button:active,
.stButton button:active p{
    transform:translateY(0);
}

[data-testid="stAlert"]{
    border-radius:12px;
    border:1px solid var(--border);
    font-family:'Plus Jakarta Sans', sans-serif;
}

[data-testid="stDataFrame"]{
    border:1px solid var(--border);
    border-radius:14px;
    overflow:hidden;
    box-shadow:var(--shadow);
}

.stSlider label{
    color:var(--ink-soft) !important;
    font-size:13px;
    font-weight:600;
}

[data-testid="stExpander"]{
    border:1px solid var(--border);
    border-radius:14px;
    background:var(--card);
    box-shadow:var(--shadow);
}

div[data-testid="stTabs"] button[data-baseweb="tab"]{
    font-weight:600;
    color:var(--ink-faint);
}
div[data-testid="stTabs"] button[aria-selected="true"]{
    color:var(--accent);
}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"]{
    background-color:var(--accent);
}

/* ---------- Generic card wrapper ---------- */
.card{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    padding:22px 26px;
    box-shadow:var(--shadow);
    margin-bottom:14px;
}

/* ---------- Verdict hero ---------- */
.verdict-box{
    background:linear-gradient(135deg, #17182B 0%, #23244A 100%);
    color:#F4F4FA;
    padding:32px 36px;
    border-radius:18px;
    margin-bottom:8px;
    box-shadow:0 20px 40px -20px rgba(23,24,43,0.55);
}
.verdict-kicker{
    font-size:11px;
    font-weight:700;
    letter-spacing:0.08em;
    text-transform:uppercase;
    color:#A9A6F6;
    margin-bottom:12px;
}
.verdict-title{
    font-weight:700;
    font-size:27px;
    line-height:1.35;
    letter-spacing:-0.01em;
    margin-bottom:14px;
}
.verdict-title em{
    font-style:normal;
    color:#B9B6FF;
}
.verdict-body{
    font-size:14.5px;
    line-height:1.65;
    color:#D2D2E2;
    max-width:640px;
}

/* ---------- Practice list ---------- */
.practice-row{
    display:flex;
    gap:14px;
    align-items:flex-start;
    padding:12px 0;
    border-bottom:1px solid var(--border);
    font-size:14.5px;
    color:var(--ink-soft);
    line-height:1.55;
}
.practice-row:last-child{ border-bottom:none; }
.practice-num{
    display:flex;
    align-items:center;
    justify-content:center;
    min-width:24px;
    height:24px;
    border-radius:7px;
    background:var(--accent-soft);
    color:var(--accent);
    font-size:12.5px;
    font-weight:800;
    flex-shrink:0;
}

.method-note{
    font-size:13.5px;
    color:var(--ink-soft);
    line-height:1.65;
}

/* ---------- Level badges ---------- */
.badge{
    display:inline-block;
    padding:3px 10px;
    border-radius:999px;
    font-size:12px;
    font-weight:700;
}
.badge-weak{ background:var(--weak-bg); color:var(--weak); }
.badge-medium{ background:var(--medium-bg); color:var(--medium); }
.badge-strong{ background:var(--strong-bg); color:var(--strong); }
</style>
""", unsafe_allow_html=True)

COLOR_MAP = {"Weak": "#E1533F", "Medium": "#DB9A2A", "Strong": "#22A66E"}
BADGE_CLASS = {"Weak": "badge-weak", "Medium": "badge-medium", "Strong": "badge-strong"}
PLOTLY_TEMPLATE = dict(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#12131A"),
    margin=dict(t=48, l=10, r=10, b=10),
)

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown('<div class="pill">🎓 Office Hours</div>', unsafe_allow_html=True)
st.title("Your AI Study Mentor")
st.caption("Rule-based scoring + K-means clustering — tells you which subject needs your attention most, and why.")

# ----------------------------------------------------------------------------
# SIDEBAR — data input
# ----------------------------------------------------------------------------
st.sidebar.markdown("### 📋 Your marksheet")

input_method = st.sidebar.radio(
    "How do you want to enter your subjects?",
    ["Use Demo Data", "Upload CSV", "Enter Manually"],
    label_visibility="collapsed",
)

df_input = None

if input_method == "Use Demo Data":
    df_input = tl.load_data("data/student_data.csv")
    st.sidebar.success("✓ Demo data loaded — 5 sample subjects.")

elif input_method == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader(
        "Upload your marksheet CSV",
        type=["csv"],
        help="Columns required: subject, quiz_score, hours_studied, attempts",
    )
    if uploaded_file is not None:
        try:
            df_input = pd.read_csv(uploaded_file)
            st.sidebar.success("✓ File uploaded successfully.")
        except Exception as e:
            st.sidebar.error(f"Could not read file: {e}")

elif input_method == "Enter Manually":
    st.sidebar.caption("Add your subjects in the table on the right.")
    if "manual_df" not in st.session_state:
        st.session_state.manual_df = pd.DataFrame({
            "subject": ["Math", "Physics", "English"],
            "quiz_score": [50, 70, 85],
            "hours_studied": [2, 3, 1],
            "attempts": [3, 1, 1],
        })
    df_input = st.session_state.manual_df

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Settings")
weak_threshold = st.sidebar.slider(
    "Where should \"weak\" start?", 0, 100, 60,
    help="Scores below this line are treated as struggling.",
)
weak_fraction = st.sidebar.slider(
    "Fraction flagged weak (rule-based)", 0.1, 0.8, 0.4,
    help="Used only for the evaluation comparison below.",
)

st.sidebar.markdown("---")
run_button = st.sidebar.button("✨ Ask for my recommendation", type="primary", use_container_width=True)

# ----------------------------------------------------------------------------
# MARKSHEET
# ----------------------------------------------------------------------------
st.subheader("Your marksheet")

with st.container():
    if input_method == "Enter Manually":
        edited_df = st.data_editor(
            df_input,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "subject": st.column_config.TextColumn("Subject"),
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
        st.info("👈 Choose an input method from the sidebar to get started.")

# ----------------------------------------------------------------------------
# RESULTS
# ----------------------------------------------------------------------------
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

            # ---- Verdict hero ----
            st.markdown(f"""
            <div class="verdict-box">
                <div class="verdict-kicker">My read on things</div>
                <div class="verdict-title">You should put your next session into <em>{top['subject']}</em>.</div>
                <div class="verdict-body">{result['explanation']}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Score", f"{top['quiz_score']:.0f}%")
            col2.metric("Attempts", int(top["attempts"]))
            col3.metric("Hours studied", f"{top['hours_studied']:.1f}h")
            col4.metric("Priority", f"{top['priority_score']}")

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Tabbed detail views ----
            tab_start, tab_rank, tab_charts, tab_confidence = st.tabs(
                ["📍 Where to start", "📊 Everything, ranked", "📈 The shape of it", "🔍 How sure am I"]
            )

            with tab_start:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                practice_html = "".join(
                    f'<div class="practice-row"><span class="practice-num">{i+1}</span><span>{q}</span></div>'
                    for i, q in enumerate(result["questions"])
                )
                st.markdown(practice_html, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with tab_rank:
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
                        lambda row: [f"background-color: {COLOR_MAP[row['Level']]}18"] * len(row),
                        axis=1,
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

            with tab_charts:
                chart_col1, chart_col2 = st.columns([1.3, 1])

                with chart_col1:
                    fig1 = px.bar(
                        df_ranked, x="subject", y="priority_score",
                        color="performance_level", color_discrete_map=COLOR_MAP,
                        text="priority_score",
                        labels={"priority_score": "Priority score", "subject": ""},
                    )
                    fig1.update_traces(textposition="outside", marker_line_width=0)
                    fig1.update_layout(**PLOTLY_TEMPLATE, showlegend=True, legend_title_text="",
                                        title=dict(text="Priority ranking", font=dict(size=16, weight="bold")))
                    st.plotly_chart(fig1, use_container_width=True)

                with chart_col2:
                    level_counts = df_ranked["performance_level"].value_counts().reset_index()
                    level_counts.columns = ["performance_level", "count"]
                    fig3 = px.pie(
                        level_counts, names="performance_level", values="count",
                        color="performance_level", color_discrete_map=COLOR_MAP,
                        hole=0.55,
                    )
                    fig3.update_traces(marker_line_width=0)
                    fig3.update_layout(**PLOTLY_TEMPLATE, showlegend=True,
                                        title=dict(text="Distribution", font=dict(size=16, weight="bold")))
                    st.plotly_chart(fig3, use_container_width=True)

                fig2 = px.bar(
                    df_ranked, x="subject", y="quiz_score",
                    color="performance_level", color_discrete_map=COLOR_MAP,
                    labels={"quiz_score": "Quiz score (%)", "subject": ""},
                )
                fig2.add_hline(y=weak_threshold, line_dash="dash", line_color="#E1533F",
                                annotation_text=f"weak threshold ({weak_threshold}%)")
                fig2.update_traces(marker_line_width=0)
                fig2.update_yaxes(range=[0, 100])
                fig2.update_layout(**PLOTLY_TEMPLATE, showlegend=True, legend_title_text="",
                                    title=dict(text="Quiz scores by subject", font=dict(size=16, weight="bold")))
                st.plotly_chart(fig2, use_container_width=True)

            with tab_confidence:
                ecol1, ecol2, ecol3 = st.columns(3)
                ecol1.metric("Flagged by the rule", len(evaluation["rule_based_weak"]))
                ecol2.metric("Flagged by clustering", len(evaluation["ml_weak"]))
                ecol3.metric("Agreement", f"{evaluation['agreement_rate']}%")

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write("**The rule says weak:**", ", ".join(evaluation["rule_based_weak"]) or "none")
                st.write("**Clustering says weak:**", ", ".join(evaluation["ml_weak"]) or "none")
                st.write("**Both agree on:**", ", ".join(evaluation["agreement"]) or "none")
                st.markdown('</div>', unsafe_allow_html=True)

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
