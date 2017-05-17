import json


class Storage:
    def get(self) -> list:
        raise NotImplementedError()

    def store(self, data: set):
        raise NotImplementedError()


class JSONFileStorage(Storage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                data = file.read()
                return json.loads(data)
        except FileNotFoundError:
            return []

    def store(self, data: list):
        with open(self.file_path, 'w+') as file:
            file.write(json.dumps(data))
