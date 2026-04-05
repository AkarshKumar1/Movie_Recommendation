import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

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
    return "API is running ✅"


@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify(["No user provided"])

        user_id = int(user_id)

        movies, ratings = load_data()  # 🔥 always fresh data

        user_ratings = ratings[ratings['user_id'] == user_id]

        # 🔥 CASE 1: No ratings → popular movies
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

        # Top 3 movies
        top_movies = user_ratings.sort_values(by='rating', ascending=False).head(3)
        top_movie_ids = top_movies['movie_id'].tolist()

        # 🔥 CORRECT GENRE MATCHING
        top_genres_list = movies[movies['movie_id'].isin(top_movie_ids)]['genres'].tolist()

        genre_set = set()
        for g in top_genres_list:
            for item in str(g).split('|'):
                genre_set.add(item.strip())

        def match_genre(genres):
            return any(g in genre_set for g in str(genres).split('|'))

        recommended = movies[
            movies['genres'].apply(match_genre) &
            (~movies['movie_id'].isin(rated_movie_ids))
        ]

        # 🔥 fallback if less results
        if recommended.shape[0] < 10:
            extra = movies[~movies['movie_id'].isin(rated_movie_ids)]
            recommended = pd.concat([recommended, extra]).drop_duplicates()

        recommended = recommended.head(10)

        return jsonify(recommended['title'].tolist())

    except Exception as e:
        print("Error:", e)
        return jsonify(["Error occurred"]), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
