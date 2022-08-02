import json

from webshuttle.adapter.outcoming.persistence.ShuttlePersistenceAdapter import ShuttlePersistenceAdapter
from webshuttle.application.port.incoming.ExportShuttlesCommand import ExportShuttlesCommand
from webshuttle.application.port.incoming.ExportShuttlesUseCase import ExportShuttlesUseCase
from webshuttle.application.port.outcoming.ShuttleRepository import ShuttleRepository


class ExportShuttlesService(ExportShuttlesUseCase):

    def __init__(self):
        self.shuttlePersistenceAdapter: ShuttleRepository = ShuttlePersistenceAdapter()

    def export(self, export_shuttles_command: ExportShuttlesCommand):
        self.shuttlePersistenceAdapter.export(export_shuttles_command)
