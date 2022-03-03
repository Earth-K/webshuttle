import time


class LogText:

    def __init__(self):
        self.now = time.localtime()

    def local_time_now(self):
        now = self.now
        return "%04d/%02d/%02d %02d:%02d:%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
