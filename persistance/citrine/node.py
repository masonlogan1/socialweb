"""
Common classes and utilities used by the Citrine database
"""
from transaction import TransactionManager
from ZODB import DB
from ZODB.FileStorage import FileStorage
from persistent import Persistent


class ConnectionProfile(Persistent):
    """
    Reusable object for storing object database connection information
    """
    # Can be persisted into the exact type of databases it is intended to
    # store info on!

    @property
    def storage(self):
        return getattr(self, '___storage___', None)

    @storage.setter
    def storage(self, val):
        setattr(self, '___storage___', val)

    @property
    def pool_size(self):
        return getattr(self, '___pool_size___', None)

    @pool_size.setter
    def pool_size(self, val):
        setattr(self, '___pool_size___', val)

    @property
    def pool_timeout(self):
        return getattr(self, '___pool_timeout___', None)

    @pool_timeout.setter
    def pool_timeout(self, val):
        setattr(self, '___pool_timeout___', val)

    @property
    def cache_size(self):
        return getattr(self, '___cache_size___', None)

    @cache_size.setter
    def cache_size(self, val):
        setattr(self, '___cache_size___', val)

    @property
    def cache_size_bytes(self):
        return getattr(self, '___cache_size_bytes___', None)

    @cache_size_bytes.setter
    def cache_size_bytes(self, val):
        setattr(self, '___cache_size_bytes___', val)

    @property
    def historical_pool_size(self):
        return getattr(self, '___historical_pool_size___', None)

    @historical_pool_size.setter
    def historical_pool_size(self, val):
        setattr(self, '___historical_pool_size___', val)

    @property
    def historical_cache_size(self):
        return getattr(self, '___historical_cache_size___', None)

    @historical_cache_size.setter
    def historical_cache_size(self, val):
        setattr(self, '___historical_cache_size___', val)

    @property
    def historical_cache_size_bytes(self):
        return getattr(self, '___historical_cache_size_bytes___', None)

    @historical_cache_size_bytes.setter
    def historical_cache_size_bytes(self, val):
        setattr(self, '___historical_cache_size_bytes___', val)

    @property
    def historical_timeout(self):
        return getattr(self, '___historical_timeout___', None)

    @historical_timeout.setter
    def historical_timeout(self, val):
        setattr(self, '___historical_timeout___', val)

    @property
    def database_name(self):
        return getattr(self, '___database_name___', None)

    @database_name.setter
    def database_name(self, val):
        setattr(self, '___database_name___', val)

    @property
    def xrefs(self):
        return getattr(self, '___xrefs___', None)

    @xrefs.setter
    def xrefs(self, val):
        setattr(self, '___xrefs___', val)

    @property
    def large_record_size(self):
        return getattr(self, '___large_record_size___', None)

    @large_record_size.setter
    def large_record_size(self, val):
        setattr(self, '___large_record_size___', val)

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

    def to_dict(self, exclude_none = False):
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


class DbNode:
    """
    A single node in a cluster database. Inherits from ZODB.DB and adds
    wrappers and restrictions to improve ease of use.
    """

    @property
    def connection(self):
        return getattr(object, '___connection___', None)

    @property
    def transaction_manager(self):
        return getattr(object, '___transaction_manager___', None)

    @property
    def root(self):
        # derive from the connection if not set and connection exists
        if not hasattr(self, '___root___') and self.connection:
            setattr(self, '___root___', self.connection.root())
        return getattr(self, '___root___', None)

    def __init__(self, storage, pool_size=7, pool_timeout=2147483648,
                 cache_size=400, cache_size_bytes=0, historical_pool_size=3,
                 historical_cache_size=1000, historical_cache_size_bytes=0,
                 historical_timeout=300, database_name='unnamed',
                 xrefs=True, large_record_size=16777216, **storage_args):
        self.___transaction_manager___ = TransactionManager()
        self.___connection___ = DB(storage=FileStorage(storage, **storage_args),
                                   pool_size=pool_size,
                                   pool_timeout=pool_timeout,
                                   cache_size=cache_size,
                                   cache_size_bytes=cache_size_bytes,
                                   historical_pool_size=historical_pool_size,
                                   historical_cache_size=historical_cache_size,
                                   historical_cache_size_bytes=
                                   historical_cache_size_bytes,
                                   historical_timeout=historical_timeout,
                                   database_name=database_name, xrefs=xrefs,
                                   large_record_size=large_record_size,
                                   ).open()

    @staticmethod
    def from_profile(profile: ConnectionProfile, exclude_none=False):
        return DbNode(**profile.to_dict(exclude_none=exclude_none))
