
class EmptyDatabaseError(Exception):
    """Exception raised when database is empty 
    """

    def __init__(self, message="Database file is empty"):
        self.message = message
        super().__init__(self.message)


class EmptyTableError(Exception):
    """Exception raised when database table is empty 
    """

    def __init__(self, message="Table is empty"):
        self.message = message
        super().__init__(self.message)


class InvalidQueryError(Exception):
    """Exception raised when query is invalid 
    """

    def __init__(self, message):
        self.message = message
        super().__init__("InvalidQuery: {}".format(self.message))


class ValidationError(Exception):
    """Exception raised when parameter validation issue occurs
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NoDbInQueryError(Exception):
    """Exception raised when no db instance is pass to Query class
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class JSONDecodingError(Exception):
    '''Raise when a specific subset of values in context of app is wrong'''

    def __init__(self, dbname, msg, pos, lineno, colno):
        self.message = """
        Error in Database {0} at line {3} col {4}.
        To fix this issue please check the database for matching square 
        and curly brackets [], {{}} and for incorrectly placed commas ,
        """.format(dbname, msg, chr(pos), lineno, colno).rstrip()
        super().__init__(self.message)
