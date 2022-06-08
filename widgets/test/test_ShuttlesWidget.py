import sys

import pytest
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLineEdit, QTextEdit

from widgets.ShuttleFrame import ShuttleFrame
from widgets.ShuttlesWidget import ShuttlesWidget


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_Saved_shuttle_frames_are_imported_to_list(qapp):
    parent = QMainWindow()
    shuttleWidget = ShuttlesWidget(parent=parent, chrome_service=None)
    shuttleWidget.add_shuttle(name="Shuttle Name",
                              url="https://google.com",
                              target_classes="Target Class Names",
                              period=300,
                              log_edittext_widget=QLineEdit())

    result = shuttleWidget.get_saved_shuttles_array()

    assert result == [('shuttle1', ["Shuttle Name", "https://google.com", "300", "Target Class Names"])]


def test_Shuttle_is_added_with_data_and_GUI(qapp):
    parent = QMainWindow()
    shuttleWidget = ShuttlesWidget(parent=parent, chrome_service=None)
    shuttleWidget.shuttles_vbox_layout = QVBoxLayout()

    shuttleWidget.add_shuttle(name="Shuttle Name",
                              url="https://targetcoders.com",
                              target_classes="class1 class2",
                              period=500,
                              log_edittext_widget=QTextEdit())

    # Check Data
    frame: ShuttleFrame = shuttleWidget.shuttle_frames[1]
    assert frame.shuttleWidgets.shuttle_name_widget.text() == "Shuttle Name"
    assert frame.shuttleWidgets.url_widget.text() == "https://targetcoders.com"
    assert frame.shuttleWidgets.period_widget.value() == 500
    assert frame.shuttleWidgets.target_classes_widget.text() == "class1 class2"
    # Check GUI
    shuttle_layout = shuttleWidget.shuttles_vbox_layout.itemAt(0).layout()
    assert shuttle_layout.count() == 2
    assert shuttle_layout.itemAt(0).widget().layout().itemAt(0).widget().text() == "Shuttle Name"
    assert shuttle_layout.itemAt(0).widget().layout().itemAt(1).widget().text() == "설정"
    assert shuttle_layout.itemAt(0).widget().layout().itemAt(2).widget().text() == "시작"
    assert shuttle_layout.itemAt(1).widget().icon() is not None
