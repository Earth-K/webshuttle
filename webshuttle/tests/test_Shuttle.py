import sys

import pytest as pytest
from PyQt5.QtWidgets import QApplication, QLineEdit, QTextEdit, QWidget, QSpinBox

from webshuttle.domain.Shuttle import Shuttle
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_shuttle_is_become_none_when_stopped(qapp):
    shuttles = []
    shuttle = Shuttle(parent_widget=QWidget(), shuttles=shuttles, shuttle_id=0,
                      shuttle_widget_group=ShuttleWidgetGroup(shuttle_name_widget=QLineEdit(),
                                                              url_widget=QLineEdit(),
                                                              period_widget=QSpinBox(),
                                                              target_classes_widget=QLineEdit(),
                                                              state_widget=QTextEdit(),
                                                              parent=None), chrome_driver=None, mixer_sound=None)
    shuttles.append(shuttle)

    shuttle.stop()

    assert shuttles[shuttle.id] is None
