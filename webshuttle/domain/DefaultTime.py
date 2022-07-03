import time


class DefaultTime:
    def __init__(self):
        pass

    def localtime(self):
        return time.localtime()

    def sleep(self, sec):
        time.sleep(sec)
