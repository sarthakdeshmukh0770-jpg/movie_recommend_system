import streamlit as st 
import pandas as pd 
import pickle 
import requests
@st.cache_data
def get_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": "d1c9d59a2d61e9c42e6dbf0f1d6ce1e2"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        print("TMDB Error:", response.status_code)
        return None

    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path is None:
        return None

    return f"https://image.tmdb.org/t/p/w500{poster_path}"


movie_dict=pickle.load(open('dict.pkl','rb'))
similarity_score=pickle.load(open('similarity.pkl','rb'))

movie=pd.DataFrame(movie_dict)

st.title('Movie Recommend System')

movie_name=st.selectbox('selecte movie here',movie['title'].values)

def recommend(movies):
    index=movie[movie['title']==movies].index[0]
    distance=similarity_score[index]
    recommend_movie=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movies=[]
    recommend_movie_poster=[]
    for i in recommend_movie:
         movie_id=movie.iloc[i[0]]['id']
         recommend_movies.append(movie.iloc[i[0]].title)
         #featch poster from api
         recommend_movie_poster.append(get_poster(movie_id))
    return recommend_movies ,recommend_movie_poster

if st.button('Recommend'):
    name,poster =recommend(movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.caption(name[i])
            st.image(poster[i])



    
