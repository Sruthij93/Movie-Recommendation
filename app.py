import streamlit as st
import pickle
import requests
import pandas as pd

# Function to fetch movie details from TMDB API
def fetch_movie_details(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=464b2949746d666c96b76e01946ecd3c&language=en-US')
    data = response.json()
    return {
        'poster': f"https://image.tmdb.org/t/p/w500/{data['poster_path']}",
        'overview': data.get('overview', 'No overview available.'),
        'release_date': data.get('release_date', 'Unknown'),
        'rating': data.get('vote_average', 'N/A')
    }

# Recommend movies function
def recommend(movie, num_recommendations):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    rec_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations + 1]

    recommended_movies = []
    recommended_details = []
    for i in rec_movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        details = fetch_movie_details(movie_id)
        recommended_movies.append({
            'title': movies.iloc[i[0]].title,
            'details': details
        })
    return recommended_movies

# Fetch movies by genre
def get_movies_by_genre(genre):
    response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key=464b2949746d666c96b76e01946ecd3c&with_genres={genre}')
    data = response.json()
    return [
        {
            'title': movie['title'],
            'poster': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}",
            'rating': movie.get('vote_average', 'N/A')
        }
        for movie in data['results']
    ]

# Get top-rated movies
def get_top_movies():
    response = requests.get('https://api.themoviedb.org/3/movie/top_rated?api_key=464b2949746d666c96b76e01946ecd3c&language=en-US&page=1')
    data = response.json()
    return [
        {
            'title': movie['title'],
            'poster': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}",
            'rating': movie.get('vote_average', 'N/A')
        }
        for movie in data['results']
    ]

# Load saved data
movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app structure
st.title("Enhanced Movie Recommender System") 

# Tabs for better UI
tab1, tab2, tab3 = st.tabs(["🎥 Recommend Movies", "🎭 Explore by Genre", "⭐ Top Movies"])

# Recommend Movies Tab
with tab1:
    st.header("Find movies similar to your favorite ones")
    selected_movie_name = st.selectbox('Select a movie:', movies_list)
    num_recommendations = st.slider('How many recommendations would you like?', 1, 10, 5)

    if st.button('Get Recommendations'):
        recommendations = recommend(selected_movie_name, num_recommendations)

        for movie in recommendations:
            st.subheader(movie['title'])
            st.image(movie['details']['poster'])
            st.write(f"**Overview**: {movie['details']['overview']}")
            st.write(f"**Release Date**: {movie['details']['release_date']}")
            st.write(f"**Rating**: {movie['details']['rating']}")

# Explore by Genre Tab
with tab2:
    st.header("Discover movies by genre")
    genres = {
        'Action': 28,
        'Comedy': 35,
        'Drama': 18,
        'Fantasy': 14,
        'Horror': 27,
        'Romance': 10749,
        'Science Fiction': 878
    }
    selected_genre = st.selectbox('Select a genre:', list(genres.keys()))

    if st.button('Find Movies'):
        genre_movies = get_movies_by_genre(genres[selected_genre])
        for movie in genre_movies:
            st.subheader(movie['title'])
            st.image(movie['poster'])
            st.write(f"**Rating**: {movie['rating']}")

# Top Movies Tab
with tab3:
    st.header("Top-Rated Movies")
    if st.button('Show Top Movies'):
        top_movies = get_top_movies()
        for movie in top_movies:
            st.subheader(movie['title'])
            st.image(movie['poster'])
            st.write(f"**Rating**: {movie['rating']}")
