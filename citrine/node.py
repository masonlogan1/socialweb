"""
Common classes and utilities used by the Citrine database
"""
import logging

from transaction import TransactionManager
from ZODB import DB
from ZODB.Connection import Connection
from ZODB.FileStorage import FileStorage
from persistent import Persistent
from persistent.mapping import PersistentMapping


class ConnectionProfile(Persistent):
    """
    Reusable object for storing object database connection information
    """

    # Can be persisted into the exact type of databases it is intended to
    # store info on!

    def __init__(self, storage, pool_size=7, pool_timeout=2147483648,
                 cache_size=400, cache_size_bytes=0, historical_pool_size=3,
                 historical_cache_size=1000, historical_cache_size_bytes=0,
                 historical_timeout=300, database_name='unnamed',
                 xrefs=True, large_record_size=16777216):
        self.storage = storage
        self.pool_size = pool_size
        self.pool_timeout = pool_timeout
        self.cache_size = cache_size
        self.cache_size_bytes = cache_size_bytes
        self.historical_pool_size = historical_pool_size
        self.historical_cache_size = historical_cache_size
        self.historical_cache_size_bytes = historical_cache_size_bytes
        self.historical_timeout = historical_timeout
        self.database_name = database_name
        self.xrefs = xrefs
        self.large_record_size = large_record_size

    def to_dict(self, exclude_none=False):
        data = {'storage': self.storage, 'pool_size': self.pool_size,
                'pool_timeout': self.pool_timeout,
                'cache_size': self.cache_size,
                'cache_size_bytes': self.cache_size_bytes,
                'historical_pool_size': self.historical_pool_size,
                'historical_cache_size': self.historical_cache_size,
                'historical_cache_size_bytes': self.historical_cache_size_bytes,
                'historical_timeout': self.historical_timeout,
                'database_name': self.database_name,
                'xrefs': self.xrefs,
                'large_record_size': self.large_record_size}

        return data if not exclude_none else {k: v for k, v in data.items()
                                              if v is not None}


class DbMetadata(Persistent):
    """
    Object used by a CitrineConnection as a form of metadata on the contents of
    the database
    """
    def __init__(self, size=None, cache=None):
        super().__init__()
        self.size = size
        self.cache = cache


class DbContainer(Persistent):
    """
    Object used to manage a collection of PersistentMapping objects within
    an object database. Uses the hash value of the object to determine which
    container it should be kept in.
    """
    @property
    def containers_size(self):
        return len(self.containers.keys())

    def __init__(self, containers: dict|PersistentMapping = None):
        super().__init__()
        # Containers will be stored as a PM of PMs
        self.containers = containers if containers is not None else \
            PersistentMapping({0: PersistentMapping()})

    def expand_size(self, new_size: int):
        if new_size <= self.containers_size:
            raise ValueError(f'Cannot expand from {self.containers_size} ' +
                             f'containers to {new_size} containers, new size ' +
                             f'must be larger than existing size')
        self.containers = PersistentMapping({
            key: self.containers.get(key, PersistentMapping())
            for key in range(new_size)
        })

    def exists(self, id) -> bool:
        """
        Return a bool describing whether the object is already present in the
        database
        :param id:
        :return:
        """
        return id in self.__locate_container(id).keys()

    def get(self, id):
        """
        Return an object by the given id
        :param id:
        :return:
        """
        return self.__locate_container(id).get(id, None)

    def save(self, id, obj):
        """
        Save an object to the database at the given id location
        :param obj:
        :param id:
        :return:
        """
        self.__locate_container(id)[id] = obj

    def remove(self, id):
        """
        Remove an object from the database by the given id
        :param id:
        :return:
        """
        self.__locate_container(id).pop(id)

    def __locate_container(self, id: str):
        """
        Locate the appropriate container based on the provided id value
        :param id:
        :return:
        """
        # ensure we get the same value each time
        val = int.from_bytes(str(id).encode(), 'big')
        val = val % self.containers_size
        return self.containers[val]


class CitrineConnection(Connection):
    """
    Modified version of the ZODB.Connection.Connection class that adds a few
    utility methods and attributes for enhanced performance.

    ALL actions performed by a CitrineConnection are transactional by default,
    unless the object is being used as a context manager in which case
    the transaction will be committed on closure. To disable automatic
    transactions, set self.auto_transaction to False.
    """

    @property
    def container(self):
        return self.root.container

    @property
    def meta(self):
        return self.root.meta

    def __init__(self, db, cache_size=400, before=None, cache_size_bytes=0,
                 transaction_manager=None, **db_args):
        if not isinstance(db, DB):
            db = DB(db, **db_args)
        super().__init__(db=db, cache_size=cache_size, before=before,
                         cache_size_bytes=cache_size_bytes)
        self.transaction_manager = transaction_manager or TransactionManager()
        self.auto_transaction = True
        self.open(self.transaction_manager)

        self.logger = getattr(self, 'logger', logging.getLogger(__name__))
        self.__checks()

    def num_containers(self) -> int:
        return self.container.containers_size

    def expand_containers(self, new_num: int):
        """
        Add the specified number of sub-containers to the connection's main
        container
        :param new_num:
        :return:
        """
        with self:
            self.container.expand_size(self.num_containers() + new_num)

    def __enter__(self):
        self.auto_transaction = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transaction_manager.commit()
        self.auto_transaction = True

    def __checks(self):
        """
        Performs checks that objects necessary for the CitrineConnection to
        function are present, and attempts to create them if they are not
        :return:
        """
        if not hasattr(self.root, 'container'):
            logging.warning('MISSING CONTAINER OBJECT "root.container", ' +
                            'CREATING NEW')
            with self:
                self.root.container = DbContainer()

        if not hasattr(self.root, 'meta'):
            logging.warning('MISSING METADATA OBJECT "root.meta", ' +
                            'CREATING NEW')
            with self:
                self.root.meta = DbMetadata()
