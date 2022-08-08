import atexit

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QDialog

from webshuttle.adapter.incoming.ui.DraftShuttleWidgets import DraftShuttleWidgets
from webshuttle.application.ScrapService import ScrapService
from webshuttle.application.port.incoming.ScrapUseCase import ScrapUseCase
from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.LogText import LogText
from webshuttle.domain.Observer import Observer
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ShuttleFrame(QWidget, Observer):
    def __init__(self, shuttles, shuttle_seq, chrome_driver, shuttle_widget_group, shuttles_widget):
        super().__init__(shuttles_widget)
        self.shuttles = shuttles
        self.chrome_driver = chrome_driver

        self.shuttle_seq = shuttle_seq
        self.shuttleWidgets: ShuttleWidgetGroup = shuttle_widget_group
        self.draft_shuttleWidgets = DraftShuttleWidgets(shuttle_widget_group)
        self.settingsButton: QPushButton = QPushButton("설정")
        self.settingsButton.clicked.connect(lambda: self.create_settings_dialog().show())
        self.shuttles_widget = shuttles_widget

        self.start_stop_button = QPushButton('시작')
        self.start_stop_button.clicked.connect(self._onclick_scrap)

        self.frame_widget = QFrame()
        self.frame_widget.setFrameShape(QFrame.Box)
        self.frame_widget.setFrameShadow(QFrame.Sunken)
        shuttle_layout: QHBoxLayout = QHBoxLayout()
        self.frame_name = QLabel(self.shuttleWidgets.shuttle_name_widget.text())
        shuttle_layout.addWidget(self.frame_name)
        shuttle_layout.addWidget(self.settingsButton)
        shuttle_layout.addWidget(self.start_stop_button)
        self.frame_widget.setLayout(shuttle_layout)
        self.shuttle_widget_group: ShuttleWidgetGroup = shuttle_widget_group
        self.shuttle_widget_group.register_observer(self)

    def update(self) -> None:
        self.shuttleWidgets.url_widget.setText(self.draft_shuttleWidgets.url_widget.text())
        self.shuttleWidgets.shuttle_name_widget.setText(self.draft_shuttleWidgets.name_widget.text())
        self.shuttleWidgets.target_classes_widget.setText(self.draft_shuttleWidgets.target_classes_widget.text())
        self.shuttleWidgets.period_widget.setValue(self.draft_shuttleWidgets.period_widget.value())
        self.shuttleWidgets.filtering_keyword_widget.setText(self.draft_shuttleWidgets.filtering_keyword_widget.text())
        self.frame_name.setText(self.draft_shuttleWidgets.name_widget.text())

    def apply_draft(self, widget):
        self.shuttle_widget_group.notify_update()
        self.shuttles_widget.save_shuttles()
        widget.close()

    def cancel_draft(self, widget):
        self.draft_shuttleWidgets.url_widget.setText(self.shuttleWidgets.url_widget.text())
        self.draft_shuttleWidgets.name_widget.setText(self.shuttleWidgets.shuttle_name_widget.text())
        self.draft_shuttleWidgets.target_classes_widget.setText(self.shuttleWidgets.target_classes_widget.text())
        self.draft_shuttleWidgets.period_widget.setValue(self.shuttleWidgets.period_widget.value())
        self.draft_shuttleWidgets.filtering_keyword_widget.setText(self.shuttleWidgets.filtering_keyword_widget.text())
        self.draft_shuttleWidgets.name_widget.setText(self.frame_name.text())
        widget.close()

    def create_settings_dialog(self):
        dialog = QDialog(self.shuttles_widget)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(300, 200)
        dialog.setWindowTitle("셔틀 설정")

        vBoxLayout = QVBoxLayout()
        name_hBoxLayout = QHBoxLayout()
        name_hBoxLayout.addWidget(QLabel("셔틀 이름 : "))
        name_hBoxLayout.addWidget(self.draft_shuttleWidgets.name_widget)
        vBoxLayout.addLayout(name_hBoxLayout)
        url_hBoxLayout = QHBoxLayout()
        url_hBoxLayout.addWidget(QLabel("URL : "))
        url_hBoxLayout.addWidget(self.draft_shuttleWidgets.url_widget)
        vBoxLayout.addLayout(url_hBoxLayout)
        period_hBoxLayout = QHBoxLayout()
        period_hBoxLayout.addWidget(QLabel("반복 주기(초) : "))
        period_hBoxLayout.addWidget(self.draft_shuttleWidgets.period_widget)
        vBoxLayout.addLayout(period_hBoxLayout)
        classes_hBoxLayout = QHBoxLayout()
        classes_hBoxLayout.addWidget(QLabel("타깃 클래스 : "))
        classes_hBoxLayout.addWidget(self.draft_shuttleWidgets.target_classes_widget)
        vBoxLayout.addLayout(classes_hBoxLayout)
        filtering_keyword_hBoxLayout = QHBoxLayout()
        filtering_keyword_hBoxLayout.addWidget(QLabel("필터링 키워드 : "))
        filtering_keyword_hBoxLayout.addWidget(self.draft_shuttleWidgets.filtering_keyword_widget)
        vBoxLayout.addLayout(filtering_keyword_hBoxLayout)
        confirm_hBoxLayout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: self.apply_draft(dialog))
        confirm_hBoxLayout.addWidget(ok_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: self.cancel_draft(dialog))
        confirm_hBoxLayout.addWidget(cancel_button)
        vBoxLayout.addLayout(confirm_hBoxLayout)

        dialog.setLayout(vBoxLayout)
        return dialog

    def get_frame_widget(self):
        return self.frame_widget

    def _onclick_scrap(self):
        if self.start_stop_button.text() == '시작':
            self._start_scrap()
        else:
            self._stop_scrap()

    def _start_scrap(self):
        scrap_usecase: ScrapUseCase = ScrapService(self)
        scrap_usecase.start_scrap()
        self.settingsButton.setDisabled(True)
        self.start_stop_button.setText('중지')
        atexit.register(self.shuttles[self.shuttle_seq].stop)

    def _stop_scrap(self):
        self.settingsButton.setDisabled(False)
        shuttle_name = self.draft_shuttleWidgets.name_widget.text()
        if shuttle_name == "":
            shuttle_name = "이름 없음"
        message = LogText(shuttle_name, DefaultTime().localtime()).stopped_shuttle()
        self.shuttleWidgets.state_widget.append(message)
        self.draft_shuttleWidgets.period_widget.setReadOnly(False)
        self.shuttles[self.shuttle_seq].stop()
        self.start_stop_button.setText('시작')
