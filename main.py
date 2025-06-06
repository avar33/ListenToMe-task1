import sys
import json

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QMessageBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QSizePolicy, 
    QGraphicsView, 
    QGraphicsScene,
    QGraphicsPixmapItem, 
    QScrollArea
)

from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from functools import partial
from PySide6.QtCore import Qt


#GLOBAL VARIABLES
displayWhat = [False, False]
preferences = []
songReccList = []
artistReccList = []

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

#TODO: MOVE TO ANOTHER FILE 
#SEARCHING UTILITY
#----------------------------------------------------------------
#search button overall functionality 
def searchClicked(artistBox, songsBox, checkboxes):
    setReccType(artistBox, songsBox)
    setPref(checkboxes)

    if displayWhat != [False, False] and preferences != []:
        #if artists then search artist json
        #if songs then search songs json
        print("IN LOOP")
        returnReccs()

def returnReccs():
    global displayWhat, preferences, songReccList, artistReccList
    songReccList.clear()
    artistReccList.clear()
    
    if displayWhat[0] == True:
        artists = readJSON("artists.json", 'artists')
        artistReccList = rankItems(artists, preferences)
        
    if displayWhat[1] == True: 
        songs = readJSON("songs.json", 'songs')
        songReccList = rankItems(songs, preferences)
    
    for artist, totalRank in artistReccList:
        print(f"{artist['artist']} - Score: {totalRank}")
    for song, totalRank in songReccList:
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

#error message box 
def createErrorAlert (msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle("Error")
    msg_box.exec()

def fillDisplayWidget(displayGrid, name, artist, genre, descriptors):
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
    mainLabel = QLabel(name)
    artist_genre = QLabel(artist, " -  genre")
    descLabel = QLabel("word | word | word")

    displayInfoWidget.addWidget(image)
    displayInfoWidget.addWidget(mainLabel)
    displayInfoWidget.addWidget(artist_genre)
    displayInfoWidget.addWidget(descLabel)

    # wrap layout in a QWidget
    container = QWidget()
    container.setLayout(displayInfoWidget) 

    # add the widget to the grid
    displayGrid.addWidget(container, z, i)
#----------------------------------------------------------------
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

searchButton.clicked.connect(partial(searchClicked, artistBox, songsBox, checkboxes))

displayGrid = selectionWindow.findChild(QGridLayout, "displayGrid")
if displayGrid:
    print("displayGrid found")

z = 0
for i in range(8):
    if i >= 4: 
        z = 1
        i = i - 4
    #fillDisplayGrid(displayGrid)


selectionWindow.show()
app.exec()
#--------------------------------------------------------------------------------------------------------------