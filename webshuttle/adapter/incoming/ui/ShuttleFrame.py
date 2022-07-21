import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QDialog

from webshuttle.adapter.incoming.ui.DraftShuttleWidgets import DraftShuttleWidgets
from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.LogText import LogText
from webshuttle.domain.Observer import Observer
from webshuttle.domain.Shuttle import Shuttle
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ShuttleFrame(QWidget, Observer):
    def __init__(self, shuttles, shuttle_seq, chrome_driver, shuttle_widget_group, shuttles_widget):
        super().__init__(shuttles_widget)
        self.shuttles = shuttles
        self.chrome_driver = chrome_driver

        self.shuttle_seq = shuttle_seq
        self.shuttleWidgets: ShuttleWidgetGroup = shuttle_widget_group
        self.draft_shuttleWidgets = DraftShuttleWidgets(name=self.shuttleWidgets.shuttle_name_widget.text(),
                                                        url=self.shuttleWidgets.url_widget.text(),
                                                        period=self.shuttleWidgets.period_widget.value(),
                                                        target_classes=self.shuttleWidgets.target_classes_widget.text())
        self.settingsButton: QPushButton = QPushButton("설정")
        self.settingsButton.clicked.connect(lambda: self.create_settings_dialog().show())
        self.shuttles_widget = shuttles_widget

        self.start_stop_button = self.start_button()
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

    def start_button(self):
        start_btn = QPushButton('시작')
        start_btn.clicked.connect(
            lambda: self._start(start_btn))
        return start_btn

    def _start(self, start_btn_widget):
        if start_btn_widget.text() == '시작':
            shuttle_name = self.draft_shuttleWidgets.name_widget.text()
            if shuttle_name == "":
                shuttle_name = "이름 없음"
            message = LogText(shuttle_name, DefaultTime().localtime()).started_shuttle()
            self.shuttleWidgets.state_widget.append(message)
            self.draft_shuttleWidgets.period_widget.setReadOnly(True)
            waiting_event = threading.Event()
            self.shuttles[self.shuttle_seq] = Shuttle(self, self.shuttles, self.shuttle_seq,
                                                      ShuttleWidgetGroup(
                                                          shuttle_name_widget=self.draft_shuttleWidgets.name_widget,
                                                          url_widget=self.draft_shuttleWidgets.url_widget,
                                                          period_widget=self.draft_shuttleWidgets.period_widget,
                                                          target_classes_widget=self.draft_shuttleWidgets.target_classes_widget,
                                                          state_widget=self.shuttleWidgets.state_widget),
                                                      self.chrome_driver, waiting_event)
            self.shuttles[self.shuttle_seq].start()
            waiting_event.wait(timeout=60)
            self.settingsButton.setDisabled(True)
            start_btn_widget.setText('중지')

        else:
            self.settingsButton.setDisabled(False)
            shuttle_name = self.draft_shuttleWidgets.name_widget.text()
            if shuttle_name == "":
                shuttle_name = "이름 없음"
            message = LogText(shuttle_name, DefaultTime().localtime()).stopped_shuttle()
            self.shuttleWidgets.state_widget.append(message)
            self.draft_shuttleWidgets.period_widget.setReadOnly(False)
            self.shuttles[self.shuttle_seq].stop()
            start_btn_widget.setText('시작')
