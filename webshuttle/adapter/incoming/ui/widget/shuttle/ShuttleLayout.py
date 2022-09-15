from PyQt5.QtWidgets import QHBoxLayout


class ShuttleLayout(QHBoxLayout):
    def __init__(self, shuttle_frame_widget, delete_shuttle_button):
        super().__init__()
        self.addWidget(shuttle_frame_widget)
        self.addWidget(delete_shuttle_button)
