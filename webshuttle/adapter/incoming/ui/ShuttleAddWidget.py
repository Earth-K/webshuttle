import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, \
    QHBoxLayout, QLabel, QMessageBox
from selenium.webdriver.remote.webelement import WebElement

from webshuttle.adapter.incoming.ui import ShuttlesWidget, StateWidget
from webshuttle.application.SelectAreaService import SelectAreaService
from webshuttle.application.port.incoming.SelectAreaUseCase import SelectAreaUseCase
from webshuttle.domain.LogText import LogText


class ShuttleAddWidget(QWidget):
    def __init__(self, parent, shuttles_widget: ShuttlesWidget, state_widget: StateWidget, chrome_driver):
        super(ShuttleAddWidget, self).__init__(parent)
        self.text_edit = QTextEdit()
        self.shuttle_name_line_edit = QLineEdit()
        self.url_line_edit = QLineEdit()
        self.addshuttle_button = QPushButton()
        self.element_class_names = None
        self.chrome_driver = chrome_driver
        self._webScraper = None
        self._init_ui(shuttles_widget, state_widget)
        self.shuttles_widget = shuttles_widget
        self.select_area_service: SelectAreaUseCase = SelectAreaService(self.url_line_edit, self.chrome_driver)

    def _init_ui(self, shuttles_widget, state_widget):
        main_layout = QVBoxLayout()

        shuttlename_layout = QHBoxLayout()
        shuttlename_layout.addWidget(QLabel('셔틀 이름: '))
        self.shuttle_name_line_edit.setPlaceholderText('셔틀의 이름')
        shuttlename_layout.addWidget(self.shuttle_name_line_edit)
        main_layout.addLayout(shuttlename_layout)

        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL : "))
        self.url_line_edit.setPlaceholderText('스크랩 하고 싶은 웹 페이지의 URL ')
        url_layout.addWidget(self.url_line_edit)
        open_browser_button = QPushButton('영역 선택하러 가기', self)
        open_browser_button.clicked.connect(lambda: self._open_browser())
        url_layout.addWidget(open_browser_button)
        main_layout.addLayout(url_layout)

        execution_layout = QHBoxLayout()
        get_element_data_button = QPushButton('선택 영역 데이터 불러오기', self)
        get_element_data_button.clicked.connect(self._get_target_element_data)
        execution_layout.addWidget(get_element_data_button)
        self.addshuttle_button.setIcon(QIcon('resource/images/plus.png'))
        self.addshuttle_button.setText("셔틀 추가")
        self.addshuttle_button.setStatusTip('Add this webshuttle')
        self.addshuttle_button.setDisabled(True)
        self.addshuttle_button.clicked.connect(lambda: self._add_shuttle(shuttles_widget, state_widget))
        execution_layout.addWidget(self.addshuttle_button)
        main_layout.addLayout(execution_layout)

        self.text_edit.setReadOnly(True)
        main_layout.addWidget(self.text_edit)

        self.setLayout(main_layout)
        self.show()

    def _open_browser(self):
        self.select_area_service.open_browser()
        self._webScraper = self.select_area_service.get_web_scraper()
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
            '{0} - get target element data.\n'.format(LogText('New Shuttle', time.localtime()).localtime()))
        self.text_edit.append('class names : {0}'.format(self.element_class_names))
        self.text_edit.append('id : {0}'.format(self._webScraper.get_element_id()))
        elements = self._webScraper.get_elements_by_classnames(self.element_class_names)
        self.text_edit.append('--- elements with same class ---\n')
        for e in elements:
            self.text_edit.append('{0}\n'.format(e.text))
        self.text_edit.append('\n--- selected element ---\n')
        self.text_edit.append(result.text)
        self.addshuttle_button.setDisabled(False)

    def _add_shuttle(self, shuttles_widget, state_widget):
        if self.url_line_edit.text() is None or self.element_class_names is None:
            QMessageBox.information(self, '에러',
                                    "먼저 선택 영역 데이터를 불러와주세요.",
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return
        shuttles_widget.add_shuttle(name=self.shuttle_name_line_edit.text(),
                                    url=self.url_line_edit.text(),
                                    period=300,
                                    target_classes=self.element_class_names,
                                    state_widget=state_widget.get_edittext())
        QMessageBox.information(self, '성공', '셔틀이 셔틀 목록에 저장되었습니다.',
                                QMessageBox.Yes, QMessageBox.NoButton)
