import sys
import json
import os
from datetime import datetime

from risk_engine import run_risk_engine
from deployment_engine import enforce_policy
from github_integration import push_to_github

BUILD_FILE = "dataset/current_build.txt"
REPORT_FILE = "reports/security_report.json"


# --------------------------------------------------
# BUILD GENERATOR
# --------------------------------------------------

def generate_build(mode):

    print("1️⃣ Generating Build...")

    if mode == "clean":

        content = """
safe application logic
normal api usage
processing data
"""

    elif mode == "medium":

        content = """
unknown_network scan
network activity detected
"""

    elif mode == "high":

        content = """
base64 encoded payload
credential password attempt
"""

    elif mode == "critical":

        content = """
powershell reverse_shell
credential password dump
"""

    else:
        content = "safe code"

    with open(BUILD_FILE, "w") as f:
        f.write(content)

    print(f"✔ Build generated in {mode.upper()} mode")


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def run_pipeline(mode=None):

    print("🚀 Starting CI/CD Security Pipeline...")

    # If mode is provided, generate simulated build
    if mode is not None:
        generate_build(mode)

    # Run risk engine on uploaded artifact
    result = run_risk_engine()

    risk_score = result["risk_score"]
    status = result["status"]

    # Step 3: Policy enforcement
    deployment, reason = enforce_policy(risk_score)

    # --------------------------------------------------
    # Step 4: Production Deployment Automation
    # --------------------------------------------------

    if deployment == "DEPLOYED":

        print("🚀 Deploying artifact to GitHub production...")

        try:

            push_to_github(
                "dataset/current_build.txt",
                "production/current_build.txt"
            )

            print("✅ Production deployment successful.")

        except Exception as e:

            print("❌ GitHub deployment failed:", str(e))

    else:

        print("⛔ Deployment skipped due to security policy.")


    # --------------------------------------------------
    # Step 5: Generate Security Report
    # --------------------------------------------------

    report_entry = {

        "artifact": "current_build.txt",
        "risk_score": risk_score,
        "status": status,
        "deployment": deployment,
        "reason": reason,
        "sha256": result["sha256"],
        "features": result["features"],
        "mitre_techniques": result["mitre_techniques"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Load existing report
    if os.path.exists(REPORT_FILE):

        with open(REPORT_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            data = [data]

    else:
        data = []

    data.append(report_entry)

    # Save updated report
    with open(REPORT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("📄 Security report updated.")
    print("✔ Pipeline Execution Complete.")


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    mode = None

    if len(sys.argv) > 1:
        mode = sys.argv[1]

    run_pipeline(mode)