import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

data = []

# Clean samples
for i in range(100):
    size = np.random.randint(50, 200)
    entropy = np.random.uniform(2.0, 4.0)
    suspicious = 0
    data.append([size, entropy, suspicious, 0])

# Medium suspicious samples
for i in range(80):
    size = np.random.randint(150, 400)
    entropy = np.random.uniform(4.0, 6.5)
    suspicious = np.random.randint(1, 3)
    data.append([size, entropy, suspicious, 1])

# Critical samples
for i in range(100):
    size = np.random.randint(300, 800)
    entropy = np.random.uniform(6.0, 8.5)
    suspicious = np.random.randint(3, 6)
    data.append([size, entropy, suspicious, 1])

df = pd.DataFrame(data, columns=["size", "entropy", "suspicious_count", "label"])

X = df[["size", "entropy", "suspicious_count"]]
y = df["label"]

model = RandomForestClassifier(n_estimators=150)
model.fit(X, y)

if not os.path.exists("../models"):
    os.makedirs("../models")

joblib.dump(model, "../models/model.pkl")

print("Improved model trained and saved.")