from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from webshuttle.adapter.incoming.ui.ShuttleFrameDialogLayout import ShuttleFrameDialogLayout


class ShuttleFrameSettingDialog(QDialog):
    def __init__(self, shuttle_frame, shuttles_widget):
        super().__init__(shuttles_widget)
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(300, 200)
        self.setWindowTitle("셔틀 설정")
        self.setLayout(ShuttleFrameDialogLayout(shuttle_frame=shuttle_frame, dialog=self))
