import threading

import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QSpinBox
from selenium import webdriver

from domain.DefaultTime import DefaultTime
from domain.LogText import LogText
from domain.WebScraper import WebScraper

pygame.init()


def shuttle_setting_layout(hbox_layout):
    result = QVBoxLayout()
    result.addLayout(hbox_layout)
    return result


def get_text_list(elements):
    result = []
    for e in elements:
        result.append(e.text)
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
        self.shuttles = {}
        self.chrome_service = chrome_service
        self.time = time
        self._init_ui()
        self.sound = pygame.mixer.Sound("resource/sounds/sound.wav")

    def _init_ui(self):
        self.title_vbox_layout = QVBoxLayout()
        title = QLabel()
        title.setText("셔틀 목록")
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

    def add_shuttle(self, url, period, target_classes, name, log_edittext):
        wrap_layout: QVBoxLayout = QVBoxLayout()

        shuttle_layout1: QHBoxLayout = QHBoxLayout()
        shuttle_layout1.addWidget(QLabel('셔틀 이름 : '))
        shuttle_name_widget = shuttle_name_lineedit(name)
        shuttle_layout1.addWidget(shuttle_name_widget)
        shuttle_layout1.addWidget(self._delete_button(wrap_layout))

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
            lambda: self._start(shuttle_name_widget, url_widget, period_widget, target_classes_widget, log_edittext,
                                start_btn))
        shuttle_layout2.addWidget(start_btn)

        wrap_layout.addLayout(shuttle_layout1)
        wrap_layout.addLayout(shuttle_layout2)

        self.shuttles_vbox_layout.addLayout(wrap_layout)

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

    def _delete_button(self, vbox_wrap_layout):
        delete_btn = QPushButton('삭제')
        delete_btn.clicked.connect(lambda: self._remove_shuttle(vbox_wrap_layout))
        return delete_btn

    def _remove_shuttle(self, vbox_wrap_layout: QVBoxLayout):
        while vbox_wrap_layout.count():
            child = vbox_wrap_layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            else:
                self._remove_shuttle(child.layout())
        vbox_wrap_layout.deleteLater()

    def _start(self, shuttle_name, url_widget, period, target_classes, log_edittext, start_btn):
        if start_btn.text() == '시작':
            message = LogText(self.time.localtime()).started_shuttle(shuttle_name.text())
            log_edittext.append(message)
            period.setReadOnly(True)
            start_btn.setText('중지')
            self.shuttles[shuttle_name.text()] = threading.Thread(target=self._start_scrap, daemon=True, args=(
                shuttle_name, url_widget, period, target_classes, log_edittext, start_btn))
            self.shuttles[shuttle_name.text()].start()
        else:
            message = LogText(self.time.localtime()).stopped_shuttle(shuttle_name.text())
            log_edittext.append(message)
            period.setReadOnly(False)
            self.shuttles[shuttle_name.text()] = None
            start_btn.setText('시작')

    def _start_scrap(self, shuttle_name, url_widget, period, target_classes, log_edittext, start_btn):
        threading.Thread(target=self._check_content, daemon=False, args=(
            shuttle_name, url_widget, period, target_classes, log_edittext, start_btn)).start()

    def _check_content(self, shuttle_name, url_widget, period, target_classes, log_edittext, start_btn: QPushButton):
        shuttle_name_text = "이름 없음"
        if shuttle_name.text() != "":
            shuttle_name_text = shuttle_name.text()

        pre_shuttle_thread = self.shuttles[shuttle_name_text]
        text_list = []
        while True:
            if pre_shuttle_thread != self.shuttles[shuttle_name_text]:
                break
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument("--start-maximized")
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            tmp_web_crawler = WebScraper(url_widget.text(), options, self.chrome_service)
            self.time.sleep(1)
            elements = tmp_web_crawler.get_elements_by_classnames(target_classes.text())
            no_newline_text = ""
            if len(text_list) > 0:
                new_text_list = get_text_list(elements)
                for new_text in new_text_list:
                    if new_text not in text_list:
                        if len(new_text) > 0:
                            # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
                            no_newline_text += new_text.replace("\n", " | ") + "\n"
                text_list = new_text_list
            else:
                for e in elements:
                    if len(e.text) > 0:
                        text_list.append(e.text)
                        # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
                        no_newline_text += e.text.replace("\n", " | ") + "\n"
            if len(no_newline_text) > 0:
                log_text = LogText(self.time.localtime())
                log_edittext.append(log_text.updated_shuttle_name(shuttle_name_text))
                log_edittext.append(f"{no_newline_text}\n")
                self.sound.play()

            tmp_web_crawler.close_driver()
            self.time.sleep(int(period.text()))
