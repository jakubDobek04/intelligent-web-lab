import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies.csv")
df["overview"] = df["overview"].fillna("")
df = df.reset_index(drop=True)            # ← DODANE: indeks = pozycja w macierzy

print(df.shape)            # (24, 4)
print(df.head(3))          # pierwsze wiersze
print(df.isnull().sum())   # braki w kolumnach

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

print(tfidf_matrix.shape)   # (24 filmy, N unikalnych słów)

sim_matrix = cosine_similarity(tfidf_matrix)   # 24 x 24, każdy z każdym

def recommend(title, top_n=5, genre=None):    # ← DODANY parametr genre
    match = df[df["title"].str.lower() == title.lower()]
    if match.empty:
        return None

    idx = match.index[0]
    scores = sorted(enumerate(sim_matrix[idx]), key=lambda x: x[1], reverse=True)

    genre_norm = genre.strip().lower() if genre else None

    out = []
    for i, s in scores:
        if i == idx:
            continue

        # ← DODANY filtr gatunku (przed obcięciem do top_n)
        if genre_norm:
            film_genres = [g.strip().lower() for g in str(df.loc[i, "genres"]).split("|")]
            if genre_norm not in film_genres:
                continue

        out.append({
            "title":  df.loc[i, "title"],
            "genres": df.loc[i, "genres"],
            "rating": round(float(df.loc[i, "rating"]), 1),
            "score":  round(float(s), 3),
        })
        if len(out) == top_n:
            break

    return out