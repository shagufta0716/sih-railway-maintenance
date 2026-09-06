"""
STEP 1: Dataset Generator
Generates realistic Indian Railways maintenance scheduling data
3 CSV files: track_sections, train_timetable, maintenance_jobs
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
NUM_SECTIONS   = 40   # track sections
NUM_TRAINS     = 200  # train entries (many trains, many timeslots)
NUM_JOBS       = 300  # maintenance jobs (ML training data)
START_DATE     = datetime(2026, 1, 1)
DAYS_WINDOW    = 30   # schedule window in days

ZONES = ["Northern Railway", "Central Railway", "Western Railway",
         "Eastern Railway", "South Central Railway", "Southern Railway"]

SECTION_TYPES = ["BG Electrified", "BG Non-Electrified", "MG", "BG Double Line"]

JOB_TYPES = [
    "Rail Replacement",
    "Ballast Tamping",
    "Weld Repair",
    "Track Geometry Correction",
    "Fish Plate Fixing",
    "Sleeper Replacement",
    "Level Crossing Repair",
    "Signal Cable Work",
    "Drainage Clearance",
    "OHE Maintenance"
]

TRAFFIC_DENSITY_MAP = {"Low": 1, "Medium": 2, "High": 3, "Very High": 4}


# ─────────────────────────────────────────
# TABLE 1: TRACK SECTIONS
# ─────────────────────────────────────────
def generate_track_sections():
    sections = []
    city_pairs = [
        ("Delhi", "Agra"), ("Mumbai", "Pune"), ("Chennai", "Bangalore"),
        ("Kolkata", "Bhubaneswar"), ("Hyderabad", "Secunderabad"),
        ("Jaipur", "Ajmer"), ("Lucknow", "Kanpur"), ("Ahmedabad", "Surat"),
        ("Patna", "Gaya"), ("Bhopal", "Indore"), ("Nagpur", "Wardha"),
        ("Amritsar", "Ludhiana"), ("Chandigarh", "Ambala"), ("Kochi", "Palakkad"),
        ("Varanasi", "Allahabad"), ("Raipur", "Bilaspur"), ("Guwahati", "Dibrugarh"),
        ("Jodhpur", "Bikaner"), ("Visakhapatnam", "Vijayawada"), ("Mysore", "Hubli"),
    ]

    for i in range(NUM_SECTIONS):
        pair = city_pairs[i % len(city_pairs)]
        direction = "Up" if i % 2 == 0 else "Down"
        zone = ZONES[i % len(ZONES)]
        age = round(random.uniform(2, 45), 1)
        density_label = random.choices(
            ["Low", "Medium", "High", "Very High"],
            weights=[15, 30, 35, 20]
        )[0]
        last_insp = START_DATE - timedelta(days=random.randint(10, 365))

        sections.append({
            "section_id":           f"SEC_{i+1:03d}",
            "section_name":         f"{pair[0]}-{pair[1]} {direction} Line",
            "zone":                 zone,
            "total_length_km":      round(random.uniform(15, 180), 1),
            "traffic_density":      density_label,
            "traffic_density_num":  TRAFFIC_DENSITY_MAP[density_label],
            "asset_age_years":      age,
            "last_inspection_date": last_insp.strftime("%Y-%m-%d"),
            "days_since_inspection":( START_DATE - last_insp).days,
            "track_type":           random.choice(SECTION_TYPES),
            "track_condition_score":round(random.uniform(30, 95), 1),
            "annual_speed_limit_kmph": random.choice([60, 90, 110, 130, 160]),
        })

    return pd.DataFrame(sections)


# ─────────────────────────────────────────
# TABLE 2: TRAIN TIMETABLE
# ─────────────────────────────────────────
def generate_train_timetable(sections_df):
    trains = []
    train_types = ["Rajdhani", "Shatabdi", "Express", "Mail", "Passenger", "Freight"]
    type_priority = {"Rajdhani": 5, "Shatabdi": 5, "Express": 4,
                     "Mail": 3, "Passenger": 2, "Freight": 1}
    type_weight   = [5, 5, 30, 20, 25, 15]

    section_ids = sections_df["section_id"].tolist()

    for i in range(NUM_TRAINS):
        ttype    = random.choices(train_types, weights=type_weight)[0]
        sec_id   = random.choice(section_ids)
        day_offset = random.randint(0, DAYS_WINDOW - 1)
        base_date  = START_DATE + timedelta(days=day_offset)

        entry_hour   = random.randint(5, 23)
        entry_min    = random.randint(0, 59)
        entry_time   = base_date.replace(hour=entry_hour, minute=entry_min)
        transit_hrs  = round(random.uniform(0.5, 3.5), 2)
        exit_time    = entry_time + timedelta(hours=transit_hrs)

        trains.append({
            "train_id":       f"TRN_{i+1:04d}",
            "train_no":       f"{12000 + random.randint(1, 8000)}",
            "section_id":     sec_id,
            "train_type":     ttype,
            "priority_level": type_priority[ttype],
            "day":            (base_date - START_DATE).days,
            "entry_time":     entry_time.strftime("%Y-%m-%d %H:%M"),
            "exit_time":      exit_time.strftime("%Y-%m-%d %H:%M"),
            "entry_hour":     entry_hour,
            "exit_hour":      exit_time.hour,
            "transit_hrs":    transit_hrs,
        })

    return pd.DataFrame(trains)


# ─────────────────────────────────────────
# TABLE 3: MAINTENANCE JOBS  (ML target)
# ─────────────────────────────────────────
def generate_maintenance_jobs(sections_df, timetable_df):
    jobs = []
    section_ids = sections_df["section_id"].tolist()
    section_map = sections_df.set_index("section_id").to_dict("index")

    risk_levels = ["Low", "Medium", "High", "Critical"]
    risk_num    = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

    for i in range(NUM_JOBS):
        sec_id   = random.choice(section_ids)
        sec_info = section_map[sec_id]

        age         = sec_info["asset_age_years"]
        condition   = sec_info["track_condition_score"]
        density_num = sec_info["traffic_density_num"]

        job_type    = random.choice(JOB_TYPES)
        days_overdue= random.randint(0, 90)
        severity    = random.randint(1, 5)

        risk_score  = (age / 45) * 30 + severity * 10 + (100 - condition) * 0.4 + days_overdue * 0.3
        risk_score  = min(100, risk_score)

        if risk_score < 25:
            risk_label = "Low"
        elif risk_score < 50:
            risk_label = "Medium"
        elif risk_score < 75:
            risk_label = "High"
        else:
            risk_label = "Critical"

        reported_date = START_DATE - timedelta(days=days_overdue)

        duration_map = {
            "Rail Replacement": (4, 8),
            "Ballast Tamping": (3, 6),
            "Weld Repair": (2, 4),
            "Track Geometry Correction": (3, 7),
            "Fish Plate Fixing": (1, 3),
            "Sleeper Replacement": (4, 9),
            "Level Crossing Repair": (2, 5),
            "Signal Cable Work": (2, 6),
            "Drainage Clearance": (1, 3),
            "OHE Maintenance": (3, 6),
        }
        dur_range   = duration_map.get(job_type, (2, 5))
        duration_hrs= round(random.uniform(*dur_range), 1)

        # TARGET: Priority Score (0–100)
        priority_score = (
            days_overdue      * 0.25 +
            severity          * 5.0  +
            (100 - condition) * 0.20 +
            age               * 0.30 +
            density_num       * 3.0  +
            risk_num[risk_label] * 4.0
        )
        priority_score = round(min(100, max(15, priority_score + random.gauss(0, 2.5))), 1)

        pref_window_start = random.choice([1, 2, 3])
        pref_window_end   = pref_window_start + int(duration_hrs) + 1

        if days_overdue > 30 or risk_label == "Critical":
            slot_day = random.randint(0, 7)
        elif days_overdue > 14 or risk_label == "High":
            slot_day = random.randint(0, 15)
        else:
            slot_day = random.randint(5, DAYS_WINDOW - 1)

        jobs.append({
            "job_id":                   f"JOB_{i+1:04d}",
            "section_id":               sec_id,
            "zone":                     sec_info["zone"],
            "job_type":                 job_type,
            "reported_date":            reported_date.strftime("%Y-%m-%d"),
            "days_overdue":             days_overdue,
            "estimated_duration_hrs":   duration_hrs,
            "asset_age_years":          age,
            "track_condition_score":    condition,
            "traffic_density_num":      density_num,
            "days_since_inspection":    sec_info["days_since_inspection"],
            "defect_severity":          severity,
            "risk_level":               risk_label,
            "risk_level_num":           risk_num[risk_label],
            "preferred_window_start_hr": pref_window_start,
            "preferred_window_end_hr":   pref_window_end,
            # ML TARGETS
            "priority_score":           priority_score,
            "assigned_block_day":       slot_day,
            "assigned_block_start_hr":  pref_window_start,
        })

    return pd.DataFrame(jobs)


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("="*55)
    print("  Indian Railways — Maintenance Dataset Generator")
    print("="*55)

    print("\n[1/3] Generating Track Sections...")
    sections_df = generate_track_sections()
    sections_df.to_csv("data/track_sections.csv", index=False)
    print(f"      > {len(sections_df)} sections -> data/track_sections.csv")

    print("\n[2/3] Generating Train Timetable...")
    timetable_df = generate_train_timetable(sections_df)
    timetable_df.to_csv("data/train_timetable.csv", index=False)
    print(f"      > {len(timetable_df)} train entries -> data/train_timetable.csv")

    print("\n[3/3] Generating Maintenance Jobs...")
    jobs_df = generate_maintenance_jobs(sections_df, timetable_df)
    jobs_df.to_csv("data/maintenance_jobs.csv", index=False)
    print(f"      > {len(jobs_df)} jobs -> data/maintenance_jobs.csv")

    print("\n" + "="*55)
    print("  Dataset Summary")
    print("="*55)
    print(f"  Track Sections   : {len(sections_df)}")
    print(f"  Train Records    : {len(timetable_df)}")
    print(f"  Maintenance Jobs : {len(jobs_df)}")
    print(f"\n  Priority Score Stats:")
    print(f"    Min  : {jobs_df['priority_score'].min():.1f}")
    print(f"    Max  : {jobs_df['priority_score'].max():.1f}")
    print(f"    Mean : {jobs_df['priority_score'].mean():.1f}")
    print(f"\n  Risk Level Distribution:")
    print(jobs_df['risk_level'].value_counts().to_string())
    print("\n  All datasets generated successfully!")
    print("\n  Next: python train_model.py")
