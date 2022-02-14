import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QAction, QMainWindow

from widgets.MainWidget import MainWidget
from widgets.ShuttlesWidget import ShuttlesWidget


def go_setting_widget(widgets):
    widgets.setCurrentIndex(1)


def go_main_widget(widgets):
    widgets.setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.widgets = QtWidgets.QStackedWidget()
        self.widgets.addWidget(MainWidget(self))
        self.widgets.addWidget(ShuttlesWidget(self))
        self.setCentralWidget(self.widgets)

        go_main_page = QAction('Main', self)
        go_main_page.setShortcut('Ctrl+1')
        go_main_page.setStatusTip('Show the main page.')
        go_main_page.triggered.connect(lambda: go_main_widget(self.widgets))

        go_setting_page = QAction('Shuttles', self)
        go_setting_page.setShortcut('Ctrl+2')
        go_setting_page.setStatusTip('Show the saved shuttles')
        go_setting_page.triggered.connect(lambda: go_setting_widget(self.widgets))

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menu_move = menubar.addMenu('&View')
        menu_move.addAction(go_main_page)
        menu_move.addAction(go_setting_page)

        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
