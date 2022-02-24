from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel


class LogWidget(QWidget):
    def __init__(self, parent):
        super(LogWidget, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self._vbox_layout = QVBoxLayout()
        title = QLabel()
        title.setText("Log : ")
        self._edit_text = QTextEdit()
        self._edit_text.setReadOnly(True)
        self._vbox_layout.addWidget(title)
        self._vbox_layout.addWidget(self._edit_text)
        self.setLayout(self._vbox_layout)
        self.show()

    def get_edittext(self):
        return self._edit_text
