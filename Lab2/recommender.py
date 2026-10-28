import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Wczytanie danych ---
df = pd.read_csv("movies.csv")
df["overview"] = df["overview"].fillna("")

# --- 2. TF-IDF: tekst -> wektory ---
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

# --- 3. Macierz podobieństw 24x24 ---
sim_matrix = cosine_similarity(tfidf_matrix)


def recommend(title, top_n=5, genre=None):
    """Zwraca top_n najbardziej podobnych filmów do `title`.

    genre=None -> bez filtra gatunku
    genre="action" -> tylko filmy, których genres zawiera "action"
    Zwraca None, gdy tytułu nie ma w bazie.
    """
    match = df[df["title"].str.lower() == title.lower()]
    if match.empty:
        return None

    idx = match.index[0]

    # sortujemy podobieństwa malejąco
    scores = sorted(
        enumerate(sim_matrix[idx]),
        key=lambda x: x[1],
        reverse=True,
    )

    results = []
    for i, s in scores:
        if i == idx:                 # pomijamy film zapytania
            continue
        if genre:                    # filtr gatunku (wyzwanie)
            if genre.lower() not in str(df["genres"][i]).lower():
                continue
        results.append({
            "title": df["title"][i],
            "genres": df["genres"][i],
            "rating": round(float(df["rating"][i]), 1),
            "score": round(float(s), 3),
        })
        if len(results) >= top_n:
            break

    return results


if __name__ == "__main__":
    # szybki test bez serwera
    print("Rekomendacje dla 'Inception':")
    for r in recommend("Inception"):
        print(f"  {r['score']:.3f}  {r['title']}  [{r['genres']}]")

    print("\nRekomendacje dla 'Inception' (genre=action):")
    for r in recommend("Inception", genre="action"):
        print(f"  {r['score']:.3f}  {r['title']}  [{r['genres']}]")