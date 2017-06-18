import sys
import requests
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg


class LanguageTab(qtw.QWidget):
    def __init__(self, tab_name):
        super().__init__()
        self.tab_name = tab_name

        self.layout = qtw.QVBoxLayout()
        self.layout.setAlignment(qtc.Qt.AlignTop)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSizeConstraint(qtw.QLayout.SetMinAndMaxSize)

        self.translationLabel = qtw.QLabel()
        self.translationLabel.setText("<Translation Here>")
        #self.translationLabel.setGeometry(0,0,400,400)
        self.translationLabel.setSizePolicy(qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))
        self.translationLabel.setAlignment(qtc.Qt.AlignCenter)

        self.clipboard_button = qtw.QPushButton("Copy to Clipboard")
        self.clipboard_button.clicked.connect(self.copyTranslationToClipboard)

        self.layout.addWidget(self.translationLabel)
        self.layout.addWidget(self.clipboard_button)

        self.setLayout(self.layout)

    def copyTranslationToClipboard(self):
        tranlation = self.translationLabel.text()
        print(tranlation)


class App(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'hello'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 600, 400)

        self.layout = qtw.QVBoxLayout()

        self.tabs = qtw.QTabWidget()
        self.tabs.resize(300,200)
        italian_tab = LanguageTab("Italian")
        self.tabs.addTab(italian_tab, "Italian")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.center()
        self.show()

    def center(self):
        frameGeometry = self.frameGeometry()
        center = qtw.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

