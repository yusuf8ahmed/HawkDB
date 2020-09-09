import json
import pathlib
import logging
import random
import webbrowser

from typing import Any, Callable, List, Dict, Tuple
from .sample import sample_database
from .errors import EmptyDatabaseError, InvalidQueryError
from .validate import validate
from .filehelper import opendatabase, closedatabase
from .query import Query

class Pydb:
    def __init__(self, connection="pydb", tablename="pydb"):
        """
        create new database in current directory
        if connection isnt found then new database
        is created
        """
        self.cached_bool = False
        self.cached = None
        self.filter_bool = False
        self.filter_cache = None
        self.connection = connection
        validate(self.connection, str,
                 "connection argument must be type str not {}".format(type(connection)))
        if ".json" not in self.connection:
            self.connection = self.connection + ".json"
        file = pathlib.Path(self.connection)
        if not file.is_file():
            print("Couldn't find database making a new")
            pathlib.Path("{}".format(self.connection)).touch()
            self.db_path = pathlib.Path(self.connection).resolve()
            with open(self.db_path, "w") as f:
                f.truncate(0)
                sample_database["tablename"] = tablename
                f.write(json.dumps(sample_database, indent=4))
        self.db_path = pathlib.Path(self.connection).resolve()
        logfile = file.parent / "db.log"
        logging.basicConfig(
            filename=str(logfile),
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # query result retrievers

    def all(self):
        logging.debug("Getting all results")
        self.cached_bool = True
        result = self.cached
        if not result == None:
            return result
        else:
            return self.selectall()

    def limit(self, num):
        """limit number of results

        Args:
            num (int): number to limit too

        Returns:
            List[Dict[str, Any]]: return result
        """
        logging.debug("limit all results to {}".format(num))
        table = self.all()
        return table[0:num]

    def asc(self):
        """
        ORDER BY ASC
        """
        logging.debug("all results asc")
        return self.all()

    def desc(self):
        """
        ORDER BY DESC
        """
        logging.debug("all results desc")
        return self.all()[::-1]

    # query operators
    def and_(*args):
        logging.debug("not implemented")
        raise NotImplementedError()

    def or_(*args):
        logging.debug("not implemented")
        raise NotImplementedError()

    def not_(other):
        logging.debug("not implemented")
        raise NotImplementedError()

    def length(self):
        """get number of columns in database

        Raises:
            InvalidQueryError: [description]

        Returns:
            List[Dict[str, Any]]: return result
        """
        logging.debug("Getting total length of database")
        try:
            with opendatabase(self.db_path, "r+", empty_table=False) as (data, f):
                table = data["table"]
                result = len(table)
                closedatabase(f, data)
            return result
        except BaseException as e:
            raise InvalidQueryError("Insert Query Error: {}".format(e))

    # Most common commands
    def insert(self, *new):
        """insert a column into database
        tuple(dict) -> json -> into file

        Raises:
            InvalidQueryError: [description]

        Returns:
            str: "OK"
        """

        validate(new, tuple, "new argument must be type dict")
        logging.debug("insert: {}".format(*new))
        try:
            with opendatabase(self.db_path, "r+", empty_table=False) as (data, f):
                table = data["table"]
                colid = 0
                for col in new:
                    col["__colid"] = random.randint(10**5, 10**10)
                    table.append(col)
                    colid += 1
                closedatabase(f, data)
            return "OK"
        except BaseException as e:
            raise InvalidQueryError("Insert Query Error: {}".format(e))

    def update(self, set_, where):
        """update specific column/s in database
        SQL equivalent:
            UPDATE **TABLENAME** SET column1 = value1, ... WHERE column1 = value1;
        Args:
            set (dict): the key/s and value/s you want to change
            where (dict): the identifying key, value pair
        Raises:
            EmptyDatabaseError: [description]
            InvalidQueryError: [description]
        Returns:
            str: str: "OK"
        """
        validate(set_, dict, "change argument must be type dict")
        validate(where, dict, "where argument must be type dict")
        logging.debug("set: {} where: {}".format(set_, where))
        try:
            with opendatabase(self.db_path, "r+") as (data, f):
                table = data["table"]
                for col in table:
                    if where.items() <= col.items():
                        for key, value in set_.items():
                            col[key] = value
                closedatabase(f, data)
            return "OK"
        except BaseException as e:
            raise InvalidQueryError("UPDATE Query Error: {}".format(e))

    # -result causing commands
    def select(self, where):
        """select specific column/s in database
        #result causing
        SQL equivalent:
            SELECT column, ... FROM **TABLENAME**
        Args:
            where (list): the identifying key, value pair
        Raises:
            EmptyDatabaseError: [description]
            InvalidQueryError: [description]
        Returns:
            List[Dict[str, Any]]: [description]
        """

        validate(where, list, "where argument must be type dict")
        result = []
        logging.debug("where: {}".format(where))
        try:
            with opendatabase(self.db_path, "r+", empty_table=False) as (data, f):
                table = data["table"]
                for col in table:
                    for keys in where:
                        if keys in col.keys():
                            result.append(col)
                # self.cached = lambda self: self.select(where)
                self.cached = result
                closedatabase(f, data)
            if self.cached_bool == True:
                return table
            else:
                return self
        except BaseException as e:
            raise InvalidQueryError("Insert Query Error: {}".format(e))

    def selectall(self):
        """query all data
        #result causing
        SQL equivalent
            SELECT * FROM **TABLENAME**
        Raises:
            EmptyDatabaseError: [description]
            InvalidQueryError: [description]
        Returns:
            List[Dict[str, Any]] : all data within database
        """
        logging.debug("selectall")
        try:
            with opendatabase(self.db_path, "r+") as (data, f):
                # self.cached = lambda self: self.selectall()
                table = data["table"]
                self.cached = table
                closedatabase(f, data)
            if self.cached_bool == True:
                return table
            else:
                return self
        except BaseException as e:
            raise InvalidQueryError("SELECT ALL Query Error: {}".format(e))

    # -irreversible
    def truncate(self):
        """truncate whole table
        #CANNOT BE UNDONE
        SQL equivalent
            : TRUNCATE TABLE **TABLENAME**;
        Raises:
            EmptyDatabaseError: [description]
            InvalidQueryError: [description]
        """
        try:
            logging.warning("Delete whole database")
            with opendatabase(self.db_path, "r+") as (data, f):
                data["table"] = []
                closedatabase(f, data)
            return "OK"
        except BaseException as e:
            raise InvalidQueryError("DELETE ALL Query Error: {}".format(e))

    def delete(self, where):
        """delete whole database or specific column/s
        # CANNOT BE UNDONE
        SQL equivalent
            : DELETE FROM **TABLENAME** WHERE name='Yusuf'; 
        Args:
            where (dict): the identifying key, value pair to delete
        Raises:
            EmptyDatabaseError: [description]
            InvalidQueryError: [description]
        """
        validate(where, dict, "where argument must be type dict or None")
        logging.debug("where: {}".format(where))
        try:
            with opendatabase(self.db_path, "r+") as (data, f):
                for col in data["table"]:
                    if where.items() <= col.items():
                        data["table"].remove(col)
                closedatabase(f, data)
            return "OK"
        except BaseException as e:
            raise InvalidQueryError("DELETE Query Error: {}".format(e))

    def trivago(self):
        logging.debug("Got Rick Rolled")
        webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # Custom Queries
    def release(self):
        """release will return the whole table where 
        you can do custom queries
        """
        logging.debug("releasing whole database")
        try:
            with opendatabase(self.db_path, "r+") as (data, f):
                closedatabase(f, data)
                return data["table"]
        except BaseException as e:
            raise InvalidQueryError("SELECT ALL Query Error: {}".format(e))

    def push(self, table):
        validate(table, list, "table argument must be type list")
        logging.debug("pushing/updating whole database")
        try:
            with opendatabase(self.db_path, "r+") as (data, f):
                data["table"] = []
                data["table"] = table
                closedatabase(f, data)
            return "OK"
        except BaseException as e:
            raise InvalidQueryError("DELETE Query Error: {}".format(e))

    def filter(self, query):
        """
        #cache
        query data for dict:
        filter can do and accept:
        :critical
        = filter(User.name == 'ed')
        = filter(User.name != 'ed')
        = filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
        = filter(or_(User.name == 'ed', User.name == 'wendy'))

        - filter(User.name.like('%ed%'))
        - filter(User.name.ilike('%ed%'))
        - filter(User.name.in_(['ed', 'wendy', 'jack']))
        - filter(User.name.notin_(['ed', 'wendy', 'jack']))
        - filter(User.name.match('wendy'))
        - <
        - <=
        - >
        - >=
        """
        self.cached = query
        if self.cached_bool == True:
            return query
        else:
            return self
