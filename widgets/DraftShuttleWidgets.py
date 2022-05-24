from PyQt5.QtWidgets import QLineEdit, QSpinBox


class DraftShuttleWidgets:
    def __init__(self, name, url, period, target_classes):
        self.name = QLineEdit(name)
        self.url = QLineEdit(url)
        self.period = QSpinBox()
        self.period.setMaximum(86000)
        self.period.setValue(period)
        self.target_classes = QLineEdit(target_classes)
