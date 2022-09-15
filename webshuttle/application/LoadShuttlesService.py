from webshuttle.application.port.incoming.LoadShuttlesCommand import LoadShuttlesCommand
from webshuttle.application.port.incoming.LoadShuttlesUseCase import LoadShuttlesUseCase
from webshuttle.application.port.outcoming.ShuttleRepository import ShuttleRepository


class LoadShuttlesService(LoadShuttlesUseCase):
    def __init__(self, shuttle_repository: ShuttleRepository):
        self.shuttle_repository = shuttle_repository

    def load(self, shuttles_widget, state_widget) -> None:
        self.shuttle_repository.load(shuttles_widget=shuttles_widget, state_widget=state_widget)
