import requests


class ApiUrl:
    """Represents an API URL with paging parameters set on it.

    Attributes:
        MAX_ROWS_PER_PAGE (int): maximum rows per page. At the moment, the API
            simply ignores any values bigger than 6.

    """
    MAX_ROWS_PER_PAGE = 6

    def __init__(self, base_api_url: str, start_from: int = 0):
        self._base_api_url = base_api_url
        self._start_from = start_from
        self.rows_per_page = self.MAX_ROWS_PER_PAGE

    def __str__(self):
        params = '?rows={rows_per_page}&start={start_from}'.format(
            rows_per_page=self.rows_per_page,
            start_from=self._start_from
        )

        return self._base_api_url + params


class DataSource:
    @classmethod
    def make_from(cls, base_api_url: str):
        url = ApiUrl(base_api_url)
        total_elements = ApiParser.get_total_sessions_count(str(url))
        return cls(base_api_url, 0, total_elements)

    def __init__(
            self,
            base_api_url: str,
            current_position: int,
            total_elements: int
    ):
        self._base_api_url = base_api_url
        self._current_position = current_position
        self.total_elements = total_elements

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_position >= self.total_elements:
            raise StopIteration()

        url = ApiUrl(self._base_api_url, self._current_position)

        self._current_position += url.rows_per_page

        return str(url)


class ApiParser:
    FIELD_TOTAL_COUNT = 'Total'
    FIELD_SESSIONS_CONTAINER = 'Sessions'

    @classmethod
    def _get_json_from_url(cls, full_url: str) -> dict:
        response = requests.get(full_url)
        return response.json()

    @classmethod
    def get_sessions(cls, full_url: str) -> list:
        json_response = cls._get_json_from_url(full_url)
        return json_response[cls.FIELD_SESSIONS_CONTAINER]

    @classmethod
    def get_total_sessions_count(cls, full_url: str) -> int:
        json_response = cls._get_json_from_url(full_url)
        return json_response[cls.FIELD_TOTAL_COUNT]
