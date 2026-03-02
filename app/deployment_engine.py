import os
import json
from github_integration import push_to_github

REPORT_PATH = "../reports/security_report.json"

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

    # Ensure proper type handling
    risk = int(latest["risk_score"])
    status = str(latest["status"]).upper()

    print("---- Deployment Policy Check ----")
    print("Status:", status)
    print("Risk Score:", risk)

    # 🚨 Strict Security Policy
    if status in ["CRITICAL", "COMPROMISED"]:
        print("❌ Deployment BLOCKED due to critical security status.")
        return

    if risk >= 50:
        print("❌ Deployment BLOCKED due to high risk score.")
        return

    # ✅ If safe
    print("✅ Deployment ALLOWED.")
    push_to_github("../dataset/current_build.txt", "production_artifact.txt")