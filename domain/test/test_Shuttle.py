import sys
import unittest

import pytest as pytest
from PyQt5.QtWidgets import QApplication, QLineEdit, QTextEdit, QPushButton, QWidget

from domain.DefaultTime import DefaultTime
from domain.Shuttle import Shuttle
from domain.ShuttleWidgetGroup import ShuttleWidgetGroup


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_create(qapp):
    shuttle = Shuttle(parent_widget=QWidget(),
                      shuttle_widget_group=ShuttleWidgetGroup(start_btn_widget=QPushButton(),
                                                              shuttle_name_widget=QLineEdit(),
                                                              url_widget=QLineEdit(), period_widget=QLineEdit(),
                                                              target_classes_widget=QLineEdit(),
                                                              update_list_widget=QTextEdit()),
                      shuttle_id=0, shuttles=[], chrome_service=None, time=DefaultTime(), mixer_sound=None)

    assert shuttle is not None


def test_shuttle_is_become_None_when_stopped(qapp):
    shuttle = Shuttle(parent_widget=QWidget(),
                      shuttle_widget_group=ShuttleWidgetGroup(start_btn_widget=QPushButton(),
                                                              shuttle_name_widget=QLineEdit(),
                                                              url_widget=QLineEdit(), period_widget=QLineEdit(),
                                                              target_classes_widget=QLineEdit(),
                                                              update_list_widget=QTextEdit()),
                      shuttle_id=0, shuttles=[], chrome_service=None, time=DefaultTime(), mixer_sound=None)
    shuttle.shuttle_list.append(shuttle)

    shuttle.stop()

    assert shuttle.shuttle_list[shuttle.id] is None
