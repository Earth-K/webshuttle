from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout


class BaseWidget(QWidget):
    def __init__(self, parent, main_widget, shuttles_widget, log_widget):
        super().__init__(parent)
        self.tabs = QTabWidget()
        self.tabs.addTab(main_widget, '셔틀 추가')
        self.tabs.addTab(shuttles_widget, '셔틀 목록')
        self.tabs.addTab(log_widget, '현황')
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
