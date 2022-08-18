import sys
from unittest.mock import MagicMock

import pytest
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QApplication, QSpinBox, QWidget, QDialog

from webshuttle.adapter.incoming.ui.ShuttleFrame import ShuttleFrame
from webshuttle.adapter.incoming.ui.ShuttleFrameDialogLayout import ShuttleFrameDialogLayout
from webshuttle.adapter.incoming.ui.ShuttlesWidget import ShuttlesWidget
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_cancel_draft(qapp):
    shuttles_widget = ShuttlesWidget(None, None, None, None, None, None)
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

    shuttle_frame_dialog_layout = ShuttleFrameDialogLayout(shuttle_frame=shuttleFrame, dialog=QDialog(), shuttles_widget=shuttles_widget)
    shuttle_frame_dialog_layout.cancel_draft(QWidget())

    assert shuttleFrame.shuttleWidgets.url_widget.text() == ""
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == ""
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == ""
    assert shuttleFrame.shuttleWidgets.period_widget.value() == 0
    assert shuttleFrame.shuttleWidgets.filtering_keyword_widget.text() == ""
    assert shuttleFrame.frame_name.text() == ""
    mock_save_shuttles.assert_not_called()


def test_apply_draft(qapp):
    shuttles_widget = ShuttlesWidget(None, None, None, None, None, None)
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

    shuttle_frame_dialog_layout = ShuttleFrameDialogLayout(shuttle_frame=shuttleFrame, dialog=QDialog(), shuttles_widget=shuttles_widget)
    shuttle_frame_dialog_layout.apply_draft(QWidget())

    assert shuttleFrame.shuttleWidgets.url_widget.text() == shuttleFrame.draft_shuttleWidgets.url_widget.text()
    assert shuttleFrame.shuttleWidgets.shuttle_name_widget.text() == shuttleFrame.draft_shuttleWidgets.name_widget.text()
    assert shuttleFrame.shuttleWidgets.target_classes_widget.text() == shuttleFrame.draft_shuttleWidgets.target_classes_widget.text()
    assert shuttleFrame.shuttleWidgets.period_widget.value() == shuttleFrame.draft_shuttleWidgets.period_widget.value()
    assert shuttleFrame.shuttleWidgets.filtering_keyword_widget.text() == shuttleFrame.draft_shuttleWidgets.filtering_keyword_widget.text()
    assert shuttleFrame.frame_name.text() == "name"
    mock_save_shuttles.assert_called_once()
