import sys
from WebCrawler import WebCrawler
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self._webCrawler = None
        self._logBox = None
        self._lineText = None
        self._initUI()

    def _initUI(self):
        self.resize(400, 400)
        self._moveToCenter()
        self.setWindowTitle('WebShuttle')
        self._logBox = QTextEdit(self)
        self._logBox.setReadOnly(True)
        startBtn = QPushButton('Browser Open', self)
        startBtn.clicked.connect(self._openBrowser)
        self._lineText = QLineEdit()
        self._lineText.setPlaceholderText('https://example.com')
        self.setLayout(self._vboxLayout(self._lineText, startBtn, self._logBox))
        self.show()

    def _moveToCenter(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())

    def _vboxLayout(self, lineText, startBtn, logBox):
        result = QVBoxLayout()
        result.addWidget(lineText)
        result.addWidget(startBtn)
        result.addWidget(logBox)
        return result

    def _openBrowser(self):
        self._webCrawler = WebCrawler(self._lineText.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
