"""
Classes and functions for managing a group of CitrineConnections under a single
object
"""
from datetime import timedelta

from citrine.citrinedb import CitrineDB
from citrine.connection.connection import CitrineConnection


class GroupReadConnection:
    """
    Takes a number of CitrineDB objects and provides functionality to read from
    all of them in a single operation.

    USES ASYNCHRONOUS FUNCTIONALITY.
    """
    def __init__(self, dbs: tuple[CitrineDB]|list[CitrineDB]|set[CitrineDB],
                 transaction_manager=None, **connection_args):
        """
        :param dbs: A list, set, or tuple of CitrineDB objects to connect to
        :param transaction_manager: shared transaction manager for group
        :param connection_args: dbname-connection args dict overriding defaults
        """
        self.connections = tuple()
        default = {'transaction_manager': transaction_manager}
        for db in dbs:
            connection_details = connection_args.get(db.database_name, default)
            self.connections += db.open(**connection_details)

    def read(self, id: str, timeout: timedelta = None, multiple: bool = False):
        """
        Reads from all connections and returns the located value.
        """

    async def __read(self, id: str):
        """
        Reads from a single connection asynchronously
        """