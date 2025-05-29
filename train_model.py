import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

# Load dataset
df = pd.read_csv("dataset/smart_career_guidance_dataset_v4.csv")
print(df["Recommended_Career"].value_counts())
print(df['Interests'].value_counts())
print(df['Skills'].value_counts())

# Drop rows with any missing essential values
df.dropna(subset=['10th_score', '12th_score', 'UG_score', 'Interests', 'Skills', 'Recommended_Career'], inplace=True)

# Normalize interests and skills
df['Interests'] = df['Interests'].str.strip().str.lower()

# Normalize and split skills into list
df['Skills'] = df['Skills'].apply(lambda x: [s.strip().capitalize() for s in x.split(',') if s.strip()])

# Prepare feature sets
X_skills = df['Skills']
X_interests = df['Interests']
X_scores = df[['10th_score', '12th_score', 'UG_score']]

# Encode skills using MultiLabelBinarizer
mlb = MultiLabelBinarizer()
X_skills_encoded = mlb.fit_transform(X_skills)

# Encode interests using LabelEncoder
le_interests = LabelEncoder()
X_interests_encoded = le_interests.fit_transform(X_interests).reshape(-1, 1)

# Combine all features
X = np.hstack([X_scores.values, X_interests_encoded, X_skills_encoded])

# Encode target
le_target = LabelEncoder()
y = le_target.fit_transform(df['Recommended_Career'])

# Train the model
clf = RandomForestClassifier(n_estimators=150, random_state=42)
clf.fit(X, y)

# Save the model and encoders
joblib.dump(clf, "model/career_model.pkl")
joblib.dump(mlb, "model/mlb_skills.pkl")
joblib.dump(le_interests, "model/le_interests.pkl")
joblib.dump(le_target, "model/le_target.pkl")

print("✅ Model and encoders saved successfully.")
