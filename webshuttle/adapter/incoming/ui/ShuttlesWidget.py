import pygame
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QSpinBox, QFrame, \
    QMessageBox

from webshuttle.adapter.incoming.ui import StateWidget
from webshuttle.application.CreateLogTextService import CreateLogTextService
from webshuttle.application.CreateShuttleFrameService import CreateShuttleFrameService
from webshuttle.application.CreateShuttleWidgetGroupService import CreateShuttleWidgetGroupService
from webshuttle.application.ExportShuttlesService import ExportShuttlesService
from webshuttle.application.GetShuttlesService import GetShuttlesService
from webshuttle.application.ImportShuttlesService import ImportShuttlesService
from webshuttle.application.port.incoming import CreateShuttleFrameUseCase
from webshuttle.application.port.incoming.CreateLogTextUseCase import CreateLogTextUseCase
from webshuttle.application.port.incoming.CreateShuttleWidgetGroupUseCase import CreateShuttleWidgetGroupUseCase
from webshuttle.application.port.incoming.ExportShuttlesUseCase import ExportShuttlesUseCase
from webshuttle.application.port.incoming.GetShuttlesUseCase import GetShuttlesUseCase
from webshuttle.application.port.incoming.ImportShuttlesUseCase import ImportShuttlesUseCase
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup

pygame.init()


def shuttle_setting_layout(hbox_layout):
    result = QVBoxLayout()
    result.addLayout(hbox_layout)
    return result


def url_lineedit(url):
    result = QLineEdit()
    result.setPlaceholderText('스크랩 하고 싶은 웹 페이지의 URL')
    result.setText(url)
    return result


def period_spinbox(period):
    result = QSpinBox()
    result.setMaximum(86400)
    result.setValue(int(period))
    return result


def target_classes_lineedit(target_classes):
    result = QLineEdit()
    result.setText(target_classes)
    return result


def shuttle_name_lineedit(name):
    result = QLineEdit(name)
    result.setPlaceholderText('셔틀의 이름')
    return result


def _stop(period, start_btn, stop_btn):
    period.setReadOnly(False)
    stop_btn.setDisabled(True)
    start_btn.setDisabled(False)


