"""
STEP 4: Streamlit Dashboard
Interactive web app to visualize the optimized maintenance schedule.

Features:
  - KPI metrics (jobs scheduled, critical count, avg priority)
  - Interactive Gantt chart (timeline of maintenance blocks)
  - Priority distribution chart
  - Per-zone breakdown
  - Job table with filters
  - "Re-run Scheduler" button
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import subprocess, os, sys

# ─────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="IR Maintenance Scheduler",
    page_icon="🛤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main { background: #0a0f1e; color: #e2e8f0; }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(99, 179, 237, 0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));
        border: 1px solid rgba(99,179,237,0.3);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }
    
    .metric-value {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #63b3ed, #4fd1c5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-critical {
        background: linear-gradient(135deg, #c53030, #9b2c2c);
        color: white; padding: 3px 10px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600;
    }
    .badge-high {
        background: linear-gradient(135deg, #c05621, #9c4221);
        color: white; padding: 3px 10px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600;
    }
    .badge-medium {
        background: linear-gradient(135deg, #b7791f, #975a16);
        color: white; padding: 3px 10px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600;
    }
    .badge-low {
        background: linear-gradient(135deg, #276749, #22543d);
        color: white; padding: 3px 10px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: rgba(30,41,59,0.6);
        border: 1px solid rgba(99,179,237,0.2);
        border-radius: 12px;
        padding: 16px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3182ce, #2b6cb0);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4299e1, #3182ce);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(66,153,225,0.4);
    }

    h1, h2, h3 { color: #e2e8f0; }
    .section-header {
        border-left: 4px solid #63b3ed;
        padding-left: 12px;
        margin: 20px 0 12px 0;
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────
URGENCY_COLORS = {
    "Critical": "#fc8181",
    "High":     "#f6ad55",
    "Medium":   "#f6e05e",
    "Low":      "#68d391",
}

@st.cache_data
def load_data():
    """Load all CSV files."""
    schedule = pd.read_csv("data/optimized_schedule.csv")
    jobs     = pd.read_csv("data/maintenance_jobs.csv")
    trains   = pd.read_csv("data/train_timetable.csv")
    sections = pd.read_csv("data/track_sections.csv")
    return schedule, jobs, trains, sections


def run_pipeline():
    """Run all 3 pipeline steps."""
    with st.spinner("Generating dataset..."):
        subprocess.run([sys.executable, "generate_dataset.py"], check=True)
    with st.spinner("Training ML model..."):
        subprocess.run([sys.executable, "train_model.py"], check=True)
    with st.spinner("Running scheduler..."):
        subprocess.run([sys.executable, "scheduler.py"], check=True)
    st.cache_data.clear()


# ─────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛤️ IR Maintenance AI")
    st.markdown("---")

    # Pipeline buttons
    if st.button("▶ Run Full Pipeline", use_container_width=True):
        run_pipeline()
        st.success("Pipeline complete!")
        st.rerun()

    st.markdown("---")
    st.markdown("### Filters")

    if os.path.exists("data/optimized_schedule.csv"):
        schedule, jobs, trains, sections = load_data()
        all_zones    = sorted(schedule["zone"].unique())
        sel_zones    = st.multiselect("Zone", all_zones, default=all_zones)
        all_urgency  = ["Critical", "High", "Medium", "Low"]
        sel_urgency  = st.multiselect("Urgency Level", all_urgency, default=all_urgency)
        max_day      = st.slider("Days window", 7, 30, 30)
    else:
        schedule = jobs = trains = sections = None

    st.markdown("---")
    st.markdown(
        "<small style='color:#718096'>Indian Railways<br>AI Maintenance Scheduler<br>SIH 2026 Prototype</small>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────
# Main Content
# ─────────────────────────────────────────
st.markdown("""
<h1 style='
    background: linear-gradient(135deg, #63b3ed, #4fd1c5, #68d391);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0;
'>🛤️ Indian Railways — AI Maintenance Scheduler</h1>
<p style='color:#94a3b8; margin-top:4px; font-size:0.95rem;'>
Smart Track Block Optimization using XGBoost + Google OR-Tools
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Check if data exists
if not os.path.exists("data/optimized_schedule.csv"):
    st.warning("⚠️ No schedule found. Click **'Run Full Pipeline'** in the sidebar to generate data.")
    st.stop()

# Apply filters
df = schedule.copy()
if sel_zones:
    df = df[df["zone"].isin(sel_zones)]
if sel_urgency:
    df = df[df["urgency"].isin(sel_urgency)]
df = df[df["scheduled_day"] <= max_day]

# ─────────────────────────────────────────
# KPI Row
# ─────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{len(df)}</div>
        <div class="metric-label">Jobs Scheduled</div>
    </div>""", unsafe_allow_html=True)

with k2:
    crit = (df["urgency"] == "Critical").sum()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value" style="background:linear-gradient(135deg,#fc8181,#e53e3e);-webkit-background-clip:text;-webkit-text-fill-color:transparent">{crit}</div>
        <div class="metric-label">Critical Jobs</div>
    </div>""", unsafe_allow_html=True)

