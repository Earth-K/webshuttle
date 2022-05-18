import sys

import pytest
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTextEdit, QApplication, QSpinBox

from domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from widgets.ShuttleFrame import ShuttleFrame


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_settings_are_applied(qapp):
    shuttleFrame = ShuttleFrame(
        ShuttleWidgetGroup(url_widget=QLineEdit(),
                           start_btn_widget=QPushButton(),
                           update_list_widget=QTextEdit(),
                           shuttle_name_widget=QLineEdit(),
                           period_widget=QSpinBox(),
                           target_classes_widget=QLineEdit(),
                           parent=None
        )
    )
    setting_widgets_draft: ShuttleWidgetGroup = shuttleFrame.showSettings()
    setting_widgets_draft.url_widget.setText("testUrl")
    setting_widgets_draft.shuttle_name_widget.setText("testShuttleName")
    setting_widgets_draft.period_widget.setValue(0)
    setting_widgets_draft.target_classes_widget.setText("testClasses")

    setting_widgets_draft._saveButtonWidget.click()

    assert shuttleFrame.shuttleWidgets.url_widget.text() == "testUrl"
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == "testShuttleName"
    assert shuttleFrame.shuttleWidgets.period_widget.value() == 0
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == "testClasses"
