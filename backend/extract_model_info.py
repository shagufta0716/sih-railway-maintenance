"""
Helper script for the Next.js API.
Loads the trained XGBoost model pickle and prints feature importances + metrics as JSON.
"""
import pickle
import json
import os
import sys

pkl_path = os.path.join(os.path.dirname(__file__), "models", "priority_model.pkl")

if not os.path.exists(pkl_path):
    print(json.dumps({"error": "Model not found. Run train_model.py first."}))
    sys.exit(0)

with open(pkl_path, "rb") as f:
    m_data = pickle.load(f)

reg = m_data["regressor"]
feat_names = m_data["features"]
importances = reg.feature_importances_.tolist()
metrics = m_data.get("metrics", {})
urgency_labels = m_data.get("urgency_labels", {})

# Sort by importance descending
paired = sorted(zip(feat_names, importances), key=lambda x: x[1], reverse=True)

print(json.dumps({
    "features": [{"name": f, "importance": round(imp, 6)} for f, imp in paired],
    "metrics": {
        "mae": metrics.get("mae", "N/A"),
        "r2": metrics.get("r2", "N/A"),
        "accuracy": metrics.get("accuracy", "N/A"),
    },
    "urgency_labels": urgency_labels,
    "model_type": "XGBoost Regressor + XGBoost Classifier",
    "solver": "Google OR-Tools CP-SAT",
    "num_features": len(feat_names),
}))
