import json

from PyQt5.QtWidgets import QSpinBox, QLineEdit

from webshuttle.application.port.incoming.ExportShuttlesCommand import ExportShuttlesCommand
from webshuttle.application.port.outcoming.ShuttleRepository import ShuttleRepository
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ShuttlePersistenceAdapter(ShuttleRepository):
    def export(self, export_shuttles_command: ExportShuttlesCommand):
        shuttles_json = {}
        for index in range(len(export_shuttles_command.shuttle_properties_list)):
            shuttle_id = f"shuttle{index}"
            shuttles_json[shuttle_id] = export_shuttles_command.shuttle_properties_list[shuttle_id]
        with open(export_shuttles_command.file_name, 'w', encoding="utf-8") as json_file:
            json_file.write(json.dumps(shuttles_json, ensure_ascii=False, indent=2))

    def load(self, shuttles_widget, state_widget) -> None:
        with open('shuttles.json', 'r', encoding="utf-8") as shuttles_file:
            shuttles: dict = json.load(shuttles_file)
        for index in range(len(shuttles.keys())):
            shuttle_attributes = shuttles[f'shuttle{index}']
            period_widget = QSpinBox()
            period_widget.setMaximum(86400)
            period_widget.setValue(int(shuttle_attributes["period"]))
            shuttles_widget.add_shuttle(
                ShuttleWidgetGroup(state_widget=state_widget.get_text_edit(),
                                   target_classes_widget=QLineEdit(shuttle_attributes["element_classes"]),
                                   period_widget=period_widget,
                                   url_widget=QLineEdit(shuttle_attributes["url"]),
                                   shuttle_name_widget=QLineEdit(shuttle_attributes["name"]),
                                   filtering_keyword_widget=QLineEdit(shuttle_attributes.get("filtering_keyword"))))