import sys
import json

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QMessageBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QSizePolicy
)

from PySide6.QtUiTools import QUiLoader
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
    songs = readJSON("songs.json", 'songs')
    #for song in songs: 
       # print(song["title"])


#extrapolates whatever type of reccomendation is picked 
def setReccType(artistBox, songsBox):
    temp = [False, False]
    temp[0] = artistBox.isChecked()
    temp[1]= songsBox.isChecked()
    if(temp == [0,0]):
        createErrorAlert("Please select at least one box of the two labeled 'artists' and 'songs'")
    else:
        displayWhat = temp 

#extrapolated preferences 
def setPref(checkboxes):
    temp = []
    for checkbox in checkboxes:
        if checkbox.isChecked():
            temp.append(checkbox.text())

    if len(temp) < 3 or len(temp) > 6:
        createErrorAlert("The amount of boxes checked is not within range. Please select 3-6 musical preferences.")
    else:
        preferences = temp

#error message box 
def createErrorAlert (msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle("Error")
    msg_box.exec()
#----------------------------------------------------------------
#access global variables 
def returnDisplayWhat():
    return displayWhat

def returnPreferences():
    return preferences
#--------------------------------------------------------------------------------------------------------------

#LOAD APPLICATION 
#--------------------------------------------------------------------------------------------------------------
app = QApplication(sys.argv)
loader = QUiLoader()
checkboxes = []

selectionWindow = loader.load("main.ui", None)

descriptors = readJSON("data.json", 'descriptors')

artistBox = selectionWindow.findChild(QCheckBox, "artistBox")
if artistBox:
    print("aBox found")
songsBox = selectionWindow.findChild(QCheckBox, "songsBox")
if songsBox:
    print("sBox found")

searchButton = selectionWindow.findChild(QPushButton, "searchButton")
if searchButton:
    print("button found")
    
prefGrid = selectionWindow.findChild(QGridLayout, "preferenceGrid")
if prefGrid:
    print("prefGrid found")
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

displayInfoWidget = loader.load("displayInfoWidget.ui", selectionWindow)
displayInfoWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
if displayInfoWidget:
    print("displayInfoW found")
    displayInfoWidget.setStyleSheet("background-color: lightblue;")

#TODO: resize display and add properly
displayGrid.addWidget(displayInfoWidget, 0, 0)
#displayGrid.addWidget(displayInfoWidget, 1,0)

selectionWindow.show()
app.exec()
#--------------------------------------------------------------------------------------------------------------