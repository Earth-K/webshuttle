import sys
import unittest

from PyQt5.QtWidgets import QPushButton, QLineEdit, QSpinBox, QTextEdit, QApplication

from domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ShuttleWidgetGroupTest(unittest.TestCase):
    def test_update_list_is_read_only(self):
        shuttleWidgetGroup = ShuttleWidgetGroup(start_btn_widget=QPushButton(),
                                                shuttle_name_widget=QLineEdit(),
                                                url_widget=QLineEdit(),
                                                period_widget=QSpinBox(),
                                                target_classes_widget=QLineEdit(),
                                                update_list_widget=QTextEdit())

        result: QTextEdit = shuttleWidgetGroup.updated_list()

        self.assertTrue(result.isReadOnly())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    unittest.main()
    sys.exit(app.exec_())
