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


    def installFilter(self):
        Krita.instance().activeWindow().qwindow().installEventFilter(self.key_release_filter)


    def createActions(self, window):
        self.settings_action = window.createAction("temporaryEraserSettings", "Configure Temporary Eraser Preset", "tools/scripts")
        self.settings_action.triggered.connect(self.openSettingsDialog)

        self.hold_action = window.createAction("temporaryEraserHold", "", "")
        self.hold_action.triggered.connect(self.holdEraser)
        self.hold_action.changed.connect(self.updateShortcutChache)
        self.updateShortcutChache()
    

    def openSettingsDialog(self):
        menu = SettingsDialog()
        menu.exec()


    def updateShortcutChache(self):
        self.keys = set()

        for shortcut in self.hold_action.shortcuts():
            for action_key_comb in shortcut:
                pure_key = action_key_comb & ~Qt.KeyboardModifier.KeyboardModifierMask
                self.keys.add(pure_key)


    def holdEraser(self):
        if self.is_swapped: 
            return

        self.eraser_name = Krita.instance().readSetting("", "TemporaryEraser", None)
        if not self.eraser_name:
            return

        view = Krita.instance().activeWindow().activeView()
        if not view:
            return
        
        # change preset
        presets = Krita.instance().resources("preset")
        if self.eraser_name in presets:
            self.old_preset = view.currentBrushPreset()
            view.setCurrentBrushPreset(presets[self.eraser_name])
            self.is_swapped = True

        # assign KeyReleased callback
        self.key_release_filter.setCallback(self.keys, self.releaseEraser)


    def releaseEraser(self):
        if not self.is_swapped:
            return
        
        view = Krita.instance().activeWindow().activeView()

        if self.old_preset:
            view.setCurrentBrushPreset(self.old_preset)
            self.old_preset = None
            self.is_swapped = False