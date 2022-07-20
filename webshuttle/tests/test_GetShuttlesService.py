import sys

import pytest
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QSpinBox

from webshuttle.application.GetShuttlesService import GetShuttlesService
from webshuttle.adapter.incoming.ui.ShuttleFrame import ShuttleFrame
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_sequence_of_shuttle_id_is_renewed_when_saved_shuttle_is_deleted(qapp):
    getShuttlesService = GetShuttlesService()
    shuttle_frames = {}
    for i in range(4):
        str_i = str(i)
        shuttle_frames["shuttle" + str_i] = ShuttleFrame(shuttles={}, shuttle_seq=i,
                                                         chrome_driver=None,
                                                         shuttle_widget_group=ShuttleWidgetGroup(QWidget(),
                                                         shuttle_name_widget=QLineEdit(f"셔틀{str_i}"),
                                                         url_widget=QLineEdit(f"http://{str_i}.com"),
                                                         period_widget=QSpinBox(),
                                                         target_classes_widget=QLineEdit(f"targetClasses{str_i}")),
                                                         shuttles_widget=QWidget())

    shuttle_frames.pop("shuttle1")
    result = getShuttlesService.saved_shuttles_to_json(shuttle_frames)

    shuttle_widget_group_2: dict = result["shuttle2"]
    assert shuttle_widget_group_2["name"] == "셔틀3"
    assert shuttle_widget_group_2["url"] == "http://3.com"
    assert shuttle_widget_group_2["element_classes"] == "targetClasses3"
