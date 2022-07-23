import sys
import threading

import pytest as pytest
from PyQt5.QtWidgets import QApplication, QLineEdit, QTextEdit, QWidget, QSpinBox

from webshuttle.domain.Shuttle import Shuttle
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_shuttle_is_become_none_when_stopped(qapp):
    shuttles = []
    waiting_event = threading.Event()
    shuttle = Shuttle(parent_widget=QWidget(), shuttles=shuttles, shuttle_seq=0,
                      shuttle_widget_group=ShuttleWidgetGroup(state_widget=QTextEdit(),
                                                              target_classes_widget=QLineEdit(),
                                                              period_widget=QSpinBox(), url_widget=QLineEdit(),
                                                              shuttle_name_widget=QLineEdit(),
                                                              filtering_keyword_widget=QLineEdit(), parent=None), chrome_driver=None,
                      waiting_event=waiting_event)
    shuttles.append(shuttle)

    shuttle.stop()

    assert shuttles[shuttle.shuttle_seq] is None
