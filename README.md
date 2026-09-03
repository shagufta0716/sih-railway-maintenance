# 🛤️ Indian Railways — AI Maintenance Scheduler
### SIH 2026 Prototype

---

## Project Structure

```
sih/
├── generate_dataset.py   ← STEP 1: Create realistic datasets
├── train_model.py        ← STEP 2: Train XGBoost ML model  
├── scheduler.py          ← STEP 3: OR-Tools optimizer
├── app.py                ← STEP 4: Streamlit dashboard
├── data/
│   ├── track_sections.csv      (40 track sections)
│   ├── train_timetable.csv     (200 train schedule entries)
│   ├── maintenance_jobs.csv    (300 jobs with ML targets)
│   └── optimized_schedule.csv  (final output)
└── models/
    └── priority_model.pkl      (trained XGBoost model)
```

---

## ▶️ How to Run (Step by Step)

### 1. Install dependencies
```bash
pip install streamlit pandas numpy plotly xgboost scikit-learn ortools
```

### 2. Generate dataset
```bash
python generate_dataset.py
```

### 3. Train ML model
```bash
python train_model.py
```

### 4. Run scheduler
```bash
python scheduler.py
```

### 5. Launch dashboard
```bash
streamlit run app.py
```

**OR — Run everything from the dashboard sidebar:**
```bash
streamlit run app.py
```
Then click **"▶ Run Full Pipeline"** in the sidebar.

---

## What Each File Does

### `generate_dataset.py`
Creates 3 CSV files simulating real Indian Railways data:
- **track_sections.csv** — 40 sections with zone, age, condition, traffic density
- **train_timetable.csv** — 200 train entries with entry/exit times per section per day
- **maintenance_jobs.csv** — 300 jobs with features + **ML targets** (priority_score, assigned_block_day)

### `train_model.py`
Trains 2 XGBoost models:
- **Regressor** — predicts `priority_score` (0–100, continuous)
- **Classifier** — predicts urgency class (Low/Medium/High/Critical)

Key features used:
| Feature | Why it matters |
|---------|---------------|
| `days_overdue` | Longer pending = more urgent |
| `defect_severity` | Defect rating 1–5 |
| `asset_age_years` | Older track = higher risk |
| `track_condition_score` | Lower score = needs attention |
| `traffic_density_num` | Busier line = higher priority |
| `risk_level_num` | Encoded risk level |

### `scheduler.py`
- Scores all 300 jobs using the trained ML model
- Builds train conflict map (which hours each section is occupied)
- Uses **Google OR-Tools CP-SAT** to assign optimal day-slots:
  - Critical jobs → within 7 days
  - High jobs → within 15 days
  - Avoids train conflict on every section
- Outputs `optimized_schedule.csv`

### `app.py`
Premium Streamlit dashboard with:
- KPI cards (total jobs, critical count, avg priority, block hours)
- **Gantt chart** — visual timeline of all maintenance blocks
- Urgency donut chart
- Priority score histogram
- Jobs-per-zone bar chart
- Jobs-per-day timeline
- Filterable schedule table
- CSV download

---

## Tech Stack
| Component | Technology |
|-----------|-----------|
| ML Priority Model | XGBoost (Gradient Boosting) |
| Optimization Engine | Google OR-Tools CP-SAT |
| Dashboard | Streamlit + Plotly |
| Data Processing | Pandas + NumPy |

---

