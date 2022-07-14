from webshuttle.application.port.incoming.CreateLogTextUseCase import CreateLogTextUseCase
from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.LogText import LogText


class CreateLogTextService(CreateLogTextUseCase):
    def __init__(self, time=DefaultTime()):
        self.time = time

    def started(self, shuttle_name) -> str:
        return LogText(shuttle_name, self.time.localtime()).started_shuttle()

    def stopped(self, shuttle_name) -> str:
        return LogText(shuttle_name, self.time.localtime()).stopped_shuttle()

    def deleted(self, shuttle_name) -> str:
        return LogText(shuttle_name, self.time.localtime()).removed_shuttle()

    def shuttle_name(self, shuttle_name) -> str:
        return LogText(shuttle_name, self.time.localtime()).shuttle_name()
