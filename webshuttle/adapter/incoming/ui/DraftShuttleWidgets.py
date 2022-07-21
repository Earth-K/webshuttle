from PyQt5.QtWidgets import QLineEdit, QSpinBox


class DraftShuttleWidgets:
    def __init__(self, name, url, period, target_classes):
        self.name_widget = QLineEdit(name)
        self.url_widget = QLineEdit(url)
        self.period_widget = QSpinBox()
        self.period_widget.setMaximum(86400)
        self.period_widget.setValue(period)
        self.target_classes_widget = QLineEdit(target_classes)
