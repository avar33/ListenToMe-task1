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
    QGraphicsPixmapItem
)

from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from functools import partial

#GLOBAL VARIABLES
displayWhat = [False, False]
preferences = []

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
        rankReccs()

def rankReccs():
    global displayWhat
    global preferences
    
    if displayWhat[0] == True:
        artists = readJSON("artists.json", 'artists')
        ranked_artists = assignRanks(artists, preferences)
        for artist, totalRank in ranked_artists:
            print(f"{artist['artist']} - Score: {totalRank}")

    if displayWhat[1] == True: #TODO: fix song selection
        songs = readJSON("songs.json", 'songs')
        ranked_songs = assignRanks(songs, preferences)
        for song, totalRank in ranked_songs:
            print(f"{song['song']} - Score: {totalRank}")

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

#error message box 
def createErrorAlert (msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle("Error")
    msg_box.exec()
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

for i in range(4):
    '''
    displayInfoWidget = loader.load("displayInfoWidget.ui", selectionWindow)
    displayInfoWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
    if displayInfoWidget:
        print("displayInfoW found")
        displayInfoWidget.setStyleSheet("background-color: lightblue;")
    '''
    displayInfoWidget = QVBoxLayout()
    scene = QGraphicsScene()
    pixmap = QPixmap("TaylorSwift.jpg")
    item = QGraphicsPixmapItem(pixmap)
    scene.addItem(item)
    image = QGraphicsView()
    image.setScene(scene)
    image.show()
    mainLabel = QLabel("mock name")
    artist_genre = QLabel("artist - genre")
    descLabel = QLabel("word | word | word")
    displayInfoWidget.addWidget(image)
    displayInfoWidget.addWidget(mainLabel)
    displayInfoWidget.addWidget(artist_genre)
    displayInfoWidget.addWidget(descLabel)

    # Wrap layout in a QWidget
    container = QWidget()
    container.setLayout(displayInfoWidget) 

    # Now you can add the widget to the grid
    displayGrid.addWidget(container, 0, i)

selectionWindow.show()
app.exec()
#--------------------------------------------------------------------------------------------------------------