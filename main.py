import sys

from EventListenerInjector import EventListenerInjector
from WebCrawler import WebCrawler
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self._webCrawler = None
        self._logBox = None
        self._content = None
        self._lineText = None
        self._check_btn = None
        self._init_ui()
        self._element_x = None
        self._element_y = None

    def _init_ui(self):
        self.resize(400, 400)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self._logBox = QTextEdit(self)
        self._logBox.setReadOnly(True)
        start_btn = QPushButton('Browser Open', self)
        start_btn.clicked.connect(self._open_browser)
        get_element_btn = QPushButton('Get Target Element', self)
        get_element_btn.clicked.connect(self._get_target_element)
        self._lineText = QLineEdit()
        self._lineText.setPlaceholderText('https://example.com')
        check_btn = QPushButton('Check')
        check_btn.clicked.connect(self._check_difference)
        self.setLayout(self._vbox_layout(self._lineText, start_btn, get_element_btn, check_btn, self._logBox))
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

    def _get_target_element(self):
        result = self._webCrawler.get_target_element()
        self._content = result.text

    def _check_difference(self, web_crawler):
        url = self._lineText.text()
        tmp_web_crawler = web_crawler(url)
        element = tmp_web_crawler.driver.execute_script('return document.elementFromPoint(arguments[0], arguments[1]);',
                                                        self._element_x, self._element_y)
        if self._content != element.text :
            self._logBox.setText('Got News!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
