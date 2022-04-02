import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, \
    QHBoxLayout, QLabel, QMessageBox
from selenium.common.exceptions import WebDriverException
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
    injector.add_startpopup()


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
        self.addshuttle_button = None
        self._init_ui()

    def _init_ui(self):
        vbox_layout = self.main_layout()
        self.setLayout(vbox_layout)
        self.show()

    def main_layout(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        self.set_shuttlename_layout(main_layout)
        self.set_url_layout(main_layout)
        self.set_addshuttle_button()
        self.set_execution_layout(main_layout)
        main_layout.addWidget(self._textedit_log())
        return main_layout

    def set_execution_layout(self, main_layout):
        execution_layout = QHBoxLayout()
        execution_layout.addWidget(self._get_element_data_button())
        execution_layout.addWidget(self.addshuttle_button)
        main_layout.addLayout(execution_layout)

    def set_addshuttle_button(self):
        self.addshuttle_button = QPushButton()
        self.addshuttle_button.setIcon(QIcon('resource/images/plus.png'))
        self.addshuttle_button.setText("셔틀 추가")
        self.addshuttle_button.setStatusTip('Add this shuttle')
        self.addshuttle_button.setDisabled(True)
        self.addshuttle_button.clicked.connect(self.parent_widget.add_shuttle)

    def set_shuttlename_layout(self, result: QVBoxLayout) -> None:
        shuttlename_layout = QHBoxLayout()
        shuttlename_layout.addWidget(QLabel('셔틀 이름: '))
        shuttlename_layout.addWidget(self.shuttle_name())
        result.addLayout(shuttlename_layout)

    def set_url_layout(self, result: QVBoxLayout) -> None:
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL : "))
        self.lineedit_url.setPlaceholderText('스크랩 하고 싶은 웹 페이지의 URL ')
        url_layout.addWidget(self.lineedit_url)
        url_layout.addWidget(self._open_browser_button(self.lineedit_url))
        result.addLayout(url_layout)

    def _get_element_data_button(self):
        get_element_data_button = QPushButton('선택 영역 데이터 불러오기', self)
        get_element_data_button.clicked.connect(self._get_target_element_data)
        return get_element_data_button

    def _open_browser_button(self, lineedit):
        open_browser_button = QPushButton('영역 선택하러 가기', self)
        open_browser_button.clicked.connect(lambda: self._open_browser(lineedit))
        return open_browser_button

    def _textedit_log(self):
        self.log_textedit.setReadOnly(True)
        return self.log_textedit

    def shuttle_name(self):
        self.lineedit_shuttle_name.setPlaceholderText('셔틀의 이름')
        return self.lineedit_shuttle_name

    def lineedit_url(self):
        self.lineedit_url.setPlaceholderText('https://example.com')
        return self.lineedit_url

    def _open_browser(self, lineedit):
        try:
            self._webScraper = WebScraper(lineedit.text(), chrome_service=self.chrome_service)
        except WebDriverException:
            return
        init_event_listener(self._webScraper)
        self.addshuttle_button.setDisabled(True)

    def _get_target_element_data(self):
        if self._webScraper is None or self._webScraper.is_selected_elements() is False:
            QMessageBox.information(self, 'Error',
                                    '먼저 선택 영역을 선택하고 데이터를 불러오세요.\n'
                                    '1. 스크랩 하고 싶은 데이터가 있는 웹 페이지의 URL을 입력하세요.\n'
                                    "2. '영역 선택하러 가기' 버튼을 클릭하세요.\n"
                                    "3. 새로 열린 브라우저에서 마우스 우클릭으로 영역을 선택하세요.\n"
                                    "4. 웹셔틀의 '선택 영역 데이터 불러오기' 버튼을 클릭하세요.\n",
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
        self.addshuttle_button.setDisabled(False)
