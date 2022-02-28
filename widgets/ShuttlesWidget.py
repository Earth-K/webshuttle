import threading
import time

import pyglet
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from selenium import webdriver

from WebCrawler import WebCrawler
from domain.Shuttle import Shuttle


def shuttle_setting_layout(hbox_layout):
    result = QVBoxLayout()
    result.addLayout(hbox_layout)
    return result


def get_text_list(elements):
    result = []
    for e in elements:
        result.append(e.text)
    return result


class ShuttlesWidget(QWidget):
    def __init__(self, parent):
        super(ShuttlesWidget, self).__init__(parent)
        self.shuttles = []
        self._init_ui()

    def _init_ui(self):
        self._vbox_layout = QVBoxLayout()
        title = QLabel()
        title.setText("Saved Shuttles : ")
        self._vbox_layout.addWidget(title)
        self._vbox_layout.addStretch(4)
        self.setLayout(self._vbox_layout)
        self.show()

    def add_shuttle(self, url, period, target_classes, log_edittext):
        self.shuttles.append(Shuttle(url, period, target_classes))

        url_lineedit = QLineEdit()
        url_lineedit.setText(url)
        url_lineedit.setReadOnly(True)
        period_lineedit = QLineEdit()
        period_lineedit.setText(period)
        target_classes_lineedit = QLineEdit()
        target_classes_lineedit.setText(target_classes)
        target_classes_lineedit.setReadOnly(True)

        vbox_wrap_layout = QVBoxLayout()
        hbox_layout_shuttle = QHBoxLayout()
        hbox_layout_shuttle.addWidget(QLabel('url : '))
        hbox_layout_shuttle.addWidget(url_lineedit)
        hbox_layout_shuttle.addWidget(QLabel('check period : '))
        hbox_layout_shuttle.addWidget(period_lineedit)
        hbox_layout_shuttle.addWidget(QLabel('target classes : '))
        hbox_layout_shuttle.addWidget(target_classes_lineedit)
        start_btn = QPushButton('Start')
        stop_btn = QPushButton('Stop')

        start_btn.clicked.connect(
            lambda: self._start(url_lineedit, period_lineedit, target_classes_lineedit, log_edittext, start_btn,
                                stop_btn))
        hbox_layout_shuttle.addWidget(start_btn)

        stop_btn.setDisabled(True)
        stop_btn.clicked.connect(lambda: self._stop(period_lineedit, start_btn, stop_btn))
        hbox_layout_shuttle.addWidget(stop_btn)

        hbox_layout_memo = QHBoxLayout()
        hbox_layout_memo.addWidget(QLabel('description : '))
        description = QLineEdit()
        description.setPlaceholderText('description...')
        hbox_layout_memo.addWidget(description)

        vbox_wrap_layout.addLayout(hbox_layout_shuttle)
        vbox_wrap_layout.addLayout(hbox_layout_memo)
        self._vbox_layout.addLayout(vbox_wrap_layout)
        self._vbox_layout.addStretch(4)

    def _stop(self, period, start_btn, stop_btn):
        period.setReadOnly(False)
        stop_btn.setDisabled(True)
        start_btn.setDisabled(False)

    def _start(self, url, period, target_classes, log_edittext, start_btn, stop_btn):
        if not period.text().isdigit():
            QMessageBox.information(self, 'Please input a number',
                                    "You have to input a number at field of 'check period'.",
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return
        period.setReadOnly(True)
        start_btn.setDisabled(True)
        stop_btn.setDisabled(False)
        thread = threading.Thread(target=self._check_content,
                                  args=(url, period, target_classes, log_edittext, start_btn))
        thread.daemon = True
        thread.start()

    def _check_content(self, url, period, target_classes, log_edittext, start_btn: QPushButton):
        text_list = []
        while True:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument("--start-maximized")
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            tmp_web_crawler = WebCrawler(url.text(), options)
            time.sleep(1)
            elements = tmp_web_crawler.get_elements_by_classnames(target_classes.text())

            no_newline_text = ""
            if len(text_list) > 0:
                new_text_list = get_text_list(elements)
                for new_text in new_text_list:
                    if new_text not in text_list:
                        # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
                        no_newline_text += new_text.replace("\n", " | ") + "\n"
                text_list = new_text_list
            else:
                for e in elements:
                    text_list.append(e.text)
                    # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
                    no_newline_text += e.text.replace("\n", " | ") + "\n"

            if len(no_newline_text) > 0:
                log_edittext.append(no_newline_text + "\n")
                pyglet.resource.media('water.wav').play()

            tmp_web_crawler.close_driver()

            if start_btn.isEnabled() is True:
                log_edittext.append("Stopped a shuttle." + "\n")
                break
            time.sleep(int(period.text()))
