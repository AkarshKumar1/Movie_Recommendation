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

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

        # Get user's rated movies
        user_ratings = ratings[ratings['user_id'] == user_id]

        if user_ratings.empty:
            return jsonify(["No ratings found for user"])

        # Get top rated movie
        top_movie_id = user_ratings.sort_values(by='rating', ascending=False).iloc[0]['movie_id']

        # Recommend movies with similar IDs (simple logic)
        similar_movies = movies[movies['movie_id'] != top_movie_id].head(10)

        return jsonify(similar_movies['title'].tolist())

    except Exception as e:
        return jsonify(["Error occurred"]), 500


if __name__ == "__main__":
    app.run()
