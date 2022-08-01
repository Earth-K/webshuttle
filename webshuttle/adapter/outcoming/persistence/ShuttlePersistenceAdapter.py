import json

from webshuttle.application.port.incoming.ExportShuttlesCommand import ExportShuttlesCommand
from webshuttle.application.port.outcoming.ShuttleRepository import ShuttleRepository


class ShuttlePersistenceAdapter(ShuttleRepository):
    def insert(self, export_shuttles_command: ExportShuttlesCommand):
        shuttles_json = {}
        for index in range(len(export_shuttles_command.shuttle_properties_list)):
            shuttle_id = f"shuttle{index}"
            shuttles_json[shuttle_id] = export_shuttles_command.shuttle_properties_list[shuttle_id]
        with open(export_shuttles_command.file_name, 'w', encoding="utf-8") as json_file:
            json_file.write(json.dumps(shuttles_json, ensure_ascii=False, indent=2))

