import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QAction, QMainWindow, QPushButton, QMessageBox

from widgets.MainWidget import MainWidget
from widgets.ShuttlesWidget import ShuttlesWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.main_widget = MainWidget(self)
        self.shuttles_widget = ShuttlesWidget(self)
        self.widgets = QtWidgets.QStackedWidget()
        self.widgets.addWidget(self.main_widget)
        self.widgets.addWidget(self.shuttles_widget)
        self.setCentralWidget(self.widgets)
        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)
        menu_move = menubar.addMenu('&View')
        menu_move.addAction(self._main_page_action())
        menu_move.addAction(self._shuttle_page_action())

        self.toolBar = self.addToolBar('Save this shuttle')
        self.toolBar.addAction(self._save_action())

        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self.show()

    def _go_setting_widget(self, widgets):
        widgets.setCurrentIndex(1)
        self.toolBar.setVisible(False)

    def _go_main_widget(self, widgets):
        widgets.setCurrentIndex(0)
        self.toolBar.setVisible(True)

    def _shuttle_page_action(self):
        result = QAction('Shuttles', self)
        result.setShortcut('Ctrl+2')
        result.setStatusTip('Show the saved shuttles')
        result.triggered.connect(lambda: self._go_setting_widget(self.widgets))
        return result

    def _main_page_action(self):
        result = QAction('Main', self)
        result.setShortcut('Ctrl+1')
        result.setStatusTip('Show the main page.')
        result.triggered.connect(lambda: self._go_main_widget(self.widgets))
        return result

    def _save_action(self):
        result = QAction(QIcon('save.png'), 'Save this shuttle', self)
        result.setShortcut('Ctrl+S')
        result.setStatusTip('Save this shuttle')
        result.triggered.connect(self._save_shuttle)
        return result

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
        main_widget = self.widgets.widget(0)
        shuttles_widget = self.widgets.widget(1)
        url = main_widget.lineedit.text()
        check_period = main_widget.lineedit_period.text()
        target_classes = main_widget.element_class_names
        if url is None or check_period is None or target_classes is None:
            QMessageBox.information(self, 'Failure',
                                    'Some setting values are blank.',
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return
        shuttles_widget.add_shuttle(url, check_period, target_classes)
        QMessageBox.information(self, 'Success', 'Current settings saved in Shuttles menu.\n(Shortcut keys : Ctrl+2)',
                                QMessageBox.Yes, QMessageBox.NoButton)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
