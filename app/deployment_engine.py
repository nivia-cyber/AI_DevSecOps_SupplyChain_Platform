def enforce_policy(risk_score):

    print("🔒 Enforcing Deployment Policy...")

    if risk_score < 30:

        deployment = "DEPLOYED"
        reason = "Clean artifact – safe for production"

    elif risk_score < 60:

        deployment = "BLOCKED"
        reason = "Medium risk detected"

    elif risk_score < 85:

        deployment = "BLOCKED"
        reason = "High risk detected"

    else:

        deployment = "BLOCKED"
        reason = "Critical security threat"

    return deployment, reason