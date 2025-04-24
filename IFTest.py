import pandas as pd
from sklearn.metrics import classification_report  # optional
import joblib  # or import pickle if you used pickle

# --- Load CSV ---
csv_file_path = 'test_data.csv'  # Change this to your actual test CSV
df = pd.read_csv(csv_file_path)

# --- Preprocessing (optional, edit based on your model) ---
# For example: df = pd.get_dummies(df)
# Or encode strings if needed

# If there’s a target column you want to evaluate against:
# X = df.drop('target_column', axis=1)
# y = df['target_column']
# If unsupervised (like Isolation Forest):
X = df.select_dtypes(include='number')  # Use numeric columns only

# --- Load Saved Model ---
model = joblib.load('model.pkl')  # Replace with your model path

# --- Make Predictions ---
predictions = model.predict(X)

# --- Optional: Show Results ---
print("Predictions:\n", predictions)

# If you have ground-truth labels and want evaluation:
#print("Classification Report:\n", classification_report(y, predictions))
