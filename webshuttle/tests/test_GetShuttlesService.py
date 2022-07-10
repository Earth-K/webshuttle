import sys

import pytest
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QSpinBox

from webshuttle.application.GetShuttlesService import GetShuttlesService
from webshuttle.domain.ShuttleFrame import ShuttleFrame
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_get_shuttles(qapp):
    getShuttlesService = GetShuttlesService()
    shuttle_frames = {}
    for i in range(4):
        str_i = str(i)
        shuttle_frames["shuttle" + str_i] = ShuttleFrame({}, i, None,
                                                         ShuttleWidgetGroup(QWidget(),
                                                                            shuttle_name_widget=QLineEdit(f"셔틀{str_i}"),
                                                                            url_widget=QLineEdit(f"http://{str_i}.com"),
                                                                            period_widget=QSpinBox(),
                                                                            target_classes_widget=QLineEdit(f"targetClasses{str_i}")),
                                                         QWidget(), None)

    shuttle_frames.pop("shuttle1")
    result = getShuttlesService.saved_shuttles_to_json(shuttle_frames)

    shuttle_widget_group_2: dict = result["shuttle2"]
    assert shuttle_widget_group_2["name"] == "셔틀3"
    assert shuttle_widget_group_2["url"] == "http://3.com"
    assert shuttle_widget_group_2["element_classes"] == "targetClasses3"
