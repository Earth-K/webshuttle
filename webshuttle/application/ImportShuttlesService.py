import json

from PyQt5.QtWidgets import QLineEdit, QSpinBox

from webshuttle.application.port.incoming.ImportShuttlesCommand import ImportShuttlesCommand
from webshuttle.application.port.incoming.ImportShuttlesUseCase import ImportShuttlesUseCase
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ImportShuttlesService(ImportShuttlesUseCase):
    def import_external_shuttles(self, import_shuttles_command: ImportShuttlesCommand) -> None:
        with open('shuttles.json', 'r', encoding="utf-8") as shuttles_file:
            shuttles: dict = json.load(shuttles_file)
        for index in range(len(shuttles.keys())):
            shuttle_attributes = shuttles[f'shuttle{index}']
            period_widget = QSpinBox()
            period_widget.setMaximum(86400)
            period_widget.setValue(int(shuttle_attributes["period"]))
            import_shuttles_command.shuttles_widget.add_shuttle(
                ShuttleWidgetGroup(state_widget=import_shuttles_command.state_widget.get_text_edit(),
                                   target_classes_widget=QLineEdit(shuttle_attributes["element_classes"]),
                                   period_widget=period_widget,
                                   url_widget=QLineEdit(shuttle_attributes["url"]),
                                   shuttle_name_widget=QLineEdit(shuttle_attributes["name"]),
                                   filtering_keyword_widget=QLineEdit(shuttle_attributes.get("filtering_keyword"))))
