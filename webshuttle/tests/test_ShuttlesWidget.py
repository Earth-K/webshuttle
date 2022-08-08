import json
import sys
from unittest.mock import MagicMock

import pytest
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLineEdit, QTextEdit, QMessageBox, QSpinBox

from webshuttle.adapter.incoming.ui.ShuttleFrame import ShuttleFrame
from webshuttle.adapter.incoming.ui.ShuttlesWidget import ShuttlesWidget
from webshuttle.adapter.outcoming.persistence.ShuttlePersistenceAdapter import ShuttlePersistenceAdapter
from webshuttle.application.CreateLogTextService import CreateLogTextService
from webshuttle.application.ExportShuttlesService import ExportShuttlesService
from webshuttle.application.GetShuttlesService import GetShuttlesService
from webshuttle.application.LoadShuttlesService import LoadShuttlesService
from webshuttle.application.port.outcoming.ShuttleRepository import ShuttleRepository
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_saved_shuttle_frames_are_imported_to_dict(qapp):
    parent = QMainWindow()
    shuttleWidget = ShuttlesWidget(parent=parent, chrome_driver=None, export_shuttles_usecase=ExportShuttlesService(ShuttlePersistenceAdapter()), create_logtext_usecase=CreateLogTextService(), load_shuttles_usecase=LoadShuttlesService(ShuttleRepository()), get_shuttles_usecase=GetShuttlesService(), file_name="shuttles_test.json")
    shuttle_widget_group = default_shuttle_widget_group()
    shuttleWidget.add_shuttle(shuttle_widget_group)

    result = shuttleWidget.saved_shuttles_json()

    assert result == {'shuttle0': {'name': 'Shuttle Name', 'url': 'https://google.com', 'period': '300', 'element_classes': 'Target Class Names', 'filtering_keyword': 'Filtering Keyword'}}
    with open('shuttles_test.json', 'r', encoding="utf-8") as shuttles_file:
        shuttles = json.load(shuttles_file)
        assert str(shuttles) \
               == "{'shuttle0': {'name': 'Shuttle Name', 'url': 'https://google.com', 'period': '300', 'element_classes': 'Target Class Names', 'filtering_keyword': 'Filtering Keyword'}}"


def test_shuttle_frame_is_added(qapp):
    parent = QMainWindow()
    shuttleWidget = ShuttlesWidget(parent=parent, chrome_driver=None, export_shuttles_usecase=ExportShuttlesService(ShuttlePersistenceAdapter()), create_logtext_usecase=CreateLogTextService(), load_shuttles_usecase=LoadShuttlesService(ShuttleRepository()), get_shuttles_usecase=GetShuttlesService(), file_name="shuttles_test.json")
    shuttleWidget.shuttles_vbox_layout = QVBoxLayout()

    shuttleWidget.add_shuttle(default_shuttle_widget_group())

    # Check Data
    frame: ShuttleFrame = shuttleWidget.shuttle_frames[0]
    assert frame.shuttleWidgets.shuttle_name_widget.text() == "Shuttle Name"
    assert frame.shuttleWidgets.url_widget.text() == "https://google.com"
    assert frame.shuttleWidgets.period_widget.value() == 300
    assert frame.shuttleWidgets.target_classes_widget.text() == "Target Class Names"
    assert frame.shuttleWidgets.filtering_keyword_widget.text() == "Filtering Keyword"


def test_shuttle_frame_widget_is_deleted(qapp):
    parent = QMainWindow()
    shuttleWidget = ShuttlesWidget(parent=parent, chrome_driver=None, export_shuttles_usecase=ExportShuttlesService(ShuttlePersistenceAdapter()), create_logtext_usecase=CreateLogTextService(), load_shuttles_usecase=LoadShuttlesService(ShuttleRepository()), get_shuttles_usecase=GetShuttlesService(), file_name="shuttles_test.json")
    shuttleWidget.shuttles_vbox_layout = QVBoxLayout()

    shuttleWidget.add_shuttle(default_shuttle_widget_group())
    layout = shuttleWidget.shuttles_vbox_layout.itemAt(0).layout()
    delete_button = layout.itemAt(1).widget()

    assert shuttleWidget.shuttles_vbox_layout.count() == 1
    QMessageBox.question = MagicMock(return_value=QMessageBox.Yes)
    delete_button.click()
    assert shuttleWidget.shuttle_frames == {}
    assert shuttleWidget.shuttles_vbox_layout.count() == 0
    with open('shuttles_test.json', 'r', encoding="utf-8") as shuttles_file:
        shuttles = json.load(shuttles_file)
        assert shuttles == {}


def default_shuttle_widget_group():
    period_widget = QSpinBox()
    period_widget.setMaximum(86400)
    period_widget.setValue(300)
    shuttle_widget_group: ShuttleWidgetGroup = ShuttleWidgetGroup(state_widget=QTextEdit(),
                                                                  target_classes_widget=QLineEdit("Target Class Names"),
                                                                  period_widget=period_widget,
                                                                  url_widget=QLineEdit("https://google.com"),
                                                                  shuttle_name_widget=QLineEdit("Shuttle Name"),
                                                                  filtering_keyword_widget=QLineEdit("Filtering Keyword"))
    return shuttle_widget_group
