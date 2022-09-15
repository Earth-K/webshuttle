import threading

from webshuttle.adapter.incoming.ui.widget.shuttle import ShuttleFrame
from webshuttle.application.port.incoming.ScrapUseCase import ScrapUseCase
from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.LogText import LogText
from webshuttle.domain.Shuttle import Shuttle
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ScrapService(ScrapUseCase):
    def __init__(self, shuttle_frame: ShuttleFrame):
        self.shuttle_frame = shuttle_frame
        self.shuttle_name = shuttle_frame.draft_shuttleWidgets.name_widget.text()
        if self.shuttle_name == "":
            self.shuttle_name = "이름 없음"
        self.state_widget = shuttle_frame.shuttleWidgets.state_widget
        self.shuttle_widgets = shuttle_frame.shuttleWidgets
        self.draft_shuttle_widgets = shuttle_frame.draft_shuttleWidgets
        self.shuttles = shuttle_frame.shuttles
        self.shuttle_seq = shuttle_frame.shuttle_seq
        self.chrome_driver = shuttle_frame.chrome_driver

    def start_scrap(self):
        message = LogText(self.shuttle_name, DefaultTime()).started_shuttle()
        self.state_widget.append(message)
        self.shuttle_widgets.period_widget.setReadOnly(True)
        waiting_event = threading.Event()
        self.shuttles[self.shuttle_seq] = Shuttle(self.shuttle_frame,
                                                  self.shuttles,
                                                  self.shuttle_seq,
                                                  ShuttleWidgetGroup(
                                                      state_widget=self.state_widget,
                                                      target_classes_widget=self.draft_shuttle_widgets.target_classes_widget,
                                                      period_widget=self.draft_shuttle_widgets.period_widget,
                                                      url_widget=self.draft_shuttle_widgets.url_widget,
                                                      shuttle_name_widget=self.draft_shuttle_widgets.name_widget,
                                                      filtering_keyword_widget=self.draft_shuttle_widgets.filtering_keyword_widget),
                                                  self.chrome_driver,
                                                  waiting_event)
        self.shuttles[self.shuttle_seq].start()
        waiting_event.wait(timeout=60)
