from domain.DefaultTime import DefaultTime
from domain.ScrapThread import ScrapThread


class Shuttle:
    def __init__(self, parent_widget, shuttles, shuttle_id, shuttle_widget_group, chrome_service, mixer_sound,
                 time=DefaultTime()):
        self.parent_widget = parent_widget
        self.shuttle_list = shuttles
        self.id = shuttle_id
        self.shuttle_widget_group = shuttle_widget_group
        self.chrome_service = chrome_service
        self.time = time
        self.sound = mixer_sound

    def start(self):
        self._create_thread().start()

    def stop(self):
        self.shuttle_list[self.id] = None

    def _create_thread(self):
        return ScrapThread(self.parent_widget, self.id, self.shuttle_widget_group, self.time, self.sound,
                           self.shuttle_list, self.chrome_service)
