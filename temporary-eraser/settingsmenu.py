from PyQt5.QtWidgets import *
from krita import *

class SettingsMenu(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dialog')