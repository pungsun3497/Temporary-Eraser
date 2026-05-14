from PyQt5.QtCore import *

class KeyReleaseFilter(QObject):

    def __init__(self):
        super().__init__()
        self.keys = set()
        self.callback : callable = None
    

    def setCallback(self, keys, callback):
        self.keys = keys
        self.callback = callback
    

    def clearCallback(self):
        self.keys = set()
        self.callback = None


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyRelease:
            for key in self.keys:
                if key == event.key() and callable(self.callback):
                    self.callback()
                    
        return False