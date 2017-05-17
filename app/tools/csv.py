import csv
import io


class CSV:
    def __init__(self, field_names: list, render_header: bool = True):
        self._field_names = field_names
        self._render_header = render_header
        self._rows = []

    def add_row(self, row: dict):
        if set(row) != set(self._field_names):
            raise ValueError("Given row doesn't match the schema of this CSV.")

        self._rows.append(row)

    def __str__(self):
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, self._field_names)

        if self._render_header:
            writer.writeheader()

        writer.writerows(self._rows)

        return buffer.getvalue()
