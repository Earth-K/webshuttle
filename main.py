import sys
from WebCrawler import WebCrawler
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QVBoxLayout, QTextEdit


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.webCrawler = None
        self.logBox = None
        self.initUI()

    def initUI(self):
        self.resize(400, 400)
        self.moveToCenter()
        self.setWindowTitle('WebShuttle')
        self.logBox = QTextEdit(self)
        self.logBox.setReadOnly(True)
        btn = self.getBodyBtn()
        btn.clicked.connect(self.bodyText)
        self.setLayout(self.vboxLayout(btn, self.logBox))
        self.show()

    def moveToCenter(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())

    def vboxLayout(self, getWebBodyBtn, logBox):
        result = QVBoxLayout()
        result.addWidget(getWebBodyBtn)
        result.addWidget(logBox)
        return result

    def getBodyBtn(self):
        return QPushButton('Start crawling', self)

    def bodyText(self):
        self.webCrawler = WebCrawler()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
