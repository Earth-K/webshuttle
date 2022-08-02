import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QSpinBox

from webshuttle.adapter.incoming.ui import StateWidget
from webshuttle.adapter.incoming.ui.ShuttleDeleteButton import ShuttleDeleteButton
from webshuttle.adapter.outcoming.persistence.ShuttlePersistenceAdapter import ShuttlePersistenceAdapter
from webshuttle.application.CreateLogTextService import CreateLogTextService
from webshuttle.application.CreateShuttleFrameService import CreateShuttleFrameService
from webshuttle.application.ExportShuttlesService import ExportShuttlesService
from webshuttle.application.GetShuttlesService import GetShuttlesService
from webshuttle.application.ImportShuttlesService import ImportShuttlesService
from webshuttle.application.port.incoming import CreateShuttleFrameUseCase
from webshuttle.application.port.incoming.CreateLogTextUseCase import CreateLogTextUseCase
from webshuttle.application.port.incoming.ExportShuttlesCommand import ExportShuttlesCommand
from webshuttle.application.port.incoming.ExportShuttlesUseCase import ExportShuttlesUseCase
from webshuttle.application.port.incoming.GetShuttlesUseCase import GetShuttlesUseCase
from webshuttle.application.port.incoming.ImportShuttlesCommand import ImportShuttlesCommand
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
    def __init__(self, parent, chrome_driver, file_name="shuttles.json"):
        super(ShuttlesWidget, self).__init__(parent)
        self.shuttle_seq = 0
        self.shuttle_frames = {}
        self.shuttles = {}
        self.driver_chrome = chrome_driver
        self._init_service()
        self._init_ui()
        self.file_name = file_name

    def _init_service(self):
        self.get_shuttles_service: GetShuttlesUseCase = GetShuttlesService()
        self.import_shuttles_service: ImportShuttlesUseCase = ImportShuttlesService()
        self.export_shuttles_service: ExportShuttlesUseCase = ExportShuttlesService(ShuttlePersistenceAdapter())
        self.create_shuttle_frame_service: CreateShuttleFrameUseCase = CreateShuttleFrameService()
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
        self._add_shuttle_hbox_layout_to_vbox_layout(shuttle_frame, shuttle_widget_group)
        self.shuttle_seq += 1
        self.save_shuttles()

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

    def _add_shuttle_hbox_layout_to_vbox_layout(self, shuttle_frame, shuttle_widget_group):
        shuttle_hbox_layout = self._shuttle_hbox_layout(shuttle_frame, shuttle_widget_group)
        self.shuttles_vbox_layout.addLayout(shuttle_hbox_layout)

    def _shuttle_hbox_layout(self, shuttle_frame, shuttle_widget_group):
        shuttleLayout = QHBoxLayout()
        shuttleLayout.addWidget(shuttle_frame.get_frame_widget())
        delete_shuttle_button = ShuttleDeleteButton(self, shuttle_frame, shuttle_widget_group)
        shuttleLayout.addWidget(delete_shuttle_button.value())
        return shuttleLayout

    def import_external_shuttles(self, state_widget: StateWidget):
        import_shuttles_command = ImportShuttlesCommand(shuttles_widget=self, state_widget=state_widget)
        self.import_shuttles_service.import_external_shuttles(import_shuttles_command)

    def save_shuttles(self):
        export_shuttles_command = ExportShuttlesCommand(shuttle_properties_list=self.saved_shuttles_json(), file_name=self.file_name)
        self.export_shuttles_service.export(export_shuttles_command)

    def saved_shuttles_json(self):
        if self.shuttles_vbox_layout is None:
            return {}
        return self.get_shuttles_service.saved_shuttles_to_json(self.shuttle_frames)

