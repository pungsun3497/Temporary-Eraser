from krita import *
from PyQt5.QtCore import *
from .settings_dialog import SettingsDialog
from .key_release_filter import KeyReleaseFilter


class TemporaryEraser(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.key_release_filter = KeyReleaseFilter()
        self.is_swapped = False


    def setup(self):
        notifier = Krita.instance().notifier()
        notifier.windowCreated.connect(self.installFilter)

        print("Complete Setup for Temporary Eraser")


    def installFilter(self):
        Krita.instance().activeWindow().qwindow().installEventFilter(self.key_release_filter)


    def createActions(self, window):
        self.settings_action = window.createAction("temporaryEraserSettings", "Configure Temporary Eraser Preset", "tools/scripts")
        self.settings_action.triggered.connect(self.openSettingsDialog)

        self.hold_action = window.createAction("temporaryEraserHold", "", "")
        self.hold_action.triggered.connect(self.holdEraser)
    

    def openSettingsDialog(self):
        menu = SettingsDialog()
        menu.exec()
    

    def holdEraser(self):
        if self.is_swapped: return

        self.toggleEraser(True)

        # parse keys
        keys = set()

        action_key_seq = self.hold_action.shortcut()
        for action_key_comb in action_key_seq:
            pure_key = action_key_comb & ~int(Qt.KeyboardModifier.KeyboardModifierMask)

            keys.add(pure_key)

            if action_key_comb & Qt.KeyboardModifier.ControlModifier:
                keys.add(Qt.Key.Key_Control)
            if action_key_comb & Qt.KeyboardModifier.AltModifier:
                keys.add(Qt.Key.Key_Alt)
            if action_key_comb & Qt.KeyboardModifier.ShiftModifier:
                keys.add(Qt.Key.Key_Shift)
        
        self.key_release_filter.setCallback(keys, self.releaseEraser)
    

    def releaseEraser(self):
        self.toggleEraser(False)
    

    def toggleEraser(self, enable):
        view = Krita.instance().activeWindow().activeView()
        if not view:
            return
        
        if enable:
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
    