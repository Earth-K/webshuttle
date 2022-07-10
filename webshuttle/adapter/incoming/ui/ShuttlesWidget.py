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
    def __init__(self, parent, chrome_service):
        super(ShuttlesWidget, self).__init__(parent)
        self.shuttle_seq = 0
        self.shuttle_frames = {}
        self.shuttles = {}
        self.chrome_service = chrome_service
        self.get_shuttles_service: GetShuttlesUseCase = GetShuttlesService()
        self.import_shuttles_service: ImportShuttlesUseCase = ImportShuttlesService()
        self.export_shuttles_service: ExportShuttlesUseCase = ExportShuttlesService()
        self.create_shuttle_frame_service: CreateShuttleFrameUseCase = CreateShuttleFrameService()
        self.create_shuttle_widget_group_service: CreateShuttleWidgetGroupUseCase = CreateShuttleWidgetGroupService()
        self.create_log_text_service: CreateLogTextUseCase = CreateLogTextService()
        self._init_ui()

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

    def add_shuttle(self, url, period, target_classes, name, state_widget, file_name="shuttles.json"):
        shuttle_name_widget = shuttle_name_lineedit(name)
        target_classes_widget = target_classes_lineedit(target_classes)
        url_widget = url_lineedit(url)
        period_widget = period_spinbox(period)

        shuttle_widget_group = self.create_shuttle_widget_group_service.create_shuttle_widget_group(
            shuttle_name_widget=shuttle_name_widget, url_widget=url_widget, target_classes_widget=target_classes_widget,
            period_widget=period_widget, state_widget=state_widget, parent=None)
        shuttle_frame = self.create_shuttle_frame_service.create_shuttle_frame(shuttles=self.shuttles,
                                                                               shuttle_seq=self.shuttle_seq,
                                                                               chrome_service=self.chrome_service,
                                                                               shuttle_widget_group=shuttle_widget_group,
                                                                               shuttles_widget=self)

        self.shuttle_frames[self.shuttle_seq] = shuttle_frame
        shuttleLayout = QHBoxLayout()
        shuttleLayout.addWidget(shuttle_frame.get_frame())
        shuttleLayout.addWidget(
            self._delete_button(shuttle_frame=shuttle_frame.get_frame(), shuttle_name_widget=shuttle_name_widget,
                                log_edittext_widget=state_widget, shuttle_seq=self.shuttle_seq,
                                file_name=file_name))
        self.shuttles_vbox_layout.addLayout(shuttleLayout)
        self.shuttle_seq += 1
        self.save_shuttles(file_name=file_name)

    def import_external_shuttles(self, state_widget: StateWidget):
        self.import_shuttles_service.import_external_shuttles(shuttles_widget=self, state_widget=state_widget)

    def save_shuttles(self, file_name="shuttles.json"):
        self.export_shuttles_service.save_shuttles_to_json(self.saved_shuttles_json(), file_name)

    def saved_shuttles_json(self):
        if self.shuttles_vbox_layout is None:
            return {}
        return self.get_shuttles_service.saved_shuttles_to_json(self.shuttle_frames)

    def _delete_button(self, shuttle_frame, shuttle_name_widget, log_edittext_widget, shuttle_seq, file_name):
        delete_btn = QPushButton()
        delete_btn.setStyleSheet("background-color: rgba(255,255,255,0);")
        delete_btn.setIcon(QIcon('resource/images/remove-48.png'))
        delete_btn.setFixedWidth(30)
        delete_btn.setFixedHeight(30)
        delete_btn.clicked.connect(
            lambda: self._remove_shuttle(shuttle_frame, shuttle_name_widget, log_edittext_widget, shuttle_seq,
                                         delete_btn, file_name))
        return delete_btn

    def _remove_shuttle(self, shuttle_frame: QFrame, shuttle_name_widget, log_edittext_widget, shuttle_seq, delete_btn,
                        file_name):
        reply = self._confirm(shuttle_name_widget)
        if reply == QMessageBox.No:
            return

        if self.shuttles.get(shuttle_seq) is not None:
            log_edittext_widget.append(self.create_log_text_service.stopped(shuttle_name_widget.text()))
            self.shuttles[shuttle_seq] = None

        log_edittext_widget.append(self.create_log_text_service.removed(shuttle_name_widget.text()))
        shuttle_frame.deleteLater()
        delete_btn.deleteLater()
        self.shuttles_vbox_layout.takeAt(shuttle_seq)
        self.shuttle_frames.pop(shuttle_seq)
        self.save_shuttles(file_name)

    def _confirm(self, shuttle_name_widget):
        return QMessageBox.question(self, '삭제 확인', f'\'{shuttle_name_widget.text()}\' 셔틀이 삭제됩니다.',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
