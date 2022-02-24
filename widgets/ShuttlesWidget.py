import threading
import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton
from selenium import webdriver

from WebCrawler import WebCrawler
from domain.Shuttle import Shuttle


def shuttle_setting_layout(hbox_layout):
    result = QVBoxLayout()
    result.addLayout(hbox_layout)
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
        period_lineedit.setReadOnly(True)
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
        start_btn.clicked.connect(lambda: self._start(url_lineedit, period_lineedit, target_classes_lineedit, log_edittext))
        hbox_layout_shuttle.addWidget(start_btn)
        hbox_layout_shuttle.addWidget(QPushButton('Stop'))
        hbox_layout_memo = QHBoxLayout()
        hbox_layout_memo.addWidget(QLabel('description : '))
        description = QLineEdit()
        description.setPlaceholderText('description...')
        hbox_layout_memo.addWidget(description)

        vbox_wrap_layout.addLayout(hbox_layout_shuttle)
        vbox_wrap_layout.addLayout(hbox_layout_memo)
        self._vbox_layout.addLayout(vbox_wrap_layout)

    def _start(self, url, period, target_classes, edittext):
        thread = threading.Thread(target=self._check_content,
                                  args=(url, period, target_classes, edittext))
        thread.daemon = True
        thread.start()

    def _check_content(self, url, period, target_classes, edittext):
        while True:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument("--start-maximized")
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            tmp_web_crawler = WebCrawler(url.text(), options)
            time.sleep(1)
            elements = tmp_web_crawler.get_elements_by_classnames(target_classes.text())
            for e in elements:
                edittext.append(e.text)
            tmp_web_crawler.close_driver()
            time.sleep(int(period.text()))
