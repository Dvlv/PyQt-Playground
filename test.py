import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg


class App(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'hello'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 600, 400)

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

