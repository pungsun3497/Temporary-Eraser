from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from krita import Krita

class SettingsDialog(QDialog):

    def __init__(self):
        super().__init__()
       
        self.all_presets = self.get_all_presets()
        self.selected_preset_name = Krita.instance().readSetting("", "TemporaryEraser", None)

        self.initUI()
    

    def get_all_presets(self):
        all_presets = Krita.instance().resources("preset")
        return all_presets


    def initUI(self):
        self.setWindowTitle('Temporary Eraser Settings')
        self.setMinimumSize(QSize(500, 400))
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # -----------------------------------------
        # Selected Preset

        self.preview_group = QGroupBox("Selected Preset")
        self.preview_layout = QHBoxLayout(self.preview_group)

        self.preview_icon = QLabel()
        self.preview_icon.setFixedSize(64, 64)
        self.preview_icon.setStyleSheet("border: 1px solid #555; background: #333;")

        self.preview_label = QLabel()
        self.preview_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.update_preview()
        
        self.preview_layout.addWidget(self.preview_icon)
        self.preview_layout.addWidget(self.preview_label)
        self.preview_layout.addStretch()
        
        self.layout.addWidget(self.preview_group)

        # -----------------------------------------
        # Preset List

        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setIconSize(QSize(64, 64))
        self.list_widget.setGridSize(QSize(80, 100))
        self.list_widget.setResizeMode(QListView.Adjust)
        self.list_widget.setSpacing(10)

        for name, resource in self.all_presets.items():
            thumbnail = QIcon(QPixmap.fromImage(resource.image()))

            item = QListWidgetItem(thumbnail, name)
            self.list_widget.addItem(item)
        
        self.list_widget.itemClicked.connect(self.select_preset)
        self.layout.addWidget(self.list_widget)

        # -----------------------------------------
        # Confirm Button

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
    

    def update_preview(self):
        if self.selected_preset_name:
            self.preview_icon.setPixmap(QPixmap.fromImage(self.all_presets[self.selected_preset_name].image()).scaled(64, 64))
            self.preview_label.setText(self.selected_preset_name)
        else:
            self.preview_icon.clear()
            self.preview_label.setText("Not Selected")


    def select_preset(self, item):
        self.selected_preset_name = item.text()
        self.update_preview()


    def accept(self):
        Krita.instance().writeSetting("", "TemporaryEraser", self.selected_preset_name)
        return super().accept()
    
    
    def reject(self):
        return super().reject()
    
