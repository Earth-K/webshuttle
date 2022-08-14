import atexit

from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QLabel, QWidget

from webshuttle.adapter.incoming.ui.DraftShuttleWidgets import DraftShuttleWidgets
from webshuttle.adapter.incoming.ui.ShuttleFrameSettingDialog import ShuttleFrameSettingDialog
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
        self.settingsButton.clicked.connect(
            lambda: ShuttleFrameSettingDialog(shuttles_widget=self.shuttles_widget, shuttle_frame=self).show())
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
