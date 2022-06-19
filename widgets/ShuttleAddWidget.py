import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, \
    QHBoxLayout, QLabel, QMessageBox
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement

from domain.EventListenerInjector import EventListenerInjector
from domain.LogText import LogText
from domain.WebScraper import WebScraper
from widgets import ShuttlesWidget, StateWidget


def init_event_listener(web_scraper):
    injector = EventListenerInjector(web_scraper)
    injector.add_mouseover()
    injector.add_mouseleave()
    injector.add_mousedown_right()
    injector.add_tooltip()
    injector.add_startpopup()


class ShuttleAddWidget(QWidget):
    def __init__(self, parent, shuttles_widget: ShuttlesWidget, state_widget: StateWidget, chrome_service):
        super(ShuttleAddWidget, self).__init__(parent)
        self.text_edit = QTextEdit()
        self.shuttle_name_line_edit = QLineEdit()
        self.url_line_edit = QLineEdit()
        self.addshuttle_button = QPushButton()
        self.element_class_names = None
        self._webScraper = None
        self._init_ui(shuttles_widget, state_widget, chrome_service)

    def _init_ui(self, shuttles_widget, state_widget, chrome_service):
        vbox_layout = self.main_layout(shuttles_widget, state_widget, chrome_service)
        self.setLayout(vbox_layout)
        self.show()

    def main_layout(self, shuttles_widget, state_widget, chrome_service) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        self.set_shuttlename_layout(main_layout)
        self.set_url_layout(main_layout, chrome_service)
        self.set_addshuttle_button(shuttles_widget, state_widget)
        self.set_execution_layout(main_layout)
        main_layout.addWidget(self._textedit_state_widget())
        return main_layout

    def set_execution_layout(self, main_layout):
        execution_layout = QHBoxLayout()
        execution_layout.addWidget(self._get_element_data_button())
        execution_layout.addWidget(self.addshuttle_button)
        main_layout.addLayout(execution_layout)

    def set_addshuttle_button(self, shuttles_widget, state_widget):
        self.addshuttle_button.setIcon(QIcon('resource/images/plus.png'))
        self.addshuttle_button.setText("셔틀 추가")
        self.addshuttle_button.setStatusTip('Add this shuttle')
        self.addshuttle_button.setDisabled(True)
        self.addshuttle_button.clicked.connect(lambda: self.add_shuttle(shuttles_widget, state_widget))

    def set_shuttlename_layout(self, result: QVBoxLayout) -> None:
        shuttlename_layout = QHBoxLayout()
        shuttlename_layout.addWidget(QLabel('셔틀 이름: '))
        shuttlename_layout.addWidget(self.shuttle_name())
        result.addLayout(shuttlename_layout)

    def set_url_layout(self, result: QVBoxLayout, chrome_service) -> None:
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL : "))
        self.url_line_edit.setPlaceholderText('스크랩 하고 싶은 웹 페이지의 URL ')
        url_layout.addWidget(self.url_line_edit)
        url_layout.addWidget(self._open_browser_button(self.url_line_edit, chrome_service))
        result.addLayout(url_layout)

    def _get_element_data_button(self):
        get_element_data_button = QPushButton('선택 영역 데이터 불러오기', self)
        get_element_data_button.clicked.connect(self._get_target_element_data)
        return get_element_data_button

    def _open_browser_button(self, url_line_edit, chrome_service):
        open_browser_button = QPushButton('영역 선택하러 가기', self)
        open_browser_button.clicked.connect(lambda: self._open_browser(url_line_edit, chrome_service))
        return open_browser_button

    def _textedit_state_widget(self):
        self.text_edit.setReadOnly(True)
        return self.text_edit

    def shuttle_name(self):
        self.shuttle_name_line_edit.setPlaceholderText('셔틀의 이름')
        return self.shuttle_name_line_edit

    def lineedit_url(self):
        self.url_line_edit.setPlaceholderText('https://example.com')
        return self.url_line_edit

    def _open_browser(self, lineedit, chrome_service):
        try:
            self._webScraper = WebScraper(start_url=lineedit.text(),
                                          driver=webdriver.Chrome(service=chrome_service))
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
        self.element_class_names = self._webScraper.get_element_class_names_of_target()
        self.text_edit.setText(
            '{0} - get target element data.\n'.format(LogText(time.localtime()).formatted_localtime()))
        self.text_edit.append('class names : {0}'.format(self.element_class_names))
        self.text_edit.append('id : {0}'.format(self._webScraper.get_element_id()))
        elements = self._webScraper.get_elements_by_classnames(self.element_class_names)
        self.text_edit.append('--- elements with same class ---\n')
        for e in elements:
            self.text_edit.append('{0}\n'.format(e.text))
        self.text_edit.append('\n--- selected element ---\n')
        self.text_edit.append(result.text)
        self.addshuttle_button.setDisabled(False)

    def add_shuttle(self, shuttles_widget, state_widget):
        if self.url_line_edit.text() is None or self.element_class_names is None:
            QMessageBox.information(self, '에러',
                                    "먼저 선택 영역 데이터를 불러와주세요.",
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return
        shuttles_widget.add_shuttle(name=self.shuttle_name_line_edit.text(),
                                    url=self.url_line_edit.text(),
                                    period=300,
                                    target_classes=self.element_class_names,
                                    log_edittext_widget=state_widget.get_edittext())
        QMessageBox.information(self, '성공', '셔틀이 셔틀 목록에 저장되었습니다.',
                                QMessageBox.Yes, QMessageBox.NoButton)

