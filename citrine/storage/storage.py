"""
Classes and functions for managing a single object database
"""
from ZODB import DB

from citrine.exceptions import CitrineIncompatibleMethodError
from citrine.connection import ManagedConnection

from citrine.storage.transaction import TransactionManager


class ManagedStorage(DB):
    """
    The CitrineDB class provides managed storage by providing a pool of
    CitrineConnection objects that supply a set of transactional CRUD (Create,
    Read, Update, Delete) methods to wrap prepared structures.

    Because Citrine objects are tightly coupled together, ``ZODB.connection``
    is unable to be used; ``DB().open_then_close_db_when_connection_closes()``
    has been disabled. If a database used as part of a collaborative structure
    were to be opened using that method, it could potentially collapse the
    entire managed structure.
    """
    klass = ManagedConnection

    def __init__(self, storage, pool_size: int = 7,
                 pool_timeout: int = 2147483648, cache_size: int = 400,
                 cache_size_bytes: int = 0, historical_pool_size: int = 3,
                 historical_cache_size: int = 1000,
                 historical_cache_size_bytes: int = 0,
                 historical_timeout: int = 300, database_name: str = 'unnamed',
                 databases: dict = None, xrefs: bool = True,
                 large_record_size: int = 16777216, **storage_args):
        """
        Creates a Citrine database object

        :param storage: the storage used by the database, such as a
        ``ZODB.FileStorage.FileStorage.FileStorage``. This can be a string
        path name to use a constructed ``ZODB.FileStorage.FileStorage.
        FileStorage`` storage or ``None`` to use a constructed ``ZODB.
        MappingStorage.MappingStorage``.

        :param pool_size: expected maximum number of open connections. Warnings
        are logged when this is exceeded and critical messages are logged if
        twice the pool size is exceeded.

        :param pool_timeout: Maximum age of inactive connections. When a
        connection has remained unused in a connection pool for more than
        pool_timeout seconds, it will be discarded and it's resources released.

        :param cache_size: target maximum number of non-ghost objects in each
        connection object cache.

        :param cache_size_bytes: target total memory usage of non-ghost objects
        in each connection object cache.

        :param historical_pool_size: expected maximum number of total historical
        connections

        :param historical_cache_size: target maximum number of non-ghost objects
         in each historical connection object cache.

        :param historical_cache_size_bytes: target total memory usage of
        non-ghost objects in each historical connection object cache.

        :param historical_timeout: Maximum age of inactive historical
        connections.  When a connection has remained unused in a historical
        connection pool for more than pool_timeout seconds, it will be discarded
        and it's resources released.

        :param database_name: The name of this database in a multi-database
        configuration.  The name is used when constructing cross-database
        references and when accessing database connections from other databases.

        :param databases: dictionary of database name to databases in a
        multi-database configuration. The new database will add itself to this
        dictionary. The dictionary is used when getting connections in other
        databases.

        :param xrefs: Flag indicating whether cross-database references are
        allowed from this database to other databases in a multi-database
        configuration.

        :param large_record_size: When object records are saved that are
        larger than this, a warning is issued, suggesting that blobs should
        be used instead.

        :param storage_args: Extra keywork arguments passed to a
             storage constructor if a path name or None is passed as
             the storage argument.
        """
        super().__init__(storage=storage, pool_size=pool_size,
                         pool_timeout=pool_timeout, cache_size=cache_size,
                         cache_size_bytes=cache_size_bytes,
                         historical_pool_size=historical_pool_size,
                         historical_cache_size=historical_cache_size,
                         historical_cache_size_bytes=
                         historical_cache_size_bytes,
                         historical_timeout=historical_timeout,
                         database_name=database_name, databases=databases,
                         xrefs=xrefs, large_record_size=large_record_size,
                         **storage_args)

    def open(self, transaction_manager=None, at=None, before=None):
        """
        Return a database Connection for use by application code.

        Note that the connection pool is managed as a stack, to increase the
        likelihood that the connection's stack will include useful objects.

        :param transaction_manager: transaction manager to use, "None" will
        default to a CitrineThreadTransactionManager
        :param at: a ``datetime.datetime`` or 8 character transaction id of the
        time to open the database with a read-only connection. Passing both
        ``at`` and ``before`` raises a ValueError, and passing neither opens a
        standard writable transaction of the newest state. A timezone-naive
        ``datetime.datetime`` is treated as a UTC value.
        :param before: like ``at``, but opens the readonly state before the tid
        or datetime.
        :return: CitrineConnection
        """
        return super().open(
            transaction_manager=(transaction_manager or
                                 TransactionManager()),
            at=at, before=before
        )

    @classmethod
    def new(cls, storage, pool_size: int = 7,
            pool_timeout: int = 2147483648, cache_size: int = 400,
            cache_size_bytes: int = 0, historical_pool_size: int = 3,
            historical_cache_size: int = 1000,
            historical_cache_size_bytes: int = 0,
            historical_timeout: int = 300, database_name: str = 'unnamed',
            databases: dict = None, xrefs: bool = True,
            large_record_size: int = 16777216, **storage_args):
        """
        Creates a new CitrineDb at the storage location and returns the object
        """
        db = cls(storage=storage, pool_size=pool_size,
                       pool_timeout=pool_timeout, cache_size=cache_size,
                       cache_size_bytes=cache_size_bytes,
                       historical_pool_size=historical_pool_size,
                       historical_cache_size=historical_cache_size,
                       historical_cache_size_bytes=
                       historical_cache_size_bytes,
                       historical_timeout=historical_timeout,
                       database_name=database_name, databases=databases,
                       xrefs=xrefs, large_record_size=large_record_size,
                       **storage_args)
        conn = db.open()
        conn.setup()
        conn.close()
        return db

    def __getitem__(self, item):
        with self as conn:
            val = conn[item]
        return val

    def __enter__(self):
        """
        Opens a temporary connection that is automatically closed.

        DOES NOT ALLOW FOR USING AN EXISTING TRANSACTION MANAGER!
        :return: CitrineConnection
        """
        self.__context_connection = self.open()
        return self.__context_connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the temporary connection
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.__context_connection.close()
        self.__context_connection = None
        del self.__context_connection


    @CitrineIncompatibleMethodError.override_method
    def open_then_close_db_when_connection_closes(self):
        """DISABLED IN CITRINEDB"""
