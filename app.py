import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

movies = None
ratings = None


def load_data():
    global movies, ratings

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    print("Loading datasets...")

    # ✅ Load movies
    try:
        movies = pd.read_csv(os.path.join(BASE_DIR, "dataset", "movies.csv"))
    except Exception as e:
        print("Error loading movies:", e)
        movies = pd.DataFrame(columns=["movie_id", "title", "genres"])

    # ✅ Load ratings from PHP API (ALWAYS FRESH)
    try:
        response = requests.get(
            "https://akarshkumar.gt.tc/get_ratings.php",
            timeout=10
        )

        data = response.json()

        if not data:
            print("No ratings found → using empty dataset")
            ratings = pd.DataFrame(columns=["user_id", "movie_id", "rating"])
        else:
            ratings = pd.DataFrame(data)

            # Convert safely
            ratings['user_id'] = pd.to_numeric(ratings['user_id'], errors='coerce')
            ratings['movie_id'] = pd.to_numeric(ratings['movie_id'], errors='coerce')
            ratings['rating'] = pd.to_numeric(ratings['rating'], errors='coerce')

            ratings = ratings.dropna()

    except Exception as e:
        print("Error fetching ratings:", e)
        ratings = pd.DataFrame(columns=["user_id", "movie_id", "rating"])

    print("Data loaded successfully")


@app.route('/')
def home():
    return "API is running ✅"


@app.route('/recommend', methods=['GET'])
def recommend():
    load_data()  # 🔥 ALWAYS reload fresh data

    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify(["No user provided"])

        user_id = int(user_id)

        # ✅ Get user's ratings
        user_ratings = ratings[ratings['user_id'] == user_id]

        # 🔥 CASE 1: No ratings → show popular movies
        if user_ratings.empty:

            if ratings.empty:
                return jsonify(movies.head(10)['title'].tolist())

            popular = (
                ratings.groupby('movie_id')['rating']
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .index
            )

            recommended = movies[movies['movie_id'].isin(popular)]
            return jsonify(recommended['title'].tolist())

        # 🔥 CASE 2: User has ratings

        rated_movie_ids = user_ratings['movie_id'].tolist()

        # Top 3 rated movies
        top_movies = user_ratings.sort_values(by='rating', ascending=False).head(3)
        top_movie_ids = top_movies['movie_id'].tolist()

        # Get genres of top movies
        top_genres = movies[movies['movie_id'].isin(top_movie_ids)]['genres']

        # Recommend based on similar genres (simple match)
        recommended = movies[
            (movies['genres'].isin(top_genres)) &
            (~movies['movie_id'].isin(rated_movie_ids))
        ]

        # 🔥 Fallback if not enough results
        if recommended.shape[0] < 10:
            extra = movies[~movies['movie_id'].isin(rated_movie_ids)]
            recommended = pd.concat([recommended, extra]).drop_duplicates()

        recommended = recommended.head(10)

        return jsonify(recommended['title'].tolist())

    except Exception as e:
        print("Error in recommend:", e)
        return jsonify(["Error occurred"]), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
