import sys
import json

from PySide6.QtWidgets import QMessageBox

def readJSON(file, key): 
        with open (file, "r") as f:
            data = json.load(f)
        if isinstance(data, dict) and key in data:
            return data[key]
        else: 
            return None
        
#error message box 
def createErrorAlert (msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle("Error")
    msg_box.exec()
        
class SearchEngine:
    displayWhat = [False, False]
    preferences = []

    def __init__(self, artistsJSON, songsJSON):
        self.artists = artistsJSON
        self.songs = songsJSON

    def assignRanks(items, userChecked):
        ranked = []
        for item in items:
            genreRank = len(set(item["genre"])& set(userChecked))
            descRank = len(set(item["descriptors"])& set(userChecked))
            totalRank = genreRank + descRank
            if totalRank > 0:
                ranked.append((item, totalRank))

        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

    #extrapolates whatever type of reccomendation is picked 
    def setReccType(artistBox, songsBox):
        global displayWhat
        displayWhat[0] = artistBox.isChecked()
        displayWhat[1]= songsBox.isChecked()
        if(displayWhat == [0,0]):
            createErrorAlert("Please select at least one box of the two labeled 'artists' and 'songs'")
        print(displayWhat)

    #extrapolated preferences 
    def setPref(checkboxes):
        global preferences
        preferences.clear()
        temp = []
        for checkbox in checkboxes:
            if checkbox.isChecked():
                temp.append(checkbox.text())

        if len(temp) < 3 or len(temp) > 6:
            createErrorAlert("The amount of boxes checked is not within range. Please select 3-6 musical preferences.")
        else:
            preferences = temp
        print(preferences)
        
    def searchClicked(artistBox, songsBox, checkboxes):
        setReccType(artistBox, songsBox)
        setPref(checkboxes)

        if displayWhat != [False, False] and preferences != []:
            #if artists then search artist json
            #if songs then search songs json
            print("IN LOOP")
            rankReccs()

    def rankReccs(self):
        global displayWhat
        global preferences
        
        if displayWhat[0] == True:
            artists = readJSON(self.artists, 'artists')
            ranked_artists = assignRanks(artists, preferences)
            for artist, totalRank in ranked_artists:
                print(f"{artist['artist']} - Score: {totalRank}")

        if displayWhat[1] == True: #TODO: fix song selection
            songs = readJSON(self.songs, 'songs')
            ranked_songs = assignRanks(songs, preferences)
            for song, totalRank in ranked_songs:
                print(f"{song['title']} - Score: {totalRank}")

