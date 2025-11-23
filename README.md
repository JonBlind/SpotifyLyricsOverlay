# Spotify Lyrics Overlay

This application connects to your Spotify account and overlays the lyrics of the currently playing song on your screen. It's designed to be lightweight and simple, offering essential features like dark/light mode, opacity adjustments, and the ability to switch between multiple lyric providers.

## Features

- **Spotify Integration**: Automatically fetches the lyrics of the song currently playing on Spotify.
- **Overlay**: Displays lyrics on top of all other windows.
- **Invert Colors**: Toggle between dark mode and light mode for easier readability.
- **Cycle Lyric Providers**: Switch between four different LRC (Lyric) providers to find the most accurate or preferred source.
- **Adjustable Opacity**: Modify the transparency of the lyrics overlay to your preference.

## Installation
ON WINDOWS:\
Download the .exe from [here](https://github.com/JonBlind/SpotifyLyricsOverlay/releases/tag/1.0.0) and simply run it.
<br>
<br>
OR  
<br>
<br>
Clone the repo or download the zip and move the .exe wherever you like. Running the .exe should start the program.

```bash
git clone https://github.com/JonBlind/SpotifyLyricsOverlay
```

ON LINUX/MAC:  
Not Yet Supported!


Compiled via Powershell with the following command:
```powershell
pyinstaller --onefile --noconsole --icon=".\imgs\icon.ico" pyinstaller.py
```


## How To Use
Open the Application. It will take you to the Spotify login and ask to link your account. Start playing a song and the lyrics will appear in the overlay window.

- LRC Cycle will swap the LRC provider to 1 of 4 providers based on the syncedlyrics API  
 *This may greatly slow down the application until the app completely syncs to the new LRC.*
- The Invert Color button simply inverts the color scheme. It should start in dark mode, and will swap to light mode if pressed.
- The opacity meter will alter the opacity of the ENTIRE window. So be careful!
- The software was made with the purpose of being overlayed over all applications. So there is NO feature to stop that.
- There is no way to change the size of the window yet. May be added soon.
- The program accesses your temp files to create a directory for storing .cache for API calls. 

## Dependencies
Spotipy Library: https://github.com/spotipy-dev/spotipy \
syncedlyrics API: https://github.com/moehmeni/syncedlyrics


Feel free to open issues or submit pull requests if you'd like to contribute to this project.


## License

[MIT](https://choosealicense.com/licenses/mit/)
