from webshuttle.application.port.incoming.ExportShuttlesCommand import ExportShuttlesCommand
from webshuttle.application.port.incoming.ExportShuttlesUseCase import ExportShuttlesUseCase
from webshuttle.application.port.outcoming.ShuttleRepository import ShuttleRepository


class ExportShuttlesService(ExportShuttlesUseCase):

    def __init__(self, shuttle_repository: ShuttleRepository):
        self.shuttle_repository: ShuttleRepository = shuttle_repository

    def export(self, export_shuttles_command: ExportShuttlesCommand):
        self.shuttle_repository.export(export_shuttles_command)
