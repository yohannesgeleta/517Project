import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

df = pd.read_csv("/home/yxg5342/Documents/Python/combined_fraud.csv")
df.drop('Unnamed: 0', axis = 1, inplace= True)


label_encoder = LabelEncoder()
df['From'] = label_encoder.fit_transform(df['From'])
df['To'] = label_encoder.fit_transform(df['To'])

df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], unit='s').astype(int) / 10**9

df = df.fillna(0)

features = ['BlockHeight', 'TimeStamp', 'From', 'To']

X = df[features]

model = IsolationForest(contamination=0.02, random_state=42)
model.fit(X)

df['anomaly'] = model.predict(X)
df['fraud'] = df['anomaly'].apply(lambda x : 1 if x == -1 else 0)

print(df['fraud'].value_counts())
