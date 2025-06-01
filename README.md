# Smart_Carrer_Guidance
# 🎓 Smart Career Guidance System

🚀 [Live Demo](https://smart-carrer-guidance.onrender.com)

## 📌 Problem Statement

In today's dynamic job market, students often face confusion and lack proper guidance when choosing a suitable career path. Traditional counseling methods are often generic and do not account for a student's personal interests, skills, and academic background. There is a need for a data-driven solution that can personalize career recommendations.

## 🎯 Project Objective

To develop an intelligent web-based system that recommends suitable career paths for students based on their:

- Academic performance (10th, 12th, UG scores)
- Interests
- Skills

This system leverages **machine learning** to make personalized predictions and provides a user-friendly interface for interaction.

---

## 🧠 How It Works

1. **User Authentication**:
   - Users can sign up and log in securely using a basic credential system.

2. **Input Form**:
   - The user enters their academic scores, selects their interests, and chooses relevant skills.

3. **Prediction Process**:
   - The backend uses a **trained Random Forest Classifier** model.
   - The model processes the input and predicts the most suitable career option.

4. **Output**:
   - The predicted career is displayed to the user.

---

## 🔍 Machine Learning Model

- **Model**: `RandomForestClassifier`
- **Dataset**: Custom dataset with features like:
  - Academic scores (10th, 12th, UG)
  - Interests (e.g., Artificial Intelligence, Design, etc.)
  - Skills (e.g., Python, HTML, Data Analysis, etc.)
- **Encoding**:
  - Interests → `LabelEncoder`
  - Skills → `MultiLabelBinarizer`
- **Output**: Career recommendation based on combined input features

---

## 🌐 Web Application Overview

### ➤ Frontend
- HTML, CSS, JavaScript
- Pages:
  - `index.html`: Home/Prediction form
  - `signup.html`: User signup
  - `login.html`: User login

### ➤ Backend
- Python (Flask)
- REST API for:
  - Login/Signup
  - Career prediction
- CORS enabled for frontend-backend communication
- Model and encoders are loaded using `joblib`


---

## 🌍 Deployment

- Platform: [Render](https://render.com)
- Live App: [https://smart-carrer-guidance.onrender.com](https://smart-carrer-guidance.onrender.com)

---

## 🛠️ Technologies Used

| Area       | Tools/Libraries                     |
|------------|--------------------------------------|
| Frontend   | HTML, CSS, JavaScript                |
| Backend    | Flask, Python, joblib                |
| ML Model   | RandomForestClassifier, scikit-learn |
| Deployment | Render                               |

---

## ✅ Features

- 🔐 User authentication (Signup/Login)
- 📊 ML-powered career predictions
- 🌈 Clean and responsive UI
- 🧠 Personalized recommendations

---






