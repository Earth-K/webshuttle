from webshuttle.application.port.incoming.GetShuttlesUseCase import GetShuttlesUseCase
from webshuttle.adapter.incoming.ui.widget.shuttle.ShuttleFrame import ShuttleFrame


class GetShuttlesService(GetShuttlesUseCase):
    def saved_shuttles_to_json(self, shuttle_frames):
        result = {}
        for index, shuttle_seq in enumerate(shuttle_frames):
            frame: ShuttleFrame = shuttle_frames[shuttle_seq]
            new_shuttle_id = "shuttle" + str(index)
            shuttle_property = {"name": frame.shuttleWidgets.shuttle_name_widget.text(),
                                "url": frame.shuttleWidgets.url_widget.text(),
                                "period": frame.shuttleWidgets.period_widget.text(),
                                "element_classes": frame.shuttleWidgets.target_classes_widget.text(),
                                "filtering_keyword": frame.shuttleWidgets.filtering_keyword_widget.text()}
            result[new_shuttle_id] = shuttle_property
        return result
