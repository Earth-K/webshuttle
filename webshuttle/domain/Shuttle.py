from PyQt5.QtCore import QThread

from webshuttle.domain.ScrapThread import ScrapThread


class Shuttle:
    def __init__(self, parent_widget, shuttles, shuttle_id, shuttle_widget_group, chrome_driver, mixer_sound):
        self.shuttle_thread = None
        self.parent_widget = parent_widget
        self.shuttle_list = shuttles
        self.id = shuttle_id
        self.shuttle_widget_group = shuttle_widget_group
        self.chrome_driver = chrome_driver

        self.sound = mixer_sound

    def start(self):
        self.shuttle_list[self.id] = self
        if self.shuttle_thread is None:
            self.shuttle_thread: QThread = ScrapThread(self.parent_widget, self.id, self.shuttle_widget_group,
                                                       self.sound, self.shuttle_list, self.chrome_driver)
        self.shuttle_thread.start()

    def stop(self):
        self.shuttle_list[self.id] = None
        if self.shuttle_thread is not None:
            self.shuttle_thread.stop()
