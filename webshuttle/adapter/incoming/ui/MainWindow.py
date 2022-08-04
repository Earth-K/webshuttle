from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QTextEdit, QLineEdit, QPushButton, QSpinBox
from webdriver_manager.chrome import ChromeDriverManager

from webshuttle.adapter.incoming.ui.BaseWidget import BaseWidget
from webshuttle.adapter.incoming.ui.ShuttleAddWidget import ShuttleAddWidget
from webshuttle.adapter.incoming.ui.ShuttlesWidget import ShuttlesWidget
from webshuttle.adapter.incoming.ui.StateWidget import StateWidget
from webshuttle.adapter.outcoming.persistence.ShuttlePersistenceAdapter import ShuttlePersistenceAdapter
from webshuttle.application.CreateLogTextService import CreateLogTextService
from webshuttle.application.CreateShuttleFrameService import CreateShuttleFrameService
from webshuttle.application.ExportShuttlesService import ExportShuttlesService
from webshuttle.application.GetShuttlesService import GetShuttlesService
from webshuttle.application.LoadShuttlesService import LoadShuttlesService
from webshuttle.application.SelectAreaService import SelectAreaService
from webshuttle.application.port.incoming.LoadShuttlesCommand import LoadShuttlesCommand


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        chrome_driver = ChromeDriverManager().install()
        state_widget = StateWidget(self)
        url_widget = QLineEdit()
        filtering_keyword_widget = QLineEdit()
        select_area_service = SelectAreaService(url_widget=url_widget,
                                                filtering_keyword_widget=filtering_keyword_widget,
                                                chrome_driver=chrome_driver)
        shuttles_widget = ShuttlesWidget(parent=self,
                                         chrome_driver=chrome_driver,
                                         get_shuttles_usecase=GetShuttlesService(),
                                         load_shuttles_usecase=LoadShuttlesService(ShuttlePersistenceAdapter()),
                                         export_shuttles_usecase=ExportShuttlesService(ShuttlePersistenceAdapter()),
                                         create_shuttleframe_usecase=CreateShuttleFrameService(),
                                         create_logtext_usecase=CreateLogTextService(),
                                         file_name="shuttles.json")
        period_widget = QSpinBox()
        period_widget.setMaximum(86400)
        period_widget.setValue(300)
        shuttle_add_widget = ShuttleAddWidget(parent=self,
                                              shuttles_widget=shuttles_widget,
                                              state_widget=state_widget,
                                              elements_report_widget=QTextEdit(),
                                              shuttle_name_widget=QLineEdit(),
                                              url_widget=url_widget,
                                              period_widget=period_widget,
                                              filtering_keyword_widget=filtering_keyword_widget,
                                              addshuttle_button=QPushButton(),
                                              select_area_usecase=select_area_service)
        base_widget = BaseWidget(self, shuttle_add_widget, shuttles_widget, state_widget)
        self.setCentralWidget(base_widget)

        load_shuttles_command = LoadShuttlesCommand(shuttles_widget=shuttles_widget,
                                                    state_widget=state_widget)
        shuttles_widget.import_external_shuttles(load_shuttles_command)

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
