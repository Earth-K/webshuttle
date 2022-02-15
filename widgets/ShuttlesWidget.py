from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


def _vbox_layout():
    result = QVBoxLayout()
    label_url = QLabel("This is a setting widget.")
    result.addWidget(label_url)
    return result


class ShuttlesWidget(QWidget):
    def __init__(self, parent):
        super(ShuttlesWidget, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        vbox_layout = _vbox_layout()
        self.setLayout(vbox_layout)
        self.show()
