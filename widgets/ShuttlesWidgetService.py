import json


class ShuttlesWidgetService:

    def __init__(self):
        pass

    def save_shuttles_to_json(self, shuttle_properties_list, file_name="shuttles.json"):
        shuttles_json = {}
        for index in range(len(shuttle_properties_list)):
            shuttle_id = f"shuttle{index}"
            shuttles_json[shuttle_id] = shuttle_properties_list[shuttle_id]
        with open(file_name, 'w', encoding="utf-8") as json_file:
            json_file.write(json.dumps(shuttles_json, ensure_ascii=False, indent=2))
