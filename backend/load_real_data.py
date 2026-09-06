import pandas as pd
import numpy as np
from datetime import datetime
import os

print("="*55)
print("  STEP 1.5: Real Data Processor")
print("="*55)

# Ensure directories exist
os.makedirs("data/real", exist_ok=True)

# 1. Load Raw Data
print("\n[1/3] Loading raw real data...")
try:
    tracks_df = pd.read_csv("data/raw/track_sections.csv")
    jobs_df = pd.read_csv("data/raw/maintenance_jobs.csv")
    trains_df = pd.read_csv("data/raw/train_timetable.csv")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please ensure you have placed the 3 CSV files in data/raw/")
    exit(1)

# Set a reference 'today' date for overdue calculations
TODAY = datetime(2026, 9, 6)

# 2. Process Track Sections
print("\n[2/3] Processing Track Sections & Train Timetable...")
proc_tracks = pd.DataFrame()
proc_tracks["section_id"] = tracks_df["section_id"]
proc_tracks["section_name"] = tracks_df["start_station"].astype(str) + "-" + tracks_df["end_station"].astype(str)
proc_tracks["zone"] = tracks_df["division"]
proc_tracks["total_length_km"] = tracks_df["distance_km"]
proc_tracks["annual_speed_limit_kmph"] = tracks_df["max_speed_kmh"]
proc_tracks["track_type"] = "BG Electrified" # Default
proc_tracks["asset_age_years"] = 15.0 # Default missing feature
proc_tracks["days_since_inspection"] = 30 # Default missing feature
proc_tracks["last_inspection_date"] = (TODAY - pd.Timedelta(days=30)).strftime("%Y-%m-%d")

tracks_count_norm = np.clip(tracks_df["tracks_count"] / 4.0, 0, 1)
speed_norm = np.clip(tracks_df["max_speed_kmh"] / 160.0, 0, 1)
proc_tracks["track_condition_score"] = (tracks_count_norm * 50 + speed_norm * 50).round(1)

# 3. Process Train Timetable & calculate Traffic Density
expanded_trains = []
section_density_scores = {sec: 0 for sec in tracks_df["section_id"]}

for _, row in trains_df.iterrows():
    route_sections = str(row["route_section_ids"]).split(",") if pd.notna(row["route_section_ids"]) else []
    try:
        dep_time = pd.to_datetime(row["departure_time"])
        arr_time = pd.to_datetime(row["arrival_time"])
    except:
        dep_time = TODAY
        arr_time = TODAY + pd.Timedelta(hours=2)

    total_duration_hrs = (arr_time - dep_time).total_seconds() / 3600
    if total_duration_hrs <= 0: total_duration_hrs = 1
    priority = int(row["priority_level"]) if pd.notna(row["priority_level"]) else 3
    
    for sec_id in route_sections:
        sec_id = sec_id.strip()
        if not sec_id: continue
        weight = max(1, 6 - priority)
        if sec_id in section_density_scores:
            section_density_scores[sec_id] += weight
            
        expanded_trains.append({
            "train_id": row["train_id"],
            "train_no": row["train_name"],
            "section_id": sec_id,
            "train_type": row["train_type"],
            "priority_level": priority,
            "day": (dep_time - datetime(2026, 1, 1)).days,
            "entry_time": dep_time.strftime("%Y-%m-%d %H:%M"),
            "exit_time": arr_time.strftime("%Y-%m-%d %H:%M"),
            "entry_hour": dep_time.hour,
            "exit_hour": arr_time.hour,
            "transit_hrs": total_duration_hrs
        })

proc_trains = pd.DataFrame(expanded_trains)

density_list = [section_density_scores.get(sec, 0) for sec in proc_tracks["section_id"]]
if max(density_list) > 0:
    density_norm = np.array(density_list) / max(density_list)
else:
    density_norm = np.zeros(len(density_list))

proc_tracks["traffic_density_num"] = np.digitize(density_norm, bins=[0.25, 0.5, 0.75]) + 1
DENSITY_LABELS = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
proc_tracks["traffic_density"] = proc_tracks["traffic_density_num"].map(DENSITY_LABELS)

# 4. Process Maintenance Jobs
print("\n[3/3] Processing Maintenance Jobs...")
proc_jobs = pd.DataFrame()
proc_jobs["job_id"] = jobs_df["job_id"]
proc_jobs["section_id"] = jobs_df["section_id"]
proc_jobs["job_type"] = jobs_df["block_type"]
proc_jobs["estimated_duration_hrs"] = jobs_df["required_hours"]

proc_jobs = pd.merge(proc_jobs, proc_tracks, on="section_id", how="left")

def map_severity(btype):
    btype = str(btype).lower()
    if "relaying" in btype: return 5
    elif "ohe" in btype: return 3
    else: return 1

proc_jobs["defect_severity"] = jobs_df["block_type"].apply(map_severity)

def calc_overdue(row):
    if str(row["status"]).lower() == "approved":
        return 0
    else:
        try:
            start_date = pd.to_datetime(row["start_time"])
            return max(0, (TODAY - start_date).days)
        except:
            return 0

proc_jobs["days_overdue"] = jobs_df.apply(calc_overdue, axis=1)

proc_jobs["reported_date"] = jobs_df["start_time"]
proc_jobs["risk_level_num"] = proc_jobs["defect_severity"] - 1
proc_jobs["risk_level_num"] = proc_jobs["risk_level_num"].clip(1, 4)
RISK_LABELS = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
proc_jobs["risk_level"] = proc_jobs["risk_level_num"].map(RISK_LABELS)
proc_jobs["preferred_window_start_hr"] = 2
proc_jobs["preferred_window_end_hr"] = 6
proc_jobs["assigned_block_day"] = 0
proc_jobs["assigned_block_start_hr"] = 2

# Check for potential columns model needs
proc_jobs.fillna(0, inplace=True)

# 5. Save Outputs
proc_tracks.to_csv("data/real/track_sections.csv", index=False)
proc_trains.to_csv("data/real/train_timetable.csv", index=False)
proc_jobs.to_csv("data/real/maintenance_jobs.csv", index=False)

print("\n  Real data processed and saved to data/real/!")
print("  You can now run: python scheduler.py --source real")
print("="*55)
