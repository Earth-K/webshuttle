from PyQt5.QtWidgets import QLineEdit, QTextEdit, QPushButton, QSpinBox
from webdriver_manager.chrome import ChromeDriverManager

from webshuttle.adapter.incoming.ui import MainWindow
from webshuttle.adapter.incoming.ui.widget.BaseWidget import BaseWidget
from webshuttle.adapter.incoming.ui.widget.ShuttleAddWidget import ShuttleAddWidget
from webshuttle.adapter.incoming.ui.widget.ShuttlesWidget import ShuttlesWidget
from webshuttle.adapter.incoming.ui.widget.StateWidget import StateWidget
from webshuttle.adapter.outcoming.persistence.ShuttlePersistenceAdapter import ShuttlePersistenceAdapter
from webshuttle.application.ExportShuttlesService import ExportShuttlesService
from webshuttle.application.GetShuttlesService import GetShuttlesService
from webshuttle.application.LoadShuttlesService import LoadShuttlesService
from webshuttle.application.SelectAreaService import SelectAreaService


class MainWindowAppConfig:

    def __init__(self, main_window: MainWindow):
        self.mainWindow = main_window
        self.chromeDriver = None
        self.stateWidget = None
        self.shuttlesWidget = None
        self.selectAreaService = None
        self.shuttleAddWidget = None

    def chrome_driver(self):
        if self.chromeDriver is None:
            self.chromeDriver = ChromeDriverManager().install()
        return self.chromeDriver

    def shuttles_widget(self):
        if self.shuttlesWidget is None:
            self.shuttlesWidget = ShuttlesWidget(parent=self.mainWindow,
                                                 chrome_driver=self.chrome_driver(),
                                                 get_shuttles_usecase=self.getShuttlesService(),
                                                 load_shuttles_usecase=self.loadShuttlesService(),
                                                 export_shuttles_usecase=self.exportShuttlesService(),
                                                 file_name="shuttles.json")
        return self.shuttlesWidget

    def select_area_service(self):
        if self.selectAreaService is None:
            self.selectAreaService = SelectAreaService(url_widget=self.qLineEdit(),
                                                       filtering_keyword_widget=self.qLineEdit(),
                                                       chrome_driver=self.chrome_driver())
        return self.selectAreaService

    def shuttle_add_widget(self):
        if self.shuttleAddWidget is None:
            self.shuttleAddWidget = ShuttleAddWidget(parent=self.mainWindow,
                                                     shuttles_widget=self.shuttles_widget(),
                                                     state_widget=self.state_widget(),
                                                     elements_report_widget=self.qTextEdit(),
                                                     shuttle_name_widget=self.qLineEdit(),
                                                     url_widget=self.qLineEdit(),
                                                     period_widget=self.period_widget(),
                                                     filtering_keyword_widget=self.qLineEdit(),
                                                     addshuttle_button=self.qPushButton(),
                                                     select_area_usecase=self.select_area_service())
        return self.shuttleAddWidget

    def state_widget(self):
        if self.stateWidget is None:
            self.stateWidget = StateWidget(self.mainWindow)
        return self.stateWidget

    def base_widget(self):
        return BaseWidget(self.mainWindow, self.shuttle_add_widget(), self.shuttles_widget(), self.state_widget())

    def getShuttlesService(self):
        return GetShuttlesService()

    def loadShuttlesService(self):
        return LoadShuttlesService(shuttle_repository=self.jsonRepository())

    def exportShuttlesService(self):
        return ExportShuttlesService(self.jsonRepository())

    def jsonRepository(self):
        return ShuttlePersistenceAdapter()

    def qLineEdit(self):
        return QLineEdit()

    def qTextEdit(self):
        return QTextEdit()

    def qPushButton(self):
        return QPushButton()

    def period_widget(self):
        period_widget = QSpinBox()
        period_widget.setMaximum(86400)
        period_widget.setValue(300)
        return period_widget
