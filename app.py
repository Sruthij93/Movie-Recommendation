import streamlit as st
import pickle
import requests

def recommend(movie, num_recommendations):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # rec_movies_list = sorted(list(enumerate(distances)), reverse = True, key=lambda x:x[1])[1:6]

    
    rec_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations + 1]

    recommended_movies = []
    recommended_movie_posters = []
    for i in rec_movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        details = fetch_movie_details(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title, 'details': details)
    return recommended_movies, recommended_movie_posters    

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

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=464b2949746d666c96b76e01946ecd3c&language=en-US'.format(movie_id))
    data = response.json()
    poster = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return poster


movies= pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System") 
# Tabs for better UI
tab1, tab2, tab3 = st.tabs(["🎥 Recommend Movies", "🎭 Explore by Genre", "⭐ Top Movies"])
selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies_list)

# if st.button('Recommend'):    
#     names, posters = recommend(selected_movie_name)
    

#     col1, col2, col3, col4, col5 = st.columns(5)

#     with col1:
#         st.text(names[0])
#         st.image(posters[0])

#     with col2:
#         st.text(names[1])
#         st.image(posters[1])

#     with col3:
#         st.text(names[2])
#         st.image(posters[2])

#     with col4:
#         st.text(names[3])
#         st.image(posters[3])    
    
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])          

num_recommendations = st.slider('How many recommendations would you like?', 1, 10, 5)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, num_recommendations)

    if names and posters:
        cols = st.columns(len(names))
        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])
                st.image(posters[idx])

