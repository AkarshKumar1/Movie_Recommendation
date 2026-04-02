import mysql.connector
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Connect DB
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="movie_recommendation"
)

movies = pd.read_sql("SELECT * FROM movies", conn)
ratings = pd.read_sql("SELECT user_id, movie_id, rating FROM ratings", conn)

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

    user_ratings = movie_matrix.loc[user_id]

    # Get highest rated movie by user
    fav_movie = user_ratings.idxmax()

    similar_movies = similarity_df[fav_movie].sort_values(ascending=False).head(10).index

    recommended = movies[movies['movie_id'].isin(similar_movies)]['title']

    return jsonify(recommended.tolist())

if __name__ == '__main__':
    app.run(debug=True)