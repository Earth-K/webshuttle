from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton

from domain.Shuttle import Shuttle


def shuttle_setting_layout(hbox_layout):
    result = QVBoxLayout()
    result.addLayout(hbox_layout)
    return result


class ShuttlesWidget(QWidget):
    def __init__(self, parent):
        super(ShuttlesWidget, self).__init__(parent)
        self.shuttles = []
        self._init_ui()

    def _init_ui(self):
        self._vbox_layout = QVBoxLayout()
        self.setLayout(self._vbox_layout)
        self.show()

    def add_shuttle(self, url, period, target_classes):
        self.shuttles.append(Shuttle(url, period, target_classes))

        url_lineedit = QLineEdit()
        url_lineedit.setText(url)
        url_lineedit.setReadOnly(True)
        period_lineedit = QLineEdit()
        period_lineedit.setText(period)
        period_lineedit.setReadOnly(True)
        target_classes_lineedit = QLineEdit()
        target_classes_lineedit.setText(target_classes)
        target_classes_lineedit.setReadOnly(True)

        vbox_wrap_layout = QVBoxLayout()
        hbox_layout_shuttle = QHBoxLayout()
        hbox_layout_shuttle.addWidget(QLabel('url : '))
        hbox_layout_shuttle.addWidget(url_lineedit)
        hbox_layout_shuttle.addWidget(QLabel('check period : '))
        hbox_layout_shuttle.addWidget(period_lineedit)
        hbox_layout_shuttle.addWidget(QLabel('target classes : '))
        hbox_layout_shuttle.addWidget(target_classes_lineedit)
        hbox_layout_shuttle.addWidget(QPushButton('Start'))
        hbox_layout_shuttle.addWidget(QPushButton('Stop'))
        hbox_layout_memo = QHBoxLayout()
        hbox_layout_memo.addWidget(QLabel('memo : '))
        memo = QLineEdit()
        memo.setPlaceholderText('description...')
        hbox_layout_memo.addWidget(memo)
        vbox_wrap_layout.addLayout(hbox_layout_shuttle)
        vbox_wrap_layout.addLayout(hbox_layout_memo)
        self._vbox_layout.addLayout(vbox_wrap_layout)
