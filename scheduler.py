"""
STEP 3: OR-Tools Scheduler
Uses trained ML model + Google OR-Tools CP-SAT solver to:
  1. Score all pending maintenance jobs (ML priority model)
  2. Find conflict-free time blocks (no train overlap)
  3. Output optimized maintenance schedule
"""

import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta
from ortools.sat.python import cp_model

print("="*55)
print("  STEP 3: OR-Tools Maintenance Scheduler")
print("="*55)

# ─────────────────────────────────────────
# Load data & model
# ─────────────────────────────────────────
jobs_df      = pd.read_csv("data/maintenance_jobs.csv")
timetable_df = pd.read_csv("data/train_timetable.csv")
sections_df  = pd.read_csv("data/track_sections.csv")

with open("models/priority_model.pkl", "rb") as f:
    model_data = pickle.load(f)

reg_model = model_data["regressor"]
cls_model = model_data["classifier"]
le        = model_data["label_encoder"]
FEATURES  = model_data["features"]

print(f"\n  Loaded {len(jobs_df)} maintenance jobs")
print(f"  Loaded {len(timetable_df)} train schedule entries")

# ─────────────────────────────────────────
# Step A: Score all jobs using ML model
# ─────────────────────────────────────────
print("\n[1/3] Scoring jobs with ML model...")

# Derived features (same as training)
jobs_df["overdue_x_severity"]  = jobs_df["days_overdue"] * jobs_df["defect_severity"]
jobs_df["age_x_condition"]     = jobs_df["asset_age_years"] * (100 - jobs_df["track_condition_score"])
jobs_df["inspection_lag_risk"] = jobs_df["days_since_inspection"] * jobs_df["risk_level_num"]

X_jobs = jobs_df[FEATURES]
jobs_df["ml_priority_score"]   = reg_model.predict(X_jobs).round(2)
pred_enc = cls_model.predict(X_jobs)          # encoded labels (0-based)
jobs_df["ml_urgency_class"]    = le.inverse_transform(pred_enc)  # original class ints

URGENCY_LABELS = {0: "Low", 1: "Medium", 2: "High", 3: "Critical"}
jobs_df["ml_urgency_label"]    = jobs_df["ml_urgency_class"].map(URGENCY_LABELS)

print(f"      Scored {len(jobs_df)} jobs")
print(f"      Critical: {(jobs_df['ml_urgency_class']==3).sum()} jobs")
print(f"      High    : {(jobs_df['ml_urgency_class']==2).sum()} jobs")


# ─────────────────────────────────────────
# Step B: Build conflict map (which hour slots have trains)
# ─────────────────────────────────────────
print("\n[2/3] Building train conflict map...")

SCHEDULE_DAYS = 30
HOURS_PER_DAY = 24

# blocked_slots[section_id][day] = set of busy hours
blocked_slots = {}
for _, row in timetable_df.iterrows():
    sec  = row["section_id"]
    day  = int(row["day"])
    e_hr = int(row["entry_hour"])
    x_hr = min(int(row["exit_hour"]) + 1, 23)
    if sec not in blocked_slots:
        blocked_slots[sec] = {}
    if day not in blocked_slots[sec]:
        blocked_slots[sec][day] = set()
    for h in range(e_hr, x_hr + 1):
        blocked_slots[sec][day].add(h)

print("      Conflict map ready")

# ─────────────────────────────────────────
# ─────────────────────────────────────────
# Helper: find free maintenance window
# ─────────────────────────────────────────
maint_slots = {}  # maint_slots[sec][day] = set of reserved maintenance hours

def find_free_window(section_id, duration_hrs, target_day=0, preferred_start_hr=1, max_day=SCHEDULE_DAYS):
    """Find earliest day + hour starting from target_day where track is free for `duration_hrs` hours."""
    needed = int(np.ceil(duration_hrs))
    sec_busy = blocked_slots.get(section_id, {})
    sec_maint = maint_slots.get(section_id, {})

    for day in range(target_day, max_day):
        busy_today = sec_busy.get(day, set()).union(sec_maint.get(day, set()))
        candidate_hours = [preferred_start_hr] + [h for h in range(0, 24 - needed) if h != preferred_start_hr]
        for start_hr in candidate_hours:
            candidate = range(start_hr, start_hr + needed)
            if not any(h in busy_today for h in candidate):
                if section_id not in maint_slots:
                    maint_slots[section_id] = {}
                if day not in maint_slots[section_id]:
                    maint_slots[section_id][day] = set()
                for h in candidate:
                    maint_slots[section_id][day].add(h)
                return day, start_hr
    return target_day, preferred_start_hr


# ─────────────────────────────────────────
# Step C: CP-SAT Optimization
# ─────────────────────────────────────────
print("\n[3/3] Running OR-Tools CP-SAT optimizer...")

