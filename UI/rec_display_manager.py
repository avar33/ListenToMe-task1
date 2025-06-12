import requests

from io import BytesIO
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class RecDisplayManager:
    def __init__(self, display_grid):
        self.grid = display_grid

    # image handling from URLs
    def load_image(self, url, default):
        pixmap = QPixmap()

        if url.startswith("http"):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    pixmap.loadFromData(image_data.read())
                else:
                    pixmap.load(default)
            except Exception as e:
                print(f"Error loading image from URL: {e}")
                pixmap.load(default)
        else:
            pixmap.load(url)

        return pixmap

    #fill anf format the info of each item in a grid square layout
    def fill_display(self, item, row, col, is_song = False):
        layout = QVBoxLayout()
        
        # --- Image ---
        pixmap = self.load_image(item["image"], "images/record.jpg")
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio) 
        image = QLabel()
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignCenter)
        image.setFixedSize(150, 150)

        # --- Labels ---
        if is_song:
            main_label = QLabel(f"{item['title']}")
            artist_genre = QLabel(f"by {item['artist']} - {', '.join(item['genre'])}")
            desc_label = QLabel(" | ".join(item['descriptors']))
        else: 
            main_label = QLabel(f"{item['artist']}")
            artist_genre = QLabel(', '.join(item['genre']))
            desc_label = QLabel(" | ".join(item['descriptors']))

        layout.addWidget(image)
        layout.addWidget(main_label)
        layout.addWidget(artist_genre)
        layout.addWidget(desc_label)

        # wrap layout in a QWidget and add the widget to the grid
        container = QWidget()
        container.setLayout(layout) 
        if not is_song:
            container.setStyleSheet("background-color: lightpink; font-family: 'Terminal';")
        self.grid.addWidget(container, row, col)
   

    #display recommendations in grid 
    def display_recs(self, artist_rec_list, song_rec_list, display_what):
        #empty current display
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        col_next = 0
        col_max = 4
        if display_what[0]: #artists
            if display_what[1]:
                col_max = 2
            for i, (artist, score) in enumerate(artist_rec_list):
                col = i % col_max
                current_row = (i // col_max)
                self.fill_display(artist, current_row, col, is_song=False)
            col_next = 2 

        if display_what[1]: #songs
            for i, (song, score) in enumerate(song_rec_list):
                col = (i % col_max) + col_next
                current_row = i // col_max
                self.fill_display(song, current_row, col, is_song=True)