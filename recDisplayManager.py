import sys
import json
import requests

from io import BytesIO
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QMessageBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QWidget, 
    QGraphicsScene,
)

from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from functools import partial
from PySide6.QtCore import Qt
from searchEngine import SearchEngine

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
    def fill_display(self, item, row, col, is_song):
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
      
        
    #fill in the info for artists #TODO: maybe delete
    def fill_artist_display(self, artist, genre, descriptors, image_url, row, col):
        layout = QVBoxLayout()
        
        # --- Image ---
        pixmap = self.load_image(image_url, "images/noProfile.jpg")
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio) 
        image = QLabel()
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignCenter)
        image.setFixedSize(150, 150)

        # --- Labels ---
        main_label = QLabel(f"{artist}")
        artist_genre = QLabel(', '.join(genre))
        desc_label = QLabel(" | ".join(descriptors))

        layout.addWidget(image)
        layout.addWidget(main_label)
        layout.addWidget(artist_genre)
        layout.addWidget(desc_label)

        # wrap layout in a QWidget
        container = QWidget()
        container.setLayout(layout) 
        container.setStyleSheet("background-color: lightpink; font-family: 'Terminal';")
        self.grid.addWidget(container, row, col)
        

    #display in grid 
    def display_recs(self):
        #empty current display
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        col_next = 0
        col_max = 4
        if SearchEngine.display_what[0]: #artists
            if SearchEngine.display_what[1]:
                col_max = 2
            for i, (artist, score) in enumerate(SearchEngine.artist_rec_list):
                col = i % col_max
                current_row = (i // col_max)
                self.fill_display(self.grid, artist, current_row, col, False)
            col_next = 2 

        if SearchEngine.display_what[1]: #songs
            for i, (song, score) in enumerate(SearchEngine.song_rec_list):
                col = (i % col_max) + col_next
                current_row = i // col_max
                self.fill_display(self.grid, song, current_row, col, True)