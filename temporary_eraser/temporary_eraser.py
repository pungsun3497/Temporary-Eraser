from krita import *
from .settings_dialog import SettingsDialog
from PyQt5.QtCore import *


class KeyFilter(QObject):

    def __init__(self):
        super().__init__()
        self.is_swapped = False


    def eventFilter(self, obj, event):
        print(event)

        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Z and not event.isAutoRepeat():
                self.toggleEraser(True)
                return True
        elif event.type() == QEvent.KeyRelease:
            if event.key() == Qt.Key_Z and not event.isAutoRepeat():
                self.toggleEraser(False)
                return True
        return False
    

    def toggleEraser(self, checked):
        print("Toggle Eraser")
        view = Krita.instance().activeWindow().activeView()
        if not view:
            return
        
        if checked:
            self.eraser_name = Krita.instance().readSetting("", "TemporaryEraser", None)
            if not self.eraser_name:
                return

            presets = Krita.instance().resources("preset")
            if self.eraser_name in presets:
                self.old_preset = view.currentBrushPreset()
                view.setCurrentBrushPreset(presets[self.eraser_name])
                self.is_swapped = True
        
        else:
            if self.is_swapped and self.old_preset:
                view.setCurrentBrushPreset(self.old_preset)
                self.old_preset = None
                self.is_swapped = False


class TemporaryEraser(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.key_filter = KeyFilter()


    def setup(self):
        notifier = Krita.instance().notifier()
        notifier.windowCreated.connect(self.installFilter)


    def installFilter(self):
        Krita.instance().activeWindow().qwindow().installEventFilter(self.key_filter)


    def createActions(self, window):
        settings_action = window.createAction("temporaryEraserSettings", "Configure Temporary Eraser Preset", "tools/scripts")
        settings_action.triggered.connect(self.openSettingsDialog)

        #toggle_action = window.createAction("temporaryEraserToggle", "", "")
        #toggle_action.triggered.connect(self.toggleEraser)
    

    def openSettingsDialog(self):
        menu = SettingsDialog()
        menu.exec()
    