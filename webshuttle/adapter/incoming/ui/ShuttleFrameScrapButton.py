import atexit

from PyQt5.QtWidgets import QPushButton

from webshuttle.application.ScrapService import ScrapService
from webshuttle.application.port.incoming.ScrapUseCase import ScrapUseCase
from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.LogText import LogText


class ShuttleFrameScrapButton(QPushButton):
    def __init__(self, shuttle_frame):
        super().__init__("시작")
        self.shuttle_frame = shuttle_frame
        self.clicked.connect(self._onclick_scrap)

    def _onclick_scrap(self):
        if self.text() == '시작':
            self._start_scrap()
        else:
            self._stop_scrap()

    def _start_scrap(self):
        scrap_usecase: ScrapUseCase = ScrapService(shuttle_frame=self.shuttle_frame)
        scrap_usecase.start_scrap()
        self.shuttle_frame.settingsButton.setDisabled(True)
        self.setText('중지')
        atexit.register(self.shuttle_frame.shuttles[self.shuttle_frame.shuttle_seq].stop)

    def _stop_scrap(self):
        self.shuttle_frame.settingsButton.setDisabled(False)
        shuttle_name = self.shuttle_frame.draft_shuttleWidgets.name_widget.text()
        if shuttle_name == "":
            shuttle_name = "이름 없음"
        message = LogText(shuttle_name, DefaultTime().localtime()).stopped_shuttle()
        self.shuttle_frame.shuttleWidgets.state_widget.append(message)
        self.shuttle_frame.draft_shuttleWidgets.period_widget.setReadOnly(False)
        self.shuttle_frame.shuttles[self.shuttle_frame.shuttle_seq].stop()
        self.setText('시작')
