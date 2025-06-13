from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QPushButton,
    QGridLayout
)
from types import SimpleNamespace
from functools import partial
from PySide6.QtUiTools import QUiLoader

from data_managers.data_loader import DataLoader
from search_managers.search_engine import SearchEngine
from export_recs import ExportRecs
from UI.change_user import ChangeUser

class MainUI:
    def __init__(self, window):
        self.window = window
        self.ui = SimpleNamespace()
        self.search_engine = SearchEngine()
        self.export_recs = ExportRecs(self.search_engine)
        self.loader = QUiLoader()

        self.load_elements()
        self.setup_preferences()
        self.connect_signals()

    def load_elements(self):
        # get base elements from UI
        self.ui.artist_box = self.window.findChild(QCheckBox, "artistBox")
        self.ui.songs_box = self.window.findChild(QCheckBox, "songsBox")
        self.ui.pref_grid = self.window.findChild(QGridLayout, "preferenceGrid")
        self.ui.search_button = self.window.findChild(QPushButton, "searchButton")
        self.ui.save_button = self.window.findChild(QPushButton, "saveButton")
        self.ui.change_button = self.window.findChild(QPushButton, "changeUserButton")
        self.ui.current_user = self.window.findChild(QLabel, "userLabel")
        self.ui.artist_title = self.window.findChild(QLabel, "artistTitle")
        self.ui.song_title = self.window.findChild(QLabel, "songTitle")
        self.ui.display_grid = self.window.findChild(QGridLayout, "displayGrid")

        # set initial visibility
        self.ui.artist_title.setHidden(True)
        self.ui.song_title.setHidden(True)

        # list of descriptor checkboxes
        self.ui.checkboxes = []

    def setup_preferences(self):
        descriptors = DataLoader.read_json("data_managers/json_files/data.json", "descriptors")
        if self.ui.pref_grid:
            cols = 5
            for i, descriptor in enumerate(descriptors):
                row = i // cols
                col = i % cols
                checkbox = QCheckBox(descriptor)
                self.ui.checkboxes.append(checkbox)
                self.ui.pref_grid.addWidget(checkbox, row, col)

    def connect_signals(self):
        # search button logic
        self.ui.search_button.clicked.connect(
            partial(
                self.search_engine.search_clicked,
                self.ui.artist_box,
                self.ui.songs_box,
                self.ui.checkboxes,
                self.ui.display_grid,
                self.ui.artist_title,
                self.ui.song_title
            )
        )

        # save button logic
        self.ui.save_button.clicked.connect(
            lambda: self.export_recs.save_list(self.ui.current_user.text(), self.search_engine.get_prefrences())
        )

        # change user dialog logic
        change_user_window = self.loader.load("UI/change_user.ui", None)
        self.change_user = ChangeUser(change_user_window)
        self.ui.change_button.clicked.connect(self.change_user.show_change_user_dialog)

        # ensure username changes after signal from change_user
        self.change_user.username_changed.connect(self.set_username)

    def set_username(self, username):
        self.ui.current_user.setText(username)
        print(self.ui.current_user.text())

    def get_ui(self):
        return self.ui
