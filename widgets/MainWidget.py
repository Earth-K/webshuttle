import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, \
    QHBoxLayout, QLabel, QMessageBox
from selenium.webdriver.remote.webelement import WebElement

from domain.EventListenerInjector import EventListenerInjector
from domain.WebScraper import WebScraper


def local_time_now():
    now = time.localtime()
    return "%04d/%02d/%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


def init_event_listener(web_scraper):
    injector = EventListenerInjector(web_scraper)
    injector.add_mouseover()
    injector.add_mouseleave()
    injector.add_mousedown_right()
    injector.add_tooltip()


class MainWidget(QWidget):
    def __init__(self, parent, chrome_service):
        super(MainWidget, self).__init__(parent)
        self.parent_widget = parent
        self.log_textedit = QTextEdit()
        self.lineedit_shuttle_name = QLineEdit()
        self.lineedit_url = QLineEdit()
        self.contents = None
        self.element_class_names = None
        self.chrome_service = chrome_service
        self._webScraper = None
        self.save_btn = None
        self._init_ui()

    def _init_ui(self):
        vbox_layout = self._vbox_layout()
        self.setLayout(vbox_layout)
        self.show()

    def _vbox_layout(self):
        result = QVBoxLayout()

        hbox_layout_shuttle_name_layout = QHBoxLayout()
        hbox_layout_shuttle_name_layout.addWidget(QLabel('Shuttle Name : '))
        shuttle_name = self.shuttle_name()
        shuttle_name.setPlaceholderText('shuttle name...')
        hbox_layout_shuttle_name_layout.addWidget(shuttle_name)
        result.addLayout(hbox_layout_shuttle_name_layout)

        hbox_layout_url = QHBoxLayout()
        label_url = QLabel("URL : ")
        hbox_layout_url.addWidget(label_url)
        self.lineedit_url.setPlaceholderText('url that you want to scrap... ')
        hbox_layout_url.addWidget(self.lineedit_url)
        hbox_layout_url.addWidget(self._button_open_browser(self.lineedit_url))
        result.addLayout(hbox_layout_url)

        self.save_btn = QPushButton()
        self.save_btn.setIcon(QIcon('resource/images/plus.png'))
        self.save_btn.setText("셔틀 추가")
        self.save_btn.setStatusTip('Add this shuttle')
        self.save_btn.clicked.connect(self.parent_widget.add_shuttle)

        hbox_layout_execution = QHBoxLayout()
        hbox_layout_execution.addWidget(self._button_get_element_data())
        hbox_layout_execution.addWidget(self.save_btn)
        result.addLayout(hbox_layout_execution)

        result.addWidget(self._textedit_log())
        return result

    def _button_get_element_data(self):
        button_get_element = QPushButton('Get target element data', self)
        button_get_element.clicked.connect(self._get_target_element_data)
        return button_get_element

    def _button_open_browser(self, lineedit):
        button_open_browser = QPushButton('Open in chrome browser', self)
        button_open_browser.clicked.connect(lambda: self._open_browser(lineedit))
        return button_open_browser

    def _textedit_log(self):
        self.log_textedit.setReadOnly(True)
        return self.log_textedit

    def shuttle_name(self):
        self.lineedit_shuttle_name.setPlaceholderText('name of shuttle...')
        return self.lineedit_shuttle_name

    def lineedit_url(self):
        self.lineedit_url.setPlaceholderText('https://example.com')
        return self.lineedit_url

    def _open_browser(self, lineedit):
        self._webScraper = WebScraper(lineedit.text(), chrome_service=self.chrome_service)
        init_event_listener(self._webScraper)

    def _get_target_element_data(self):
        if self._webScraper is None or self._webScraper.is_selected_elements() is False:
            QMessageBox.information(self, 'Error',
                                    'Please select elements in chrome browser first.\n'
                                    '1. Write URL that you want to scrap.\n'
                                    "2. Click the 'Open in chrome browser' button.\n"
                                    "3. Select elements that you want to scrap.\n"
                                    "See the README.md file for details.",
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return

        result: WebElement = self._webScraper.get_target_element()
        self.element_class_names = self._webScraper.get_element_class_names()
        self.contents = result.text
        self.log_textedit.setText('{0} - get target element data.\n'.format(local_time_now()))
        self.log_textedit.append('class names : {0}'.format(self.element_class_names))
        self.log_textedit.append('id : {0}'.format(self._webScraper.get_element_id()))
        elements = self._webScraper.get_elements_by_classnames(self.element_class_names)
        self.log_textedit.append('--- elements with same class ---\n')
        for e in elements:
            self.log_textedit.append('{0}\n'.format(e.text))
        self.log_textedit.append('\n--- selected element ---\n')
        self.log_textedit.append(self.contents)
