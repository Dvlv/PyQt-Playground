import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt as qt


class App(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Todo List'

        self.colour_schemes = {
            0: "background: lightgrey; color: black; padding:20px;",
            1: "background: grey; color: white; padding:20px;"
        }

        self.tasks = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 300, 400)

        #widgets

        # tasks
        default_task = qtw.QLabel(self)
        default_task.setText("--- Add Tasks Here ---")
        default_task.setStyleSheet(self.colour_schemes[0])
        #default_task.setContentsMargins(0, 0, 0, 0)
        default_task.setAlignment(qt.AlignCenter)

        self.default_task = default_task
        self.tasks.append(self.default_task)

        # text input
        text_input = qtw.QTextEdit(self)
        text_input.setAlignment(qt.AlignBottom)
        text_input.setMaximumHeight(75)

        #button
        button = qtw.QPushButton("Create", self)
        button.clicked.connect(self.addTask)

        self.text_input = text_input

        # vertical layout
        vbox = qtw.QVBoxLayout()
        vbox.setAlignment(qt.AlignTop)
        vbox.addWidget(self.default_task)
        vbox.addStretch(1)
        vbox.addWidget(self.text_input)
        vbox.addWidget(button)
        vbox.setContentsMargins(0,0,0,0)

        self.vbox = vbox

        self.setLayout(self.vbox)

        self.center()
        self.show()

    def addTask(self):
        task_text = self.text_input.toPlainText()
        task = qtw.QLabel(self)
        task.setText(task_text)
        task.setAlignment(qt.AlignCenter)

        # choose colour scheme
        _, colour_scheme_choice = divmod(len(self.tasks), 2)
        task.setStyleSheet(self.colour_schemes[colour_scheme_choice])
        self.tasks.append(task)

        # calculate position to insert at
        number_of_widgets = self.vbox.count()
        for index in range(number_of_widgets):
            widget = self.vbox.itemAt(index).widget()
            if isinstance(widget, qtw.QLabel):
                continue
            else:
                self.vbox.insertWidget(index, task)
                break

    def center(self):
        frameGeometry = self.frameGeometry()
        center = qtw.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

