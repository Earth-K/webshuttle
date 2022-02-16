from PyQt5.QtWidgets import QWidget


class Shuttle(QWidget):

    def __init__(self, url, period, target_classes):
        super().__init__()
        self.url = url
        self.period = period
        self.target_classes = target_classes
