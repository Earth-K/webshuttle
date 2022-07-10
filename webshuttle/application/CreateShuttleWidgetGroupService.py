from webshuttle.application.port.incoming.CreateShuttleWidgetGroupUseCase import CreateShuttleWidgetGroupUseCase
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class CreateShuttleWidgetGroupService(CreateShuttleWidgetGroupUseCase):
    def __init__(self):
        pass

    def create_shuttle_widget_group(self, shuttle_name_widget, url_widget, target_classes_widget, period_widget,
                                    state_widget, parent=None):
        return ShuttleWidgetGroup(
            shuttle_name_widget=shuttle_name_widget,
            url_widget=url_widget,
            target_classes_widget=target_classes_widget,
            period_widget=period_widget,
            state_widget=state_widget,
            parent=None
        )
