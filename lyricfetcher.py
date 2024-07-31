#Utilizes genius API to fetch lyrics:
import requests
from nolookie import MUSIXMATCH_API_TOKEN

def get_lyrics(track, artist):
    url = f"https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"
    params = {
        "q_track": track,
        "q_artist": artist,
        "apikey": MUSIXMATCH_API_TOKEN
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        status_code = data['message']['header']['status_code']
        if status_code == 200:
            return data['message']['body']['lyrics']['lyrics_body']
        elif status_code == 404:
            return "Lyrics not found."
        else:
            return f"Error: Received status code {status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
#Test
track = "Viva La Vida"
artist = "coldplay"

print(get_lyrics(track, artist))
