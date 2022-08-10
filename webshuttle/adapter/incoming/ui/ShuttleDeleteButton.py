from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QMessageBox

from webshuttle.adapter.incoming.ui.ShuttleFrame import ShuttleFrame
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ShuttleDeleteButton(QPushButton):
    def __init__(self, parent: QWidget, shuttle_frame: ShuttleFrame, shuttle_widget_group: ShuttleWidgetGroup):
        super().__init__(parent)
        self.shuttles_widget = parent
        self.shuttle_frame = shuttle_frame
        self.shuttle_widget_group = shuttle_widget_group

        self.setStyleSheet("background-color: rgba(255,255,255,0);")
        self.setIcon(QIcon('resource/images/remove-48.png'))
        self.setFixedWidth(30)
        self.setFixedHeight(30)
        self.clicked.connect(lambda: self._onclick())

    def _onclick(self):
        reply = self._confirm(self.shuttle_widget_group.shuttle_name_widget)
        if reply == QMessageBox.No:
            return

        if self.shuttles_widget.shuttles.get(self.shuttle_frame.shuttle_seq) is not None:
            self.shuttle_widget_group.state_widget.append(self.shuttles_widget.create_log_text_service.stopped(self.shuttle_widget_group.shuttle_name_widget.text()))
            self.shuttles_widget.shuttles[self.shuttle_frame.shuttle_seq] = None

        self.shuttle_widget_group.state_widget.append(self.shuttles_widget.create_log_text_service.deleted(self.shuttle_widget_group.shuttle_name_widget.text()))
        self.shuttle_frame.get_frame_widget().deleteLater()
        self.deleteLater()
        self.shuttles_widget.shuttles_vbox_layout.takeAt(self.shuttle_frame.shuttle_seq)
        self.shuttles_widget.shuttle_frames.pop(self.shuttle_frame.shuttle_seq)
        self.shuttles_widget.save_shuttles()

    def _confirm(self, shuttle_name_widget):
        return QMessageBox.question(self.shuttles_widget, '삭제 확인', f'\'{shuttle_name_widget.text()}\' 셔틀이 삭제됩니다.',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
