from PyQt5.QtCore import QThread

from webshuttle.domain.ScrapThread import ScrapThread


class Shuttle:
    def __init__(self, parent_widget, shuttles, shuttle_seq, shuttle_widget_group, chrome_driver, waiting_event):
        self.parent_widget = parent_widget
        self.chrome_driver = chrome_driver
        self.shuttle_thread = None
        self.shuttle_list = shuttles
        self.shuttle_seq = shuttle_seq
        self.shuttle_widget_group = shuttle_widget_group
        self.waiting_event = waiting_event

    def start(self):
        self.shuttle_list[self.shuttle_seq] = self
        if self.shuttle_thread is None:
            self.shuttle_thread: QThread = ScrapThread(self.parent_widget, self.shuttle_seq, self.shuttle_widget_group,
                                                       self.shuttle_list, self.chrome_driver, self.waiting_event)
        self.shuttle_thread.start()

    def stop(self):
        self.shuttle_list[self.shuttle_seq] = None
        if self.shuttle_thread is not None:
            self.shuttle_thread.stop()
