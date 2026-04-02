# 🎬 Movie Recommendation System

![Banner](screenshots/banner.png)

> A full-stack **Movie Recommendation System** that intelligently suggests movies to users based on their preferences and ratings.
> This project integrates **database management, backend development, and machine learning** to create a complete recommendation pipeline.
> Users can register, log in, rate movies, and receive personalized recommendations generated using **collaborative filtering algorithms** implemented in Python (Flask).
> The system demonstrates real-world concepts like **user-item interaction, REST API integration, and full-stack development**, all wrapped in a modern Netflix-inspired UI.

---

## 🚀 Features

* 🔐 User Authentication (Login / Register)
* 🎥 Browse Movies from Database
* ⭐ Rate Movies (1–5)
* 🎯 Personalized Recommendations (ML-based)
* 🔍 Search Movies
* 🌙 Modern Dark UI with Glassmorphism Design
* ⚡ Real-time recommendation system using Flask API

---

## 🧠 Tech Stack

| Layer            | Technology                           |
| ---------------- | ------------------------------------ |
| Frontend         | HTML, CSS, JavaScript                |
| Backend          | PHP                                  |
| Database         | MySQL                                |
| Machine Learning | Python (Flask, Pandas, Scikit-learn) |

---

## 📁 Project Structure

```plaintext id="yg8p8h"
movie_recommendation/
├── backend/
│   └── app.py                # Flask ML API
├── frontend/
│   ├── css/style.css        # UI styling
│   ├── js/script.js         # JavaScript
│   ├── partials/            # Header & Footer
│   ├── dashboard.php        # Main page
│   ├── login.php
│   ├── register.php
│   ├── rate.php
│   └── logout.php
├── dataset/                 # Movie dataset (CSV)
├── database/                # SQL schema / database files
├── screenshots/             # UI images (banner, login, register)
├── config.php
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash id="8f3z4m"
git clone https://github.com/your-username/movie-recommendation.git
cd movie-recommendation
```

---

### 2️⃣ Setup Database

* Open **phpMyAdmin / MySQL**
* Create database:

```sql id="zv1kpf"
CREATE DATABASE movie_recommendation;
```

* Import your dataset or SQL schema from `/database`

---

### 3️⃣ Start XAMPP

* Start **Apache**
* Start **MySQL**

---

### 4️⃣ Run Flask Backend

```bash id="c2m6rq"
cd backend
python app.py
```

👉 Runs at:

```id="91i4ks"
http://127.0.0.1:5000/
```

---

### 5️⃣ Open Project

```id="d1y3lc"
http://localhost/movie_recommendation/frontend/login.php
```

---

## 🤖 How It Works

* Uses **Collaborative Filtering**
* Builds a **User-Movie Rating Matrix**
* Applies **Cosine Similarity**
* Returns personalized movie recommendations via Flask API

---

## 🖼️ Screenshots

### 🔐 Login Page

![Login](screenshots/login-ui.png)

### 📝 Register Page

![Register](screenshots/register-ui.png)

### 🎥 Dashboard

![Dashboard](screenshots/dashboard-ui.png)

---

## 🎨 UI Highlights

* 🌙 Dark cinematic theme
* 🧊 Glassmorphism login/register forms
* 🔥 Hover animations (buttons & logout)
* 📦 Clean and structured layout

---

## 📊 Dataset

* MovieLens Dataset (Kaggle)
* Contains:

  * Movies
  * Ratings
  * Genres

---

## 💡 Future Improvements

* ⭐ Star-based rating system (UI)
* 🎞️ Movie posters integration
* 📱 Mobile responsiveness
* ⚡ Performance optimization (caching)
* 🤖 Advanced ML models

---

## 👨‍💻 Author

**Akarsh Kumar**
B.Tech (AI & ML)

---

⭐ If you like this project, don’t forget to star the repository!
