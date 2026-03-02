import hashlib
import math

SUSPICIOUS_KEYWORDS = [
    "mimikatz",
    "powershell -enc",
    "nc -e",
    "whoami",
    "base64"
]

def calculate_entropy(data):
    if not data:
        return 0

    entropy = 0
    for x in range(256):
        p_x = float(data.count(chr(x))) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)

    return entropy


def extract_features(file_path):

    with open(file_path, "r", errors="ignore") as f:
        content = f.read()

    size = len(content)
    entropy = calculate_entropy(content)

    suspicious_count = 0
    detected_keywords = []

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in content.lower():
            suspicious_count += 1
            detected_keywords.append(keyword)

    sha256_hash = hashlib.sha256(content.encode()).hexdigest()

    return {
        "size": size,
        "entropy": round(entropy, 3),
        "suspicious_count": suspicious_count,
        "sha256": sha256_hash,
        "detected_keywords": detected_keywords
    }