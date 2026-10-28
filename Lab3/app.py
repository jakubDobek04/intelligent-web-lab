from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask import Flask, jsonify, request, send_from_directory

if __package__:
    from .recommender import matrix, recommend, similar_users
else:
    from recommender import matrix, recommend, similar_users

app = Flask(__name__)

@app.route("/api/recommend")
def api_recommend():
    user = request.args.get("user", "").strip()
    if not user:
        return jsonify({"error": "podaj parametr ?user=..."}), 400

    try:
        k = int(request.args.get("k", 3))
    except ValueError:
        return jsonify({"error": "k musi byc liczba calkowita"}), 400
    if not (1 <= k <= 11):
        return jsonify({"error": "k musi byc w zakresie 1..11"}), 400

    recs = recommend(user, k=k)
    if recs is None:
        return jsonify({"error": "nie znam takiego użytkownika",
                        "known_users": sorted(matrix.index.tolist())}), 404
    return jsonify({"user": user, "k": k,
                    "count": len(recs), "recommendations": recs})

@app.route("/api/users")
def api_users():
    return jsonify({"count": len(matrix.index), "users": sorted(matrix.index.tolist())})


@app.route("/api/similar")
def api_similar():
    user = request.args.get("user", "").strip()
    if not user:
        return jsonify({"error": "podaj parametr ?user=..."}), 400
    s = similar_users(user)
    if s is None:
        return jsonify({"error": "nie znam takiego użytkownika"}), 404
    return jsonify({"user": user, "similar": s})



if __name__ == "__main__":
    app.run(debug=True)
