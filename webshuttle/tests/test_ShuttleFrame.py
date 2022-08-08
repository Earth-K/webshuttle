import sys
from unittest.mock import MagicMock

import pytest
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QApplication, QSpinBox, QWidget, QVBoxLayout

from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from webshuttle.adapter.incoming.ui.ShuttleFrame import ShuttleFrame
from webshuttle.adapter.incoming.ui.ShuttlesWidget import ShuttlesWidget


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_settings_are_applied_when_clicked_ok(qapp):
    shuttles_widget = ShuttlesWidget(None, None, None, None, None, None, None)
    mock_save_shuttles = MagicMock()
    shuttles_widget.save_shuttles = mock_save_shuttles
    spinbox = QSpinBox()
    spinbox.setMaximum(38000)
    shuttleFrame = ShuttleFrame(shuttles={}, shuttle_seq=0, chrome_driver=None,
                                shuttle_widget_group=ShuttleWidgetGroup(state_widget=QTextEdit(),
                                                                        target_classes_widget=QLineEdit(),
                                                                        period_widget=spinbox, url_widget=QLineEdit(),
                                                                        shuttle_name_widget=QLineEdit(),
                                                                        filtering_keyword_widget=QLineEdit(),
                                                                        parent=None), shuttles_widget=shuttles_widget)

    dialog = shuttleFrame.create_settings_dialog()
    shuttleFrame.draft_shuttleWidgets.url_widget.setText("testUrl")
    shuttleFrame.draft_shuttleWidgets.period_widget.setValue(3600)
    shuttleFrame.draft_shuttleWidgets.name_widget.setText("No Name")
    shuttleFrame.draft_shuttleWidgets.target_classes_widget.setText("class1 class2")
    shuttleFrame.draft_shuttleWidgets.filtering_keyword_widget.setText("testFilteringKeyword")
    shuttleFrame.apply_draft(dialog)

    assert shuttleFrame.shuttleWidgets.url_widget.text() == "testUrl"
    assert shuttleFrame.shuttleWidgets.period_widget.value() == 3600
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == "No Name"
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == "class1 class2"
    assert shuttleFrame.draft_shuttleWidgets.filtering_keyword_widget.text() == "testFilteringKeyword"
    assert shuttleFrame.frame_name.text() == "No Name"
    mock_save_shuttles.assert_called_once()


def test_cancel_draft(qapp):
    shuttles_widget = ShuttlesWidget(None, None, None, None, None, None, None)
    mock_save_shuttles = MagicMock()
    shuttles_widget.save_shuttles = mock_save_shuttles
    spinbox = QSpinBox()
    spinbox.setMaximum(86400)
    shuttleFrame = ShuttleFrame(shuttles={}, shuttle_seq=0, chrome_driver=None,
                                shuttle_widget_group=ShuttleWidgetGroup(state_widget=QTextEdit(),
                                                                        target_classes_widget=QLineEdit(),
                                                                        period_widget=spinbox, url_widget=QLineEdit(),
                                                                        shuttle_name_widget=QLineEdit(),
                                                                        filtering_keyword_widget=QLineEdit(),
                                                                        parent=None), shuttles_widget=shuttles_widget)
    shuttleFrame.draft_shuttleWidgets.url_widget.setText("url")
    shuttleFrame.draft_shuttleWidgets.name_widget.setText("name")
    shuttleFrame.draft_shuttleWidgets.target_classes_widget.setText("targetClasses")
    shuttleFrame.draft_shuttleWidgets.filtering_keyword_widget.setText("testFilteringKeyword")
    shuttleFrame.draft_shuttleWidgets.period_widget.setValue(3600)

    shuttleFrame.cancel_draft(QWidget())

    assert shuttleFrame.shuttleWidgets.url_widget.text() == ""
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == ""
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == ""
    assert shuttleFrame.shuttleWidgets.period_widget.value() == 0
    assert shuttleFrame.shuttleWidgets.filtering_keyword_widget.text() == ""
    assert shuttleFrame.frame_name.text() == ""
    mock_save_shuttles.assert_not_called()


def test_apply_draft(qapp):
    shuttles_widget = ShuttlesWidget(None, None, None, None, None, None, None)
    mock_save_shuttles = MagicMock()
    shuttles_widget.save_shuttles = mock_save_shuttles
    spinbox = QSpinBox()
    spinbox.setMaximum(86400)
    shuttleFrame = ShuttleFrame(shuttles={}, shuttle_seq=0, chrome_driver=None,
                                shuttle_widget_group=ShuttleWidgetGroup(state_widget=QTextEdit(),
                                                                        target_classes_widget=QLineEdit(),
                                                                        period_widget=spinbox, url_widget=QLineEdit(),
                                                                        shuttle_name_widget=QLineEdit(),
                                                                        filtering_keyword_widget=QLineEdit(),
                                                                        parent=None), shuttles_widget=shuttles_widget)
    shuttleFrame.draft_shuttleWidgets.url_widget.setText("url")
    shuttleFrame.draft_shuttleWidgets.name_widget.setText("name")
    shuttleFrame.draft_shuttleWidgets.target_classes_widget.setText("targetClasses")
    shuttleFrame.draft_shuttleWidgets.filtering_keyword_widget.setText("testFilteringKeyword")
    shuttleFrame.draft_shuttleWidgets.period_widget.setValue(3600)

    shuttleFrame.apply_draft(QWidget())

    assert shuttleFrame.shuttleWidgets.url_widget.text() == shuttleFrame.draft_shuttleWidgets.url_widget.text()
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == shuttleFrame.draft_shuttleWidgets.name_widget.text()
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == shuttleFrame.draft_shuttleWidgets.target_classes_widget.text()
    assert shuttleFrame.shuttleWidgets.period_widget.value() == shuttleFrame.draft_shuttleWidgets.period_widget.value()
    assert shuttleFrame.shuttleWidgets.filtering_keyword_widget.text() == shuttleFrame.draft_shuttleWidgets.filtering_keyword_widget.text()
    assert shuttleFrame.frame_name.text() == "name"
    mock_save_shuttles.assert_called_once()
