import json
import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QAction, QMainWindow, QMessageBox
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from widgets.BaseWidget import BaseWidget
from widgets.StateWidget import StateWidget
from widgets.ShuttleAddWidget import ShuttleAddWidget
from widgets.ShuttlesWidget import ShuttlesWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        chrome_service = Service(ChromeDriverManager().install())
        chrome_service.creationflags = 0x08000000

        self.shuttles_widget = ShuttlesWidget(self, chrome_service)
        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)
        menu_save = menubar.addMenu('&저장')
        menu_save.addAction(self._export_saved_shuttles_action(self.shuttles_widget))
        self.statusBar()
        self.state_widget = StateWidget(self)
        self.shuttle_add_widget = ShuttleAddWidget(self, self.shuttles_widget, self.state_widget, chrome_service)
        self.base_widget = BaseWidget(self, self.shuttle_add_widget, self.shuttles_widget, self.state_widget)
        self.setCentralWidget(self.base_widget)

        self.shuttles_widget.import_external_shuttles(self.state_widget)

        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self.show()

    def _export_saved_shuttles_action(self, shuttles_widget):
        result = QAction('셔틀 목록 저장하기', self)
        result.setShortcut('Ctrl+S')
        result.setStatusTip('Save added shuttles.')
        result.triggered.connect(shuttles_widget.save_shuttles)
        return result

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
