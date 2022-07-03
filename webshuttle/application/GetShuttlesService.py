from webshuttle.application.port.incoming.GetShuttlesUseCase import GetShuttlesUseCase
from webshuttle.domain.ShuttleFrame import ShuttleFrame


class GetShuttlesService(GetShuttlesUseCase):
    def get_shuttles(self, shuttles_vbox_layout, shuttle_frames):
        if shuttles_vbox_layout is None:
            return {}
        result = {}
        for i in shuttle_frames:
            frame: ShuttleFrame = shuttle_frames[i]
            shuttle_id = "shuttle" + str(i)
            shuttle_property = {"name": frame.shuttleWidgets.shuttle_name_widget.text(),
                                "url": frame.shuttleWidgets.url_widget.text(),
                                "period": frame.shuttleWidgets.period_widget.text(),
                                "element_classes": frame.shuttleWidgets.target_classes_widget.text()}
            result[shuttle_id] = shuttle_property
        return result
