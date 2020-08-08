"""pydb.query holds the Field and Query Class

When running a query a in-memory version of the database 
is stored
"""
from .errors import InvalidQueryError, NoDbInQueryError
from .validate import validate
from .filehelper import opendatabase, closedatabase


class Field():
    def __init__(self, db_path, field):
        self.field = field
        self.db_path = db_path
        self.cached_bool = None
        self.cached = None

    def __eq__(self, other):
        """
        equality
        """
        result = []
        try:
            with opendatabase(self.db_path, "r+", empty_table=False) as (data, f):
                table = data["table"]
                for col in table:
                    if (self.field, other) in col.items():
                        result.append(col)
                closedatabase(f, data)
            return result
        except BaseException as e:
            raise InvalidQueryError("Insert Query Error: {}".format(e))

    def __ne__(self, other):
        """
        inequality.
        loop throught table and find ever 
        """
        validate(other, str, "where argument must be type dict")
        result = []
        try:
            with opendatabase(self.db_path, "r+", empty_table=False) as (data, f):
                table = data["table"]
                for col in table:
                    if (self.field, other) not in col.items():
                        result.append(col)
                closedatabase(f, data)
            return result
        except BaseException as e:
            raise InvalidQueryError("Insert Query Error: {}".format(e))

    def __and__(self, *other):
        return []

    def __or__(self, *other):
        return []

    def __rand__(self, *other):
        return []

    def __ror__(self, *other):
        return []


class Query:
    def __init__(self, db=None, QueryClass=Field):
        self.QueryClass = QueryClass
        self.db = db
        if self.db == None:
            raise NoDbInQueryError("No Db instance was passed to Query")

    def __getattr__(self, other):
        self.query_param = self.QueryClass(self.db.db_path, other)
        return self.query_param

    def __getitem__(self, other):
        return getattr(self, other)
