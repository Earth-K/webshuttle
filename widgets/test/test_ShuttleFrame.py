import sys

import pytest
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QApplication, QSpinBox, QWidget

from domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from widgets.ShuttleFrame import ShuttleFrame


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_settings_are_applied_when_clicked_ok(qapp):
    parent = QWidget()
    shuttleFrame = ShuttleFrame(shuttles={}, shuttle_seq=0, chrome_service=None,
                                shuttleWidgetGroup=ShuttleWidgetGroup(url_widget=QLineEdit(),
                                                                      update_list_widget=QTextEdit(),
                                                                      shuttle_name_widget=QLineEdit(),
                                                                      period_widget=QSpinBox(),
                                                                      target_classes_widget=QLineEdit(),
                                                                      parent=None
                                                                      ),
                                parent=parent, time=None)

    shuttleFrame.showSettings()
    shuttleFrame.draft_shuttleWidgets.url.setText("testUrl")
    shuttleFrame.draft_shuttleWidgets.period.setValue(60)
    shuttleFrame.draft_shuttleWidgets.name.setText("No Name")
    shuttleFrame.draft_shuttleWidgets.target_classes.setText("class1 class2")
    shuttleFrame.ok.click()

    assert shuttleFrame.shuttleWidgets.url_widget.text() == "testUrl"
    assert shuttleFrame.shuttleWidgets.period_widget.value() == 60
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == "No Name"
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == "class1 class2"


def test_apply_draft_shuttle(qapp):
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
