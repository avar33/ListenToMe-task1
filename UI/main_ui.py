from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QPushButton,
    QGridLayout
)
from types import SimpleNamespace
from functools import partial
from data_managers.data_loader import DataLoader
from search_managers.search_engine import SearchEngine
from export_recs import ExportRecs
from PySide6.QtUiTools import QUiLoader

# builds the ui that will be displayed on the main window 
def create_ui(window):
    ui = SimpleNamespace() #blank item
    ui.checkboxes = []
    descriptors = DataLoader.read_json("data_managers/json_files/data.json", 'descriptors')

    # reccomendation type selection boxes
    ui.artist_box = window.findChild(QCheckBox, "artistBox")
    ui.songs_box = window.findChild(QCheckBox, "songsBox")
    
    # fills out the prefrences 
    ui.pref_grid = window.findChild(QGridLayout, "preferenceGrid")
    if ui.pref_grid:
        cols = 5 
        for i, descriptor in enumerate(descriptors):
            row = i // cols
            col = i % cols
            checkbox = QCheckBox(descriptor)
            ui.checkboxes.append(checkbox)
            ui.pref_grid.addWidget(checkbox, row, col)

    # below are the rest of the elements from the ui base 
    ui.search_button = window.findChild(QPushButton, "searchButton")
    ui.save_button = window.findChild(QPushButton, "saveButton")
    ui.change_button = window.findChild(QPushButton, "changeUserButton")
    ui.current_user = window.findChild(QLabel, "userLabel")
    ui.artist_title = window.findChild(QLabel, "artistTitle")
    ui.artist_title.setHidden(True)
    ui.song_title = window.findChild(QLabel, "songTitle")
    ui.song_title.setHidden(True)
    ui.display_grid = window.findChild(QGridLayout, "displayGrid")

    search_engine = SearchEngine()
    ui.search_button.clicked.connect(
        partial(
            search_engine.search_clicked,
            ui.artist_box,
            ui.songs_box,
            ui.checkboxes,
            ui.display_grid,
            ui.artist_title,
            ui.song_title
        )
    )

    export_recs = ExportRecs(search_engine)
    ui.save_button.clicked.connect(
        partial(
            export_recs.save_list, 
            "Mia",
            "test.csv"
        )
    )


    return ui
