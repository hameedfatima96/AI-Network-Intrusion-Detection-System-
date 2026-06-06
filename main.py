import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ----------------------------
# 1. Load Dataset
# ----------------------------

columns = [
'duration','protocol_type','service','flag','src_bytes',
'dst_bytes','land','wrong_fragment','urgent','hot',
'num_failed_logins','logged_in','num_compromised','root_shell',
'su_attempted','num_root','num_file_creations','num_shells',
'num_access_files','num_outbound_cmds','is_host_login',
'is_guest_login','count','srv_count','serror_rate',
'srv_serror_rate','rerror_rate','srv_rerror_rate',
'same_srv_rate','diff_srv_rate','srv_diff_host_rate',
'dst_host_count','dst_host_srv_count',
'dst_host_same_srv_rate','dst_host_diff_srv_rate',
'dst_host_same_src_port_rate',
'dst_host_srv_diff_host_rate',
'dst_host_serror_rate','dst_host_srv_serror_rate',
'dst_host_rerror_rate','dst_host_srv_rerror_rate',
'label','difficulty'
]

file_path = os.path.join("dataset", "KDDTrain.txt")

df = pd.read_csv(file_path, header=None, names=columns)

print("Dataset Loaded Successfully!")
print(df.head())


# ----------------------------
# 2. Preprocessing
# ----------------------------

# Drop unnecessary column
df = df.drop(['difficulty'], axis=1)

# Encode categorical features
le = LabelEncoder()

for col in ['protocol_type', 'service', 'flag']:
    df[col] = le.fit_transform(df[col])

# Convert labels (normal = 0, attack = 1)
df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)


# ----------------------------
# 3. Split Data
# ----------------------------

X = df.drop('label', axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ----------------------------
# 4. Train Model
# ----------------------------

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# ----------------------------
# 5. Evaluate Model
# ----------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)


# ----------------------------
# 6. Save Model
# ----------------------------

joblib.dump(model, "nids_model.pkl")

print("\nModel Saved Successfully as nids_model.pkl")