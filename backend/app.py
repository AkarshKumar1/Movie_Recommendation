import pandas as pd
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load dataset (from backend folder)
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pd.read_csv(os.path.join(BASE_DIR, "dataset", "movies.csv"))
ratings = pd.read_csv(os.path.join(BASE_DIR, "dataset", "ratings.csv"))

# Create pivot table
movie_matrix = ratings.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)

# Compute similarity
similarity = cosine_similarity(movie_matrix.T)

similarity_df = pd.DataFrame(similarity, index=movie_matrix.columns, columns=movie_matrix.columns)

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify(["No user provided"])

    user_id = int(user_id)

    if user_id not in movie_matrix.index:
        return jsonify(["User not found"])

    user_ratings = movie_matrix.loc[user_id]

    fav_movie = user_ratings.idxmax()

    similar_movies = similarity_df[fav_movie].sort_values(ascending=False).head(10).index

    recommended = movies[movies['movie_id'].isin(similar_movies)]['title']

    return jsonify(recommended.tolist())


if __name__ == "__main__":
    app.run()
