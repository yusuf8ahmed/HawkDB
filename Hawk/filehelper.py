import json
import mmap
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
        self.file_open = open(self.filepath, self.mode)
        self.file = mmap.mmap(self.file_open.fileno(), length=0, access=mmap.ACCESS_READ) 
        
        if not self.file:
            raise EmptyDatabaseError

        data = json.loads(self.file.read())

        if data["table"] == [] and self.empty_table == True:
            raise EmptyTableError
        return (data, self.file)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # self.file.close()
        self.file.flush()


def closedatabase(f, data):
    f.seek(0)
    f.write(json.dumps(data, indent=4))
    f.truncate()
