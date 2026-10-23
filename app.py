
import streamlit as st
import csv
import io
import plotly.graph_objects as go

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="CareerAI | Career Recommendation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- THEME ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

with st.sidebar:
    st.title("⚙️ Settings")

    theme = st.radio(
        "Choose Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1
    )
    st.session_state.theme = theme

if theme == "Dark":
    bg = "#0E1117"
    panel = "#1B2230"
    text = "#F1F5F9"
    muted = "#B6C2D2"
    accent = "#8B5CF6"
    border = "#334155"
else:
    bg = "#F4F7FB"
    panel = "#FFFFFF"
    text = "#172033"
    muted = "#526078"
    accent = "#4F46E5"
    border = "#DCE3EE"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg};
        color: {text};
    }}
    [data-testid="stSidebar"] {{
        background-color: {panel};
    }}
    h1, h2, h3, p, label, span {{
        color: {text};
    }}
    .hero {{
        background: linear-gradient(120deg, {panel}, {accent}30);
        padding: 30px;
        border: 1px solid {border};
        border-radius: 18px;
        margin-bottom: 25px;
    }}
    .metric-card {{
        background-color: {panel};
        padding: 20px;
        border: 1px solid {border};
        border-radius: 14px;
        min-height: 115px;
    }}
    .metric-label {{
        color: {muted};
        font-size: 14px;
    }}
    .metric-value {{
        color: {accent};
        font-size: 27px;
        font-weight: bold;
        margin-top: 8px;
    }}
    .career-card {{
        background-color: {panel};
        padding: 20px;
        border: 1px solid {border};
        border-radius: 14px;
        margin-bottom: 12px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- CAREER DATA ----------------
CAREERS = {
    "AI Engineer": {
        "skills": [
            "Python", "Machine Learning", "Deep Learning",
            "Statistics", "SQL", "Problem Solving"
        ],
        "interests": ["Artificial Intelligence", "Building Applications"],
        "roadmap": [
            "Strengthen Python and data structures",
            "Learn NumPy, Pandas and statistics",
            "Study machine learning algorithms",
            "Learn neural networks and PyTorch",
            "Build and deploy an AI application"
        ]
    },
    "Data Scientist": {
        "skills": [
            "Python", "Statistics", "Machine Learning",
            "Data Analysis", "SQL", "Data Visualization"
        ],
        "interests": ["Data Analysis", "Research", "Artificial Intelligence"],
        "roadmap": [
            "Learn Python, NumPy and Pandas",
            "Master probability and statistics",
            "Practice SQL and data cleaning",
            "Learn machine learning and evaluation",
            "Build end-to-end data science projects"
        ]
    },
    "Software Developer": {
        "skills": [
            "Python", "Data Structures", "Problem Solving",
            "Git", "SQL", "Web Development"
        ],
        "interests": ["Building Applications", "Software Development"],
        "roadmap": [
            "Master Python and data structures",
            "Practice algorithms and problem solving",
            "Learn Git and GitHub",
            "Build applications using FastAPI or Django",
            "Create and deploy full-stack projects"
        ]
    },
    "Data Analyst": {
        "skills": [
            "SQL", "Python", "Data Analysis",
            "Statistics", "Data Visualization", "Excel"
        ],
        "interests": ["Data Analysis", "Business"],
        "roadmap": [
            "Learn Excel and SQL",
            "Practice data cleaning with Pandas",
            "Learn descriptive statistics",
            "Build dashboards and visualizations",
            "Complete real-world data analysis projects"
        ]
    },
    "Machine Learning Engineer": {
        "skills": [
            "Python", "Machine Learning", "Deep Learning",
            "SQL", "Git", "Statistics", "Problem Solving"
        ],
        "interests": ["Artificial Intelligence", "Building Applications"],
        "roadmap": [
            "Strengthen Python and software engineering",
            "Learn machine learning fundamentals",
            "Study model evaluation and feature engineering",
            "Learn model deployment and APIs",
            "Build and deploy machine learning projects"
        ]
    },
    "Web Developer": {
        "skills": [
            "Python", "Web Development", "SQL",
            "Git", "Problem Solving"
        ],
        "interests": ["Building Applications", "Software Development"],
        "roadmap": [
            "Learn HTML, CSS and JavaScript",
            "Learn frontend development",
            "Build APIs using Python",
            "Learn databases and authentication",
            "Deploy a complete web application"
        ]
    }
}

ALL_SKILLS = sorted({
    skill
    for career in CAREERS.values()
    for skill in career["skills"]
})

ALL_INTERESTS = sorted({
    interest
    for career in CAREERS.values()
    for interest in career["interests"]
})

# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="hero">
        <h1>🎯 CareerAI</h1>
        <p>
            Discover suitable career paths, identify skill gaps,
            and create your personalized learning roadmap.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- USER INPUT ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Your Profile")

name = st.sidebar.text_input("Your name", value="Student")

experience = st.sidebar.selectbox(
    "Experience level",
    ["Beginner", "Intermediate", "Advanced"]
)

skills = st.sidebar.multiselect(
    "Select your skills",
    ALL_SKILLS,
    default=["Python", "SQL", "Problem Solving"]
)

extra_skills_text = st.sidebar.text_input(
    "Other skills (comma-separated)",
    placeholder="e.g. Blender, Unity, Blockchain"
)

interests = st.sidebar.multiselect(
    "Select your interests",
    ALL_INTERESTS,
    default=["Artificial Intelligence"]
)

extra_interests_text = st.sidebar.text_input(
    "Other interests (comma-separated)",
    placeholder="e.g. Game development, Finance"
)

# ---------------- CUSTOM CAREER: OTHER ----------------
if "custom_careers" not in st.session_state:
    st.session_state.custom_careers = {}

if "show_custom_career_form" not in st.session_state:
    st.session_state.show_custom_career_form = False

if st.sidebar.button("➕ Other: Add your own career", use_container_width=True):
    st.session_state.show_custom_career_form = not st.session_state.show_custom_career_form

if st.session_state.show_custom_career_form:
    st.sidebar.markdown("#### Create a custom career")
    with st.sidebar.form("custom_career_form", clear_on_submit=True):
        custom_name = st.text_input(
            "Career title",
            placeholder="e.g. Game Developer"
        )
        custom_required_skills = st.text_area(
            "Required skills (comma-separated)",
            placeholder="Python, C++, Unity"
        )
        custom_career_interests = st.text_input(
            "Related interests (comma-separated)",
            placeholder="Gaming, Building Applications"
        )
        custom_roadmap_text = st.text_area(
            "Learning roadmap (one step per line)",
            placeholder="Learn the fundamentals\\nBuild a small project\\nCreate a portfolio"
        )
        save_custom_career = st.form_submit_button("Save custom career")

    if save_custom_career:
        clean_name = custom_name.strip()
        clean_skills = [item.strip() for item in custom_required_skills.split(",") if item.strip()]
        clean_interests = [item.strip() for item in custom_career_interests.split(",") if item.strip()]
        clean_roadmap = [item.strip() for item in custom_roadmap_text.splitlines() if item.strip()]

        if not clean_name:
            st.sidebar.error("Enter a career title.")
        elif not clean_skills:
            st.sidebar.error("Enter at least one required skill.")
        else:
            st.session_state.custom_careers[clean_name] = {
                "skills": clean_skills,
                "interests": clean_interests,
                "roadmap": clean_roadmap or [
                    f"Learn the fundamentals of {clean_name}",
                    f"Practice the required skills: {', '.join(clean_skills)}",
                    f"Build a portfolio project related to {clean_name}"
                ]
            }
            st.session_state.show_custom_career_form = False
            st.sidebar.success(f"Added {clean_name}!")
            st.rerun()

active_careers = {**CAREERS, **st.session_state.custom_careers}
user_skills = sorted(set(skills + [item.strip() for item in extra_skills_text.split(",") if item.strip()]))
user_interests = sorted(set(interests + [item.strip() for item in extra_interests_text.split(",") if item.strip()]))

analyze = st.sidebar.button(
    "🚀 Analyze My Career",
    use_container_width=True,
    type="primary"
)

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if analyze:
    st.session_state.analyzed = True

# ---------------- RECOMMENDATION LOGIC ----------------
def calculate_match(user_skills, user_interests, career):
    required_skills = set(career["skills"])
    desired_interests = set(career["interests"])

    skill_score = (
        len(set(user_skills) & required_skills)
        / len(required_skills)
        if required_skills else 0
    )

    interest_score = (
        len(set(user_interests) & desired_interests)
        / len(desired_interests)
        if desired_interests else 0
    )

    score = (0.8 * skill_score + 0.2 * interest_score) * 100

    return round(score), sorted(required_skills - set(user_skills))


if not st.session_state.analyzed:
    st.info(
        "👈 Select your skills and interests in the sidebar, "
        "then click **Analyze My Career** to view your results."
    )

    st.subheader("✨ What you will discover")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="metric-card"><h3>🎯 Career Matches</h3>'
            '<p>Compare six potential career paths.</p></div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="metric-card"><h3>📊 Skill Gaps</h3>'
            '<p>Identify skills to develop for each career.</p></div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="metric-card"><h3>🗺️ Learning Roadmap</h3>'
            '<p>Explore practical steps toward your goals.</p></div>',
            unsafe_allow_html=True
        )

else:
    if not user_skills and not user_interests:
        st.warning("Please select at least one skill or interest.")
        st.stop()

    results = []

    for career_name, career in active_careers.items():
        score, missing = calculate_match(user_skills, user_interests, career)

        results.append({
            "Career": career_name,
            "Match Score (%)": score,
            "Missing Skills": missing
        })

    results.sort(
        key=lambda item: item["Match Score (%)"],
        reverse=True
    )

    best = results[0]

    # ---------------- METRICS ----------------
    st.subheader(f"Welcome, {name}! 👋")
    st.caption(
        f"Profile level: {experience} · "
        f"Selected skills: {len(user_skills)} · "
        f"Interests: {len(interests)}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Top Career Match</div>'
            f'<div class="metric-value">{best["Career"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Skill Match Score</div>'
            f'<div class="metric-value">{best["Match Score (%)"]}%</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Skills to Develop</div>'
            f'<div class="metric-value">{len(best["Missing Skills"])}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ---------------- CHART ----------------
    st.subheader("📊 Career Match Comparison")

    careers = [item["Career"] for item in results]
    scores = [item["Match Score (%)"] for item in results]

    fig = go.Figure(
        data=[
            go.Bar(
                x=careers,
                y=scores,
                text=[f"{score}%" for score in scores],
                textposition="outside",
                marker=dict(
                    color=scores,
                    colorscale="Purples",
                    showscale=False
                )
            )
        ]
    )

    fig.update_layout(
        title="Your Career Suitability Scores",
        xaxis_title="Career",
        yaxis_title="Match Score (%)",
        template="plotly_dark" if theme == "Dark" else "plotly_white",
        yaxis=dict(range=[0, 110]),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    # ---------------- CAREER RESULTS ----------------
    st.subheader("🏆 Your Career Recommendations")

    for index, result in enumerate(results, start=1):
        with st.expander(
            f'{index}. {result["Career"]} — {result["Match Score (%)"]}% match',
            expanded=(index == 1)
        ):
            st.progress(result["Match Score (%)"] / 100)

            if result["Missing Skills"]:
                st.write("**Skills to develop:**")
                st.write(", ".join(result["Missing Skills"]))
            else:
                st.success("You selected all the skills listed for this career!")

    # ---------------- ROADMAP ----------------
    st.markdown("---")
    st.subheader("🗺️ Personalized Learning Roadmap")

    selected_career = st.selectbox(
        "Choose a career to explore",
        [item["Career"] for item in results]
    )

    selected_data = active_careers[selected_career]
    selected_result = next(
        item for item in results
        if item["Career"] == selected_career
    )

    st.write(f"### Your path to becoming a {selected_career}")

    for index, step in enumerate(selected_data["roadmap"], start=1):
        st.checkbox(
            f"Step {index}: {step}",
            key=f"{selected_career}_{index}"
        )

    st.write("**Skills required for this career:**")
    st.write(", ".join(selected_data["skills"]))

    if selected_result["Missing Skills"]:
        st.write("**Your skill gap:**")
        st.write(", ".join(selected_result["Missing Skills"]))

    # ---------------- DOWNLOAD REPORT ----------------
    st.subheader("📥 Download Your Career Report")

    report_rows = [
        {
            "Name": name,
            "Experience": experience,
            "Career": item["Career"],
            "Match Score (%)": item["Match Score (%)"],
            "Selected Skills": ", ".join(user_skills),
            "Interests": ", ".join(user_interests),
            "Missing Skills": ", ".join(item["Missing Skills"])
        }
        for item in results
    ]

    output = io.StringIO()

    fieldnames = list(report_rows[0].keys())

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(report_rows)

    st.download_button(
        "⬇️ Download Career Report (CSV)",
        data=output.getvalue().encode("utf-8"),
        file_name="career_recommendations.csv",
        mime="text/csv"
    )

    st.caption(
        "Match scores represent skill and interest overlap, "
        "not guaranteed employment outcomes."
    )
# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("CareerAI | Built with Python, Streamlit & Plotly")