# Select 50 jobs with realistic representation across urgencies
crit_jobs = jobs_df[jobs_df["ml_urgency_class"] == 3].nlargest(15, "ml_priority_score")
high_jobs = jobs_df[jobs_df["ml_urgency_class"] == 2].nlargest(20, "ml_priority_score")
med_jobs  = jobs_df[jobs_df["ml_urgency_class"] <= 1].nlargest(15, "ml_priority_score")
selected_jobs = pd.concat([crit_jobs, high_jobs, med_jobs]).drop_duplicates(subset=["job_id"]).reset_index(drop=True)
if len(selected_jobs) < 50:
    rem = jobs_df[~jobs_df["job_id"].isin(selected_jobs["job_id"])].nlargest(50 - len(selected_jobs), "ml_priority_score")
    selected_jobs = pd.concat([selected_jobs, rem]).reset_index(drop=True)
top_jobs = selected_jobs.head(50).copy().reset_index(drop=True)

model  = cp_model.CpModel()
solver = cp_model.CpSolver()
MAX_JOBS_PER_DAY = 3

# Variables: for each job, which day slot (0..SCHEDULE_DAYS-1)
job_vars = {}
for idx, row in top_jobs.iterrows():
    job_id = row["job_id"]
    job_vars[job_id] = model.NewIntVar(0, SCHEDULE_DAYS - 1, f"day_{job_id}")
    
    # Critical jobs: must be within first 7 days (day 0..6)
    if row["ml_urgency_class"] == 3:
        model.Add(job_vars[job_id] <= 6)
    # High urgency jobs: must be within first 16 days (day 0..15)
    elif row["ml_urgency_class"] == 2:
        model.Add(job_vars[job_id] <= 15)

# Crew capacity constraint: at most 3 jobs per day across the network
for d in range(SCHEDULE_DAYS):
    bools = []
    for idx, row in top_jobs.iterrows():
        jid = row["job_id"]
        b = model.NewBoolVar(f"b_{jid}_{d}")
        model.Add(job_vars[jid] == d).OnlyEnforceIf(b)
        model.Add(job_vars[jid] != d).OnlyEnforceIf(b.Not())
        bools.append(b)
    model.Add(sum(bools) <= MAX_JOBS_PER_DAY)

# Objective: minimize weighted day (higher priority = schedule earlier)
objective_terms = []
for idx, row in top_jobs.iterrows():
    weight = int(row["ml_priority_score"])
    objective_terms.append(weight * job_vars[row["job_id"]])

model.Minimize(sum(objective_terms))

# Solve
solver.parameters.max_time_in_seconds = 10.0
status = solver.Solve(model)

print(f"      Solver status : {solver.StatusName(status)}")

# ─────────────────────────────────────────
# Build final schedule
# ─────────────────────────────────────────
schedule = []
START_DATE = datetime(2026, 1, 1)

for idx, row in top_jobs.iterrows():
    job_id   = row["job_id"]
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        day = solver.Value(job_vars[job_id])
    else:
        day = int(row["assigned_block_day"])  # fallback

    # Find actual free hour starting from target day
    assigned_day, start_hr = find_free_window(
        row["section_id"],
        row["estimated_duration_hrs"],
        target_day=day,
        preferred_start_hr=int(row["preferred_window_start_hr"]),
        max_day=SCHEDULE_DAYS,
    )

    end_hr = start_hr + int(np.ceil(row["estimated_duration_hrs"]))
    block_date = START_DATE + timedelta(days=assigned_day)

    schedule.append({
        "job_id":            job_id,
        "section_id":        row["section_id"],
        "zone":              row["zone"],
        "job_type":          row["job_type"],
        "ml_priority_score": row["ml_priority_score"],
        "urgency":           row["ml_urgency_label"],
        "estimated_duration_hrs": row["estimated_duration_hrs"],
        "scheduled_date":    block_date.strftime("%Y-%m-%d"),
        "scheduled_day":     assigned_day,
        "block_start_hr":    start_hr,
        "block_end_hr":      end_hr,
        "block_start_time":  f"{start_hr:02d}:00",
        "block_end_time":    f"{end_hr:02d}:00",
        "days_overdue":      row["days_overdue"],
        "defect_severity":   row["defect_severity"],
    })

schedule_df = pd.DataFrame(schedule).sort_values("ml_priority_score", ascending=False)
schedule_df.to_csv("data/optimized_schedule.csv", index=False)

print(f"\n  Schedule saved -> data/optimized_schedule.csv")
print(f"  Total jobs scheduled: {len(schedule_df)}")
print(f"  Critical jobs: {(schedule_df['urgency']=='Critical').sum()}")
print(f"  High jobs    : {(schedule_df['urgency']=='High').sum()}")
print(f"  Avg priority : {schedule_df['ml_priority_score'].mean():.1f}")

print("\n" + "="*55)
print("  Scheduling Complete!")
print("="*55)
print("\n  Next: streamlit run app.py")
