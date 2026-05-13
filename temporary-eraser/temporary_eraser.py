from krita import *
from .settings_dialog import SettingsDialog

class TemporaryEraser(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("temperaser", "Configure a Temporary Eraser Preset", "tools/scripts")
        action.triggered.connect(self.openSettingsDialog)
    
    def openSettingsDialog(self):
        menu = SettingsDialog()
        menu.exec()