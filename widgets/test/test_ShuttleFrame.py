import sys

import pytest
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QApplication, QSpinBox, QWidget, QVBoxLayout

from domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from widgets.ShuttleFrame import ShuttleFrame


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_settings_are_applied_when_clicked_ok(qapp):
    parent = QWidget()
    spinbox = QSpinBox()
    spinbox.setMaximum(38000)
    shuttleFrame = ShuttleFrame(shuttles={}, shuttle_seq=0, chrome_service=None,
                                shuttleWidgetGroup=ShuttleWidgetGroup(url_widget=QLineEdit(),
                                                                      update_list_widget=QTextEdit(),
                                                                      shuttle_name_widget=QLineEdit(),
                                                                      period_widget=spinbox,
                                                                      target_classes_widget=QLineEdit(),
                                                                      parent=None
                                                                      ),
                                parent=parent, time=None)

    shuttleFrame.showSettings()
    shuttleFrame.draft_shuttleWidgets.url.setText("testUrl")
    shuttleFrame.draft_shuttleWidgets.period.setValue(3600)
    shuttleFrame.draft_shuttleWidgets.name.setText("No Name")
    shuttleFrame.draft_shuttleWidgets.target_classes.setText("class1 class2")
    shuttleFrame.ok.click()

    assert shuttleFrame.shuttleWidgets.url_widget.text() == "testUrl"
    assert shuttleFrame.shuttleWidgets.period_widget.value() == 3600
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == "No Name"
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == "class1 class2"
    assert shuttleFrame.frame_name.text() == "No Name"


def test_apply_draft_shuttle(qapp):
    parent = QWidget()
    spinbox = QSpinBox()
    spinbox.setMaximum(86000)
    shuttleFrame = ShuttleFrame(shuttles={}, shuttle_seq=0, chrome_service=None,
                                shuttleWidgetGroup=ShuttleWidgetGroup(url_widget=QLineEdit(),
                                                                      update_list_widget=QTextEdit(),
                                                                      shuttle_name_widget=QLineEdit(),
                                                                      period_widget=spinbox,
                                                                      target_classes_widget=QLineEdit(),
                                                                      parent=None
                                                                      ),
                                parent=parent, time=None)
    shuttleFrame.draft_shuttleWidgets.url.setText("url")
    shuttleFrame.draft_shuttleWidgets.name.setText("name")
    shuttleFrame.draft_shuttleWidgets.target_classes.setText("targetClasses")
    shuttleFrame.draft_shuttleWidgets.period.setValue(3600)

    shuttleFrame.applyDraft(QWidget())

    assert shuttleFrame.shuttleWidgets.url_widget.text() == shuttleFrame.draft_shuttleWidgets.url.text()
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == shuttleFrame.draft_shuttleWidgets.name.text()
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == shuttleFrame.draft_shuttleWidgets.target_classes.text()
    assert shuttleFrame.shuttleWidgets.period_widget.value() == shuttleFrame.draft_shuttleWidgets.period.value()
    assert shuttleFrame.frame_name.text() == "name"


def test_UI_of_showSettings_QDialog(qapp):
    parent = QWidget()
    spinbox = QSpinBox()
    spinbox.setMaximum(86000)
    shuttleFrame = ShuttleFrame(shuttles={}, shuttle_seq=0, chrome_service=None,
                                shuttleWidgetGroup=ShuttleWidgetGroup(url_widget=QLineEdit(),
                                                                      update_list_widget=QTextEdit(),
                                                                      shuttle_name_widget=QLineEdit(),
                                                                      period_widget=spinbox,
                                                                      target_classes_widget=QLineEdit(),
                                                                      parent=None
                                                                      ),
                                parent=parent, time=None)

    shuttleFrame.setSettingsLayout()

    layout: QVBoxLayout = shuttleFrame.vBoxLayout
    assert layout.count() == 5
    assert layout.itemAt(0).layout().itemAt(0).widget().text() == "셔틀 이름 : "
    assert type(layout.itemAt(0).layout().itemAt(1).widget()) == QLineEdit
    assert layout.itemAt(1).layout().itemAt(0).widget().text() == "URL : "
    assert type(layout.itemAt(1).layout().itemAt(1).widget()) == QLineEdit
    assert layout.itemAt(2).layout().itemAt(0).widget().text() == "반복 주기(초) : "
    assert type(layout.itemAt(2).layout().itemAt(1).widget()) == QSpinBox
    assert layout.itemAt(2).layout().itemAt(1).widget().maximum() == 86000
    assert layout.itemAt(3).layout().itemAt(0).widget().text() == "타깃 클래스 : "
    assert type(layout.itemAt(3).layout().itemAt(1).widget()) == QLineEdit
