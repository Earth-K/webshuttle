import sys

from PyQt5.QtWidgets import QPushButton, QLineEdit, QSpinBox, QTextEdit, QApplication

from domain.ShuttleWidgetGroup import ShuttleWidgetGroup


def test_update_list_is_read_only():
    app = QApplication(sys.argv)
    shuttleWidgetGroup = ShuttleWidgetGroup(start_btn_widget=QPushButton(),
                                            shuttle_name_widget=QLineEdit(),
                                            url_widget=QLineEdit(),
                                            period_widget=QSpinBox(),
                                            target_classes_widget=QLineEdit(),
                                            update_list_widget=QTextEdit())

    result: QTextEdit = shuttleWidgetGroup.updated_list()

    assert result.isReadOnly() is True
