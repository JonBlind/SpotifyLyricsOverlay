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
    if current_track and current_track.get('item'):
        name = current_track['item'].get('name')
        artist = current_track['item']['artists'][0].get('name') if current_track['item']['artists'] else None
        progress = current_track.get('progress_ms', 0)
        
        # Ensure name and artist are not None before returning
        if name and artist:
            return name, artist, progress
    
    # Default to no track found
    return None, None, None
