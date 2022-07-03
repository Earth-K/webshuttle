import json

from webshuttle.application.ExportShuttlesService import ExportShuttlesService

JSON_FILE_NAME = "shuttles_test.json"


def test_save_shuttles_to_json():
    shuttles_widget_service = ExportShuttlesService()
    shuttle_properties = {"shuttle0": {"name": "Shuttle Name", "url": "https://google.com", "period": "300", "element_classes": "Target Class Names"}}
    shuttles_widget_service.save_shuttles_to_json(shuttle_properties, JSON_FILE_NAME)

    with open(JSON_FILE_NAME, 'r', encoding="utf-8") as shuttles_file:
        shuttles = json.load(shuttles_file)
        assert str(shuttles) \
               == "{'shuttle0': {'name': 'Shuttle Name', 'url': 'https://google.com', 'period': '300', 'element_classes': 'Target Class Names'}}"
