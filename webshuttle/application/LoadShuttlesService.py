from webshuttle.application.port.incoming.LoadShuttlesCommand import LoadShuttlesCommand
from webshuttle.application.port.incoming.LoadShuttlesUseCase import LoadShuttlesUseCase
from webshuttle.application.port.outcoming.ShuttleRepository import ShuttleRepository


class LoadShuttlesService(LoadShuttlesUseCase):
    def __init__(self, shuttle_repository: ShuttleRepository):
        self.shuttle_repository = shuttle_repository

    def load(self, load_shuttles_command: LoadShuttlesCommand) -> None:
        self.shuttle_repository.load(load_shuttles_command=load_shuttles_command)
