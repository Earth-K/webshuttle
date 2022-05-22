import sys

import pytest
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QFrame, QHBoxLayout, QLineEdit, QSpinBox

from widgets.ShuttlesWidget import ShuttlesWidget


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_create_from_saved_ShuttleFrames_to_list(qapp):
    shuttleWidget = ShuttlesWidget(parent=QMainWindow(), chrome_service=None)
    shuttleWidget.shuttles_vbox_layout = QVBoxLayout()
    frame = QFrame()
    inner_vBoxLayout = QVBoxLayout()
    inner_inner_hBoxLayout = QHBoxLayout()
    inner_inner_hBoxLayout.addWidget(QLineEdit("Shuttle Name"))
    inner_inner_hBoxLayout.addWidget(QLineEdit("https://google.com"))
    spinbox = QSpinBox()
    spinbox.setMaximum(30000)
    spinbox.setValue(300)
    inner_inner_hBoxLayout.addWidget(spinbox)
    inner_inner_hBoxLayout.addWidget(QLineEdit("Target Class Names"))
    inner_vBoxLayout.addLayout(inner_inner_hBoxLayout)
    frame.setLayout(inner_vBoxLayout)
    shuttleWidget.shuttles_vbox_layout.addWidget(frame)

    result = shuttleWidget.get_saved_shuttles_array()

    assert result == [('shuttle0', ["Shuttle Name", "https://google.com", "300", "Target Class Names"])]
