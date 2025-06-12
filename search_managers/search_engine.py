from PySide6.QtWidgets import QMessageBox
from data_managers.data_loader import DataLoader
from UI.rec_display_manager import RecDisplayManager
from UI.ui_helpers import createErrorAlert
        
class SearchEngine:
    def __init__(self):
        #self.artists = artists_json
        #self.songs = songs_json 
        self._display_what = [False, False] #[artists, songs]
        self._preferences = []
        self._song_rec_list = []
        self._artist_rec_list = []

    #extrapolates whatever type of Recomendation is picked 
    def set_rec_type(self, artist_box, songs_box):
        self._display_what[0] = artist_box.isChecked()
        self._display_what[1]= songs_box.isChecked()
        if(self._display_what == [0,0]):
            createErrorAlert("Please select at least one box of the two labeled 'artists' and 'songs'")
        print(self._display_what)

    #input is read from the checkboxes seleceted and put into a 'preference' list if it fits within the length constraints 
    def set_pref(self, checkboxes):
        temp = []
        for checkbox in checkboxes:
            if checkbox.isChecked():
                temp.append(checkbox.text())
    
        if len(temp) < 3 or len(temp) > 6:
            createErrorAlert("The amount of boxes checked is not within range. Please select 3-6 musical _preferences.")
        else:
            self._preferences = temp
        print(self._preferences)

    #provide each item with a rank 
    def rank_items(self, items):
        ranked = []
        for item in items:
            genre_rank = len(set(item["genre"])& set(self._preferences))
            desc_rank = len(set(item["descriptors"])& set(self._preferences))
            total_rank = (genre_rank*2) + desc_rank
            if total_rank > 0:
                ranked.append((item, total_rank))

        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

    #final recommendations 
    def return_recs(self):
        self._song_rec_list.clear()
        self._artist_rec_list.clear()
        
        if self._display_what[0] == True:
            artists = DataLoader.read_json("data_managers/json_files/artists.json", 'artists')
            self._artist_rec_list = self.rank_items(artists)
            print("printing from return recs")
            
        if self._display_what[1] == True: 
            songs = DataLoader.read_json("data_managers/json_files/songs.json", 'songs')
            self._song_rec_list = self.rank_items(songs)
            #for song, total_rank in self._song_rec_list:
                #print(f"{song['title']} by {song['artist']} - Score: {total_rank}")

    #search button overall functionality 
    def search_clicked(self, artist_box, songs_box, checkboxes, display_grid, artist_title, song_title):
        self.set_rec_type(artist_box, songs_box)
        self.set_pref(checkboxes)

        if self._display_what != [False, False] and self._preferences:
            print("IN LOOP")
            self.return_recs()

            artist_title.setHidden(not self._display_what[0])
            song_title.setHidden(not self._display_what[1])  # Fix: should reflect songs, not artists again

            manager = RecDisplayManager(display_grid)
            manager.display_recs(self._artist_rec_list, self._song_rec_list, self._display_what)

    def get_artist_list(self):
        return self._artist_rec_list

    def get_song_list(self):
        return self._song_rec_list
            
