import sys
import requests
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg


class LanguageTab(qtw.QWidget):
    def __init__(self, language, shortCode):
        super().__init__()
        self.language = language
        self.shortCode = shortCode

        self.layout = qtw.QVBoxLayout()
        self.layout.setAlignment(qtc.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSizeConstraint(qtw.QLayout.SetMinAndMaxSize)

        self.translationLabel = qtw.QLabel()
        self.translationLabel.setText("<Translation Here>")
        self.translationLabel.setSizePolicy(qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))
        self.translationLabel.setWordWrap(1)
        self.translationLabel.setAlignment(qtc.Qt.AlignCenter)

        self.clipboard_button = qtw.QPushButton("Copy to Clipboard")
        self.clipboard_button.clicked.connect(self.copyTranslationToClipboard)

        self.layout.addWidget(self.translationLabel)
        self.layout.addWidget(self.clipboard_button)

        self.setLayout(self.layout)

    def copyTranslationToClipboard(self):
        translation = self.translationLabel.text()
        clipboard = qtw.QApplication.clipboard()
        clipboard.setText(translation)


class EnglishTab(qtw.QWidget):
    def __init__(self, parent):
        super().__init__()

        self.language = "English"
        self.parent = parent

        self.layout = qtw.QVBoxLayout()
        self.layout.setAlignment(qtc.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSizeConstraint(qtw.QLayout.SetMinAndMaxSize)

        self.textInput = qtw.QTextEdit()
        self.textInput.setSizePolicy(qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

        self.translateButton = qtw.QPushButton("Translate")
        self.translateButton.clicked.connect(self.translate)

        self.layout.addWidget(self.textInput)
        self.layout.addWidget(self.translateButton)

        self.setLayout(self.layout)

    def translate(self):
        textToTranslate = self.textInput.toPlainText().strip()

        if textToTranslate:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}"

            try:
                for language in self.parent.languageTabs:
                    full_url = url.format("en", language.shortCode, textToTranslate)
                    r = requests.get(full_url)
                    r.raise_for_status()
                    translation = r.json()[0][0][0]
                    language.translationLabel.setText(translation)
            except Exception as e:
                qtw.QMessageBox.critical(self, "An error occurred", str(e))
            else:
                qtw.QMessageBox.information(self, "Translation Successful", "Text successfully translated!")
        else:
            self.textInput.clear()


class AddLanguageForm(qtw.QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Add New Language")
        self.setGeometry(0, 0, 200, 130)

        self.layout = qtw.QVBoxLayout()
        self.layout.setAlignment(qtc.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSizeConstraint(qtw.QLayout.SetMinAndMaxSize)

        self.languageNameLabel = qtw.QLabel()
        self.languageNameLabel.setText("Language Name:")

        self.languageNameInput = qtw.QLineEdit()

        self.languageShortCodeLabel = qtw.QLabel()
        self.languageShortCodeLabel.setText("Language Short Code:")

        self.languageShortCodeInput = qtw.QLineEdit()

        self.submitButton = qtw.QPushButton("Submit")
        self.submitButton.clicked.connect(self.submit)

        self.layout.addWidget(self.languageNameLabel)
        self.layout.addWidget(self.languageNameInput)
        self.layout.addWidget(self.languageShortCodeLabel)
        self.layout.addWidget(self.languageShortCodeInput)
        self.layout.addWidget(self.submitButton)

        self.setLayout(self.layout)
        self.center()
        self.exec_()

    def submit(self):
        language = self.languageNameInput.text()
        shortCode = self.languageShortCodeInput.text()

        if language and shortCode:
            newTab = LanguageTab(language, shortCode)
            self.parent.mainWidget.addTab(newTab)
            qtw.QMessageBox.information(self, "Tab Added", language + " tab added")
            self.destroy()

    def center(self):
        frameGeometry = self.frameGeometry()
        center = self.parent.frameGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())



class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(10, 10, 600, 400)
        self.setWindowTitle("Translation Tool")

        menubar = self.menuBar()
        self.populateMenuBar(menubar)



        self.mainWidget = App()
        self.setCentralWidget(self.mainWidget)

        self.center()
        self.show()

    def populateMenuBar(self, menubar):
        addPortAction = qtw.QAction("Add Portuguese Tab", self)
        addPortAction.setStatusTip("Adds Portuguese")
        addPortAction.triggered.connect(self.addPortugueseTab)

        addLanguageAction = qtw.QAction("Add Language", self)
        addLanguageAction.setStatusTip("Add any language")
        addLanguageAction.triggered.connect(self.addNewLanguage)

        languagesMenu = menubar.addMenu("&Languages")
        languagesMenu.addAction(addPortAction)
        languagesMenu.addAction(addLanguageAction)

    def addPortugueseTab(self):
        portTab = LanguageTab("Portuguese", "pt")
        self.mainWidget.addTab(portTab)

    def addNewLanguage(self):
        AddLanguageForm(self)

    def center(self):
        frameGeometry = self.frameGeometry()
        center = qtw.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())


class App(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = qtw.QVBoxLayout()

        self.languageTabs = []

        self.tabs = qtw.QTabWidget()
        self.tabs.resize(300,200)

        englishTab = EnglishTab(self)
        italianTab = LanguageTab("Italian", "it")

        self.tabs.addTab(englishTab, "English")

        self.addTab(italianTab)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def addTab(self, tab):
        self.languageTabs.append(tab)
        self.tabs.addTab(tab, tab.language)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