class ShuttlesWidget(QWidget):
    def __init__(self, parent, chrome_driver):
        super(ShuttlesWidget, self).__init__(parent)
        self.shuttle_seq = 0
        self.shuttle_frames = {}
        self.shuttles = {}
        self.driver_chrome = chrome_driver
        self._init_service()
        self._init_ui()

    def _init_service(self):
        self.get_shuttles_service: GetShuttlesUseCase = GetShuttlesService()
        self.import_shuttles_service: ImportShuttlesUseCase = ImportShuttlesService()
        self.export_shuttles_service: ExportShuttlesUseCase = ExportShuttlesService()
        self.create_shuttle_frame_service: CreateShuttleFrameUseCase = CreateShuttleFrameService()
        self.create_shuttle_widget_group_service: CreateShuttleWidgetGroupUseCase = CreateShuttleWidgetGroupService()
        self.create_log_text_service: CreateLogTextUseCase = CreateLogTextService()

    def _init_ui(self):
        self.title_vbox_layout = QVBoxLayout()
        self.shuttles_vbox_layout = QVBoxLayout()
        self.title_vbox_layout.addWidget(QLabel('셔틀 목록'))
        wrap_vbox_layout = QVBoxLayout()
        wrap_vbox_layout.addLayout(self.title_vbox_layout)
        wrap_vbox_layout.addLayout(self.shuttles_vbox_layout)
        stretch_vbox_layout = QVBoxLayout()
        stretch_vbox_layout.addStretch(4)
        wrap_vbox_layout.addLayout(stretch_vbox_layout)
        self.setLayout(wrap_vbox_layout)
        self.show()

    def add_shuttle(self, shuttle_widget_group: ShuttleWidgetGroup):
        shuttle_frame = self._add_shuttle_frame(shuttle_widget_group)
        self._add_shuttle_hbox_layout_to_vbox_layout("shuttles.json", shuttle_frame, shuttle_widget_group)
        self.shuttle_seq += 1
        self.save_shuttles(file_name="shuttles.json")

    def _add_shuttle_frame(self, shuttle_widget_group: ShuttleWidgetGroup):
        shuttle_frame = self._create_shuttle_frame(shuttle_widget_group)
        self.shuttle_frames[self.shuttle_seq] = shuttle_frame
        return shuttle_frame

    def _create_shuttle_frame(self, shuttle_widget_group):
        return self.create_shuttle_frame_service.create(shuttles=self.shuttles,
                                                        shuttle_seq=self.shuttle_seq,
                                                        chrome_driver=self.driver_chrome,
                                                        shuttle_widget_group=shuttle_widget_group,
                                                        shuttles_widget=self)

    def _add_shuttle_hbox_layout_to_vbox_layout(self, file_name, shuttle_frame, shuttle_widget_group):
        shuttle_hbox_layout = self._shuttle_hbox_layout(file_name, shuttle_frame, shuttle_widget_group)
        self.shuttles_vbox_layout.addLayout(shuttle_hbox_layout)

    def _shuttle_hbox_layout(self, file_name, shuttle_frame, shuttle_widget_group):
        shuttleLayout = QHBoxLayout()
        shuttleLayout.addWidget(shuttle_frame.get_frame())
        shuttleLayout.addWidget(self._delete_button(shuttle_frame=shuttle_frame.get_frame(),
                                                    shuttle_widget_group=shuttle_widget_group,
                                                    shuttle_seq=self.shuttle_seq, file_name=file_name))
        return shuttleLayout

    def _delete_button(self, shuttle_frame, shuttle_widget_group, shuttle_seq, file_name):
        delete_btn = QPushButton()
        delete_btn.setStyleSheet("background-color: rgba(255,255,255,0);")
        delete_btn.setIcon(QIcon('resource/images/remove-48.png'))
        delete_btn.setFixedWidth(30)
        delete_btn.setFixedHeight(30)
        delete_btn.clicked.connect(
            lambda: self._delete_shuttle(shuttle_frame, shuttle_widget_group, shuttle_seq, delete_btn, file_name))
        return delete_btn

    def _delete_shuttle(self, shuttle_frame: QFrame, shuttle_widget_group, shuttle_seq, delete_btn, file_name):
        reply = self._confirm(shuttle_widget_group.shuttle_name_widget)
        if reply == QMessageBox.No:
            return

        if self.shuttles.get(shuttle_seq) is not None:
            shuttle_widget_group.state_widget.append(self.create_log_text_service.stopped(shuttle_widget_group.text()))
            self.shuttles[shuttle_seq] = None

        shuttle_widget_group.state_widget.append(self.create_log_text_service.deleted(shuttle_widget_group.text()))
        shuttle_frame.deleteLater()
        delete_btn.deleteLater()
        self._delete_layout_and_frame(shuttle_seq)
        self.save_shuttles(file_name)

    def _delete_layout_and_frame(self, shuttle_seq):
        self.shuttles_vbox_layout.takeAt(shuttle_seq)
        self.shuttle_frames.pop(shuttle_seq)

    def _confirm(self, shuttle_name_widget):
        return QMessageBox.question(self, '삭제 확인', f'\'{shuttle_name_widget.text()}\' 셔틀이 삭제됩니다.',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def import_external_shuttles(self, state_widget: StateWidget):
        self.import_shuttles_service.import_external_shuttles(shuttles_widget=self, state_widget=state_widget)

    def save_shuttles(self, file_name="shuttles.json"):
        self.export_shuttles_service.save_shuttles_to_json(self.saved_shuttles_json(), file_name)

    def saved_shuttles_json(self):
        if self.shuttles_vbox_layout is None:
            return {}
        return self.get_shuttles_service.saved_shuttles_to_json(self.shuttle_frames)

