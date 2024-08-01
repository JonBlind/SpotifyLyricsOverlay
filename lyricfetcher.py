#Utilizes syncedlyrics to obtain LRC formatted lyrics. Github: https://github.com/moehmeni/syncedlyrics
import syncedlyrics

def parse_lrc(lrc):
    lyrics_dict = {}
    #For every line in the lrc, split them
    for line in lrc.split('\n'):
        #If there is a line, split it based on the right bracket
        if line:
            parts = line.split(']')
            #If there is more than 1 part: implying correctness, split it
            #The first part, we ignore the left bracket and grab the rest for time.
            #The second, we grab every character after the right bracket. 
            if len(parts) > 1:
                time_str = parts[0][1:]
                lyric = parts[1].strip()
                #If there actually exists a lyric,
                #We split each time into minutes and seconds.
                #Multiply each minute by 60 seconds and add the seconds, multiply it by 1000 to reach ms.
                if lyric:
                    minutes, seconds = map(float, time_str.split(':'))
                    time_ms = int((minutes * 60 + seconds) * 1000)
                    lyrics_dict[time_ms] = lyric
    return lyrics_dict

def get_lyrics(track, artist):
    try:
        #Synced_Only show only songs with timestamps. 
        lrc = syncedlyrics.search(f"{track} {artist}", synced_only=True, providers=["Lrclib", "Musixmatch"])
        if lrc:
            return parse_lrc(lrc)
        else:
            return None
    except Exception as e:
        print(f"Error fetching lyrics(Likely No TimeStamps): {e}")
        return None
    
#Test
track = "Viva La Vida"
artist = "coldplay"

lyrics_dict = get_lyrics(track, artist)