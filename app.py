import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

movies = None
ratings = None
data_loaded = False


def load_data():
    global movies, ratings, data_loaded

    if data_loaded:
        return

    BASE_DIR = os.path.dirname(os.path.abspath(_file_))

    print("Loading datasets...")

    movies = pd.read_csv(os.path.join(BASE_DIR, "dataset", "movies.csv"))
    ratings = pd.read_csv(os.path.join(BASE_DIR, "dataset", "ratings.csv"))

    data_loaded = True
    print("Data loaded successfully")


@app.route('/')
def home():
    return "API is running ✅"


@app.route('/recommend', methods=['GET'])
def recommend():
    load_data()

    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify(["No user provided"])

        user_id = int(user_id)

        # Get user's ratings
        user_ratings = ratings[ratings['user_id'] == user_id]

        # 🔥 NEW USER CASE
        if user_ratings.empty:
            # return top popular movies
            popular = ratings.groupby('movie_id')['rating'].mean().sort_values(ascending=False).head(10)
            recommended = movies[movies['movie_id'].isin(popular.index)]
            return jsonify(recommended['title'].tolist())

        # Movies already rated
        rated_movie_ids = user_ratings['movie_id'].tolist()

        # Get top 3 highest rated movies by user
        top_movies = user_ratings.sort_values(by='rating', ascending=False).head(3)
        top_movie_ids = top_movies['movie_id'].tolist()

        # Get genres of top movies
        top_genres = movies[movies['movie_id'].isin(top_movie_ids)]['genres']

        # Recommend based on similar genres
        recommended = movies[
            (movies['genres'].isin(top_genres)) &
            (~movies['movie_id'].isin(rated_movie_ids))
        ]

        # If not enough recommendations → fallback
        if recommended.shape[0] < 10:
            extra = movies[~movies['movie_id'].isin(rated_movie_ids)]
            recommended = pd.concat([recommended, extra]).drop_duplicates()

        recommended = recommended.head(10)

        return jsonify(recommended['title'].tolist())

    except Exception as e:
        print("Error:", e)
        return jsonify(["Error occurred"]), 500


if __name__ == "_main_":
    app.run(host="0.0.0.0", port=10000)
