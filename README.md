# Indian Railways — AI Track Maintenance & Block Optimizer
### Smart India Hackathon 2026

---

## Project Structure

```
sih-railway-maintenance/
├── backend/                        ← Python AI/ML Engine
│   ├── data/
│   │   ├── track_sections.csv      (40 track sections)
│   │   ├── train_timetable.csv     (200 train schedule entries)
│   │   ├── maintenance_jobs.csv    (300 jobs with ML targets)
│   │   └── optimized_schedule.csv  (generated output — gitignored)
│   ├── models/
│   │   └── priority_model.pkl      (trained XGBoost — gitignored)
│   ├── generate_dataset.py         ← Step 1: Create synthetic datasets
│   ├── train_model.py              ← Step 2: Train XGBoost model
│   ├── scheduler.py                ← Step 3: Run OR-Tools optimizer
│   ├── load_real_data.py           ← Load real CSV data
│   └── extract_model_info.py       ← Helper for model diagnostics API
│
└── frontend/                       ← Next.js Web Application
    ├── app/
    │   ├── page.js                 ← Landing page (/)
    │   ├── login/page.js           ← Login (/login)
    │   ├── register/page.js        ← Register (/register)
    │   ├── dashboard/page.js       ← Dashboard (/dashboard)
    │   └── api/
    │       ├── auth/[...nextauth]/ ← NextAuth login endpoint
    │       ├── register/           ← User registration endpoint
    │       ├── schedule/           ← Reads optimized_schedule.csv
    │       ├── optimize/           ← Triggers scheduler.py
    │       └── model-info/         ← Reads model metrics from pickle
    ├── components/
    │   ├── LandingPage.jsx
    │   ├── AuthPage.jsx
    │   └── Dashboard.jsx           ← All 4 tabs: Summary, Gantt, Timetable, Diagnostics
    ├── prisma/
    │   └── schema.prisma           ← PostgreSQL User model
    ├── .env.example                ← Copy to .env and fill in credentials
    └── middleware.js               ← Protects /dashboard route
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Priority Model | XGBoost (Regression + Classification) |
| Optimization Engine | Google OR-Tools CP-SAT |
| Web Framework | Next.js 16 (App Router) |
| Database | PostgreSQL via Neon (cloud) |
| ORM | Prisma |
| Authentication | NextAuth.js (Credentials provider + bcrypt) |
| Charts | Recharts |
| UI Icons | Lucide React |
| Data Processing | Pandas + NumPy |

---

## Setup & Run

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Neon](https://neon.tech) PostgreSQL database (free tier works)

---

### Step 1 — Clone & configure environment

```bash
git clone <your-repo-url>
cd sih-railway-maintenance
```

Create the frontend environment file:
```bash
cd frontend
cp .env.example .env
```

Edit `frontend/.env` and fill in:
```
DATABASE_URL="postgresql://user:password@host/dbname?sslmode=require&channel_binding=require"
NEXTAUTH_SECRET="<generate with: python -c 'import secrets; print(secrets.token_hex(32))'>"
```

---

### Step 2 — Install Python dependencies

```bash
pip install pandas numpy xgboost scikit-learn ortools
```

---

### Step 3 — Train the AI model (one-time setup)

```bash
cd backend
python generate_dataset.py   # creates 300 synthetic maintenance jobs
python train_model.py        # trains XGBoost priority model
python scheduler.py          # runs OR-Tools optimizer → optimized_schedule.csv
```

---

### Step 4 — Install frontend dependencies & set up database

```bash
cd frontend
npm install
npx prisma db push           # creates User table in your Neon database
```

---

### Step 5 — Run the web app

```bash
cd frontend
npm run dev
```

Open **http://localhost:3000** in your browser.

---

## Daily Usage

After initial setup, you only need:

```bash
cd frontend
npm run dev
```

The **"Run Optimization"** button in the dashboard sidebar will automatically re-run `scheduler.py` in the background and refresh all charts.

---

## What Each Backend File Does

| File | Purpose |
|---|---|
| `generate_dataset.py` | Creates synthetic track sections, timetables, and 300 maintenance jobs |
| `train_model.py` | Trains XGBoost regressor (priority score 0-100) + classifier (urgency class) |
| `scheduler.py` | Uses trained model + OR-Tools CP-SAT to assign conflict-free maintenance windows |
| `load_real_data.py` | Loads actual Indian Railways CSV data into the backend data folder |
| `extract_model_info.py` | Reads the trained pickle and outputs feature importances as JSON for the dashboard |

---

## Dashboard Tabs

| Tab | Content |
|---|---|
| Executive Summary | KPI cards, urgency donut chart, jobs-per-zone bar chart |
| Gantt Timeline | Horizontal timeline of each block by hour (0-24), colored by urgency |
| Master Timetable | Searchable & sortable table of all scheduled jobs |
| Model Diagnostics | XGBoost feature importance, priority score histogram, optimization constraints, solver stats |
