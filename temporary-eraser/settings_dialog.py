from PyQt5.QtWidgets import *
#from krita import *

class SettingsMenu(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dialog')
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        button1 = QPushButton("Test Button1", self)
        button2 = QPushButton("Test Button2", self)

        self.layout.addWidget(button1)
        self.layout.addWidget(button2)
