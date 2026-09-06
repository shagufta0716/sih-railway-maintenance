"""
STEP 2: ML Model Training
Trains XGBoost model to predict priority_score for maintenance jobs.
Also trains a classifier to predict assigned_block_day category.

Features used:
  - days_overdue
  - defect_severity
  - asset_age_years
  - track_condition_score
  - traffic_density_num
  - days_since_inspection
  - risk_level_num
  - estimated_duration_hrs

Targets:
  - priority_score      (regression, 0-100)
  - urgency_class       (classification: 0=Low, 1=Medium, 2=High, 3=Critical)
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

URGENCY_LABELS = {0: "Low", 1: "Medium", 2: "High", 3: "Critical"}

# ─────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────
print("="*55)
print("  STEP 2: Training ML Priority Model")
print("="*55)

if not os.path.exists("data/maintenance_jobs.csv"):
    print("\nERROR: data/maintenance_jobs.csv not found!")
    print("Run: python generate_dataset.py first.\n")
    exit(1)

df = pd.read_csv("data/maintenance_jobs.csv")
print(f"\n  Loaded {len(df)} maintenance job records")

# ─────────────────────────────────────────
# Feature Engineering
# ─────────────────────────────────────────
FEATURES = [
    "days_overdue",
    "defect_severity",
    "asset_age_years",
    "track_condition_score",
    "traffic_density_num",
    "days_since_inspection",
    "risk_level_num",
    "estimated_duration_hrs",
]

# Derived features
df["overdue_x_severity"]   = df["days_overdue"] * df["defect_severity"]
df["age_x_condition"]      = df["asset_age_years"] * (100 - df["track_condition_score"])
df["inspection_lag_risk"]  = df["days_since_inspection"] * df["risk_level_num"]

FEATURES += ["overdue_x_severity", "age_x_condition", "inspection_lag_risk"]

X = df[FEATURES]
y_reg = df["priority_score"]          # Regression target

# Urgency class from priority score
def to_urgency(score):
    if score >= 70:   return 3   # Critical
    elif score >= 52: return 2   # High
    elif score >= 35: return 1   # Medium
    else:             return 0   # Low

y_cls = y_reg.apply(to_urgency)       # Classification target

print(f"\n  Features ({len(FEATURES)}): {', '.join(FEATURES)}")

# ─────────────────────────────────────────
# Train/Test Split
# ─────────────────────────────────────────
X_train, X_test, yr_train, yr_test, yc_train, yc_test = train_test_split(
    X, y_reg, y_cls, test_size=0.2, random_state=42
)

# Remap urgency classes to 0-based (XGBoost requirement)
le = LabelEncoder()
yc_train_enc = le.fit_transform(yc_train)
yc_test_enc  = le.transform(yc_test)
print(f"\n  Train: {len(X_train)} samples  |  Test: {len(X_test)} samples")

# ─────────────────────────────────────────
# MODEL A: Priority Score Regressor (XGBoost)
# ─────────────────────────────────────────
print("\n[1/2] Training Priority Score Regressor (XGBoost)...")

reg_model = xgb.XGBRegressor(
    n_estimators=200,
    learning_rate=0.08,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbosity=0,
)
reg_model.fit(X_train, yr_train)

yr_pred = reg_model.predict(X_test)
mae     = mean_absolute_error(yr_test, yr_pred)
r2      = r2_score(yr_test, yr_pred)

print(f"      MAE  : {mae:.2f} points")
print(f"      R2   : {r2:.4f}")

# ─────────────────────────────────────────
# MODEL B: Urgency Classifier (XGBoost)
# ─────────────────────────────────────────
print("\n[2/2] Training Urgency Classifier (XGBoost)...")

cls_model = xgb.XGBClassifier(
    n_estimators=200,
    learning_rate=0.08,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbosity=0,
    eval_metric="mlogloss",
)
cls_model.fit(X_train, yc_train_enc)

yc_pred_enc = cls_model.predict(X_test)
yc_pred     = le.inverse_transform(yc_pred_enc)   # decode back to original labels
accuracy    = accuracy_score(yc_test, yc_pred)
print(f"      Accuracy : {accuracy*100:.1f}%")

# ─────────────────────────────────────────
# Feature Importance
# ─────────────────────────────────────────
print("\n  Top 5 Important Features (Regressor):")
importances = pd.Series(
    reg_model.feature_importances_, index=FEATURES
).sort_values(ascending=False)
for feat, imp in importances.head(5).items():
    bar = "#" * int(imp * 50)
    print(f"    {feat:<30} {imp:.4f}  {bar}")

# ─────────────────────────────────────────
# Save Models
# ─────────────────────────────────────────
os.makedirs("models", exist_ok=True)

model_data = {
    "regressor":       reg_model,
    "classifier":      cls_model,
    "label_encoder":   le,          # needed to decode predictions
    "features":        FEATURES,
    "urgency_labels":  URGENCY_LABELS,
    "metrics": {
        "mae":       round(mae, 3),
        "r2":        round(r2, 4),
        "accuracy":  round(accuracy, 4),
    }
}

with open("models/priority_model.pkl", "wb") as f:
    pickle.dump(model_data, f)

print(f"\n  Model saved -> models/priority_model.pkl")
print("\n" + "="*55)
print("  Training Complete!")
print(f"  Regressor MAE   : {mae:.2f}   R2: {r2:.4f}")
print(f"  Classifier Acc  : {accuracy*100:.1f}%")
print("="*55)
print("\n  Next: python scheduler.py")
