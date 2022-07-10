from webshuttle.application.port.incoming.CreateShuttleFrameUseCase import CreateShuttleFrameUseCase
from webshuttle.domain.ShuttleFrame import ShuttleFrame


class CreateShuttleFrameService(CreateShuttleFrameUseCase):
    def __init__(self):
        pass

    def create_shuttle_frame(self, shuttles, shuttle_seq, chrome_service, shuttle_widget_group, shuttles_widget) -> ShuttleFrame:
        return ShuttleFrame(shuttles=shuttles, shuttle_seq=shuttle_seq, chrome_service=chrome_service,
                            shuttle_widget_group=shuttle_widget_group, shuttles_widget=shuttles_widget)
