import sys
import json

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
)

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

#LOAD JSON DATA 
with open ("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("printing data: ")
print (data[0]["title"])

#LOAD APPLICATION 
app = QApplication(sys.argv)
#window = MainWindow()
loader = QUiLoader()
window = loader.load("main.ui", None)
window.show()
app.exec()