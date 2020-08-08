import json
import pathlib
from .errors import EmptyDatabaseError, EmptyTableError, JSONDecodingError


class opendatabase():
    def __init__(self, filepath, mode, empty_table=True):
        self.filepath = filepath
        self.filename = pathlib.Path(self.filepath).name
        self.mode = mode
        self.file = None
        self.empty_table = empty_table

    def __enter__(self):
        self.file = open(self.filepath, self.mode)
        if not self.file:
            raise EmptyDatabaseError

        data = json.loads(self.file.read())

        if data["table"] == [] and self.empty_table == True:
            raise EmptyTableError
        return (data, self.file)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()


def closedatabase(f, data):
    f.seek(0)
    f.write(json.dumps(data, indent=4))
    f.truncate()
