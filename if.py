import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import joblib

# Load data
with open('mock_blockchain_transactions_large.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Label encode type, from, to
label_encoders = {}
for col in ['type', 'from', 'to']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Save to reuse this encoding later

# Prep features
X = df.drop(columns=['tx_hash'])  # Only drop pure identifier

# Train IF model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(X)

# Save model
joblib.dump(model, 'isolation_forest_model.pkl')

# Save encoders 
joblib.dump(label_encoders, 'label_encoders.pkl')

# Predict anomalies
df['anomaly'] = model.predict(X)
df['anomaly'] = df['anomaly'].map({1: 'authentic', -1: 'anomaly'})

# Save results
df.to_json('blockchain_anomaly_results_encoded.json', orient='records', indent=2)

print("Model, encoders, and results saved successfully.")
