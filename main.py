import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st.set_page_config(page_title="DiscoverSounds",
                  page_icon="🎶",
                  layout="centered",
                  initial_sidebar_state="auto",)
st.header('🎶Music Recommendation System')
st.write("Discover new music effortlessly with our Music Recommendation System. Input a song you love, and our system will provide you with a handpicked selection of 5 similar songs, making it easy to expand your musical horizons. Whether you're looking for songs in the same genre or with a similar mood, our recommendation system has you covered. Explore a world of music right at your fingertips and find your next favorite track today.")
# Create the top bar with elements
st.sidebar.title('DiscoverSounds Menu')
st.sidebar.write('Let us present ourselves : we are a group of ambitious students from Efrei Paris, a french engineering school. We are currently studying in the 2025 promotion. We are majoring in Analytics and Business Intelligence, and this app was a challenge for us to improve our skills in Data Science.')
st.sidebar.image('logo efrei.png', use_column_width=True)




CLIENT_ID = '1a2c9eb891224ec4b7b65e26b8b74574'
CLIENT_SECRET = 'eda7b316eb56462da8a8fbda90289330'

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


def recommend(song_name):
    recommended_music_names = []
    recommended_music_posters = []

    if song_name in music['Name'].values:
        index = music[music['Name'] == song_name].index[0]
        distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)
        recommended_song_set = set()  # To keep track of recommended songs
        for distance in distances:
            if len(recommended_music_names) >= 5:
                break  # We have enough recommendations

            artist = music.iloc[distance[0]]['Artist']
            recommended_song_name = music.iloc[distance[0]]['Name']

            if recommended_song_name != song_name:
                recommended_music_posters.append(get_song_album_cover_url(recommended_song_name, artist))
                recommended_music_names.append(recommended_song_name)

    return recommended_music_names, recommended_music_posters

music_list = music['Name'].values
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    for i in range(5):
        if i < len(recommended_music_names):
            with col1 if i % 5 == 0 else col2 if i % 5 == 1 else col3 if i % 5 == 2 else col4 if i % 5 == 3 else col5:
                st.text(recommended_music_names[i])
                st.image(recommended_music_posters[i])
                st.markdown(
                    f"[Play on Spotify](https://open.spotify.com/search/{recommended_music_names[i].replace(' ', '%20')})",
                    unsafe_allow_html=True)
        else:
            break

