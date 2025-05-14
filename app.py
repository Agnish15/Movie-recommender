import streamlit as st
import pickle
import pandas as pd
import requests

# Load preprocessed data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDb API key
API_KEY = 'a6c2e4115a404c76ac6d92dc5d8b4b84'

# Function to fetch poster from TMDb
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', "")

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:7]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommender System")

# Add a blank option at the top
movie_options = ['-- Select a Movie --'] + list(movies['title'].values)
selected_movie = st.selectbox("Enter the name of the movie", movie_options)

if st.button('Recommend'):
    if selected_movie == '-- Select a Movie --':
        st.warning("⚠️ Please select a movie first.")
    else:
        names, posters = recommend(selected_movie)
        cols = st.columns(len(names))
        for i, col in enumerate(cols):
            with col:
                st.markdown(
                    f"<div style='margin-bottom: 10px;height: 40px; font-size: 14px; text-align: center; overflow: hidden; padding:-4px'>{names[i]}</div>",
                    unsafe_allow_html=True
                )
                st.image(posters[i], use_container_width=True)
