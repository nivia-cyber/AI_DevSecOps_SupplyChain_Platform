def calculate_risk(suspicious_count, entropy, prediction):

    risk = 0

    risk += suspicious_count * 15
    risk += entropy * 5

    if prediction == 1:
        risk += 40

    return min(int(risk), 100)


def classify_severity(risk_score):

    if risk_score >= 85:
        return "CRITICAL"
    elif risk_score >= 60:
        return "HIGH"
    elif risk_score >= 40:
        return "MEDIUM"
    elif risk_score >= 20:
        return "LOW"
    else:
        return "MINIMAL"