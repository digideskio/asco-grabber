import click

from .helpers import extract_application_instance_from_context
from .views import CountOfItemsView, JSONView
from ..core import config
from ..core.convertation import V1DataConverter


@click.command(
    short_help='Fill the local storage with the data from the API.',
)
@click.option(
    '--base-api-url',
    default=config.base_api_url,
    help='Base URL of the API to grab the data from',
)
@click.pass_context
def grab_data(context, base_api_url: str):
    click.echo('Grabbing data from {url}'.format(url=base_api_url))

    with click.progressbar(length=1) as progressbar:
        application = extract_application_instance_from_context(context)
        application.grab_data(
            base_api_url,
            lambda fraction_done: progressbar.update(fraction_done),
        )

    click.echo('Done.')


@click.command(
    short_help='Display the data currently stored in local storage.',
)
@click.option(
    '--count-only',
    default=False,
    is_flag=True,
    help='If set, displays only count of elements and no data itself.',
)
@click.option(
    '--for-machines',
    default=False,
    is_flag=True,
    help='If set, displays only data - a number or a JSON string',
)
@click.pass_context
def print_stored_data(context, count_only: bool, for_machines: bool):
    application = extract_application_instance_from_context(context)
    data = application.get_stored_data()

    if count_only:
        result = CountOfItemsView(data)
    else:
        result = JSONView(data)

    click.echo(result.as_string(for_machines))


@click.command(
    short_help='Make a CSV string from the data that is currently stored in '
               'the local storage and echo it to the stdout.',
)
@click.option(
    '--as-file',
    help='If passed, will write the data to a file instead of stdout.',
    type=click.Path(resolve_path=True),
)
@click.pass_context
def generate_csv(context, as_file: str = None):
    application = extract_application_instance_from_context(context)
    csv_string = application.get_stored_data_as_csv_string(V1DataConverter())

    if as_file is None:
        click.echo(csv_string)
    else:
        with open(as_file, 'w+') as file:
            file.write(csv_string)

        click.echo('CSV has been written '
                   'to {file_path}'.format(file_path=as_file))
