import sys
import os
import sqlite3
from functools import partial
from Crypto.Cipher import AES
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

class NewDialog(qtw.QDialog):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.initUI()

    def initUI(self):

        siteLabel = qtw.QLabel()
        siteLabel.setText("Site")

        self.siteEntry = qtw.QLineEdit()

        passLabel = qtw.QLabel()
        passLabel.setText("Passwsord")

        self.passEntry = qtw.QLineEdit()

        submitButton = qtw.QPushButton("Add")
        submitButton.clicked.connect(self.addSite)

        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(siteLabel)
        self.layout.addWidget(self.siteEntry)
        self.layout.addWidget(passLabel)
        self.layout.addWidget(self.passEntry)
        self.layout.addWidget(submitButton)

        self.setLayout(self.layout)

        self.center()
        self.exec_()

    def addSite(self):
        site = self.siteEntry.text()
        password = self.passEntry.text()

        self.master.addSite(site, password)

    def center(self):
        frameGeometry = self.frameGeometry()
        center = self.master.frameGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())



class MainWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.currentRow = 0

        self.layout = qtw.QGridLayout()
        self.layout.setColumnStretch(0, 200)
        self.layout.setColumnStretch(1, 600)
        self.layout.setColumnStretch(2, 200)
        self.layout.setColumnStretch(3, 200)
        self.setSizePolicy(qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def addRow(self, site):
        label = qtw.QLabel()
        label.setText(site)
        label.setWordWrap(1)

        pwdField = qtw.QLineEdit()
        pwdField.setDisabled(1)

        showButton = qtw.QPushButton("Show")
        showFunction = partial(self.showPassword, site)
        showButton.clicked.connect(showFunction)

        copyButton = qtw.QPushButton("Copy")
        copyFunction = partial(self.copyPassword, site)
        copyButton.clicked.connect(copyFunction)

        self.layout.addWidget(label, self.currentRow, 0)
        self.layout.addWidget(pwdField, self.currentRow, 1)
        self.layout.addWidget(showButton, self.currentRow, 2)
        self.layout.addWidget(copyButton, self.currentRow, 3)

        self.currentRow += 1

    def showPassword(self, site):
        pass
    def copyPassword(self, site):
        pass


class App(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Password Manager'
        self.key = 'abacus1337abacus'
        self.cipher = AES.new(self.key, AES.MODE_ECB)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 600, 400)

        self.mainWidget = MainWidget()
        self.load()

        title = qtw.QLabel()
        title.setText("Manage Passwords")
        title.setAlignment(qtc.Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px;")

        addButton = qtw.QPushButton("Add Site")
        addButton.clicked.connect(self.addSite)

        self.scrollArea = qtw.QScrollArea(self)
        #self.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scrollArea.widgetResizable()
        self.scrollArea.setWidget(self.mainWidget)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)

        self.mainLayout = qtw.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setAlignment(qtc.Qt.AlignCenter)
        self.mainLayout.addWidget(title)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(addButton)

        self.setLayout(self.mainLayout)

        self.center()
        self.show()

    def addSite(self):
        NewDialog(self)

    def load(self):
        sql = "SELECT site FROM stuff"
        sites = self.runQuery(sql, None, True)
        for site in sites:
            oneSite = site[0]
            self.mainWidget.addRow(oneSite)

    def center(self):
        frameGeometry = self.frameGeometry()
        center = qtw.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())

    @staticmethod
    def runQuery(sql, data=None, receive=False):
        conn = sqlite3.connect("nothing.db")
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive:
            return cursor.fetchall()
        else:
            conn.commit()

        conn.close()

    @staticmethod
    def firstTimeDB():
        create_tables = "CREATE TABLE stuff (site TEXT, thing TEXT)"
        App.runQuery(create_tables)


if __name__ == '__main__':
    if not os.path.isfile("nothing.db"):
        App.firstTimeDB()
    app = qtw.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