with k3:
    avg_p = df["ml_priority_score"].mean()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{avg_p:.1f}</div>
        <div class="metric-label">Avg Priority Score</div>
    </div>""", unsafe_allow_html=True)

with k4:
    total_hrs = df["estimated_duration_hrs"].sum()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{total_hrs:.0f}h</div>
        <div class="metric-label">Total Block Time</div>
    </div>""", unsafe_allow_html=True)

with k5:
    zones_count = df["zone"].nunique()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{zones_count}</div>
        <div class="metric-label">Zones Covered</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Gantt Chart
# ─────────────────────────────────────────
st.markdown('<div class="section-header">📅 Maintenance Block Gantt Chart</div>', unsafe_allow_html=True)

gantt_df = df.copy()
gantt_df["Start"] = pd.to_datetime(gantt_df["scheduled_date"]) + pd.to_timedelta(gantt_df["block_start_hr"], unit="h")
gantt_df["Finish"] = pd.to_datetime(gantt_df["scheduled_date"]) + pd.to_timedelta(gantt_df["block_end_hr"], unit="h")
gantt_df["Label"]  = gantt_df["job_id"] + " | " + gantt_df["job_type"]

fig_gantt = px.timeline(
    gantt_df.head(40),   # show top 40 for readability
    x_start="Start",
    x_end="Finish",
    y="section_id",
    color="urgency",
    hover_name="Label",
    hover_data={
        "ml_priority_score": ":.1f",
        "zone": True,
        "estimated_duration_hrs": ":.1f",
        "Start": False,
        "Finish": False,
    },
    color_discrete_map=URGENCY_COLORS,
    title="",
    template="plotly_dark",
    height=480,
)
fig_gantt.update_layout(
    plot_bgcolor="#0d1b2a",
    paper_bgcolor="#0d1b2a",
    font_color="#e2e8f0",
    legend_title="Urgency",
    xaxis_title="Date / Time",
    yaxis_title="Track Section",
    margin=dict(l=10, r=10, t=10, b=10),
    showlegend=True,
)
fig_gantt.update_yaxes(categoryorder="array", categoryarray=gantt_df["section_id"].unique().tolist())
st.plotly_chart(fig_gantt, use_container_width=True)

