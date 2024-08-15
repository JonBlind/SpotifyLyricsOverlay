#Display Spotify Lyrics Above all Apps: PC. I Hope This Works -_- 

from PyQt6.QtWidgets import QApplication
from gui import LyricsApp
import sys
import lyricfetcher, nolookie, gui, spotify_api

def main():
    app = QApplication(sys.argv)
    window = LyricsApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":  
    main()