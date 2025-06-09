from PySide6.QtWidgets import QMessageBox
from dataLoader import DataLoader
        
#error message box 
def createErrorAlert (msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle("Error")
    msg_box.exec()
        
class SearchEngine:
    #display_what = [False, False]
    #preferences = []
    def __init__(self, artists_json, songs_json):
        self.artists = artists_json
        self.songs = songs_json 
        self.display_what = [False, False] #[artists, songs]
        self.preferences = []
        self.song_rec_list = []
        self.artist_rec_list = []

    #extrapolates whatever type of Recomendation is picked 
    def set_rec_type(self, artist_box, songs_box):
        self.display_what[0] = artist_box.isChecked()
        self.display_what[1]= songs_box.isChecked()
        if(self.display_what == [0,0]):
            createErrorAlert("Please select at least one box of the two labeled 'artists' and 'songs'")
        print(self.display_what)

    #extrapolated preferences 
    def set_pref(self, checkboxes):
        self.preferences.clear()
        temp = []
        for checkbox in checkboxes:
            if checkbox.isChecked():
                temp.append(checkbox.text())

        if len(temp) < 3 or len(temp) > 6:
            createErrorAlert("The amount of boxes checked is not within range. Please select 3-6 musical preferences.")
        else:
            self.preferences = temp
        print(self.preferences)

    #provide each item with a rank 
    def rank_items(self, items):
        ranked = []
        for item in items:
            genre_rank = len(set(item["genre"])& set(self.preferences))
            desc_rank = len(set(item["descriptors"])& set(self.preferences))
            total_rank = (genre_rank*2) + desc_rank
            if total_rank > 0:
                ranked.append((item, total_rank))

        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

    #final recommendations 
    def return_recs(self):
        self.song_rec_list.clear()
        self.artist_rec_list.clear()
        
        if self.display_what[0] == True:
            artists = DataLoader.read_json("artists.json", 'artists')
            artist_rec_list = self.rank_items(artists)
            for artist, total_rank in artist_rec_list:
                print(f"{artist['artist']} - Score: {total_rank}")
            
        if self.display_what[1] == True: 
            songs = DataLoader.read_json("songs.json", 'songs')
            song_rec_list = self.rank_items(songs)
            for song, total_rank in song_rec_list:
                print(f"{song['title']} by {song['artist']} - Score: {total_rank}")

    #search button overall functionality 
    def search_clicked(self, artist_box, songs_box, checkboxes, display_grid):
        self.set_rec_type(artist_box, songs_box)
        self.set_pref(checkboxes)
        if self.display_what != [False, False] and self.preferences != []:
            #if artists then search artist json
            #if songs then search songs json
            print("IN LOOP")
            self.return_recs()
            '''
            artist_title.setHidden(not display_what[0])
            song_title.setHidden(not display_what[1])
            display_recs(display_grid)
            '''
            #TODO: FIX THISI ONCE THE OTHER CLASSES ARE DONE

