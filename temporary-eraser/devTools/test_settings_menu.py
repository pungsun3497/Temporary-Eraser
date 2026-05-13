import os
import sys
from PyQt5.QtWidgets import *

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from settings_dialog import SettingsDialog

app = QApplication(sys.argv)

menu = SettingsMenu()
menu.show()

sys.exit(app.exec())

