#Handling API
import os
import tempfile
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from nolookie import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
import time
import requests




# Retry mechanism decorator
def retry_on_exception(retries=3, delay=5, exception=Exception):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    print(f"Exception occurred: {e}. Retrying {attempt + 1}/{retries} in {delay} seconds...")
                    time.sleep(delay)
            print("Max retries reached. Function failed.")
            return None
        return wrapper
    return decorator

# Function to get a suitable cache path in the temp directory.
def get_cache_file():
    cache_dir = os.path.join(tempfile.gettempdir(), 'SpotifyLyrics')
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, '.cache') # Create the .cache

cache_path = get_cache_file()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = SPOTIFY_CLIENT_ID,
                                               client_secret= SPOTIFY_CLIENT_SECRET,
                                               redirect_uri= SPOTIFY_REDIRECT_URI,
                                               scope = "user-read-playback-state",
                                               cache_path=cache_path))


# Checks the status of the current token, if it expires grab a new token.
@retry_on_exception(retries=5, delay=5, exception=requests.exceptions.RequestException)
def ensure_token_valid():
    #Try to obtain a cached_token.
    token_info = sp.auth_manager.get_cached_token()

    # Check if the current token is valid or even exits. If not, generate new one.
    if not token_info or sp.auth_manager.is_token_expired(token_info):
        print("Token expired or not found, Grabbing new one...")
        sp.auth_manager.get_access_token()  


#Grab the current track that the spotify user is listening to.
@retry_on_exception(retries=5, delay=5, exception=requests.exceptions.RequestException)
def get_current_track():
    ensure_token_valid()
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
