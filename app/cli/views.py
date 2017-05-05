import json


class DataView:
    def __init__(self, data):
        self._data = data

    def as_string(self, for_machines: bool) -> str:
        if for_machines:
            return self._for_machines(self._data)
        else:
            return self._for_humans(self._data)

    @staticmethod
    def _for_machines(data) -> str:
        raise NotImplementedError()

    @staticmethod
    def _for_humans(data) -> str:
        raise NotImplementedError()


class CountOfItemsView(DataView):
    @staticmethod
    def _for_machines(data) -> str:
        return len(data)

    @staticmethod
    def _for_humans(data) -> str:
        return 'Count of items: {}'.format(len(data))


class JSONView(DataView):
    @staticmethod
    def _for_humans(data) -> str:
        return json.dumps(data, indent=4)

    @staticmethod
    def _for_machines(data) -> str:
        return json.dumps(data)
