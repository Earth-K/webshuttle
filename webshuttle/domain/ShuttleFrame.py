import pygame
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QDialog

from webshuttle.domain.Observer import Observer
from webshuttle.domain.LogText import LogText
from webshuttle.domain.Shuttle import Shuttle
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from webshuttle.adapter.incoming.ui.DraftShuttleWidgets import DraftShuttleWidgets


class ShuttleFrame(QWidget, Observer):
    def __init__(self, shuttles, shuttle_seq, chrome_service, shuttleWidgetGroup, shuttles_widget, time):
        super().__init__(shuttles_widget)
        self.shuttles = shuttles
        self.chrome_service = chrome_service
        self.time = time
        self.vBoxLayout = None
        self.cancel = QPushButton("Cancel")
        self.ok = QPushButton("OK")
        self.shuttle_seq = shuttle_seq

        self.shuttleWidgets: ShuttleWidgetGroup = shuttleWidgetGroup
        self.draft_shuttleWidgets = DraftShuttleWidgets(name=self.shuttleWidgets.shuttle_name_widget.text(),
                                                        url=self.shuttleWidgets.url_widget.text(),
                                                        period=self.shuttleWidgets.period_widget.value(),
                                                        target_classes=self.shuttleWidgets.target_classes_widget.text())
        self.settingsButton: QPushButton = QPushButton("설정")
        self.settingsButton.clicked.connect(self.showSettings)
        self.shuttles_widget = shuttles_widget

        self.start_stop_button = self.start_button(self.shuttle_seq, self.draft_shuttleWidgets.name,
                                                   self.draft_shuttleWidgets.url, self.draft_shuttleWidgets.period,
                                                   self.draft_shuttleWidgets.target_classes,
                                                   self.shuttleWidgets.update_list_widget)
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Sunken)
        shuttle_layout: QHBoxLayout = QHBoxLayout()
        self.frame_name = QLabel(self.shuttleWidgets.shuttle_name_widget.text())
        shuttle_layout.addWidget(self.frame_name)
        shuttle_layout.addWidget(self.settingsButton)
        shuttle_layout.addWidget(self.start_stop_button)
        self.frame.setLayout(shuttle_layout)
        self.shuttle_widget_group: ShuttleWidgetGroup = shuttleWidgetGroup
        self.shuttle_widget_group.register_observer(self)

    def update(self) -> None:
        self.shuttleWidgets.url_widget.setText(self.draft_shuttleWidgets.url.text())
        self.shuttleWidgets.shuttle_name_widget.setText(self.draft_shuttleWidgets.name.text())
        self.shuttleWidgets.target_classes_widget.setText(self.draft_shuttleWidgets.target_classes.text())
        self.shuttleWidgets.period_widget.setValue(self.draft_shuttleWidgets.period.value())
        self.frame_name.setText(self.draft_shuttleWidgets.name.text())

    def showSettings(self):
        widget = self.createSettingDialog()
        widget.show()

    def createSettingDialog(self):
        widget = QDialog(self.shuttles_widget)
        widget.setWindowModality(Qt.ApplicationModal)
        widget.resize(300, 200)
        self.setSettingsLayout()
        widget.setLayout(self.vBoxLayout)
        self.cancel.clicked.connect(widget.close)
        self.ok.clicked.connect(lambda: self.applyDraft(widget))
        return widget

    def getFrame(self):
        return self.frame

    def setSettingsLayout(self):
        if self.vBoxLayout is not None:
            return
        self.vBoxLayout = QVBoxLayout()
        name_hBoxLayout = QHBoxLayout()
        name_hBoxLayout.addWidget(QLabel("셔틀 이름 : "))
        name_hBoxLayout.addWidget(self.draft_shuttleWidgets.name)
        self.vBoxLayout.addLayout(name_hBoxLayout)

        url_hBoxLayout = QHBoxLayout()
        url_hBoxLayout.addWidget(QLabel("URL : "))
        url_hBoxLayout.addWidget(self.draft_shuttleWidgets.url)
        self.vBoxLayout.addLayout(url_hBoxLayout)

        period_hBoxLayout = QHBoxLayout()
        period_hBoxLayout.addWidget(QLabel("반복 주기(초) : "))
        period_hBoxLayout.addWidget(self.draft_shuttleWidgets.period)
        self.vBoxLayout.addLayout(period_hBoxLayout)

        classes_hBoxLayout = QHBoxLayout()
        classes_hBoxLayout.addWidget(QLabel("타깃 클래스 : "))
        classes_hBoxLayout.addWidget(self.draft_shuttleWidgets.target_classes)
        self.vBoxLayout.addLayout(classes_hBoxLayout)

        confirm_hBoxLayout = QHBoxLayout()
        confirm_hBoxLayout.addWidget(self.ok)
        confirm_hBoxLayout.addWidget(self.cancel)
        self.vBoxLayout.addLayout(confirm_hBoxLayout)

    def applyDraft(self, widget):
        self.shuttle_widget_group.notify_update()
        self.shuttles_widget.save_shuttles()
        widget.close()

    def start_button(self, shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget,
                     log_edittext_widget):
        start_btn = QPushButton('시작')
        start_btn.clicked.connect(
            lambda: self._start(shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget,
                                log_edittext_widget, start_btn))
        return start_btn

    def _start(self, shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget,
               log_edittext_widget, start_btn_widget):
        if start_btn_widget.text() == '시작':
            self.settingsButton.setDisabled(True)
            shuttle_name = shuttle_name_widget.text()
            if shuttle_name == "":
                shuttle_name = "이름 없음"
            message = LogText(self.time.localtime()).started_shuttle(shuttle_name)
            log_edittext_widget.append(message)
            period_widget.setReadOnly(True)
            start_btn_widget.setText('중지')
            self.shuttles[shuttle_seq] = Shuttle(self, self.shuttles, shuttle_seq,
                                                 ShuttleWidgetGroup(shuttle_name_widget=shuttle_name_widget,
                                                                    url_widget=url_widget,
                                                                    period_widget=period_widget,
                                                                    target_classes_widget=target_classes_widget,
                                                                    update_list_widget=log_edittext_widget),
                                                 self.chrome_service, pygame.mixer.Sound("resource/sounds/sound.wav"))
            self.shuttles[shuttle_seq].start()
        else:
            self.settingsButton.setDisabled(False)
            message = LogText(self.time.localtime()).stopped_shuttle(shuttle_name_widget.text())
            log_edittext_widget.append(message)
            period_widget.setReadOnly(False)
            self.shuttles[shuttle_seq] = None
            start_btn_widget.setText('시작')
