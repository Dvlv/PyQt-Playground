import sys
import PyQt5.QtWidgets as qt


class App(qt.QWidget):
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
        center = qt.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())

if __name__ == '__main__':
    app = qt.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

