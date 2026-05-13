from krita import *
from .settingsmenu import SettingsMenu

class TemporaryEraser(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("temperaser", "Configure a Temporary Eraser Preset", "tools/scripts")
        action.triggered.connect(self.openSettingsMenu)
    
    def openSettingsMenu(self):
        menu = SettingsMenu()
        menu.exec()