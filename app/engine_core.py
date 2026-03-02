import joblib
import os
import json
from datetime import datetime

from fingerprinting import extract_features
from risk_engine import calculate_risk, classify_severity

MODEL_PATH = "../models/model.pkl"
REPORT_PATH = "../reports/security_report.json"
ARTIFACT_PATH = "../dataset/current_build.txt"


def run_detection():

    if not os.path.exists(ARTIFACT_PATH):
        print("No artifact found.")
        return

    model = joblib.load(MODEL_PATH)

    features = extract_features(ARTIFACT_PATH)

    feature_vector = [[
        features["size"],
        features["entropy"],
        features["suspicious_count"]
    ]]

    prediction = model.predict(feature_vector)[0]
    probability = model.predict_proba(feature_vector)[0]

    confidence_clean = round(probability[0] * 100, 2)
    confidence_compromised = round(probability[1] * 100, 2)

    risk_score = calculate_risk(
        features["suspicious_count"],
        features["entropy"],
        prediction
    )

    severity = classify_severity(risk_score)

    if risk_score >= 70:
        status = "COMPROMISED"
    elif prediction == 1:
        status = "COMPROMISED"
    else:
        status = "CLEAN"

    report = {
        "timestamp": str(datetime.now()),
        "artifact": ARTIFACT_PATH,
        "status": status,
        "risk_score": risk_score,
        "severity": severity,
        "model_confidence_clean": confidence_clean,
        "model_confidence_compromised": confidence_compromised,
        "features": features
    }

    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r") as f:
            existing = json.load(f)
            if not isinstance(existing, list):
                existing = [existing]
    else:
        existing = []

    existing.append(report)

    with open(REPORT_PATH, "w") as f:
        json.dump(existing, f, indent=4)

    print("Detection complete.")
    print("Status:", status)
    print("Risk:", risk_score)