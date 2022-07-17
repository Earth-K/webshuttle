import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, \
    QHBoxLayout, QLabel, QMessageBox
from selenium.webdriver.remote.webelement import WebElement

from webshuttle.adapter.incoming.ui import ShuttlesWidget, StateWidget
from webshuttle.application.ParseTargetElementsService import ParseTargetElementsService
from webshuttle.application.SelectAreaService import SelectAreaService
from webshuttle.application.port.incoming.ParseTargetElementsUseCase import ParseTargetElementsUseCase
from webshuttle.application.port.incoming.SelectAreaUseCase import SelectAreaUseCase
from webshuttle.domain.LogText import LogText


class ShuttleAddWidget(QWidget):
    def __init__(self, parent, shuttles_widget: ShuttlesWidget, state_widget: StateWidget, chrome_driver):
        super(ShuttleAddWidget, self).__init__(parent)
        self.elements_report_widget = QTextEdit()
        self.shuttle_name_widget = QLineEdit()
        self.url_widget = QLineEdit()
        self.addshuttle_button = QPushButton()
        self.chrome_driver = chrome_driver
        self._init_ui(shuttles_widget, state_widget)
        self.shuttles_widget = shuttles_widget
        self.select_area_service: SelectAreaUseCase = SelectAreaService(self.url_widget, self.chrome_driver)
        self.parse_target_elements_service: ParseTargetElementsUseCase = None

    def _init_ui(self, shuttles_widget, state_widget):
        main_layout = QVBoxLayout()

        shuttlename_layout = QHBoxLayout()
        shuttlename_layout.addWidget(QLabel('셔틀 이름: '))
        self.shuttle_name_widget.setPlaceholderText('셔틀의 이름')
        shuttlename_layout.addWidget(self.shuttle_name_widget)
        main_layout.addLayout(shuttlename_layout)

        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL : "))
        self.url_widget.setPlaceholderText('스크랩 하고 싶은 웹 페이지의 URL ')
        url_layout.addWidget(self.url_widget)
        open_browser_button = QPushButton('영역 선택하러 가기', self)
        open_browser_button.clicked.connect(lambda: self._open_browser())
        url_layout.addWidget(open_browser_button)
        main_layout.addLayout(url_layout)

        execution_layout = QHBoxLayout()
        get_element_data_button = QPushButton('선택 영역 데이터 불러오기', self)
        get_element_data_button.clicked.connect(self._parse_target_elements)
        execution_layout.addWidget(get_element_data_button)
        self.addshuttle_button.setIcon(QIcon('resource/images/plus.png'))
        self.addshuttle_button.setText("셔틀 추가")
        self.addshuttle_button.setStatusTip('Add this webshuttle')
        self.addshuttle_button.setDisabled(True)
        self.addshuttle_button.clicked.connect(lambda: self._add_shuttle(shuttles_widget, state_widget))
        execution_layout.addWidget(self.addshuttle_button)
        main_layout.addLayout(execution_layout)

        self.elements_report_widget.setReadOnly(True)
        main_layout.addWidget(self.elements_report_widget)

        self.setLayout(main_layout)
        self.show()

    def _open_browser(self):
        self.select_area_service.open_browser()
        _web_scraper = self.select_area_service.get_web_scraper()
        self.parse_target_elements_service = ParseTargetElementsService(self, _web_scraper, self.elements_report_widget)
        self.addshuttle_button.setDisabled(True)

    def _parse_target_elements(self):
        try:
            self.parse_target_elements_service.parse()
            self.addshuttle_button.setDisabled(False)
        except Exception:
            return

    def _add_shuttle(self, shuttles_widget, state_widget):
        if self.url_widget.text() is None or self.element_class_names is None:
            QMessageBox.information(self, '에러',
                                    "먼저 선택 영역 데이터를 불러와주세요.",
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return
        shuttles_widget.add_shuttle(name=self.shuttle_name_widget.text(),
                                    url=self.url_widget.text(),
                                    period=300,
                                    target_classes=self.element_class_names,
                                    state_widget=state_widget.get_edittext())
        QMessageBox.information(self, '성공', '셔틀이 셔틀 목록에 저장되었습니다.',
                                QMessageBox.Yes, QMessageBox.NoButton)
