import sys
import time

from selenium.webdriver.remote.webelement import WebElement

from EventListenerInjector import EventListenerInjector
from WebCrawler import WebCrawler
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit


class MyApp(QWidget):
    _log_textedit: QTextEdit
    _webCrawler: WebCrawler

    def __init__(self):
        super().__init__()
        self._contents = None
        self._lineText = None
        self._check_btn = None
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
        self._log_textedit = QTextEdit(self)
        self._log_textedit.setReadOnly(True)
        start_btn = QPushButton('Open the chrome browser', self)
        start_btn.clicked.connect(self._open_browser)
        get_element_btn = QPushButton('Get target element data', self)
        get_element_btn.clicked.connect(self._get_target_element_data)
        self._lineText = QLineEdit()
        self._lineText.setPlaceholderText('https://example.com')
        check_btn = QPushButton('Check')
        check_btn.clicked.connect(self._check)
        self.setLayout(self._vbox_layout(self._lineText, start_btn, get_element_btn, check_btn, self._log_textedit))
        self.show()

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())

    def _vbox_layout(self, line_text, start_btn, get_element_btn, check_btn, log_box):
        result = QVBoxLayout()
        result.addWidget(line_text)
        result.addWidget(start_btn)
        result.addWidget(get_element_btn)
        result.addWidget(check_btn)
        result.addWidget(log_box)
        return result

    def _open_browser(self):
        self._webCrawler = WebCrawler(self._lineText.text())
        self._init_eventlistener(self._webCrawler)

    def _init_eventlistener(self, web_crawler):
        injector = EventListenerInjector(web_crawler)
        injector.add_mouseover()
        injector.add_mouseleave()
        injector.add_mousedown_right()
        injector.add_tooltip()

    def _get_target_element_data(self):
        result: WebElement = self._webCrawler.get_target_element()
        self._element_y = self._webCrawler.get_element_pos_y()
        self._element_x = self._webCrawler.get_element_pos_x()
        self._scroll_x = self._webCrawler.get_scroll_x()
        self._scroll_y = self._webCrawler.get_scroll_y()
        self._contents = result.text
        self._log_textedit.setText('{0} - Successfully get target element data.\n'.format(self._local_time_now()))
        self._log_textedit.append('scroll_y : {0}'.format(self._scroll_y))
        self._log_textedit.append('scroll_x : {0}'.format(self._scroll_x))
        self._log_textedit.append('element_y : {0}'.format(self._element_y))
        self._log_textedit.append('element_x : {0}'.format(self._element_x))
        self._log_textedit.append('\n--- contents ---\n')
        self._log_textedit.append(self._contents)

    def _check(self):
        url = self._lineText.text()
        tmp_web_crawler = WebCrawler(url)
        tmp_web_crawler.scroll_to(self._scroll_x, self._scroll_y)
        self._log_textedit.setText(
            '{0} - scroll_to({1}, {2})\n'.format(self._local_time_now(), self._scroll_x, self._scroll_y))
        time.sleep(3)
        element = tmp_web_crawler.execute_js(
            'return document.elementFromPoint({0}, {1});'.format(self._element_x, self._element_y))
        self._log_textedit.append(
            '{0} - Get text of document.elementFromPoint({1}, {2}) \n'.format(self._local_time_now(), self._element_x,
                                                                              self._element_y))
        self._log_textedit.append(element.text)

    def _local_time_now(self):
        now = time.localtime()
        return "%04d/%02d/%02d %02d:%02d:%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