# ─────────────────────────────────────────
# Charts Row
# ─────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="section-header">🚨 Urgency Distribution</div>', unsafe_allow_html=True)
    urgency_counts = df["urgency"].value_counts().reset_index()
    urgency_counts.columns = ["Urgency", "Count"]
    fig_pie = px.pie(
        urgency_counts,
        names="Urgency",
        values="Count",
        color="Urgency",
        color_discrete_map=URGENCY_COLORS,
        hole=0.55,
        template="plotly_dark",
    )
    fig_pie.update_layout(
        paper_bgcolor="#0d1b2a",
        plot_bgcolor="#0d1b2a",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        showlegend=True,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.markdown('<div class="section-header">📊 Priority Score Histogram</div>', unsafe_allow_html=True)
    fig_hist = px.histogram(
        df, x="ml_priority_score", nbins=20,
        color_discrete_sequence=["#63b3ed"],
        template="plotly_dark",
        labels={"ml_priority_score": "ML Priority Score"},
    )
    fig_hist.update_layout(
        paper_bgcolor="#0d1b2a",
        plot_bgcolor="#0d1b2a",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        showlegend=False,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with c3:
    st.markdown('<div class="section-header">🗺️ Jobs per Zone</div>', unsafe_allow_html=True)
    zone_df = df.groupby("zone").agg(
        jobs=("job_id", "count"),
        avg_priority=("ml_priority_score", "mean")
    ).reset_index().sort_values("jobs", ascending=True)
    fig_bar = px.bar(
        zone_df, x="jobs", y="zone",
        orientation="h",
        color="avg_priority",
        color_continuous_scale=["#276749", "#f6e05e", "#c53030"],
        template="plotly_dark",
        labels={"jobs": "Jobs", "zone": "", "avg_priority": "Avg Priority"},
    )
    fig_bar.update_layout(
        paper_bgcolor="#0d1b2a",
        plot_bgcolor="#0d1b2a",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────
# Jobs per Day timeline
# ─────────────────────────────────────────
st.markdown('<div class="section-header">📆 Jobs Scheduled per Day</div>', unsafe_allow_html=True)
day_df = df.groupby("scheduled_date").agg(
    jobs=("job_id", "count"),
    critical=("urgency", lambda x: (x == "Critical").sum()),
).reset_index()
fig_day = go.Figure()
fig_day.add_trace(go.Bar(
    x=day_df["scheduled_date"], y=day_df["jobs"],
    name="Total Jobs", marker_color="#63b3ed",
))
fig_day.add_trace(go.Bar(
    x=day_df["scheduled_date"], y=day_df["critical"],
    name="Critical", marker_color="#fc8181",
))
fig_day.update_layout(
    barmode="overlay",
    paper_bgcolor="#0d1b2a",
    plot_bgcolor="#0d1b2a",
    font_color="#e2e8f0",
    margin=dict(l=10, r=10, t=10, b=10),
    height=250,
    xaxis_title="Date",
    yaxis_title="Number of Jobs",
    template="plotly_dark",
)
st.plotly_chart(fig_day, use_container_width=True)

# ─────────────────────────────────────────
# Schedule Table
# ─────────────────────────────────────────
st.markdown('<div class="section-header">📋 Optimized Schedule</div>', unsafe_allow_html=True)

display_cols = [
    "job_id", "section_id", "zone", "job_type",
    "ml_priority_score", "urgency", "scheduled_date",
    "block_start_time", "block_end_time",
    "estimated_duration_hrs", "days_overdue", "defect_severity",
]
display_df = df[display_cols].sort_values("ml_priority_score", ascending=False)
display_df.columns = [
    "Job ID", "Section", "Zone", "Job Type",
    "Priority Score", "Urgency", "Date",
    "Block Start", "Block End",
    "Duration (hrs)", "Days Overdue", "Severity",
]

st.dataframe(
    display_df,
    use_container_width=True,
    height=400,
    column_config={
        "Priority Score": st.column_config.ProgressColumn(
            "Priority Score", min_value=0, max_value=100, format="%.1f"
        ),
        "Urgency": st.column_config.TextColumn("Urgency"),
        "Severity": st.column_config.NumberColumn("Severity", format="%d ⭐"),
    }
)

# Download button
csv_bytes = display_df.to_csv(index=False).encode()
st.download_button(
    label="⬇️ Download Schedule CSV",
    data=csv_bytes,
    file_name="maintenance_schedule.csv",
    mime="text/csv",
)

# ─────────────────────────────────────────
# Footer
# ─────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small style='color:#4a5568;'>Indian Railways AI Maintenance Scheduler &nbsp;|&nbsp; "
    "XGBoost Priority Model + Google OR-Tools CP-SAT &nbsp;|&nbsp; SIH 2026</small></center>",
    unsafe_allow_html=True
)
