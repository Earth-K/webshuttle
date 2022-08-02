import json

from webshuttle.adapter.outcoming.persistence.ShuttlePersistenceAdapter import ShuttlePersistenceAdapter
from webshuttle.application.ExportShuttlesService import ExportShuttlesService
from webshuttle.application.port.incoming.ExportShuttlesCommand import ExportShuttlesCommand

JSON_FILE_NAME = "shuttles_test.json"


def test_save_shuttles_to_json():
    export_shuttles_service = ExportShuttlesService(ShuttlePersistenceAdapter())
    shuttle_properties = {"shuttle0": {"name": "Shuttle Name", "url": "https://google.com", "period": "300", "element_classes": "Target Class Names"}}
    export_shuttles_command = ExportShuttlesCommand(shuttle_properties, JSON_FILE_NAME)
    export_shuttles_service.export(export_shuttles_command)

    with open(JSON_FILE_NAME, 'r', encoding="utf-8") as shuttles_file:
        shuttles = json.load(shuttles_file)
        assert str(shuttles) \
               == "{'shuttle0': {'name': 'Shuttle Name', 'url': 'https://google.com', 'period': '300', 'element_classes': 'Target Class Names'}}"
