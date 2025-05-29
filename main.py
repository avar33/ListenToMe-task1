import sys
import math

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #PREFERENCE SELECTIONS
        descriptors = [ 
            "pop", "hip-hop", "r'n'b", "electronic", "techno", "rock", "alternative", "indie", "country", "latin", "k-pop", 
            "romantic", "sad", "happy", "bubbly", "upbeat", "relaxed", "loud", "nostalgic", "lyrical", "bass", "intense", 
            "catchy", "emotional", "light-hearted", "experimental",
        ]

        self.setWindowTitle("Listen to Me!")
        self.setStyleSheet("background-color: lightpink")

        layout = QVBoxLayout()

        #MAIN TITLE FOR APP 
        title = QLabel("Welcome to \"Listen to Me!\"")
        #change font and size 
        from PySide6.QtGui import QFont
        font = QFont("Tahoma", 40)
        title.setFont(font)
        #center it at the top 
        from PySide6.QtCore import Qt
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #INSTRUCTION LABEL 1 
        instruction1 = QLabel("please select the type of reccomendation you'd like:")
        font = QFont("Tahoma", 14)
        instruction1.setFont(font)
        instruction1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #INSTRUCTION LABEL 2
        instruction2 = QLabel("please select 3-5 musical prefences below")
        font = QFont("Tahoma", 14)
        instruction2.setFont(font)
        instruction2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(instruction1)
        layout.addWidget(instruction2)

        #preferences selection boxes 
        gridLayout = QGridLayout()
        cols = 5 
        for i, descriptor in enumerate(descriptors):
            row = i // cols
            col = i % cols
            checkbox = QCheckBox(descriptor)
            gridLayout.addWidget(checkbox, row, col)

        layout.addLayout(gridLayout)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()