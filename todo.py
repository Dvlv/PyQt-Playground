import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc


class TaskDisplayWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.colour_schemes = {
            0: "background: lightgrey; color: black;",
            1: "background: grey; color: white;;"
        }

        default_task = qtw.QLabel(self)
        default_task.setText("--- Add Tasks Here ---")
        default_task.setStyleSheet(self.colour_schemes[0])
        default_task.setAlignment(qtc.Qt.AlignCenter)
        default_task.setFixedHeight(75)

        vbox = qtw.QVBoxLayout()
        vbox.setAlignment(qtc.Qt.AlignTop)
        vbox.addWidget(default_task, 1)
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSizeConstraint(qtw.QLayout.SetMinAndMaxSize)

        self.layout = vbox

        self.setLayout(self.layout)

        self.tasks = [default_task]
        self.maxWidth = 200

    def addTask(self, task_text):
        task = qtw.QLabel(self)
        task.setWordWrap(1)
        task.setGeometry(0,0,200,100)
        task.setText(task_text)
        task.setAlignment(qtc.Qt.AlignCenter)
        task.setFixedHeight(75)

        _, colour_scheme_choice = divmod(len(self.tasks), 2)
        task.setStyleSheet(self.colour_schemes[colour_scheme_choice])
        task.setMaximumWidth(self.maxWidth)

        number_of_widgets = self.layout.count()
        self.layout.insertWidget(number_of_widgets+1, task)
        self.tasks.append(task)

    def setTaskMaxWidths(self, width):
        self.maxWidth = width
        for index in range(self.layout.count()):
            self.layout.itemAt(index).widget().setMaximumWidth(self.maxWidth)


class TaskCreateTextEdit(qtw.QTextEdit):
    def keyPressEvent(self, event):
        if event.key() == qtc.Qt.Key_Return:
            self.parent().addTask()
        else:
            return super().keyPressEvent(event)


class App(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Todo List'

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 300, 400)

        #widgets

        # text input
        text_input = TaskCreateTextEdit(self)
        text_input.setAlignment(qtc.Qt.AlignBottom)
        text_input.setMaximumHeight(75)

        #button
        button = qtw.QPushButton("Create", self)
        button.clicked.connect(self.addTask)

        self.text_input = text_input

        self.task_display = TaskDisplayWidget()

        # scrolling
        self.scrollArea = qtw.QScrollArea(self)
        self.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scrollArea.widgetResizable()
        self.scrollArea.setWidget(self.task_display)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)

        self.mainLayout = qtw.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(self.text_input)
        self.mainLayout.addWidget(button)

        self.setLayout(self.mainLayout)

        self.center()
        self.show()

    def addTask(self):
        task_text = self.text_input.toPlainText()
        if task_text:
            self.task_display.addTask(task_text)
            self.text_input.clear()

    def center(self):
        frameGeometry = self.frameGeometry()
        center = qtw.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())

    def resizeEvent(self, event):
        new_width = event.size().width() - 25
        self.task_display.resize(new_width, 200)
        self.task_display.setTaskMaxWidths(new_width)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

