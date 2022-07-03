import sys

from PyQt5.QtWidgets import QLineEdit, QSpinBox, QTextEdit, QApplication

from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


def test_update_list_is_read_only():
    app = QApplication(sys.argv)
    shuttleWidgetGroup = ShuttleWidgetGroup(shuttle_name_widget=QLineEdit(),
                                            url_widget=QLineEdit(),
                                            period_widget=QSpinBox(),
                                            target_classes_widget=QLineEdit(),
                                            update_list_widget=QTextEdit())

    result: QTextEdit = shuttleWidgetGroup.updated_list()

    assert result.isReadOnly() is True
