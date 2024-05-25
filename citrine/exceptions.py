"""
Exceptions for Citrine classes
"""


class CitrineIncompatibleMethodError(Exception):
    """
    Raised when a ZODB method has to be disabled because of incompatibilities
    with necessary methods and functions of Citrine
    """

    def __init__(self, method_name):
        msg = f'Method "{method_name}" is disabled by Citrine'
        super().__init__(msg)

    @staticmethod
    def override_method(fn):
        """
        Decorate a method with this and it'll automatically raise when called
        """

        def decorator(*args, **kwargs):
            raise CitrineIncompatibleMethodError(fn.__name__)

        return decorator


class CitrineDuplicateIdError(Exception):
    """
    Exception thrown when attempting to read from multiple databases and
    multiple results are returned for the same ID.
    """

    def __init__(self, id, dbs=None):
        msg = f'ID "{id}" found in multiple databases'
        if dbs:
            msg += f'; {", ".join(db.database_name for db in dbs)}'
        super().__init__(msg)


class IncompatibleDatabaseError(Exception):
    """
    Exception thrown when a connection object dependent on some kind of
    managed storage is given a database that is incompatible with the needs
    of the connection
    """


class ObjectOverwriteError(Exception):
    """
    Exception thrown when a write action in a database will overwrite an
    existing object
    """

    def __init__(self, id):
        msg = f"Overwrite not permitted for '{id}'"
        super().__init__(msg)


class CrystalAttributeCollisionError(Exception):
    """
    Exception thrown when one or more attributes are requested during
    decrystallization but those attributes will conflict with template class
    """

    def __init__(self, id=None, class_name=None, attributes=None):
        msg = ("Cannot load crystal" +
               f" '{id}'" if id else ""
               f" as '{class_name}', " if class_name else ""
               ", conflicting attributes"
               f": '{', '.join(attributes)}'") if attributes else ""
        super().__init__(msg)
