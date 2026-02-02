import streamlit as st
import pickle
import pandas as pd
import requests

# ------------------ TMDB CONFIG ------------------
API_KEY = "601091ff350c847a8639bf1d8f1ff480"
BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# ------------------ FETCH POSTER ------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("poster_path"):
        return BASE_IMAGE_URL + data["poster_path"]
    else:
        return None

# ------------------ LOAD DATA ------------------
movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# ------------------ RECOMMEND FUNCTION ------------------
def recommend(movie_name):
    movie_index = movies[movies["title"] == movie_name].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# ------------------ STREAMLIT UI ------------------
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster not available")
