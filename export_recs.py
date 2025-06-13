import csv 
import os

from UI.ui_helpers import createErrorAlert
from PySide6.QtWidgets import QMessageBox

class ExportRecs:
    def __init__(self, search_engine):
        self.search_engine = search_engine
        self.artist_rec_list = []
        self.song_rec_list = []

    #writes certain feilds into a csv file for the user to reference later 
    def write_to_csv(self, user, filename, list, is_song):
        folder_path = os.path.join("saved_recs", user)
        os.makedirs(folder_path, exist_ok=True)
        filepath= os.path.join(folder_path, filename)

        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if is_song:
                writer.writerow(["Song", " Artist", " Genres", " Descriptors", " Score"])
            else:
                writer.writerow(["Artist", " Genres", " Descriptors", " Score"])

            for item, score in list:
                if not is_song:
                    writer.writerow([
                        f" {item['artist']} ",
                        f" {', '.join(item['genre'])} ",
                        f" {', '.join(item['descriptors'])} "
                    ])
                else:
                    writer.writerow([
                        f" {item['title']} ",
                        f" {item['artist']} ",
                        f" {', '.join(item['genre'])} ",
                        f" {', '.join(item['descriptors'])} "
                    ])

    # manages saving the list when the user clicks the button 
    def save_list(self, username, descriptors):
        username_clean = username.strip()
        if username_clean == "":
            createErrorAlert("No user has been set. Please change your username to save your recommendations.")
            return
        else: 
            self.artist_rec_list = self.search_engine.get_artist_list()
            self.song_rec_list = self.search_engine.get_song_list()

            if(len(self.artist_rec_list)):
                filename = "_artists" + descriptors + ".csv"
                try:
                    self.write_to_csv(username_clean, filename, self.artist_rec_list, False)
                    QMessageBox.information(None, "Success", "Artist recommendations saved successfully!")
                except Exception as e:
                    createErrorAlert(f"Failed to save artist recommendations:\n{e}")

            if(len(self.song_rec_list)):
                filename = "_songs" + descriptors + ".csv"
                try:
                    self.write_to_csv(username_clean, filename, self.song_rec_list, True)
                    QMessageBox.information(None, "Success", "Song recommendations saved successfully!")
                except Exception as e:
                    createErrorAlert(f"Failed to save artist recommendations:\n{e}")

            if(not len(self.artist_rec_list) and not len(self.song_rec_list)):
                createErrorAlert("There are no recommendations available to save.")
       