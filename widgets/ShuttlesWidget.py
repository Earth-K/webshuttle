import threading

import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QSpinBox
from selenium import webdriver

from domain.DefaultTime import DefaultTime
from domain.LogText import LogText
from domain.Shuttle import Shuttle
from domain.WebScraper import WebScraper

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
        wrap_layout: QVBoxLayout = QVBoxLayout()

        shuttle_layout1: QHBoxLayout = QHBoxLayout()
        shuttle_layout1.addWidget(QLabel('셔틀 이름 : '))
        shuttle_name_widget = shuttle_name_lineedit(name)
        shuttle_layout1.addWidget(shuttle_name_widget)
        shuttle_layout1.addWidget(self._delete_button(wrap_layout, shuttle_name_widget, log_edittext_widget))
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
        start_btn = QPushButton('시작')
        start_btn.clicked.connect(
            lambda: self._start(self.shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget,
                                log_edittext_widget, start_btn))
        shuttle_layout2.addWidget(start_btn)
        wrap_layout.addLayout(shuttle_layout2)

        self.shuttles_vbox_layout.addLayout(wrap_layout)
        self.shuttle_seq += 1

    def get_saved_shuttles_array(self):
        if self.shuttles_vbox_layout is None:
            return
        result = []
        for i in range(self.shuttles_vbox_layout.count()):
            shuttle_id = "shuttle" + str(i)
            shuttle_wrap_layout = self.shuttles_vbox_layout.itemAt(i)
            shuttle_data_list = []
            for j in range(shuttle_wrap_layout.count()):
                shuttle_inner_layout = shuttle_wrap_layout.itemAt(j)
                for k in range(shuttle_inner_layout.count()):
                    widget = shuttle_inner_layout.itemAt(k).widget()
                    if type(widget) is QLineEdit or type(widget) is QSpinBox:
                        shuttle_data_list.append(widget.text())
            result.append((shuttle_id, shuttle_data_list))
        return result

    def _delete_button(self, vbox_wrap_layout, shuttle_name_widget, log_edittext_widget):
        delete_btn = QPushButton('삭제')
        delete_btn.clicked.connect(
            lambda: self._remove_shuttle(vbox_wrap_layout, shuttle_name_widget, log_edittext_widget))
        return delete_btn

    def _remove_shuttle(self, vbox_wrap_layout: QVBoxLayout, shuttle_name_widget, log_edittext_widget):
        self.shuttles[self.shuttle_seq].stop()
        log_edittext_widget.append(LogText(self.time.localtime()).stopped_shuttle(shuttle_name_widget.text()))
        log_edittext_widget.append(LogText(self.time.localtime()).removed_shuttle(shuttle_name_widget.text()))
        self._remove_shuttle_layout(vbox_wrap_layout)

    def _remove_shuttle_layout(self, vbox_wrap_layout):
        while vbox_wrap_layout.count():
            child = vbox_wrap_layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            else:
                self._remove_shuttle_layout(child.layout())
        vbox_wrap_layout.deleteLater()

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
            self.shuttles[shuttle_seq] = Shuttle(self.shuttles, shuttle_seq, shuttle_name_widget, url_widget,
                                                 period_widget, target_classes_widget, log_edittext_widget,
                                                 start_btn_widget, self.chrome_service)
            self.shuttles[shuttle_seq].start()
        else:
            message = LogText(self.time.localtime()).stopped_shuttle(shuttle_name_widget.text())
            log_edittext_widget.append(message)
            period_widget.setReadOnly(False)
            self.shuttles[shuttle_name_widget.text()] = None
            start_btn_widget.setText('시작')
