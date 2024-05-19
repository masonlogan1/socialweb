"""
Classes and functions for managing a group of CitrineConnections under a single
object
"""
from asyncio import timeout as aiotimeout
from asyncio import run as aiorun
from asyncio import TaskGroup
from datetime import timedelta

from citrine.exceptions import CitrineDuplicateIdError


class GroupReadConnection:
    """
    Takes a number of CitrineDB objects and provides functionality to read from
    all of them in a single operation.

    USES ASYNCHRONOUS FUNCTIONALITY.
    """
    def __init__(self, dbs,
                 transaction_manager=None, **connection_args):
        """
        :param dbs: A list, set, or tuple of CitrineDB objects to connect to
        :param transaction_manager: shared transaction manager for group
        :param connection_args: dbname-connection args dict overriding defaults
        """
        self.connections = tuple()
        default = {'transaction_manager': transaction_manager}
        for db in dbs:
            connection_details = {
                **connection_args.get(db.database_name, default),
                **default
            }
            self.connections += (db.open(**connection_details),)

    def read(self, id: str, timeout: timedelta = None, multiple: bool = False):
        """
        Reads from all connections and returns the located value(s).
        """
        results = aiorun(self.__read(id=id, timeout=timeout, multiple=multiple))
        if not results:
            return None
        if len(results) > 1 and not multiple:
            CitrineDuplicateIdError(id)
        return results[0] if not multiple else results

    async def __read(self, id: str, timeout: timedelta = None,
                     multiple: bool = None):
        """
        Reads from all connections and returns all located values.
        """
        if timeout:
            with aiotimeout(timeout.seconds):
                with TaskGroup() as tg:
                    # if we're getting multiple back, it's good to give a link
                    # back to the relevant db
                    if multiple:
                        results = {
                            connection: tg.create_task(self.__read_db(connection, id))
                            for connection in self.connections
                        }
                    else:
                        results = [
                            tg.create_task(self.__read_db(connection, id))
                            for connection in self.connections
                        ]
        else:
            async with TaskGroup() as tg:
                if multiple:
                    results = {
                        connection: tg.create_task(self.__read_db(connection, id))
                        for connection in self.connections
                    }
                else:
                    results = [
                        tg.create_task(self.__read_db(connection, id))
                        for connection in self.connections
                    ]
        if not multiple:
            results = [res.result() for res in results
                       if res.result() is not None]
        else:
            results = {key: val.results() for key, val in results.items()
                       if val.results() is not None}
        return results

    async def __read_db(self, connection, id: str):
        """
        Reads from a single connection asynchronously
        """
        return connection.read(id)
