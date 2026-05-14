from PyQt5.QtCore import *

class KeyReleaseFilter(QObject):

    def __init__(self):
        super().__init__()
        self.keys = set()
        self.callback : callable = None
        self.holding = False
    

    def setCallback(self, keys, callback):
        self.keys = keys
        self.callback = callback
        self.holding = True
    

    def clearCallback(self):
        self.callback = None
        self.holding = False


    def eventFilter(self, obj, event):
        if not self.holding:
            return False

        if event.type() == QEvent.KeyRelease:
            if event.isAutoRepeat():
                return False
            
            for key in self.keys:
                if key == event.key() and callable(self.callback):
                    self.callback()
                    self.clearCallback()
                    return False
                    
        return False