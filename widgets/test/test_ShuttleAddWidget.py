import pytest
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

from widgets.ShuttleAddWidget import ShuttleAddWidget


@pytest.fixture
def qapp():
    import sys
    return QApplication(sys.argv)


def test_shuttle_add_widget_ui(qapp):
    main_window = QMainWindow()
    main_window.add_shuttle = lambda: None

    shuttleadd_widget = ShuttleAddWidget(main_window, None)
    main_layout = shuttleadd_widget.layout()

    assert main_layout.itemAt(0).layout().itemAt(0).widget().text() == "셔틀 이름: "
    assert main_layout.itemAt(1).layout().itemAt(0).widget().text() == "URL : "
    assert main_layout.itemAt(1).layout().itemAt(2).widget().text() == "영역 선택하러 가기"
    assert main_layout.itemAt(2).layout().itemAt(0).widget().text() == "선택 영역 데이터 불러오기"
    assert main_layout.itemAt(2).layout().itemAt(1).widget().text() == "셔틀 추가"
    assert type(main_layout.itemAt(3).widget()) == QTextEdit
