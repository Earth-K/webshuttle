import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QAction, QMainWindow, QPushButton

from widgets.MainWidget import MainWidget
from widgets.ShuttlesWidget import ShuttlesWidget


def go_setting_widget(widgets):
    widgets.setCurrentIndex(1)


def go_main_widget(widgets):
    widgets.setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.main_widget = MainWidget(self)
        self.shuttles_widget = ShuttlesWidget(self)
        self.widgets = QtWidgets.QStackedWidget()
        self.widgets.addWidget(self.main_widget)
        self.widgets.addWidget(self.shuttles_widget)
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

        save_action = QAction(QIcon('save.png'), 'Save this shuttle', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save this shuttle')
        save_action.triggered.connect(self._save_shuttle)
        self.toolBar = self.addToolBar('Save this shuttle')
        self.toolBar.addAction(save_action)

        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self.show()

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())

    def _button_save(self):
        button_save = QPushButton('Save this shuttle')
        button_save.clicked.connect(self._save_shuttle)
        return button_save

    def _save_shuttle(self):
        print(self.main_widget.lineedit_period.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
