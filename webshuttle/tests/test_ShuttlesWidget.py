import json
import sys

import pytest
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLineEdit, QTextEdit, QMessageBox

from webshuttle.domain.ShuttleFrame import ShuttleFrame
from webshuttle.adapter.incoming.ui.ShuttlesWidget import ShuttlesWidget


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_saved_shuttle_frames_are_imported_to_list(qapp):
    parent = QMainWindow()
    shuttleWidget = ShuttlesWidget(parent=parent, chrome_service=None)
    shuttleWidget.add_shuttle(name="Shuttle Name",
                              url="https://google.com",
                              target_classes="Target Class Names",
                              period=300,
                              log_edittext_widget=QLineEdit(),
                              file_name="shuttles_test.json")

    result = shuttleWidget.saved_shuttles_json()

    assert result == {'shuttle0': {'name': 'Shuttle Name', 'url': 'https://google.com', 'period': '300', 'element_classes': 'Target Class Names'}}
    with open('shuttles_test.json', 'r', encoding="utf-8") as shuttles_file:
        shuttles = json.load(shuttles_file)
        assert str(shuttles) \
               == "{'shuttle0': {'name': 'Shuttle Name', 'url': 'https://google.com', 'period': '300', 'element_classes': 'Target Class Names'}}"


def test_shuttle_is_added_with_data_and_gui(qapp):
    parent = QMainWindow()
    shuttleWidget = ShuttlesWidget(parent=parent, chrome_service=None)
    shuttleWidget.shuttles_vbox_layout = QVBoxLayout()

    shuttleWidget.add_shuttle(name="Shuttle Name",
                              url="https://targetcoders.com",
                              target_classes="class1 class2",
                              period=500,
                              log_edittext_widget=QTextEdit(),
                              file_name="shuttles_test.json")

    # Check Data
    frame: ShuttleFrame = shuttleWidget.shuttle_frames[0]
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


def test_remove_shuttle(qapp):
    parent = QMainWindow()
    shuttleWidget = ShuttlesWidget(parent=parent, chrome_service=None)
    shuttleWidget.shuttles_vbox_layout = QVBoxLayout()

    shuttleWidget.add_shuttle(name="Shuttle Name",
                              url="https://targetcoders.com",
                              target_classes="class1 class2",
                              period=500,
                              log_edittext_widget=QTextEdit(),
                              file_name="shuttles_test.json")
    layout = shuttleWidget.shuttles_vbox_layout.itemAt(0).layout()
    delete_button = layout.itemAt(1).widget()

    assert shuttleWidget.shuttles_vbox_layout.count() == 1
    shuttleWidget._confirm = lambda x: QMessageBox.Yes
    delete_button.click()
    assert shuttleWidget.shuttle_frames == {}
    assert shuttleWidget.shuttles_vbox_layout.count() == 0
    with open('shuttles_test.json', 'r', encoding="utf-8") as shuttles_file:
        shuttles = json.load(shuttles_file)
        assert shuttles == {}

