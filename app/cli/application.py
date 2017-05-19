import click

from .commands import generate_csv, grab_data, print_stored_data
from .helpers import put_application_instance_into_context
from ..core.application import Application
from ..core.parsing import ApiParser, RequestsHttpJsonClient
from ..core.storage import JSONFileStorage


class CLI:
    def __init__(self, default_storage_file_path: str):
        self._default_storage_file_path = default_storage_file_path

    def _make_cli_app(self):
        @click.group(help='ASCO Grabber command line interface')
        @click.option(
            '--storage-file',
            help='Where to store grabbed data, JSON file path. Default '
                 'value - storage.json in current directory.',
            type=click.Path(resolve_path=True),
            default=self._default_storage_file_path,
        )
        @click.pass_context
        def entrypoint(context, storage_file):
            put_application_instance_into_context(
                Application(
                    JSONFileStorage(storage_file),
                    ApiParser(RequestsHttpJsonClient())
                ),
                context,
            )

        entrypoint.add_command(grab_data)
        entrypoint.add_command(print_stored_data)
        entrypoint.add_command(generate_csv)

        return entrypoint

    def run(self):
        app = self._make_cli_app()
        app()
