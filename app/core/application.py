from .convertation import DataConverter
from .parsing import ApiParser, DataSource
from .storage import Storage
from ..tools.csv import CSV


class Application:
    def __init__(self, storage: Storage, api_parser: ApiParser):
        self._storage = storage
        self._api_parser = api_parser

    def grab_data(self, base_api_url: str, progress_callback: callable = None):
        data = []

        data_source = DataSource.make_from(base_api_url, self._api_parser)
        for url in data_source:
            chunk_of_data = self._api_parser.get_sessions(url)
            data += chunk_of_data

            if progress_callback is not None:
                progress_callback(
                    len(chunk_of_data) / data_source.total_elements)

        self._storage.store(data)

    def get_stored_data(self) -> list:
        return self._storage.get()

    def get_stored_data_as_csv_string(self, converter: DataConverter) -> str:
        csv = CSV(converter.get_header())
        for item in self.get_stored_data():
            csv.add_row(converter.convert_item(item))

        return str(csv)
