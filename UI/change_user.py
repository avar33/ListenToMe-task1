from PySide6.QtWidgets import (
    QPlainTextEdit,
    QDialogButtonBox
)
from PySide6.QtCore import Signal, QObject
from UI.ui_helpers import createErrorAlert

class ChangeUser(QObject):
    username_changed = Signal(str)  # signal for username change

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.username_text = window.findChild(QPlainTextEdit, "usernameText")
        self.button_box = window.findChild(QDialogButtonBox, "buttonBox")

        # change OK button text
        ok_button = self.button_box.button(QDialogButtonBox.Ok)
        if ok_button:
            ok_button.setText("Save User")

        # Connect accepted and rejected signals
        self.button_box.accepted.connect(self.handle_ok)
        self.button_box.rejected.connect(self.handle_cancel)

    def handle_ok(self):
        username = self.username_text.toPlainText()
        if self.find_invalid_folder_chars(username):
            createErrorAlert("Username has invalid characters. Please pick a new user name.")
        else:
            print("User saved:", username)
            self.username_changed.emit(username)  # emit signal with new username

    def handle_cancel(self):
        print("User change canceled")

    def show_change_user_dialog(self):
        self.window.show()

    def find_invalid_folder_chars(self, name):
        invalid_chars = set('<>:"/\\|?*')
        return [char for char in name if char in invalid_chars]
