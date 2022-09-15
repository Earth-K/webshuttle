from PyQt5.QtWidgets import QDesktopWidget, QMainWindow

from webshuttle.adapter.incoming.ui.MainWindowAppConfig import MainWindowAppConfig


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        app_config = MainWindowAppConfig(self)
        state_widget = app_config.state_widget()
        shuttles_widget = app_config.shuttles_widget()
        load_shuttles_service = app_config.loadShuttlesService()
        load_shuttles_service.load(shuttles_widget, state_widget)

        self.setCentralWidget(app_config.base_widget())
        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self.statusBar()
        self.show()

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())
