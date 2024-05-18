import logging

from collections.abc import Iterable

from persistent import Persistent
from ZODB.Connection import Connection

from citrine.exceptions import IncompatibleDatabaseError, ObjectOverwriteError
from citrine.storage.transaction import ThreadTransactionManager, autocommit


class ContainerConnectionMeta(Persistent):
    """
    Metadata objects for keeping track of the status of the container
    """

    @property
    def container(self):
        """
        The Container object at the heart of the database
        :return:
        """
        return self.obj.container

    @property
    def capacity(self):
        """
        The maximum writable size of the container
        """
        return self.container.capacity

    @property
    def used(self) -> float:
        """
        The number of items in the writable container
        :return:
        """
        return self.container.used

    @property
    def usage(self) -> float:
        """
        Percentage of the container's writable space that has been used
        """
        return self.container.usage

    @property
    def status(self) -> int:
        """
        Enumerated type giving a brief summary of how full the container is
        """
        return self.container.status

    @property
    def strict(self) -> bool:
        """
        Whether the ContainerConnection will enforce size limits with exceptions
        """
        return self.container.strict

    def __init__(self, obj):
        self.obj = obj


class ContainerConnectionProperties:

    # The actual purpose of this class is to make it easier to separate the
    # boilerplate property logic and docstrings from the actual functionality

    # should be overridden by instances of implementing class
    ___metadata___ = None
    ___root___ = None
    ___autocommit___ = None

    @property
    def container(self):
        """
        The Container object at the heart of the database
        :return:
        """
        return self.___root___.container

    @property
    def meta(self) -> ContainerConnectionMeta:
        """
        Quick reference to the metadata object
        :return:
        """
        return self.___metadata___

    @property
    def capacity(self):
        """
        The maximum size of the primary group
        """
        return self.meta.capacity

    @property
    def used(self) -> float:
        """
        The number of items in the primary group
        :return:
        """
        return self.meta.used

    @property
    def usage(self) -> float:
        """
        Percentage of the container's max_size that has been used
        """
        return self.meta.usage

    @property
    def status(self) -> int:
        """
        Enumerated type giving a brief summary of how full the container is
        """
        return self.meta.status

    @property
    def strict(self) -> bool:
        return self.container.strict

    @strict.setter
    def strict(self, value):
        if not isinstance(value, bool):
            raise TypeError("'strict' must be a boolean")
        self.container.strict = value

    @property
    def autocommit(self) -> bool:
        """
        Whether to automatically commit actions performed by ``create``,
        ``update``, and ``delete``
        """
        return self.___autocommit___

    @autocommit.setter
    def autocommit(self, value):
        if not isinstance(value, bool):
            raise TypeError("'autocommit' must be a boolean")
        self.___autocommit___ = value
        self.transaction_manager.autocommit = value


class ContainerConnection(Connection, ContainerConnectionProperties):
    """
    Expansion of ``ZODB.Connection`` that obscures the under-the-hood functions
    in favor of ``create``, ``read``, ``update``, and ``delete`` methods.
    """

    def __init__(self, db, cache_size=400, before=None, cache_size_bytes=0,
                 transaction_manager=None, autocommit=True):
        super().__init__(db=db, cache_size=cache_size, before=before,
                         cache_size_bytes=cache_size_bytes)
        self.___metadata___ = ContainerConnectionMeta(self)
        self.___autocommit___ = autocommit

        self.transaction_manager = (transaction_manager or
                                    ThreadTransactionManager())
        self.open(self.transaction_manager)

        self.___root___ = self.root

        if not getattr(self.root, 'container', None):
            raise IncompatibleDatabaseError(
                f'Cannot open {db.database_name} as a ContainerDb; database ' +
                f"lacks a Container object at 'root.container'"
            )

    @autocommit
    def create(self, id, obj):
        """
        Saves the provided object to the database at the provided id

        :param id: database identifier
        :param obj: the object to be stored
        """
        if not self.container.has(id):
            return self.container.write(id, obj)
        else:
            raise ObjectOverwriteError(id=id)

    def read(self, id, default=None):
        """
        Retrieves the object from the database at the provided id. If no object
        is found, default will be returned

        :param id: database identifier
        :param default: value to return if no object is found
        """
        return self.container.read(id, default)

    @autocommit
    def update(self, id, obj):
        """
        Updates the object at the provided id. If no object exists, one will
        be created

        :param id: database identifier
        :param obj: the new value to be stored at the id
        :return: previous value at that id, if applicable
        """
        previous = self.container.read(id, default=None)
        self.container.write(id, obj)
        return previous

    @autocommit
    def delete(self, id):
        """
        Removes the object at the provided id from the database. Will return
        the value at the id, if applicable

        :param id: database identifier
        :return: the object removed from the database, if applicable
        """
        return self.container.delete(id)

    def __getitem__(self, ids):
        """
        Shortcut for ``read`` that can return multiple entities

        :param ids: ids of the entities to be returned
        :return: list of objects found from the ids OR single object if only one
        id is provided
        """
        if isinstance(ids, str):
            if not self.container.has(ids):
                raise KeyError(f'{ids} not found')
            return self.container.read(ids)
        if not isinstance(ids, Iterable):
            raise IndexError(f'index selector must be string or iterable of ' +
                             f'strings, not {ids}')
        results = [self.container.read(id) for id in ids]
        if not any(results):
            raise KeyError(f'No values found for any of {ids}')
        return results

    def __enter__(self):
        """
        Creates a transaction block that will commit all actions at the end
        """

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ends the transaction block
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        """