import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import random

app = Flask(__name__)
CORS(app)


def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Load movies
    try:
        movies = pd.read_csv(os.path.join(BASE_DIR, "dataset", "movies.csv"))
    except:
        movies = pd.DataFrame(columns=["movie_id", "title", "genres"])

    # Load ratings from PHP API
    try:
        response = requests.get(
            "https://akarshkumar.gt.tc/get_ratings.php",
            timeout=10
        )
        data = response.json()

        if not data:
            ratings = pd.DataFrame(columns=["user_id", "movie_id", "rating"])
        else:
            ratings = pd.DataFrame(data)

            ratings['user_id'] = pd.to_numeric(ratings['user_id'], errors='coerce')
            ratings['movie_id'] = pd.to_numeric(ratings['movie_id'], errors='coerce')
            ratings['rating'] = pd.to_numeric(ratings['rating'], errors='coerce')

            ratings = ratings.dropna()

    except:
        ratings = pd.DataFrame(columns=["user_id", "movie_id", "rating"])

    return movies, ratings


@app.route('/')
def home():
    return "API Version FINAL (Dynamic Recommendations) ✅"


@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify(["No user provided"])

        user_id = int(user_id)

        movies, ratings = load_data()

        user_ratings = ratings[ratings['user_id'] == user_id]

        # 🔥 CASE 1: New user → random popular
        if user_ratings.empty:

            if ratings.empty:
                return jsonify(movies.sample(10)['title'].tolist())

            popular_ids = (
                ratings.groupby('movie_id')['rating']
                .mean()
                .sort_values(ascending=False)
                .head(20)
                .index
            )

            recommended = movies[movies['movie_id'].isin(popular_ids)]

            if recommended.empty:
                recommended = movies.sample(10)

            return jsonify(recommended.head(10)['title'].tolist())

        # 🔥 CASE 2: Existing user

        rated_movie_ids = user_ratings['movie_id'].tolist()

        # ⭐ Get top 5 rated movies
        top_movies = user_ratings.sort_values(by='rating', ascending=False).head(5)

        # ⭐ Get genres of these movies (if match exists)
        top_movie_ids = top_movies['movie_id'].tolist()

        matched_movies = movies[movies['movie_id'].isin(top_movie_ids)]

        genre_set = set()

        for g in matched_movies['genres']:
            for item in str(g).split('|'):
                genre_set.add(item.strip())

        # 🔥 If genres found → use them
        if genre_set:

            def match_genre(genres):
                return any(g in str(genres).split('|') for g in genre_set)

            recommended = movies[
                movies['genres'].apply(match_genre) &
                (~movies['movie_id'].isin(rated_movie_ids))
            ]

            if recommended.shape[0] >= 10:
                return jsonify(recommended.head(10)['title'].tolist())

            # 🔥 FINAL FALLBACK (only if no match)
            remaining = movies[~movies['movie_id'].isin(rated_movie_ids)]

            if remaining.empty:
                remaining = movies

            recommended = remaining.sample(min(10, len(remaining)))

            return jsonify(recommended['title'].tolist())

            # 🔥 FINAL FALLBACK (GUARANTEED DIFFERENT RESULTS)
            remaining = movies[~movies['movie_id'].isin(rated_movie_ids)]

            if remaining.empty:
                remaining = movies

            recommended = remaining.sample(min(10, len(remaining)))

            return jsonify(recommended['title'].tolist())

    except Exception as e:
        print("Error:", e)
        return jsonify(["Error occurred"]), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
