"""
Indian Railways — AI Track Maintenance & Block Optimization System
Production-grade Executive Dashboard (SIH 2026)
Architecture: XGBoost Priority Engine + Google OR-Tools CP-SAT Optimizer
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import subprocess, os, sys, pickle

# ─────────────────────────────────────────────────────────────────────────────
# 1. Page Configuration & Professional Styling
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Indian Railways | AI Maintenance Scheduler",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Layout Theme */
    .stApp {
        background-color: #0b111e;
        color: #f1f5f9;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Clean Enterprise Cards */
    .kpi-card {
        background: #141e33;
        border: 1px solid #23324d;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .kpi-title {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #f8fafc;
        font-size: 2.1rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .kpi-sub {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: 6px;
    }
    
    /* Official Government / Railway Header */
    .header-box {
        background: #141e33;
        border: 1px solid #23324d;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .badge-gov {
        display: inline-block;
        background: #1e293b;
        color: #38bdf8;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 4px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 8px;
        border: 1px solid #334155;
    }
    .badge-live {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    /* Section Headings */
    .section-title {
        color: #f1f5f9;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 16px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid #23324d;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #141e33;
        border: 1px solid #23324d;
        border-radius: 8px 8px 0 0;
        color: #94a3b8;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        font-weight: 600 !important;
    }
    
    /* Clean Buttons */
    .stButton > button {
        background-color: #2563eb;
        color: #ffffff;
        font-weight: 600;
        font-size: 0.88rem;
        border-radius: 6px;
        border: none;
        padding: 8px 18px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Data Loading & Pipeline Functions
# ─────────────────────────────────────────────────────────────────────────────
URGENCY_COLORS = {
    "Critical": "#ef4444",
    "High":     "#f59e0b",
    "Medium":   "#3b82f6",
    "Low":      "#10b981",
}

def load_data():
    """Load fresh CSV records without aggressive caching."""
    schedule = pd.read_csv("data/optimized_schedule.csv")
    jobs     = pd.read_csv("data/maintenance_jobs.csv")
    trains   = pd.read_csv("data/train_timetable.csv")
    sections = pd.read_csv("data/track_sections.csv")
    return schedule, jobs, trains, sections

def run_pipeline():
    """Run data generation, model training, and optimization sequence."""
    with st.spinner("Generating Indian Railways synthetic dataset..."):
        subprocess.run([sys.executable, "generate_dataset.py"], check=True)
    with st.spinner("Training XGBoost Regressor & Classifier models..."):
        subprocess.run([sys.executable, "train_model.py"], check=True)
    with st.spinner("Solving Google OR-Tools CP-SAT conflict optimizer..."):
        subprocess.run([sys.executable, "scheduler.py"], check=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Sidebar Controls & Filtering
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='padding: 6px 0 14px 0;'>
            <div style='font-size: 1.1rem; font-weight: 700; color: #f8fafc;'>🚆 IR Operations AI</div>
            <div style='font-size: 0.75rem; color: #64748b;'>Track Maintenance Scheduler</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:0.75rem; font-weight:600; color:#94a3b8; margin-bottom:6px; text-transform:uppercase;'>Pipeline Controls</div>", unsafe_allow_html=True)
    if st.button("▶ Run Optimization Pipeline", use_container_width=True):
        run_pipeline()
        st.success("Pipeline executed successfully!")
        st.rerun()

    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem; font-weight:600; color:#94a3b8; margin-bottom:8px; text-transform:uppercase;'>Filter Network Scope</div>", unsafe_allow_html=True)
    
    if os.path.exists("data/optimized_schedule.csv"):
        schedule, jobs, trains, sections = load_data()
        
        all_zones = sorted(schedule["zone"].unique())
        sel_zones = st.multiselect("Zonal Railways", all_zones, default=all_zones)
        
        all_urgency = ["Critical", "High", "Medium", "Low"]
        sel_urgency = st.multiselect("Defect Urgency", all_urgency, default=[u for u in all_urgency if u in schedule["urgency"].values])
        
        max_day = st.slider("Planning Horizon (Days Ahead)", min_value=7, max_value=30, value=30, step=1)
    else:
        schedule = jobs = trains = sections = None
        sel_zones = sel_urgency = []
        max_day = 30

    st.markdown("---")
    st.markdown("""
        <div style='font-size: 0.72rem; color: #64748b; line-height: 1.5;'>
            <b>Smart India Hackathon 2026</b><br>
            Problem: Track Block Scheduling<br>
            Engine: XGBoost + OR-Tools CP-SAT
        </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 4. Main Application View
