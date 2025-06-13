import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from UI.main_ui import MainUI

# LOAD APPLICATION
# --------------------------------------------------------------------------------------------------------------
app = QApplication(sys.argv)
loader = QUiLoader()
selectionWindow = loader.load("UI/main.ui", None)
main_ui = MainUI(selectionWindow)
selectionWindow.show()
app.exec()
# --------------------------------------------------------------------------------------------------------------
