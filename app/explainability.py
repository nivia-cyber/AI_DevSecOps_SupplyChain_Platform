def generate_explanation(event):
    risk = event["risk_score"]

    if risk >= 80:
        return "Critical risk detected due to anomalous artifact behavior and attack patterns."
    elif risk >= 50:
        return "Medium risk detected. Suspicious indicators found."
    else:
        return "Artifact passed all security checks with low risk."