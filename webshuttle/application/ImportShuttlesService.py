import json

from webshuttle.adapter.incoming.ui import ShuttlesWidget, StateWidget
from webshuttle.application.port.incoming.ImportShuttlesUseCase import ImportShuttlesUseCase


class ImportShuttlesService(ImportShuttlesUseCase):
    def import_external_shuttles(self, shuttles_widget: ShuttlesWidget, state_widget: StateWidget) -> None:
        with open('shuttles.json', 'r', encoding="utf-8") as shuttles_file:
            shuttles: dict = json.load(shuttles_file)
        for index in range(len(shuttles.keys())):
            shuttle_attributes = shuttles[f'shuttle{index}']
            shuttles_widget.add_shuttle(name=shuttle_attributes["name"],
                                        url=shuttle_attributes["url"],
                                        period=shuttle_attributes["period"],
                                        target_classes=shuttle_attributes["element_classes"],
                                        state_widget=state_widget.get_edittext(),
                                        file_name="shuttles.json")
