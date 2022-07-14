from webshuttle.application.port.incoming.CreateShuttleFrameUseCase import CreateShuttleFrameUseCase
from webshuttle.domain.ShuttleFrame import ShuttleFrame


class CreateShuttleFrameService(CreateShuttleFrameUseCase):
    def __init__(self):
        pass

    def create(self, shuttles, shuttle_seq, chrome_driver, shuttle_widget_group, shuttles_widget) -> ShuttleFrame:
        return ShuttleFrame(shuttles=shuttles, shuttle_seq=shuttle_seq, chrome_driver=chrome_driver,
                            shuttle_widget_group=shuttle_widget_group, shuttles_widget=shuttles_widget)
