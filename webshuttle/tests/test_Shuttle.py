import sys

import pytest as pytest
from PyQt5.QtWidgets import QApplication, QLineEdit, QTextEdit, QWidget, QSpinBox

from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.Shuttle import Shuttle
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_shuttle_is_become_None_when_stopped(qapp):
    widget = QWidget()
    shuttle = Shuttle(parent_widget=widget,
                      shuttle_widget_group=ShuttleWidgetGroup(shuttle_name_widget=QLineEdit(),
                                                              url_widget=QLineEdit(),
                                                              period_widget=QSpinBox(),
                                                              target_classes_widget=QLineEdit(),
                                                              state_widget=QTextEdit(),
                                                              parent=None),
                      shuttle_id=0, shuttles=[], chrome_service=None, time=DefaultTime(), mixer_sound=None)
    shuttle.shuttle_list.append(shuttle)

    shuttle.stop()

    assert shuttle.shuttle_list[shuttle.id] is None
