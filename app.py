import streamlit as st
import pandas as pd
import requests
import pickle

with open('movies_data.pkl','rb') as file:
    movies,cosine_sim=pickle.load(file)
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]
def fetch_poster(movie_title):
    api_key = '4c02aab5'
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    print("API Response:", data) 
    if 'Poster' in data and data['Poster'] != 'N/A':
        poster_path = data['Poster']
        print("Poster found:", poster_path) 
    else:
        poster_path = None
        print("No poster found.")  
    if poster_path:
        return poster_path
    else:
        return 'https://via.placeholder.com/130x200.png?text=No+Poster+Available'


st.title("movie recomendation system")
selected_movie=st.selectbox("choose a movie:",movies['title'].values)
if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 Recommended Movies:")
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]  
                poster_url = fetch_poster(movie_title)  
                    st.image(poster_url, width=130)  
                    st.write(movie_title)  #
