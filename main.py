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
        self._addClassAtAllElements()

    def _addClassAtAllElements(self):
        script = ''' 
        let childNodes = document.getElementsByTagName('body')[0].childNodes;
        const func = (c) => {
          if(c==undefined) return;
          for(let i = 0 ; i<c.length; i++) {
            c[i].addEventListener("mouseover", function(event) {
                event.stopPropagation();
                console.log(event);
                event.target.style.border = "3px solid rgba(217,217,243,90)";
            });
            c[i].addEventListener("mouseleave", function(event) {
                event.stopPropagation();
                console.log(event);
                event.target.style.border = "";
            });
            func(c[i].childNodes);
          }
        }
        func(childNodes);
        '''
        self._webCrawler.executeJs(script)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
