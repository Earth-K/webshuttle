import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from EventListenerInjector import EventListenerInjector
from WebCrawler import WebCrawler
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit


def init_event_listener(web_crawler):
    injector = EventListenerInjector(web_crawler)
    injector.add_mouseover()
    injector.add_mouseleave()
    injector.add_mousedown_right()
    injector.add_tooltip()


def local_time_now():
    now = time.localtime()
    return "%04d/%02d/%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


class MyApp(QWidget):
    textedit_log: QTextEdit
    _webCrawler: WebCrawler

    def __init__(self):
        super().__init__()
        self.textedit_log = QTextEdit()
        self.lineedit = QLineEdit()
        self.lineedit_period = QLineEdit()
        self.thread_auto_check = None
        self._contents = None
        self._element_x = None
        self._element_y = None
        self._scroll_x = None
        self._scroll_y = None
        self._element_class_names = None
        self._init_ui()

    def _init_ui(self):
        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        vbox_layout = self._vbox_layout()
        self.setLayout(vbox_layout)
        self.show()

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())

    def _vbox_layout(self):
        result = QVBoxLayout()
        lineedit = self.lineedit_url()
        result.addWidget(lineedit)
        result.addWidget(self._button_open_browser(lineedit))
        result.addWidget(self._button_get_element_data())
        result.addWidget(self._lineedit_period())
        result.addWidget(self._button_check())
        result.addWidget(self._textedit_log())
        return result

    def _lineedit_period(self):
        self.lineedit_period.setPlaceholderText('Check Period (sec)')
        return self.lineedit_period

    def _button_check(self):
        button_check = QPushButton('Check')
        button_check.clicked.connect(self._check)
        return button_check

    def _button_get_element_data(self):
        button_get_element = QPushButton('Get target element data', self)
        button_get_element.clicked.connect(self._get_target_element_data)
        return button_get_element

    def _button_open_browser(self, lineedit):
        button_open_browser = QPushButton('Open in chrome browser', self)
        button_open_browser.clicked.connect(lambda: self._open_browser(lineedit))
        return button_open_browser

    def _textedit_log(self):
        self.textedit_log.setReadOnly(True)
        return self.textedit_log

    def lineedit_url(self):
        self.lineedit.setPlaceholderText('https://example.com')
        return self.lineedit

    def _open_browser(self, lineedit):
        self._webCrawler = WebCrawler(lineedit.text())
        init_event_listener(self._webCrawler)

    def _get_target_element_data(self):
        result: WebElement = self._webCrawler.get_target_element()
        self._element_y = self._webCrawler.get_element_pos_y()
        self._element_x = self._webCrawler.get_element_pos_x()
        self._scroll_x = self._webCrawler.get_scroll_x()
        self._scroll_y = self._webCrawler.get_scroll_y()
        self._contents = result.text
        self.textedit_log.setText('{0} - get target element data.\n'.format(local_time_now()))
        self.textedit_log.append('scroll_y : {0}'.format(self._scroll_y))
        self.textedit_log.append('scroll_x : {0}'.format(self._scroll_x))
        self.textedit_log.append('element_y : {0}'.format(self._element_y))
        self.textedit_log.append('element_x : {0}'.format(self._element_x))
        self.textedit_log.append('\n--- contents ---\n')
        self.textedit_log.append(self._contents)

    def _check(self):
        self.thread_auto_check = threading.Thread(target=self.check_content, args=(
            self.lineedit.text(), self._scroll_x, self._scroll_y, self._element_x, self._element_y))
        self.thread_auto_check.daemon = True
        self.thread_auto_check.start()

    def check_content(self, lineedit_url, scroll_x, scroll_y, element_x, element_y):
        url = lineedit_url
        while True:
            options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
            options.add_argument('headless')  # headless 모드 설정
            options.add_argument("--start-maximized")  # add
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            tmp_web_crawler = WebCrawler(url, options)
            time.sleep(1)
            tmp_web_crawler.scroll_to(scroll_x, scroll_y)
            print('{0} - scrollTo({1}, {2}).\n'.format(local_time_now(), scroll_x, scroll_y))
            time.sleep(2)
            element = tmp_web_crawler.execute_js(
                'return document.elementFromPoint({0}, {1});'.format(element_x, element_y))
            print('{0} - get text of document.elementFromPoint({1}, {2}).\n'.format(local_time_now(), self._element_x,
                                                                                    self._element_y))
            print(element.text)
            tmp_web_crawler.close_driver()
            time.sleep(int(self._lineedit_period().text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
