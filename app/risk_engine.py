import hashlib

BUILD_FILE = "dataset/current_build.py"

def run_risk_engine():

    print("2️⃣ Running Risk Engine...")

    with open(BUILD_FILE,"r") as f:
        content = f.read().lower()

    # -----------------------------
    # Risk detection
    # -----------------------------

    if "powershell" in content or "reverse_shell" in content:
        risk_score = 90
        status = "CRITICAL"

    elif "base64" in content or "credential" in content:
        risk_score = 70
        status = "HIGH"

    elif "network" in content or "unknown_network" in content:
        risk_score = 45
        status = "MEDIUM"

    else:
        risk_score = 7
        status = "CLEAN"

    # -----------------------------
    # SHA256
    # -----------------------------

    sha256 = hashlib.sha256(content.encode()).hexdigest()

    # -----------------------------
    # Features
    # -----------------------------

    features = {
        "api_calls": content.count("api"),
        "entropy": round(len(set(content))/100,2),
        "network_calls": content.count("network")
    }

    # -----------------------------
    # MITRE ATT&CK Mapping
    # -----------------------------

    mitre = []

    if "powershell" in content:
        mitre.append("T1059 - Command Interpreter")

    if "reverse_shell" in content:
        mitre.append("T1105 - Ingress Tool Transfer")

    if "network" in content:
        mitre.append("T1046 - Network Discovery")

    if "base64" in content:
        mitre.append("T1027 - Obfuscated Files")

    if "credential" in content or "password" in content:
        mitre.append("T1552 - Credential Access")

    print("✔ Risk analysis complete.")
    print("Risk Score:",risk_score)
    print("Status:",status)

    return {
        "risk_score":risk_score,
        "status":status,
        "sha256":sha256,
        "features":features,
        "mitre_techniques":mitre
    }