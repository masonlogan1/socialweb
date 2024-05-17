import logging

from persistent import Persistent
from ZODB.Connection import Connection

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

    @property
    def capacity(self):
        """
        The maximum writable size of the container
        """

    @property
    def used(self) -> float:
        """
        The number of items in the writable container
        :return:
        """

    @property
    def usage(self) -> float:
        """
        Percentage of the container's writable space that has been used
        """

    @property
    def status(self) -> int:
        """
        Enumerated type giving a brief summary of how full the container is
        """

    @property
    def strict(self) -> bool:
        """
        Whether the ContainerConnection will enforce size limits with exceptions
        """

    def __init__(self, obj):
        self.obj = obj


class ContainerConnectionProperties:

    # The actual purpose of this class is to make it easier to separate the
    # boilerplate property logic and docstrings from the actual functionality

    # should be overridden by instances of implementing class
    ___metadata___ = None
    ___root___ = None

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


class ContainerConnection(Connection, ContainerConnectionProperties):
    """
    Expansion of ``ZODB.Connection`` that obscures the under-the-hood functions
    in favor of ``create``, ``read``, ``update``, and ``delete`` methods.
    """

    def __init__(self, db, cache_size=400, before=None, cache_size_bytes=0,
                 transaction_manager=None, auto_transaction=True):
        super().__init__(db=db, cache_size=cache_size, before=before,
                         cache_size_bytes=cache_size_bytes)
        self.transaction_manager = (transaction_manager or
                                    ThreadTransactionManager())
        self.auto_transaction = auto_transaction
        self.open(self.transaction_manager)

        self.logger = getattr(self, 'logger', logging.getLogger(__name__))

    @autocommit
    def create(self, id, obj):
        """
        Saves the provided object to the database at the provided id

        :param id: database identifier
        :param obj: the object to be stored
        """

    def read(self, id, default=None):
        """
        Retrieves the object from the database at the provided id. If no object
        is found, default will be returned

        :param id: database identifier
        :param default: value to return if no object is found
        """

    @autocommit
    def update(self, id, obj):
        """
        Updates the object at the provided id. If no object exists, one will
        be created

        :param id: database identifier
        :param obj: the new value to be stored at the id
        :return: previous value at that id, if applicable
        """

    @autocommit
    def delete(self, id):
        """
        Removes the object at the provided id from the database. Will return
        the value at the id, if applicable

        :param id: database identifier
        :return: the object removed from the database, if applicable
        """

    def __getitem__(self, ids):
        """
        Shortcut for ``read`` that can return multiple entities

        :param ids: ids of the entities to be returned
        :return: list of objects found from the ids OR single object if only one
        id is provided
        """

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