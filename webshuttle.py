import json
import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QAction, QMainWindow, QMessageBox
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from widgets.BaseWidget import BaseWidget
from widgets.LogWidget import LogWidget
from widgets.MainWidget import MainWidget
from widgets.ShuttlesWidget import ShuttlesWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        chrome_service = Service(ChromeDriverManager().install())
        chrome_service.creationflags = 0x08000000

        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)
        menu_save = menubar.addMenu('&저장')
        menu_save.addAction(self._export_saved_shuttles_action())
        self.statusBar()

        self.main_widget = MainWidget(self, chrome_service)
        self.shuttles_widget = ShuttlesWidget(self, chrome_service)
        self.log_widget = LogWidget(self)
        self.base_widget = BaseWidget(self, self.main_widget, self.shuttles_widget, self.log_widget)
        self.setCentralWidget(self.base_widget)

        self._import_external_shuttles_config()

        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self.show()

    def _export_saved_shuttles_action(self):
        result = QAction('셔틀 목록 저장하기', self)
        result.setShortcut('Ctrl+S')
        result.setStatusTip('Save added shuttles.')
        result.triggered.connect(self._export_saved_shuttles)
        return result

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())

    def add_shuttle(self):
        main_widget = self.main_widget
        shuttles_widget = self.shuttles_widget
        log_widget = self.log_widget
        shuttle_name = main_widget.lineedit_shuttle_name.text()
        url = main_widget.lineedit_url.text()

        target_classes = main_widget.element_class_names
        if url is None or target_classes is None:
            QMessageBox.information(self, '에러',
                                    "먼저 선택 영역 데이터를 불러와주세요.",
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return
        shuttles_widget.add_shuttle(url, 300, target_classes, shuttle_name, log_widget.get_edittext())
        QMessageBox.information(self, '성공', '셔틀이 셔틀 목록에 저장되었습니다.',
                                QMessageBox.Yes, QMessageBox.NoButton)

    def _export_saved_shuttles(self):
        saved_shuttles_tuple_list = self.shuttles_widget.get_saved_shuttles_array()
        shuttles_json = {}
        for saved_shuttle in saved_shuttles_tuple_list:
            shuttle_id = saved_shuttle[0]
            attribute_names = ['name', 'url', 'period', 'element_classes']
            attributes = {}
            for index, name in enumerate(attribute_names):
                attributes[name] = saved_shuttle[1][index]
            shuttles_json[shuttle_id] = attributes

        with open('shuttles.json', 'w', encoding="utf-8") as json_file:
            json_file.write(json.dumps(shuttles_json, ensure_ascii=False, indent=2))

    def _import_external_shuttles_config(self):
        with open('shuttles.json', 'r', encoding="utf-8") as shuttles_file:
            shuttles: dict = json.load(shuttles_file)
        for index in range(len(shuttles.keys())):
            shuttle_attributes = shuttles[f'shuttle{index}']
            self.shuttles_widget.add_shuttle(name=shuttle_attributes["name"], url=shuttle_attributes["url"],
                                             period=shuttle_attributes["period"],
                                             target_classes=shuttle_attributes["element_classes"],
                                             log_edittext=self.log_widget.get_edittext())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
