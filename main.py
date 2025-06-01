import sys
import json

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
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

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel

#FUNCTION DECL
#---------------------------------------------------------------
#loads json data into a list
def readJSON(file, key): 
    with open (file, "r") as f:
        data = json.load(f)
    if isinstance(data, dict) and key in data:
        return data[key]
    else: 
        return None
#----------------------------------------------------------------

#LOAD APPLICATION 
app = QApplication(sys.argv)
loader = QUiLoader()
selectionWindow = loader.load("main.ui", None)

descriptors = readJSON("data.json", 'descriptors')

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
        prefGrid.addWidget(checkbox, row, col)

displayGrid = selectionWindow.findChild(QGridLayout, "displayGrid")
if displayGrid:
    print("displayGrid found")

displayInfoWidget = loader.load("displayInfoWidget.ui", selectionWindow)
displayInfoWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
if displayInfoWidget:
    print("displayInfoW found")
    displayInfoWidget.setStyleSheet("background-color: lightblue;")

displayGrid.addWidget(displayInfoWidget, 0, 0)

selectionWindow.show()
app.exec()