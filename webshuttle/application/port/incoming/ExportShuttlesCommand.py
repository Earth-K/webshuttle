class ExportShuttlesCommand:
    def __init__(self, shuttle_properties_list, file_name="shuttles.json"):
        self.shuttle_properties_list = shuttle_properties_list
        self.file_name = file_name

        if shuttle_properties_list is None or type(shuttle_properties_list) is not dict:
            raise ValueError
        if file_name is None or type(file_name) is not str:
            raise ValueError
