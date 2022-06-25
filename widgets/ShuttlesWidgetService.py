import json


class ShuttlesWidgetService:

    def __init__(self):
        pass

    def save_shuttles_to_json(self, shuttle_properties_list, file_name="shuttles.json"):
        shuttles_json = {}
        for index, shuttle_properties in enumerate(shuttle_properties_list):
            shuttles_json[f"shuttle{index}"] = shuttle_properties
        with open(file_name, 'w', encoding="utf-8") as json_file:
            json_file.write(json.dumps(shuttles_json, ensure_ascii=False, indent=2))
