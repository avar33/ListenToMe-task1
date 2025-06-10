import sys

from PySide6.QtWidgets import QApplication

from PySide6.QtUiTools import QUiLoader
from main_ui import create_ui

#LOAD APPLICATION 
#--------------------------------------------------------------------------------------------------------------
app = QApplication(sys.argv)
loader = QUiLoader()
selectionWindow = loader.load("main.ui", None)
create_ui(selectionWindow)
selectionWindow.show()
app.exec()
#--------------------------------------------------------------------------------------------------------------