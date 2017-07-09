import sys
import os
import sqlite3
import base64
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
        passLabel.setText("Password")

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
        self.deleteLater()

    def center(self):
        frameGeometry = self.frameGeometry()
        center = self.master.frameGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())


class Row(qtw.QWidget):

    deletedEvent = qtc.pyqtSignal()
    FIXED_HEIGHT_CONTANT = 50

    def __init__(self, site):
        super().__init__()
        self.site = site
        self.initUI()

    def initUI(self):
        self.layout = qtw.QHBoxLayout()
        self.setFixedHeight(Row.FIXED_HEIGHT_CONTANT)

        self.label = qtw.QLabel()
        self.label.setText(self.site)
        self.label.setWordWrap(1)

        self.pwdField = qtw.QLineEdit()
        self.pwdField.setDisabled(1)

        self.showButton = qtw.QPushButton("Show")
        self.showButton.clicked.connect(self.showPassword)

        self.copyButton = qtw.QPushButton("Copy")
        self.copyButton.clicked.connect(self.copyPassword)

        self.removeButton = qtw.QPushButton("Remove")
        self.removeButton.clicked.connect(self.removePassword)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.pwdField)
        self.layout.addWidget(self.showButton)
        self.layout.addWidget(self.copyButton)
        self.layout.addWidget(self.removeButton)

        self.setSizePolicy(qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def getPassword(self):
        sql = "SELECT thing FROM stuff WHERE site = ?"
        data = (self.site,)
        passwords = App.runQuery(sql, data, True)
        password = passwords[0][0]
        if password:
            decrypted_password = App.decryptPassword(password)
            return decrypted_password.decode()

    def showPassword(self):
        password = self.getPassword()
        if password:
            self.pwdField.setText(password)

    def removePassword(self):
        sql = "DELETE FROM stuff WHERE site = ?"
        data = (self.site,)
        try:
            App.runQuery(sql, data)
        except Exception as e:
            qtw.QMessageBox.critical(self, "Failed", "Delete Failed")
        else:
            qtw.QMessageBox.information(self, "Deleted", self.site + " deleted from the database!")
            self.deletedEvent.emit()

    def copyPassword(self):
        password = self.getPassword()
        clipboard = qtw.QApplication.clipboard()
        clipboard.setText(password)


class MainWidget(qtw.QWidget):
    triggerReloadEvent = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.currentRow = 0

        self.layout = qtw.QVBoxLayout()
        self.setSizePolicy(qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def addRow(self, site):
        row = Row(site)
        self.layout.addWidget(row)
        row.deletedEvent.connect(self.triggerReload)

    def addStretch(self):
        self.layout.addStretch()

    def triggerReload(self):
        self.triggerReloadEvent.emit()

    def clear(self):
        number_of_widgets = self.layout.count()
        for index in reversed(range(number_of_widgets)):
            item = self.layout.takeAt(index)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)


class App(qtw.QWidget):
    key = 'abacus1337abacus'
    cipher = AES.new(key, AES.MODE_ECB)

    def __init__(self):
        super().__init__()
        self.title = 'Password Manager'

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 600, 400)

        self.mainWidget = MainWidget()
        self.mainWidget.triggerReloadEvent.connect(self.reload)
        self.load()

        title = qtw.QLabel()
        title.setText("Manage Passwords")
        title.setAlignment(qtc.Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px;")

        addButton = qtw.QPushButton("Add Site")
        addButton.clicked.connect(self.addSiteButtonPressed)

        self.scrollArea = qtw.QScrollArea(self)
        #self.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setSizePolicy(qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

        self.mainLayout = qtw.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setAlignment(qtc.Qt.AlignTop)
        self.mainLayout.addWidget(title)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(addButton)

        self.setLayout(self.mainLayout)

        self.center()
        self.show()

    def addSiteButtonPressed(self):
        NewDialog(self)

    def addSite(self, site, password):
        encrypted_password = base64.b64encode(self.cipher.encrypt(password.rjust(32)))
        sql = "INSERT INTO stuff VALUES (?,?)"
        data = (site, encrypted_password)
        try:
            self.runQuery(sql, data)
        except Exception as e:
            qtw.QMessageBox.critical(self, "Add Failed", str(e))
        else:
            qtw.QMessageBox.information(self, "Add Successful", site + " added!")

        self.reload()


    def load(self):
        sql = "SELECT site FROM stuff"
        sites = self.runQuery(sql, None, True)
        for site in sites:
            oneSite = site[0]
            self.mainWidget.addRow(oneSite)
        self.mainWidget.addStretch()

    def reload(self):
        self.mainWidget.clear()
        self.load()
        self.mainWidget.repaint()


    def center(self):
        frameGeometry = self.frameGeometry()
        center = qtw.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())

    @staticmethod
    def decryptPassword(password):
        return App.cipher.decrypt(base64.b64decode(password))

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

