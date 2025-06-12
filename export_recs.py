import csv 
import os

from UI.ui_helpers import createErrorAlert

class ExportRecs:
    def __init__(self, search_engine):
        self.search_engine = search_engine
        self.artist_rec_list = []
        self.song_rec_list = []

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

    def save_list(self, user, name):
        self.artist_rec_list = self.search_engine.get_artist_list()
        self.song_rec_list = self.search_engine.get_song_list()

        if(len(self.artist_rec_list)):
            filename = "_artists_" + name 
            self.write_to_csv(user, filename, self.artist_rec_list, False)

        if(len(self.song_rec_list)):
            filename = "_songs_" + name 
            self.write_to_csv(user, filename, self.song_rec_list, True)

        if(not len(self.artist_rec_list) and not len(self.song_rec_list)):
            createErrorAlert("There are no recommendations available to save.")
       