from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QMessageBox, QFrame

from webshuttle.domain.ShuttleFrame import ShuttleFrame
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ShuttleDeleteButton:
    def __init__(self, parent: QWidget, shuttle_frame: ShuttleFrame, shuttle_widget_group: ShuttleWidgetGroup):
        self.parent = parent
        self.shuttle_frame = shuttle_frame
        self.shuttle_widget_group = shuttle_widget_group

        delete_btn = QPushButton(parent=parent)
        delete_btn.setStyleSheet("background-color: rgba(255,255,255,0);")
        delete_btn.setIcon(QIcon('resource/images/remove-48.png'))
        delete_btn.setFixedWidth(30)
        delete_btn.setFixedHeight(30)
        delete_btn.clicked.connect(lambda: self._onclick())
        self._value: QPushButton = delete_btn

    def _onclick(self):
        reply = self._confirm(self.shuttle_widget_group.shuttle_name_widget)
        if reply == QMessageBox.No:
            return

        if self.parent.shuttles.get(self.shuttle_frame.shuttle_seq) is not None:
            self.shuttle_widget_group.state_widget.append(self.parent.create_log_text_service.stopped(self.shuttle_widget_group.shuttle_name_widget.text()))
            self.parent.shuttles[self.shuttle_frame.shuttle_seq] = None

        self.shuttle_widget_group.state_widget.append(self.parent.create_log_text_service.deleted(self.shuttle_widget_group.shuttle_name_widget.text()))
        self.shuttle_frame.get_frame_widget().deleteLater()
        self._value.deleteLater()
        self.parent.shuttles_vbox_layout.takeAt(self.shuttle_frame.shuttle_seq)
        self.parent.shuttle_frames.pop(self.shuttle_frame.shuttle_seq)
        self.parent.save_shuttles()

    def _confirm(self, shuttle_name_widget):
        return QMessageBox.question(self.parent, '삭제 확인', f'\'{shuttle_name_widget.text()}\' 셔틀이 삭제됩니다.',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def value(self) -> QPushButton:
        return self._value
