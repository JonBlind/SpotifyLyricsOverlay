#Handling API
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from nolookie import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = SPOTIFY_CLIENT_ID,
                                               client_secret= SPOTIFY_CLIENT_SECRET,
                                               redirect_uri= SPOTIFY_REDIRECT_URI,
                                               scope = "user-read-playback-state"))

#Grab the current track that the spotify user is listening to.
def get_current_track():
    current_track = sp.current_playback()
    #If I successfully get a new track:
    #Return name, artist, and the song progress in ms. 
    if current_track:
        name = current_track['item']['name']
        artist = current_track['item']['artists'][0]['name']
        progress = current_track['progress_ms']
        return name, artist, progress
    return None, None, None

