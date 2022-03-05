import threading
import time

import pyglet
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from selenium import webdriver

from WebCrawler import WebCrawler
from domain.LogText import LogText


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
    def __init__(self, parent, chrome_service):
        super(ShuttlesWidget, self).__init__(parent)
        self.shuttles = []
        self.chrome_service = chrome_service
        self._init_ui()

    def _init_ui(self):
        self.title_vbox_layout = QVBoxLayout()
        title = QLabel()
        title.setText("Saved Shuttles : ")
        self.shuttles_vbox_layout = QVBoxLayout()
        self.title_vbox_layout.addWidget(title)
        stretch_vbox_layout = QVBoxLayout()
        stretch_vbox_layout.addStretch(4)
        wrap_vbox_layout = QVBoxLayout()
        wrap_vbox_layout.addLayout(self.title_vbox_layout)
        wrap_vbox_layout.addLayout(self.shuttles_vbox_layout)
        wrap_vbox_layout.addLayout(stretch_vbox_layout)
        self.setLayout(wrap_vbox_layout)
        self.show()

    def add_shuttle(self, url, period, target_classes, log_edittext):
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

        hbox_layout_memo = QHBoxLayout()
        hbox_layout_memo.addWidget(QLabel('name : '))
        shuttle_name = QLineEdit()
        shuttle_name.setPlaceholderText('Set name...')
        hbox_layout_memo.addWidget(shuttle_name)
        delete_btn = QPushButton('remove')
        delete_btn.clicked.connect(lambda: self.remove_shuttles(vbox_wrap_layout))
        hbox_layout_memo.addWidget(delete_btn)

        start_btn = QPushButton('Start')
        stop_btn = QPushButton('Stop')

        start_btn.clicked.connect(
            lambda: self._start(shuttle_name, url_lineedit, period_lineedit, target_classes_lineedit, log_edittext, start_btn,
                                stop_btn))
        hbox_layout_shuttle.addWidget(start_btn)

        stop_btn.setDisabled(True)
        stop_btn.clicked.connect(lambda: self._stop(period_lineedit, start_btn, stop_btn))
        hbox_layout_shuttle.addWidget(stop_btn)

        vbox_wrap_layout.addLayout(hbox_layout_shuttle)
        vbox_wrap_layout.addLayout(hbox_layout_memo)

        self.shuttles_vbox_layout.addLayout(vbox_wrap_layout)

    def remove_shuttles(self, vbox_wrap_layout: QVBoxLayout):
        while vbox_wrap_layout.count():
            child = vbox_wrap_layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            else:
                self.remove_shuttles(child.layout())

    def get_saved_shuttles_array(self):
        if self.shuttles_vbox_layout is None:
            return
        result = []
        for i in range(self.shuttles_vbox_layout.count()):
            shuttle_id = "shuttle"+str(i)
            shuttle_wrap_layout = self.shuttles_vbox_layout.itemAt(i)
            shuttle_data_list = []
            for j in range(shuttle_wrap_layout.count()):
                shuttle_inner_layout = shuttle_wrap_layout.itemAt(j)
                for k in range(shuttle_inner_layout.count()):
                    widget = shuttle_inner_layout.itemAt(k).widget()
                    if type(widget) is QLineEdit:
                        shuttle_data_list.append(widget.text())
            result.append((shuttle_id, shuttle_data_list))
        return result

    def _stop(self, period, start_btn, stop_btn):
        period.setReadOnly(False)
        stop_btn.setDisabled(True)
        start_btn.setDisabled(False)

    def _start(self, shuttle_name, url, period, target_classes, log_edittext, start_btn, stop_btn):
        if not period.text().isdigit():
            QMessageBox.information(self, 'Please input a number',
                                    "You have to input a number at field of 'check period'.",
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return
        period.setReadOnly(True)
        start_btn.setDisabled(True)
        stop_btn.setDisabled(False)
        thread = threading.Thread(target=self._check_content,
                                  args=(shuttle_name, url, period, target_classes, log_edittext, start_btn))
        thread.daemon = True
        thread.start()

    def _check_content(self, shuttle_name, url, period, target_classes, log_edittext, start_btn: QPushButton):
        text_list = []
        while True:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument("--start-maximized")
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            tmp_web_crawler = WebCrawler(url.text(), options, self.chrome_service)
            time.sleep(1)
            elements = tmp_web_crawler.get_elements_by_classnames(target_classes.text())

            shuttle_name_text = "No Named"
            if shuttle_name.text() != "":
                shuttle_name_text = shuttle_name.text()

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
                log_text = LogText()
                log_edittext.append("[ " + shuttle_name_text + " ]" + log_text.local_time_now())
                log_edittext.append(no_newline_text + "\n")
                pyglet.resource.media('water.wav').play()

            tmp_web_crawler.close_driver()

            if start_btn.isEnabled() is True:
                log_edittext.append("Stopped a shuttle." + "\n")
                break
            time.sleep(int(period.text()))
