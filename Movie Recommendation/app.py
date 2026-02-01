import streamlit as st
import pickle

# Load data safely
with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

st.title("🎬 Movie Recommendation System")

movies_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movies_list)


def recommend(movie):
    # Get index directly (no lower() needed since selectbox gives exact title)
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.warning("Movie not found")
        return []

    distances = sorted(
        list(enumerate(similarity[index])),
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


if st.button("Show Recommendations"):
    recommendations = recommend(selected_movie)

    if recommendations:
        cols = st.columns(len(recommendations))
        for col, movie in zip(cols, recommendations):
            with col:
                st.text(movie)
