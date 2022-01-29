import sys

from EventListenerInjector import EventListenerInjector
from WebCrawler import WebCrawler
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self._webCrawler = None
        self._logBox = None
        self._lineText = None
        self._init_ui()

    def _init_ui(self):
        self.resize(400, 400)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self._logBox = QTextEdit(self)
        self._logBox.setReadOnly(True)
        startBtn = QPushButton('Browser Open', self)
        startBtn.clicked.connect(self._open_browser)
        self._lineText = QLineEdit()
        self._lineText.setPlaceholderText('https://example.com')
        self.setLayout(self._vbox_layout(self._lineText, startBtn, self._logBox))
        self.show()

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())

    def _vbox_layout(self, lineText, startBtn, logBox):
        result = QVBoxLayout()
        result.addWidget(lineText)
        result.addWidget(startBtn)
        result.addWidget(logBox)
        return result

    def _open_browser(self):
        self._webCrawler = WebCrawler(self._lineText.text())
        self._init_eventlistener(self._webCrawler)

    def _init_eventlistener(self, webCrawler):
        injector = EventListenerInjector(webCrawler)
        injector.add_mouseover()
        injector.add_mouseleave()
        injector.add_mousedown_right()
        injector.add_tooltip()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
