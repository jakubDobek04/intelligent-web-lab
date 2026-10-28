from flask import Flask, jsonify, request
from recommender import recommend, df

app = Flask(__name__)


@app.route("/api/recommend")
def api_recommend():
    # --- walidacja ?title= ---
    title = request.args.get("title", "").strip()
    if not title:
        return jsonify({"error": "podaj parametr ?title=..."}), 400

    # --- walidacja ?top_n= (1-10) ---
    if "top_n" in request.args:
        n = request.args.get("top_n", type=int)
        if n is None or not 1 <= n <= 10:
            return jsonify({"error": "top_n musi byc z zakresu 1-10"}), 400
    else:
        n = 5

    # --- opcjonalny ?genre= (wyzwanie) ---
    genre = request.args.get("genre")
    if genre is not None:
        genre = genre.strip()
        if not genre:
            return jsonify({"error": "genre nie moze byc pusty"}), 400

    recs = recommend(title, top_n=n, genre=genre)

    # --- nieznany tytul -> 404 ---
    if recs is None:
        return jsonify({"error": "nie znam takiego filmu"}), 404

    return jsonify({
        "title": title,
        "count": len(recs),
        "recommendations": recs,
    })


@app.route("/api/movies")
def api_movies():
    """Lista wszystkich filmów — przyda się do frontendu (zadanie C)."""
    movies = [
        {
            "title": row["title"],
            "genres": row["genres"],
            "rating": round(float(row["rating"]), 1),
        }
        for _, row in df.iterrows()
    ]
    return jsonify({"count": len(movies), "movies": movies})


if __name__ == "__main__":
    app.run(debug=True)