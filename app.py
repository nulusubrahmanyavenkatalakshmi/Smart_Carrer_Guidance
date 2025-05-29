from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model and encoders
model = joblib.load("model/career_model.pkl")
mlb = joblib.load("model/mlb_skills.pkl")
le_interests = joblib.load("model/le_interests.pkl")
le_target = joblib.load("model/le_target.pkl")

# In-memory user store
users = {}

@app.route("/")
def home():
    return "✅ Smart Career Guidance API is running."

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    users[username] = password
    return jsonify({"message": "Signup successful"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users.get(username) != password:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        score10 = float(data["score10"])
        score12 = float(data["score12"])
        ugscore = float(data["ugscore"])
        interests = data["interests"].strip().lower()
        skills = [s.strip().capitalize() for s in data["skills"]]

        # Validate interest
        if interests not in le_interests.classes_:
            return jsonify({"error": "Interest not recognized"}), 400

        # Encode interest
        interest_encoded = le_interests.transform([interests])

        # Filter and encode skills
        valid_skills = [s for s in skills if s in mlb.classes_]
        skills_encoded = mlb.transform([valid_skills])

        # Combine all inputs
        features = np.hstack([[score10, score12, ugscore], interest_encoded, skills_encoded[0]])
        features = features.reshape(1, -1)

        # Predict
        pred = model.predict(features)
        recommended_career = le_target.inverse_transform(pred)[0]

        return jsonify({"recommended_career": recommended_career})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
