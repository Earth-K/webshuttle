import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QSpinBox, QFrame

from domain.DefaultTime import DefaultTime
from domain.LogText import LogText
from domain.Shuttle import Shuttle
from domain.ShuttleWidgetGroup import ShuttleWidgetGroup

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
        wrap_layout: QVBoxLayout = QVBoxLayout()

        shuttle_frame = QFrame()
        shuttle_frame.setFrameShape(QFrame.Box)
        shuttle_frame.setFrameShadow(QFrame.Sunken)
        shuttle_frame.setLayout(wrap_layout)

        # TODO: 박스 안에 셔틀 이름, 편집 버튼, 시작/종료 버튼 넣고 편집 버튼 누르면 내용 수정 및 삭제 가능 하게 만들어 보기
        shuttle_layout1: QHBoxLayout = QHBoxLayout()
        shuttle_layout1.addWidget(QLabel('셔틀 이름 : '))
        shuttle_name_widget = shuttle_name_lineedit(name)
        shuttle_layout1.addWidget(shuttle_name_widget)
        shuttle_layout1.addWidget(
            self._delete_button(shuttle_frame, shuttle_name_widget, log_edittext_widget, self.shuttle_seq))
        wrap_layout.addLayout(shuttle_layout1)

        shuttle_layout2: QHBoxLayout = QHBoxLayout()
        shuttle_layout2.addWidget(QLabel('URL : '))
        url_widget = url_lineedit(url)
        shuttle_layout2.addWidget(url_widget)
        shuttle_layout2.addWidget(QLabel('확인 주기(초) : '))
        period_widget = period_spinbox(period)
        shuttle_layout2.addWidget(period_widget)
        shuttle_layout2.addWidget(QLabel('타깃 클래스 : '))
        target_classes_widget = target_classes_lineedit(target_classes)
        shuttle_layout2.addWidget(target_classes_widget)
        shuttle_layout2.addWidget(
            self.start_button(self.shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget,
                              log_edittext_widget))
        wrap_layout.addLayout(shuttle_layout2)
        self.shuttles_vbox_layout.addWidget(shuttle_frame)

    def start_button(self, shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget, log_edittext_widget):
        start_btn = QPushButton('시작')
        start_btn.clicked.connect(
            lambda: self._start(shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget,
                                log_edittext_widget, start_btn))
        return start_btn

    def get_saved_shuttles_array(self):
        if self.shuttles_vbox_layout is None:
            return []
        result = []
        for i in range(self.shuttles_vbox_layout.count()):
            shuttle_id = "shuttle" + str(i)
            shuttle_wrap_layout = self.shuttles_vbox_layout.itemAt(i).widget().layout()
            shuttle_data_list = []
            for j in range(shuttle_wrap_layout.count()):
                shuttle_inner_layout = shuttle_wrap_layout.itemAt(j).layout()
                for k in range(shuttle_inner_layout.count()):
                    widget = shuttle_inner_layout.itemAt(k).widget()
                    if type(widget) is QLineEdit or type(widget) is QSpinBox:
                        shuttle_data_list.append(widget.text())
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
        log_edittext_widget.append(LogText(self.time.localtime()).removed_shuttle(shuttle_name_widget.text()))
        shuttle_frame.deleteLater()

    def _start(self, shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget,
               log_edittext_widget, start_btn_widget):
        if start_btn_widget.text() == '시작':
            shuttle_name = shuttle_name_widget.text()
            if shuttle_name == "":
                shuttle_name = "이름 없음"
            message = LogText(self.time.localtime()).started_shuttle(shuttle_name)
            log_edittext_widget.append(message)
            period_widget.setReadOnly(True)
            start_btn_widget.setText('중지')
            self.shuttles[shuttle_seq] = Shuttle(self, self.shuttles, shuttle_seq,
                                                 ShuttleWidgetGroup(shuttle_name_widget=shuttle_name_widget,
                                                                    url_widget=url_widget,
                                                                    period_widget=period_widget,
                                                                    target_classes_widget=target_classes_widget,
                                                                    update_list_widget=log_edittext_widget,
                                                                    start_btn_widget=start_btn_widget),
                                                 self.chrome_service, pygame.mixer.Sound("resource/sounds/sound.wav"))
            self.shuttles[shuttle_seq].start()
        else:
            message = LogText(self.time.localtime()).stopped_shuttle(shuttle_name_widget.text())
            log_edittext_widget.append(message)
            period_widget.setReadOnly(False)
            self.shuttles[shuttle_seq] = None
            start_btn_widget.setText('시작')
