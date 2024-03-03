import streamlit as st
import pickle
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=724a1aab08569827dd38a23c95b49ecb&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

    
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))


# Styling for headers
st.title("Movie Recommendation System")
st.markdown("---")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "What are you looking for today",
    movie_list
)

if st.button('Show Recommendations'):
    with st.spinner("Loading Recommendations..."):
        st.markdown("---")
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)

        # With this line
        cols = st.columns(5)

        # Then, update your code to use cols instead of col1, col2, col3, col4, col5
        with cols[0]:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with cols[1]:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with cols[2]:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with cols[3]:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with cols[4]:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])

        st.markdown("---")
        st.info("Enjoy your movie recommendations! 🍿")