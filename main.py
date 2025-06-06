import sys
import json

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



#FUNCTION DECL
#--------------------------------------------------------------------------------------------------------------
#loads json data into a list
def readJSON(file, key): 
    with open (file, "r") as f:
        data = json.load(f)
    if isinstance(data, dict) and key in data:
        return data[key]
    else: 
        return None

#GLOBAL VARIABLES
displayWhat = [False, False] #artist, song
preferences = []
songRecList = []
artistRecList = []

#TODO: MOVE TO ANOTHER FILE 
#SEARCHING UTILITY
#----------------------------------------------------------------
#search button overall functionality 
def searchClicked(artistBox, songsBox, checkboxes, displayGrid):
    setRecType(artistBox, songsBox)
    setPref(checkboxes)

    if displayWhat != [False, False] and preferences != []:
        #if artists then search artist json
        #if songs then search songs json
        print("IN LOOP")
        returnRecs()
        displayRecs(displayGrid)

def returnRecs():
    global displayWhat, preferences, songRecList, artistRecList
    songRecList.clear()
    artistRecList.clear()
    
    if displayWhat[0] == True:
        artists = readJSON("artists.json", 'artists')
        artistRecList = rankItems(artists, preferences)
        for artist, totalRank in artistRecList:
            print(f"{artist['artist']} - Score: {totalRank}")
        
    if displayWhat[1] == True: 
        songs = readJSON("songs.json", 'songs')
        songRecList = rankItems(songs, preferences)
        for song, totalRank in songRecList:
            print(f"{song['title']} by {song['artist']} - Score: {totalRank}")

def rankItems(items, userChecked):
    ranked = []
    for item in items:
        genreRank = len(set(item["genre"])& set(userChecked))
        descRank = len(set(item["descriptors"])& set(userChecked))
        totalRank = genreRank + descRank
        if totalRank > 0:
            ranked.append((item, totalRank))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked

#extrapolates whatever type of Recomendation is picked 
def setRecType(artistBox, songsBox):
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
#----------------------------------------------------------------

#error message box 
def createErrorAlert (msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle("Error")
    msg_box.exec()

#fill in the info for songs 
def fillSongDisplay(displayGrid, title, artist, genre, descriptors, row, col):
    displayInfoWidget = QVBoxLayout()
    
    # --- Image handling ---
    scene = QGraphicsScene()
    pixmap = QPixmap("images/record.jpg")
    image = QLabel()

    pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio) 
    image.setPixmap(pixmap)
    image.setAlignment(Qt.AlignCenter)
    image.setFixedSize(150, 150)

     # --- Labels ---
    mainLabel = QLabel(f"{title}")
    artist_genre = QLabel(f"by {artist} - {', '.join(genre)}")
    descLabel = QLabel(" | ".join(descriptors))

    displayInfoWidget.addWidget(image)
    displayInfoWidget.addWidget(mainLabel)
    displayInfoWidget.addWidget(artist_genre)
    displayInfoWidget.addWidget(descLabel)

    # wrap layout in a QWidget
    container = QWidget()
    container.setLayout(displayInfoWidget) 

    # add the widget to the grid
    displayGrid.addWidget(container, row, col)

#fill in the info for artists 
def fillArtistDisplay(displayGrid, artist, genre, descriptors, row, col):
    displayInfoWidget = QVBoxLayout()
    
    # --- Image handling ---
    scene = QGraphicsScene()
    pixmap = QPixmap("images/noProfile.jpg")
    image = QLabel()

    pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio) 
    image.setPixmap(pixmap)
    image.setAlignment(Qt.AlignCenter)
    image.setFixedSize(150, 150)

     # --- Labels ---
    mainLabel = QLabel(f"{artist}")
    artist_genre = QLabel(', '.join(genre))
    descLabel = QLabel(" | ".join(descriptors))

    displayInfoWidget.addWidget(image)
    displayInfoWidget.addWidget(mainLabel)
    displayInfoWidget.addWidget(artist_genre)
    displayInfoWidget.addWidget(descLabel)

    # wrap layout in a QWidget
    container = QWidget()
    container.setLayout(displayInfoWidget) 

    # add the widget to the grid
    displayGrid.addWidget(container, row, col)

#display in grid 
def displayRecs(displayGrid):
    #empty current display
    while displayGrid.count():
        child = displayGrid.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

    colNext = 0
    colMax = 4
    if displayWhat[0]: #artists
        if displayWhat[1]:
            colMax = 2
        for i, (artist, score) in enumerate(artistRecList):
            col = i % colMax
            currentRow = (i // colMax)
            fillArtistDisplay(displayGrid, artist["artist"], artist["genre"], artist["descriptors"], currentRow, col)
        colNext = 2 

    if displayWhat[1]: #songs
        for i, (song, score) in enumerate(songRecList):
            col = (i % colMax) + colNext
            currentRow = i // colMax
            fillSongDisplay(displayGrid, song["title"], song["artist"], song["genre"], song["descriptors"], currentRow, col)

def randomRecs(displayGrid): #TODO: PUT ON BACKBURNER FOR NOW 
    colNext = 0
    colMax = 4
    if displayWhat[0]: #artists
        if displayWhat[1]:
            colMax = 2
        for i, (artist, score) in enumerate(artistRecList):
            col = i % colMax
            currentRow = (i // colMax)
            fillArtistDisplay(displayGrid, artist["artist"], artist["genre"], artist["descriptors"], currentRow, col)
        colNext = 2 

    if displayWhat[1]: #songs
        for i, (song, score) in enumerate(songRecList):
            col = (i % colMax) + colNext
            currentRow = i // colMax
            fillSongDisplay(displayGrid, song["title"], song["artist"], song["genre"], song["descriptors"], currentRow, col)

#--------------------------------------------------------------------------------------------------------------

#LOAD APPLICATION 
#--------------------------------------------------------------------------------------------------------------
app = QApplication(sys.argv)
loader = QUiLoader()
checkboxes = []

selectionWindow = loader.load("main.ui", None)

descriptors = readJSON("data.json", 'descriptors')

artistBox = selectionWindow.findChild(QCheckBox, "artistBox")
songsBox = selectionWindow.findChild(QCheckBox, "songsBox")

searchButton = selectionWindow.findChild(QPushButton, "searchButton")
    
prefGrid = selectionWindow.findChild(QGridLayout, "preferenceGrid")
if prefGrid:
    cols = 5 
    for i, descriptor in enumerate(descriptors):
        row = i // cols
        col = i % cols
        checkbox = QCheckBox(descriptor)
        checkboxes.append(checkbox)
        prefGrid.addWidget(checkbox, row, col)

displayGrid = selectionWindow.findChild(QGridLayout, "displayGrid")
if displayGrid:
    print("displayGrid found")

searchButton.clicked.connect(partial(searchClicked, artistBox, songsBox, checkboxes, displayGrid))

selectionWindow.show()
app.exec()
#--------------------------------------------------------------------------------------------------------------