# gui.py
import tkinter as tk
from tkinter import ttk
from spotify_api import get_current_track
from lyricfetcher import get_lyrics
from tkinter import font

class LyricsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #Window Title
        self.title("Spotify Lyrics")
        self.geometry("400x300") #Start at a small scale
        self.attributes('-topmost', True)
        self.attributes('-alpha', 1.0)  # Set initial opacity to 80%

        self.normal_font = font.Font(size=10)
        self.bold_font = font.Font(size=14, weight='bold')

        #Setup the previous_lyric section.
        self.previous_lyric_label = ttk.Label(self, text="", wraplength=380, justify="center", font=self.normal_font)
        self.previous_lyric_label.pack(expand=True)

        #Setup the current_lyric section: Should be bolded and larger.
        self.current_lyric_label = ttk.Label(self, text="", wraplength=380, justify="center", font=self.bold_font)
        self.current_lyric_label.pack(expand=True)

        #Setup the next_lyrics section
        self.next_lyric_label = ttk.Label(self, text="", wraplength=380, justify="center", font=self.normal_font)
        self.next_lyric_label.pack(expand=True)

        #Creates a bar that can control opacity from 0.1 to 1.0. Do not set to 0 or else its impossible to revert without insane memory and luck.
        self.opacity_scale = ttk.Scale(self, from_=0.1, to=1.0, orient='horizontal', command=self.change_opacity)
        self.opacity_scale.set(1.0)
        self.opacity_scale.pack(fill='x')

        #Set the lyrics and update them when called.
        self.lyrics_dict = {}
        self.current_track = None
        self.update_lyrics()

    def change_opacity(self, value):
        self.attributes('-alpha', float(value))

    def update_lyrics(self):
        track, artist, progress = get_current_track()
        if track and artist:
            #If the track changed, get the current track again.
            if (track, artist) != self.current_track:
                self.current_track = (track, artist)
                self.lyrics_dict = get_lyrics(track, artist)
                #If the track and artist cant form an lrc, show error message.
                if not self.lyrics_dict:
                    self.current_lyric_label.config(text="No lyrics available for this song.")
                    self.previous_lyric_label.config(text="")
                    self.next_lyric_label.config(text="")
                    self.lyrics_dict = {}

            prev_lyric, current_lyric, next_lyric = self.get_current_lyric(progress)
            self.previous_lyric_label.config(text=prev_lyric)
            self.current_lyric_label.config(text=current_lyric)
            self.next_lyric_label.config(text=next_lyric)
        
        self.after(125, self.update_lyrics)  # Update every 125 milliseconds

    def get_current_lyric(self, progress):
        if not self.lyrics_dict:
            return "", "No lyrics available for this song.", ""

        lyrics_keys = sorted(self.lyrics_dict.keys())
        current_lyric = ""
        prev_lyric = ""
        next_lyric = ""
        for i, key in enumerate(lyrics_keys):
            if progress < key:
                if i > 0:
                    current_lyric = self.lyrics_dict[lyrics_keys[i-1]]
                    prev_lyric = self.lyrics_dict[lyrics_keys[i-2]] if i > 1 else ""
                else:
                    current_lyric = self.lyrics_dict[lyrics_keys[i]]
                next_lyric = self.lyrics_dict[key]
                break
        else:
            if lyrics_keys:
                prev_lyric = self.lyrics_dict[lyrics_keys[-2]] if len(lyrics_keys) > 1 else ""
                current_lyric = self.lyrics_dict[lyrics_keys[-1]]
                next_lyric = "[END]"

        return prev_lyric, current_lyric, next_lyric

