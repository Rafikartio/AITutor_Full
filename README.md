# 🎓 AI Tutor App — "Mentor"

A personalized study recommendation system. It analyses **one student's own
marksheet** (quiz scores, hours studied, attempts) and tells them which
subject needs the most attention next — with charts and a plain-language
explanation, in the voice of an AI mentor.

This project ships **two versions of the same app**:

| Version | Location | Best for |
|---|---|---|
| **Web app (polished UI)** | `web/index.html` | Presentation/demo — open directly in any browser, no install needed |
| **Python/Streamlit app** | `app.py` + `tutor_logic.py` | Showing your Python/ML code for grading — real scikit-learn KMeans |

Both implement the exact same AI logic (rule-based priority scoring +
KMeans-style clustering into Weak/Medium/Strong) — the web version reimplements
KMeans in plain JavaScript so it runs with zero setup; the Python version uses
`scikit-learn` directly for your source-code submission.

---

## Problem

Students often don't know which of their own subjects deserves more study
time. This app answers that question using their own performance data —
no external dataset required.

## Method / AI Used

1. **Rule-based scoring** — a weighted formula turns score, attempts, and
   hours studied into a single "priority score" per subject.
2. **KMeans clustering (Machine Learning)** — groups the student's subjects
   into Weak / Medium / Strong based on the same three features.
   KMeans (unsupervised) was chosen instead of a Decision Tree because a
   single student's handful of subjects isn't enough labeled data to train
   a supervised model properly.
3. The two methods are compared in an **evaluation panel** (agreement rate).

## Results

The app outputs: a ranked table, 3 charts (priority bar chart, score bar
chart with threshold line, performance-level pie chart), a plain-language
recommendation, and an evaluation comparing rule-based vs ML flags.

---

## 🗂️ Project Structure

```
AITutor_Full/
├── web/
│   └── index.html            # Standalone polished web app (HTML+CSS+JS, no install)
├── app.py                    # Streamlit frontend (Python UI)
├── tutor_logic.py             # All AI logic (rules, KMeans ML, explanations, evaluation)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── data/
│   └── student_data.csv       # Sample demo dataset
└── screenshots/                # Put your UI screenshots here for submission
```

## 🛠️ Tools Used

- **Python 3.10+**
- **Streamlit** — web UI framework
- **pandas** — data handling
- **scikit-learn** — KMeans clustering
- **Plotly** — interactive charts

## ▶️ Option A: Run the Web App (fastest, no install)

1. Go into the `web/` folder
2. Double-click `index.html` — it opens directly in your browser
3. Enter your subjects (or click "Try demo data"), click **"Ask Mentor to review my subjects"**
4. Done — no Python, no terminal, no install needed for this version

This is the best version to **screen-record or screenshot for your submission**
and to demo live in your viva — it looks and feels like a real product.

## ▶️ Option B: Run the Python/Streamlit App (for source-code grading)

1. **Install Python 3.10+** if you don't have it: https://python.org

2. **Open the project folder in VS Code**
   - File → Open Folder → select `AITutor_Project`

3. **Open a terminal in VS Code** (Terminal → New Terminal)

4. **(Recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the app:**
   ```bash
   streamlit run app.py
   ```

7. Your browser will open automatically at `http://localhost:8501`.
   If not, copy that URL into your browser manually.

## 🧪 How to Use the App

1. In the sidebar, choose an input method:
   - **Use Demo Data** — instantly loads the sample CSV
   - **Upload CSV** — upload your own marksheet (columns: `subject, quiz_score, hours_studied, attempts`)
   - **Enter Manually** — type your subjects directly into an editable table
2. Adjust the **weak score threshold** slider if desired.
3. Click **🚀 Analyse My Subjects**.
4. View your recommendation, charts, ranked table, and evaluation metrics.

## 📌 Notes

- No external/public dataset is used. The student's own small marksheet
  (5–10 subjects) is the complete dataset — this is a personal analysis
  tool, not a comparative prediction model across many students.
- To test different scenarios, just change the score/hours/attempts values
  and re-run the analysis.

## 🔮 Limitations & Future Improvements

- Currently analyses one student at a time (by design).
- Priority score weights are fixed; could be made user-adjustable.
- Could integrate with a real LMS (Moodle/Google Classroom API) to pull
  data automatically instead of manual entry/upload.
