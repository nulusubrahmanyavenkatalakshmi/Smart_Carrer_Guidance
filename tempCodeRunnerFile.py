from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# Load model and encoders
model = joblib.load("model/career_model.pkl")
mlb = joblib.load("model/mlb_skills.pkl")
le_interests = joblib.load("model/le_interests.pkl")
le_target = joblib.load("model/le_target.pkl")

# In-memory user store
users = {}

# Serve the home page
@app.route("/")
def serve_home():
    return send_from_directory(app.static_folder, "index.html")

# Serve signup page
@app.route("/signup-page")
def serve_signup():
    return send_from_directory(app.static_folder, "signup.html")

# Serve login page
@app.route("/login-page")
def serve_login():
    return send_from_directory(app.static_folder, "login.html")

# Signup API
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    users[username] = password
    return jsonify({"message": "Signup successful"}), 200

# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users.get(username) != password:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful"}), 200

# Predict API
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

# Serve static files like JS, CSS
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)