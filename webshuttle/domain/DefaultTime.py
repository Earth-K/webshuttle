import time


class DefaultTime:
    def __init__(self, time_int=None):
        self.time_int = time_int

    def localtime(self):
        if self.time_int is None:
            return time.localtime()
        return time.localtime(self.time_int)

    def sleep(self, sec):
        time.sleep(sec)
