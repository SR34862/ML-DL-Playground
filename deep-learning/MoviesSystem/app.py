import asyncio
import os
import pickle
import aiohttp
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_icon="🍿",
    page_title="Movie Recommender System",
    layout="wide"
)

@st.cache_data
def load_data():
    with open("movies.pkl", "rb") as file:
         movies = pickle.load(file)
    movies = pd.DataFrame(movies)
        
    with open("similarity.pkl", "rb") as file:
        similarity = pickle.load(file)
        
    return movies, similarity

def my_api_key():
    api_key = os.environ["MOVIES_API_KEY"]
    if not api_key:
        st.error("API key not found. Please check your .env file.")
        st.stop()
        
    return api_key

async def fetch_poster(session, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={my_api_key()}&language=en-US"
    try:
        async with session.get(url) as response:
            data = await response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        st.error(f"Error fetching poster for movie ID {movie_id}:{str(e)}")
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"
    
async def get_recommendations(movie, movies, similarity):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x:x[1])[1:6]
    async with aiohttp.ClientSession() as session:
        tasks = []
        recommended_movies_names = []
        for i in movies_list:
            movie_id = movies.loc[i[0]].movie_id
            recommended_movies_names.append(movies.loc[i[0]].title)
            tasks.append(fetch_poster(session, movie_id))
        recommended_movies_posters = await asyncio.gather(*tasks)
        return (recommended_movies_names, recommended_movies_posters)

def main():
    st.header("🎬 Movie Recommender System")
    
    with st.spinner("Loading Movie Data..."):
        movies, similarity = load_data()
        
    with st.sidebar:
        st.header("About")
        st.write("""
                 This movie recommender system suggests similar movies based on your selection.
                 It uses content based filtering to make recommendations.
                 """)
        st.metric("Total Movies", len(movies))
    
    movies_list = movies["title"].values
    selected_movie_name = st.selectbox(
        "Select a movie you like: ",
        movies_list,
        help="Choose a movie to get similar recommendations"
    )
    
    if st.button("Show Recommendations", type="primary"):
        with st.spinner("Finding similar movies..."):
            recommended_movies_names, recommended_movies_posters = asyncio.run(
                get_recommendations(selected_movie_name, movies, similarity)
            )
        st.subheader("Recommended Movies")
        cols = st.columns(5)
        for idx, (col, name, poster) in enumerate(zip(cols, recommended_movies_names, recommended_movies_posters)):
            with col:
                st.image(poster, caption="name", use_container_width=True)
                st.button("More Info", key=f"info{idx}", help="Click to learn more about {name}")
    
if __name__ == "__main__":
    main()
    
    