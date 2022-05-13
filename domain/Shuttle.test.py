import sys
import unittest

from PyQt5.QtWidgets import QApplication, QLineEdit, QTextEdit, QPushButton, QWidget

from domain.DefaultTime import DefaultTime
from domain.Shuttle import Shuttle
from domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ShuttleTest(unittest.TestCase):
    def test_create(self):
        shuttle = Shuttle(parent_widget=QWidget(),
                          shuttle_widget_group=ShuttleWidgetGroup(start_btn_widget=QPushButton(),
                                                                  shuttle_name_widget=QLineEdit(),
                                                                  url_widget=QLineEdit(), period_widget=QLineEdit(),
                                                                  target_classes_widget=QLineEdit(),
                                                                  update_list_widget=QTextEdit()),
                          shuttle_id=0, shuttles=[], chrome_service=None, time=DefaultTime(), mixer_sound=None)

        self.assertIsNotNone(shuttle)

    def test_shuttle_is_become_None_when_stopped(self):
        shuttle = Shuttle(parent_widget=QWidget(),
                          shuttle_widget_group=ShuttleWidgetGroup(start_btn_widget=QPushButton(),
                                                                  shuttle_name_widget=QLineEdit(),
                                                                  url_widget=QLineEdit(), period_widget=QLineEdit(),
                                                                  target_classes_widget=QLineEdit(),
                                                                  update_list_widget=QTextEdit()),
                          shuttle_id=0, shuttles=[], chrome_service=None, time=DefaultTime(), mixer_sound=None)
        shuttle.shuttle_list.append(shuttle)

        shuttle.stop()

        self.assertEqual(shuttle.shuttle_list[shuttle.id], None)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    unittest.main()
    sys.exit(app.exec_())
