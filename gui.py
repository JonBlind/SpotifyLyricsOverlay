from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QColor, QPalette
from spotify_api import get_current_track
from lyricfetcher import get_lyrics
import sys

class LyricsApp(QWidget):
    def __init__(self):
        super().__init__()

        # Window Title
        self.setWindowTitle("Spotify Lyrics")
        self.setGeometry(100, 100, 400, 300)  # Start at a small scale
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        
        self.setWindowOpacity(1.0)  # Set initial opacity to 100%

        # Fonts
        self.normal_font = QFont()
        self.normal_font.setPointSize(10)
        
        self.bold_font = QFont()
        self.bold_font.setPointSize(14)
        self.bold_font.setBold(True)

         # Initial colors
        self.default_bg_color = QColor("#1e1e1e")
        self.bg_color = self.default_bg_color
        self.text_color = QColor(255, 255, 255)

        # Layout
        self.layout = QVBoxLayout()

        # Add the exit button
        self.exit_btn = QPushButton("X", self)
        self.exit_btn.setFixedSize(30, 30)
        self.exit_btn.clicked.connect(self.close)

         # Add the invert colors button
        self.invert_colors_btn = QPushButton("Invert Colors", self)
        self.invert_colors_btn.setFixedSize(100, 30)
        self.invert_colors_btn.setCheckable(True)
        self.invert_colors_btn.setStyleSheet("QPushButton:checked { background-color: none; }")
        self.invert_colors_btn.clicked.connect(self.toggle_colors)

        # Add the buttons to a horizontal layout to place them at the top right
        self.top_layout = QHBoxLayout()
        self.top_layout.addStretch()  # Pushes the buttons to the right
        self.top_layout.addWidget(self.invert_colors_btn)
        self.top_layout.addWidget(self.exit_btn)

        # Add the top layout to the main layout
        self.layout.addLayout(self.top_layout)

        # Setup the previous_lyric section
        self.previous_lyric_label = QLabel("", self)
        self.previous_lyric_label.setWordWrap(True)
        self.previous_lyric_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.previous_lyric_label.setFont(self.normal_font)
        self.layout.addWidget(self.previous_lyric_label)

        # Setup the current_lyric section
        self.current_lyric_label = QLabel("", self)
        self.current_lyric_label.setWordWrap(True)
        self.current_lyric_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_lyric_label.setFont(self.bold_font)
        self.layout.addWidget(self.current_lyric_label)

        # Setup the next_lyrics section
        self.next_lyric_label = QLabel("", self)
        self.next_lyric_label.setWordWrap(True)
        self.next_lyric_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.next_lyric_label.setFont(self.normal_font)
        self.layout.addWidget(self.next_lyric_label)

        # Creates a slider that can control opacity from 0.1 to 1.0
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        self.layout.addWidget(self.opacity_slider)

        self.setLayout(self.layout)

        # Set the lyrics and update them when called
        self.lyrics_dict = {}
        self.current_track = None

        self.update_lyrics()

        # Variables for moving the window
        self.dragging = False
        self.drag_position = QPoint()

    def change_opacity(self, value):
        self.setWindowOpacity(value / 100)

    def toggle_colors(self):
        if self.invert_colors_btn.isChecked():
            self.bg_color = QColor(255, 255, 255)
            self.text_color = QColor(0, 0, 0)
        else:
            self.bg_color = self.default_bg_color
            self.text_color = QColor(255, 255, 255)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, self.bg_color)
        palette.setColor(QPalette.ColorRole.WindowText, self.text_color)
        self.setPalette(palette)

        # Update the text color for labels
        self.previous_lyric_label.setStyleSheet(f"color: {self.text_color.name()}")
        self.current_lyric_label.setStyleSheet(f"color: {self.text_color.name()}")
        self.next_lyric_label.setStyleSheet(f"color: {self.text_color.name()}")

    def update_lyrics(self):
        track, artist, progress = get_current_track()
        if track and artist:
            # If the track changed, get the current track again.
            if (track, artist) != self.current_track:
                self.current_track = (track, artist)
                self.lyrics_dict = get_lyrics(track, artist)
                # If the track and artist can't form an LRC, show an error message.
                if not self.lyrics_dict:
                    self.current_lyric_label.setText("No lyrics available for this song.")
                    self.previous_lyric_label.setText("")
                    self.next_lyric_label.setText("")
                    self.lyrics_dict = {}

            prev_lyric, current_lyric, next_lyric = self.get_current_lyric(progress)
            self.previous_lyric_label.setText(prev_lyric)
            self.current_lyric_label.setText(current_lyric)
            self.next_lyric_label.setText(next_lyric)
        else:
            self.previous_lyric_label.setText("Song Unidentified")
            self.current_lyric_label.setText("No Lyrics Available")
            self.next_lyric_label.setText("Try Another Song!")
        
        QTimer.singleShot(125, self.update_lyrics)  # Update every 125 milliseconds

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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()

    def resizeEvent(self, event):
        self.setGeometry(self.x(), self.y(), event.size().width(), event.size().height())
        event.accept()