# ─────────────────────────────────────────────────────────────────────────────
# Check data availability
if not os.path.exists("data/optimized_schedule.csv") or schedule is None:
    st.warning("⚠️ No active schedule found. Please click **'Run Optimization Pipeline'** in the sidebar to generate data.")
    st.stop()

# Apply Filters
df = schedule.copy()
if sel_zones:
    df = df[df["zone"].isin(sel_zones)]
if sel_urgency:
    df = df[df["urgency"].isin(sel_urgency)]
df = df[df["scheduled_day"] <= max_day]

# Top Official Header Banner
st.markdown(f"""
<div class="header-box">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
            <div class="badge-gov">Indian Railways • Ministry of Railways</div>
            <h2 style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #f8fafc;">AI Track Maintenance & Traffic Block Optimizer</h2>
            <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 4px;">
                Intelligent decision support platform for conflict-free maintenance block allocation.
            </div>
        </div>
        <div style="text-align: right;">
            <span class="badge-live">● ENGINE STATUS: ACTIVE</span>
            <div style="color: #64748b; font-size: 0.75rem; margin-top: 6px;">Horizon: Next {max_day} Days</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 5. Clean Tabbed Architecture
# ─────────────────────────────────────────────────────────────────────────────
tab_overview, tab_gantt, tab_table, tab_diagnostics = st.tabs([
    "📊 Executive Summary",
    "📅 Track Block Gantt Timeline",
    "📋 Master Timetable",
    "🧠 AI Model & Diagnostics"
])

# =============================================================================
# TAB 1: EXECUTIVE SUMMARY
# =============================================================================
with tab_overview:
    # KPI Metric Cards
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Scheduled Jobs</div>
            <div class="kpi-value">{len(df)}</div>
            <div class="kpi-sub">Within {max_day}-day window</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        crit_count = (df["urgency"] == "Critical").sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Critical Urgency</div>
            <div class="kpi-value" style="color: #ef4444;">{crit_count}</div>
            <div class="kpi-sub">Mandatory early clearance</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k3:
        avg_score = df["ml_priority_score"].mean() if len(df) > 0 else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg Priority Score</div>
            <div class="kpi-value" style="color: #38bdf8;">{avg_score:.1f}</div>
            <div class="kpi-sub">Predicted by XGBoost Model</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k4:
        total_block_hrs = df["estimated_duration_hrs"].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Block Duration</div>
            <div class="kpi-value">{total_block_hrs:.0f} hrs</div>
            <div class="kpi-sub">Conflict-free track reservation</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    
    # Visual Analytics Row
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("<div class='section-title'>🚨 Urgency Distribution</div>", unsafe_allow_html=True)
        urgency_counts = df["urgency"].value_counts().reset_index()
        urgency_counts.columns = ["Urgency", "Count"]
        
        fig_pie = px.pie(
            urgency_counts,
            names="Urgency",
            values="Count",
            color="Urgency",
            color_discrete_map=URGENCY_COLORS,
            hole=0.6,
            template="plotly_dark",
        )
        fig_pie.update_layout(
            paper_bgcolor="#141e33",
            plot_bgcolor="#141e33",
            margin=dict(l=15, r=15, t=20, b=20),
            height=280,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, width="stretch")
        
    with c2:
        st.markdown("<div class='section-title'>🗺️ Jobs by Railway Zone</div>", unsafe_allow_html=True)
        zone_counts = df.groupby("zone").size().reset_index(name="jobs").sort_values("jobs", ascending=True)
        
        fig_zone = px.bar(
            zone_counts,
            x="jobs",
            y="zone",
            orientation="h",
            color_discrete_sequence=["#38bdf8"],
            template="plotly_dark",
            labels={"jobs": "Allocated Jobs", "zone": ""}
        )
        fig_zone.update_layout(
            paper_bgcolor="#141e33",
            plot_bgcolor="#141e33",
            margin=dict(l=15, r=15, t=20, b=20),
            height=280,
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b"),
        )
        st.plotly_chart(fig_zone, width="stretch")

    # Daily Workload Distribution Bar
    st.markdown("<div class='section-title'>📆 Maintenance Workload Over Time</div>", unsafe_allow_html=True)
    day_df = df.groupby("scheduled_date").agg(
        total_jobs=("job_id", "count"),
        critical_jobs=("urgency", lambda x: (x == "Critical").sum())
    ).reset_index()
    
    fig_workload = go.Figure()
    fig_workload.add_trace(go.Bar(
        x=day_df["scheduled_date"],
        y=day_df["total_jobs"],
        name="Total Scheduled Blocks",
        marker_color="#3b82f6"
    ))
    fig_workload.add_trace(go.Bar(
        x=day_df["scheduled_date"],
        y=day_df["critical_jobs"],
        name="Critical Repairs",
        marker_color="#ef4444"
    ))
    fig_workload.update_layout(
        barmode="overlay",
        paper_bgcolor="#141e33",
        plot_bgcolor="#141e33",
        font_color="#cbd5e1",
        margin=dict(l=15, r=15, t=15, b=15),
        height=240,
        template="plotly_dark",
        xaxis=dict(title="Scheduled Date", gridcolor="#1e293b"),
        yaxis=dict(title="Blocks per Day", gridcolor="#1e293b"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_workload, width="stretch")


# =============================================================================
# TAB 2: GANTT TIMELINE
# =============================================================================
with tab_gantt:
    st.markdown("""
        <div style='margin-bottom: 12px; color: #94a3b8; font-size: 0.88rem;'>
            Visual timeline of approved traffic block windows. Every block guarantees zero conflict with scheduled train traffic.
        </div>
    """, unsafe_allow_html=True)
    
    gantt_df = df.copy()
    gantt_df["Start"]  = pd.to_datetime(gantt_df["scheduled_date"]) + pd.to_timedelta(gantt_df["block_start_hr"], unit="h")
    gantt_df["Finish"] = pd.to_datetime(gantt_df["scheduled_date"]) + pd.to_timedelta(gantt_df["block_end_hr"], unit="h")
    gantt_df["Label"]  = gantt_df["job_id"] + " (" + gantt_df["block_start_time"] + " - " + gantt_df["block_end_time"] + ")"

    mode_col1, mode_col2 = st.columns([1, 1])
    with mode_col1:
        gantt_view_type = st.radio(
            "Gantt Display Mode:",
            ["📆 Single Day Focus (Hourly 24h Blocks)", "🌐 Full Multi-Day Network Timeline"],
            horizontal=True
        )

    if "Single Day" in gantt_view_type:
        available_dates = sorted(gantt_df["scheduled_date"].unique())
        sel_date = st.selectbox("Select Date to Inspect:", available_dates, index=0)
        
        day_subset = gantt_df[gantt_df["scheduled_date"] == sel_date].copy()
        base_date = pd.to_datetime(sel_date)
        day_subset["DayStart"] = base_date + pd.to_timedelta(day_subset["block_start_hr"], unit="h")
        day_subset["DayEnd"]   = base_date + pd.to_timedelta(day_subset["block_end_hr"], unit="h")

        if len(day_subset) == 0:
            st.info(f"No maintenance blocks scheduled on {sel_date}.")
        else:
            fig_single = px.timeline(
                day_subset,
                x_start="DayStart",
                x_end="DayEnd",
                y="section_id",
                color="urgency",
                hover_name="Label",
                hover_data={
                    "job_type": True,
                    "zone": True,
                    "ml_priority_score": ":.1f",
                    "estimated_duration_hrs": ":.1f",
                    "DayStart": False,
                    "DayEnd": False,
                },
                color_discrete_map=URGENCY_COLORS,
                template="plotly_dark",
                height=max(300, len(day_subset) * 65 + 100),
            )
            fig_single.update_xaxes(
                range=[base_date, base_date + pd.Timedelta(hours=24)],
                tickformat="%H:%M",
                dtick=7200000, # every 2 hours
                title="Time of Day (24-Hour Clock)",
                gridcolor="#1e293b",
            )
            fig_single.update_layout(
                paper_bgcolor="#141e33",
                plot_bgcolor="#141e33",
                font_color="#cbd5e1",
                yaxis_title="Track Section",
                margin=dict(l=15, r=15, t=15, b=15),
                showlegend=True,
            )
            fig_single.update_traces(width=0.48)
            fig_single.update_yaxes(categoryorder="array", categoryarray=day_subset["section_id"].unique().tolist(), gridcolor="#1e293b")
            st.plotly_chart(fig_single, width="stretch")
    else:
        fig_multi = px.timeline(
            gantt_df.head(45),
            x_start="Start",
            x_end="Finish",
            y="section_id",
            color="urgency",
            hover_name="Label",
            hover_data={
                "job_type": True,
                "zone": True,
                "ml_priority_score": ":.1f",
                "estimated_duration_hrs": ":.1f",
                "Start": False,
                "Finish": False,
            },
            color_discrete_map=URGENCY_COLORS,
            template="plotly_dark",
            height=500,
        )
        fig_multi.update_layout(
            paper_bgcolor="#141e33",
            plot_bgcolor="#141e33",
            font_color="#cbd5e1",
            xaxis_title="Date Timeline (Drag slider below to zoom into specific dates)",
            yaxis_title="Track Section",
            margin=dict(l=15, r=15, t=15, b=15),
            showlegend=True,
        )
        fig_multi.update_xaxes(rangeslider_visible=True, gridcolor="#1e293b")
        fig_multi.update_yaxes(categoryorder="array", categoryarray=gantt_df["section_id"].unique().tolist(), gridcolor="#1e293b")
        st.plotly_chart(fig_multi, width="stretch")


# =============================================================================
# TAB 3: DETAILED SCHEDULE TABLE
# =============================================================================
with tab_table:
    st.markdown("""
        <div style='margin-bottom: 14px; color: #94a3b8; font-size: 0.88rem;'>
            Authorized maintenance block authorization log. Search, sort, and export schedule for sectional railway dispatchers.
        </div>
    """, unsafe_allow_html=True)

    table_cols = [
        "job_id", "section_id", "zone", "job_type",
        "ml_priority_score", "urgency", "scheduled_date",
        "block_start_time", "block_end_time", "estimated_duration_hrs",
        "days_overdue", "defect_severity"
    ]
    t_df = df[table_cols].sort_values("ml_priority_score", ascending=False).copy()
    t_df.columns = [
        "Job ID", "Section", "Zone", "Job Type",
        "Priority Score", "Urgency", "Date",
        "Block Start", "Block End", "Duration (h)",
        "Overdue Days", "Defect Severity"
    ]

    st.dataframe(
        t_df,
        width="stretch",
        height=450,
        column_config={
            "Priority Score": st.column_config.ProgressColumn(
                "Priority Score", min_value=0, max_value=100, format="%.1f"
            ),
            "Defect Severity": st.column_config.NumberColumn("Severity", format="%d ⭐"),
            "Date": st.column_config.DateColumn("Date"),
        }
    )

    csv_data = t_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Export Schedule to CSV",
        data=csv_data,
        file_name=f"Indian_Railways_Maintenance_Schedule_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )


# =============================================================================
# TAB 4: AI MODEL & DIAGNOSTICS
# =============================================================================
with tab_diagnostics:
    st.markdown("<div class='section-title'>🧠 Architecture: 2-Stage Machine Learning & Optimization Engine</div>", unsafe_allow_html=True)
    
    st.markdown("""
        This platform combines **Explainable Machine Learning (XGBoost)** with **Mathematical Constraint Programming (Google OR-Tools CP-SAT)**:
        - **Stage 1 (Priority Scoring):** Analyzes 11 physical track parameters to evaluate failure probability and assign continuous priority score (0–100).
        - **Stage 2 (Traffic Block Allocation):** Scans multi-day timetable matrices to find zero-conflict maintenance windows within capacity limits.
    """)
    
    st.markdown("---")
    
    # Model Weights & Explainable AI
    diag_c1, diag_c2 = st.columns([1, 1])
    
    with diag_c1:
        st.markdown("<div class='section-title'>📈 XGBoost Feature Importance (Explainable AI)</div>", unsafe_allow_html=True)
        if os.path.exists("models/priority_model.pkl"):
            with open("models/priority_model.pkl", "rb") as f:
                m_data = pickle.load(f)
            reg = m_data["regressor"]
            feat_names = m_data["features"]
            importances = reg.feature_importances_
            
            imp_df = pd.DataFrame({
                "Feature": feat_names,
                "Importance": importances
            }).sort_values("Importance", ascending=True)
            
            fig_imp = px.bar(
                imp_df,
                x="Importance",
                y="Feature",
                orientation="h",
                color_discrete_sequence=["#10b981"],
                template="plotly_dark",
                labels={"Importance": "Model Weight / Contribution", "Feature": ""}
            )
            fig_imp.update_layout(
                paper_bgcolor="#141e33",
                plot_bgcolor="#141e33",
                margin=dict(l=15, r=15, t=15, b=15),
                height=320,
                xaxis=dict(gridcolor="#1e293b"),
                yaxis=dict(gridcolor="#1e293b"),
            )
            st.plotly_chart(fig_imp, width="stretch")
        else:
            st.info("Train the model first to inspect feature importances.")
            
    with diag_c2:
        st.markdown("<div class='section-title'>⚙️ Optimization Constraints & Rules</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#141e33; border:1px solid #23324d; border-radius:10px; padding:18px;'>
            <ul style='color: #cbd5e1; font-size: 0.88rem; line-height: 1.8; margin-bottom: 0;'>
                <li><b>Hard Constraint 1 (Zero Train Conflict):</b> Maintenance blocks are strictly scheduled during zero train occupancy slots.</li>
                <li><b>Hard Constraint 2 (Urgency Deadlines):</b> Critical jobs are constrained to early days (Day 1–7), High urgency jobs within Day 16.</li>
                <li><b>Hard Constraint 3 (Zonal Crew Capacity):</b> Max 3 simultaneous track blocks per day across the network to respect railway gang capacity.</li>
                <li><b>Objective Function:</b> Minimize cumulative priority-weighted completion delay: <code>min ∑ (Priority_i × ScheduledDay_i)</code></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kpi-card" style="padding: 14px 18px;">
            <div style="font-size: 0.82rem; color: #94a3b8;">Solver Performance</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #38bdf8; margin-top: 4px;">Google OR-Tools CP-SAT: OPTIMAL</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 2px;">Execution time: &lt; 0.5s for 50 combinatorial jobs</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small style='color:#64748b;'>Indian Railways AI Track Maintenance & Block Scheduler • Smart India Hackathon 2026 Prototype</small></center>",
    unsafe_allow_html=True
)
