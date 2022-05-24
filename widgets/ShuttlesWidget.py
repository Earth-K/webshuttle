import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QSpinBox, QFrame

from domain.DefaultTime import DefaultTime
from domain.LogText import LogText
from domain.Shuttle import Shuttle
from domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from widgets.ShuttleFrame import ShuttleFrame

pygame.init()


def shuttle_setting_layout(hbox_layout):
    result = QVBoxLayout()
    result.addLayout(hbox_layout)
    return result


def url_lineedit(url):
    result = QLineEdit()
    result.setPlaceholderText('스크랩 하고 싶은 웹 페이지의 URL')
    result.setText(url)
    return result


def period_spinbox(period):
    result = QSpinBox()
    result.setMaximum(86400)
    result.setValue(int(period))
    return result


def target_classes_lineedit(target_classes):
    result = QLineEdit()
    result.setText(target_classes)
    return result


def shuttle_name_lineedit(name):
    result = QLineEdit(name)
    result.setPlaceholderText('셔틀의 이름')
    return result


def _stop(period, start_btn, stop_btn):
    period.setReadOnly(False)
    stop_btn.setDisabled(True)
    start_btn.setDisabled(False)


class ShuttlesWidget(QWidget):
    def __init__(self, parent, chrome_service, time=DefaultTime()):
        super(ShuttlesWidget, self).__init__(parent)
        self.shuttle_seq = 0
        self.shuttle_frames = {}
        self.shuttles = {}
        self.chrome_service = chrome_service
        self.time = time
        self._init_ui()

    def _init_ui(self):
        self.title_vbox_layout = QVBoxLayout()
        self.shuttles_vbox_layout = QVBoxLayout()
        self.title_vbox_layout.addWidget(QLabel('셔틀 목록'))
        wrap_vbox_layout = QVBoxLayout()
        wrap_vbox_layout.addLayout(self.title_vbox_layout)
        wrap_vbox_layout.addLayout(self.shuttles_vbox_layout)
        stretch_vbox_layout = QVBoxLayout()
        stretch_vbox_layout.addStretch(4)
        wrap_vbox_layout.addLayout(stretch_vbox_layout)
        self.setLayout(wrap_vbox_layout)
        self.show()

    def add_shuttle(self, url, period, target_classes, name, log_edittext_widget):
        self.shuttle_seq += 1

        shuttle_name_widget = shuttle_name_lineedit(name)
        target_classes_widget = target_classes_lineedit(target_classes)
        url_widget = url_lineedit(url)
        period_widget = period_spinbox(period)

        shuttle_frame = ShuttleFrame(shuttles=self.shuttles,
                                     shuttle_seq=self.shuttle_seq,
                                     chrome_service=self.chrome_service,
                                     shuttleWidgetGroup=ShuttleWidgetGroup(
                                         shuttle_name_widget=shuttle_name_widget,
                                         url_widget=url_widget,
                                         target_classes_widget=target_classes_widget,
                                         period_widget=period_widget,
                                         update_list_widget=log_edittext_widget,
                                         parent=None
                                     ), parent=self, time=self.time)

        self.shuttle_frames[self.shuttle_seq] = shuttle_frame
        self.shuttles_vbox_layout.addWidget(shuttle_frame.getFrame())

    def get_saved_shuttles_array(self):
        if self.shuttles_vbox_layout is None:
            return []
        result = []
        for i in self.shuttle_frames:
            frame: ShuttleFrame = self.shuttle_frames[i]
            shuttle_id = "shuttle" + str(i)
            shuttle_data_list = [frame.shuttleWidgets.shuttle_name_widget.text(),
                                 frame.shuttleWidgets.url_widget.text(), frame.shuttleWidgets.period_widget.text(),
                                 frame.shuttleWidgets.target_classes_widget.text()]
            result.append((shuttle_id, shuttle_data_list))
        return result

    def _delete_button(self, vbox_wrap_layout, shuttle_name_widget, log_edittext_widget, shuttle_seq):
        delete_btn = QPushButton('삭제')
        delete_btn.clicked.connect(
            lambda: self._remove_shuttle(vbox_wrap_layout, shuttle_name_widget, log_edittext_widget, shuttle_seq))
        return delete_btn

    def _remove_shuttle(self, shuttle_frame: QFrame, shuttle_name_widget, log_edittext_widget, shuttle_seq):
        if self.shuttles.get(shuttle_seq) is not None:
            log_edittext_widget.append(LogText(self.time.localtime()).stopped_shuttle(shuttle_name_widget.text()))
            self.shuttles[shuttle_seq] = None
            self.shuttle_frames.pop(shuttle_seq)
        log_edittext_widget.append(LogText(self.time.localtime()).removed_shuttle(shuttle_name_widget.text()))
        shuttle_frame.deleteLater()
