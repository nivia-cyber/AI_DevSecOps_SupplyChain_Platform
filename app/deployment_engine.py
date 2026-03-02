import os
import json

REPORT_PATH = "../reports/security_report.json"

from github_integration import push_to_github

def enforce_policy():

    if not os.path.exists(REPORT_PATH):
        print("No report found.")
        return

    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    # If report is list, take latest entry
    if isinstance(data, list):
        latest = data[-1]
    else:
        latest = data

    risk = latest["risk_score"]
    status = latest["status"]

    print("---- Deployment Policy Check ----")
    print("Status:", status)
    print("Risk Score:", risk)

    if risk >= 80:
        print("❌ Deployment BLOCKED due to security risk.")
    else:
        print("✅ Deployment ALLOWED.")
        push_to_github("../dataset/current_build.txt", "production_artifact.txt")