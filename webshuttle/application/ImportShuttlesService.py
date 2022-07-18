import json

from PyQt5.QtWidgets import QLineEdit, QSpinBox

from webshuttle.adapter.incoming.ui import ShuttlesWidget, StateWidget
from webshuttle.application.port.incoming.ImportShuttlesUseCase import ImportShuttlesUseCase
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class ImportShuttlesService(ImportShuttlesUseCase):
    def import_external_shuttles(self, shuttles_widget: ShuttlesWidget, state_widget: StateWidget) -> None:
        with open('shuttles.json', 'r', encoding="utf-8") as shuttles_file:
            shuttles: dict = json.load(shuttles_file)
        for index in range(len(shuttles.keys())):
            shuttle_attributes = shuttles[f'shuttle{index}']
            period_widget = QSpinBox()
            period_widget.setValue(86400)
            period_widget.setValue(int(shuttle_attributes["period"]))
            shuttles_widget.add_shuttle(ShuttleWidgetGroup(shuttle_name_widget=QLineEdit(shuttle_attributes["name"]),
                                                           url_widget=QLineEdit(shuttle_attributes["url"]),
                                                           period_widget=period_widget,
                                                           target_classes_widget=QLineEdit(shuttle_attributes["element_classes"]),
                                                           state_widget=state_widget.get_text_edit()))
