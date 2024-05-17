"""
Classes and functions for creating and working with ``ContainerDb`` objects,
an implementation of ``ZODB.DB`` that provides an easy interface for managed
storage using a ``Container`` object.
"""
from ZODB import DB
from ZODB.FileStorage import FileStorage

from citrine.connection.container_connection import ContainerConnection
from citrine.storage.consts import DEFAULT_CONTAINER_SIZE
from citrine.storage.container import Container


class ContainerDb(DB):
    """
    An implementation of ``ZODB.DB`` that wraps a single ``Container`` object
    that provides an easy interface for managing storage.

    ContainerDb objects implement a transactional set of Create, Read, Update,
    and Delete methods, and can be used as a context manager to perform multiple
    operations as a single block. Additionally, they provide a simple set of
    methods for resizing the internal container in a way that does not render
    the internal storage inaccessible during the operation
    """

    klass = ContainerConnection

    def __init__(self, storage, pool_size: int = 7,
                 pool_timeout: int = 2147483648, cache_size: int = 400,
                 cache_size_bytes: int = 0, historical_pool_size: int = 3,
                 historical_cache_size: int = 1000,
                 historical_cache_size_bytes: int = 0,
                 historical_timeout: int = 300, database_name: str = 'unnamed',
                 databases: dict = None, xrefs: bool = True,
                 large_record_size: int = 16777216, strict: bool = False,
                 **storage_args):
        """
        Creates a database object that uses a ``Container`` as a way of
        managing storage.

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

        :param strict: Whether to enforce size maximums via exceptions

        :param storage_args: Extra keyword arguments passed to a
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

    @classmethod
    def create(cls, file_name: str, capacity: int = DEFAULT_CONTAINER_SIZE,
               create: bool = False, read_only: bool = False, stop=None,
               quota=None, pack_gc=True, pack_keep_old=True, packer=None,
               blob_dir=None, strict: bool = False):
        """
        Creates a new ``ContainerDb`` at the specified storage location.

        :param capacity: expected maximum number of storage connections

        :param file_name: Path to store data file

        :param create: Flag indicating whether a file should be created
        even if it already exists.

        :param read_only: Flag indicating whether the file is read only.
        Only one process is able to open the file non-read-only.

        :param stop: Time-travel transaction id. When the file is opened,
        data will be read up to the given transaction id. Transaction ids
        correspond to times computed using ``ZODB.TimeStamp.TimeStamp``.

        :param quota: File-size quota.

        :param pack_gc: Flag indicating whether garbage collection should
        be performed when packing.

        :param pack_keep_old: flag indicating whether old data files
        should be retained after packing as a ``.old`` file.

        :param packer: An alternative packer to the standard
        ``<ZODB.FileStorage.interfaces.IFileStoragePacker>``.

        :param blob_dir: A blob-directory path name. Blobs will be
        supported if this option is provided.

        :param strict: Whether to enforce size maximums via exceptions

        :return: FileStorage object connecting back to the new ``ContainerDb``
        """
        container = Container.new(capacity=capacity)
        storage = FileStorage(file_name, create=create, read_only=read_only,
                              stop=stop, quota=quota, pack_gc=pack_gc,
                              pack_keep_old=pack_keep_old, packer=packer,
                              blob_dir=blob_dir)
        # store the container in the database
        conn = DB(storage).open()
        with conn.transaction_manager as tm:
            conn.root.container = container
            tm.commit()
        conn.close()
        return storage

    @classmethod
    def load(cls, storage, pool_size: int = 7,
            pool_timeout: int = 2147483648, cache_size: int = 400,
            cache_size_bytes: int = 0, historical_pool_size: int = 3,
            historical_cache_size: int = 1000,
            historical_cache_size_bytes: int = 0,
            historical_timeout: int = 300, database_name: str = 'unnamed',
            databases: dict = None, xrefs: bool = True,
            large_record_size: int = 16777216, strict: bool = False):
        """
        Load a ``ContainerDb`` from the provided location

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

        :param storage_args: Extra keyword arguments passed to a
             storage constructor if a path name or None is passed as
             the storage argument.

        :return: ``ContainerDb`` at the location
        """
        return cls(storage, pool_size=pool_size, pool_timeout=pool_timeout,
                   cache_size=cache_size, cache_size_bytes=cache_size_bytes,
                   historical_pool_size=historical_pool_size,
                   historical_cache_size=historical_cache_size,
                   historical_cache_size_bytes=historical_cache_size_bytes,
                   historical_timeout=historical_timeout,
                   database_name=database_name,
                   databases=databases, xrefs=xrefs,
                   large_record_size=large_record_size,
                   strict=strict)

    @classmethod
    def new(cls, file_name: str, capacity: int = DEFAULT_CONTAINER_SIZE,
            create: bool = False, read_only: bool = False, stop=None,
            quota=None, pack_gc=True, pack_keep_old=True, packer=None,
            blob_dir=None, strict: bool = False, pool_size: int = 7,
            pool_timeout: int = 2147483648, cache_size: int = 400,
            cache_size_bytes: int = 0, historical_pool_size: int = 3,
            historical_cache_size: int = 1000,
            historical_cache_size_bytes: int = 0,
            historical_timeout: int = 300, database_name: str = 'unnamed',
            databases: dict = None, xrefs: bool = True,
            large_record_size: int = 16777216):
        """
        Creates a new ContainerDb at the storage location and returns the object

        :param capacity: expected maximum number of storage connections

        :param file_name: Path to store data file

        :param create: Flag indicating whether a file should be created
        even if it already exists.

        :param read_only: Flag indicating whether the file is read only.
        Only one process is able to open the file non-read-only.

        :param stop: Time-travel transaction id. When the file is opened,
        data will be read up to the given transaction id. Transaction ids
        correspond to times computed using ``ZODB.TimeStamp.TimeStamp``.

        :param quota: File-size quota.

        :param pack_gc: Flag indicating whether garbage collection should
        be performed when packing.

        :param pack_keep_old: flag indicating whether old data files
        should be retained after packing as a ``.old`` file.

        :param packer: An alternative packer to the standard
        ``<ZODB.FileStorage.interfaces.IFileStoragePacker>``.

        :param blob_dir: A blob-directory path name. Blobs will be
        supported if this option is provided.

        :param strict: Whether to enforce size maximums via exceptions

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

        :param storage_args: Extra keyword arguments passed to a storage
        constructor if a path name or None is passed as the storage argument.

        :return: newly created ``ContainerDb`` object
        """
        return cls.load(cls.create(file_name, capacity=capacity,
                                   create=create, read_only=read_only,
                                   stop=stop, quota=quota, pack_gc=pack_gc,
                                   pack_keep_old=pack_keep_old, packer=packer,
                                   blob_dir=blob_dir,
                                   strict=strict,
                                   ),
                        pool_size=pool_size, pool_timeout=pool_timeout,
                        cache_size=cache_size,
                        historical_pool_size=historical_pool_size,
                        historical_cache_size=historical_cache_size,
                        historical_cache_size_bytes=historical_cache_size_bytes,
                        database_name=database_name,
                        databases=databases, xrefs=xrefs,
                        large_record_size=large_record_size)

    def __enter__(self):
        """
        Provides a temporary connection that will close at the end of the
        context management process
        :return: connection object
        """
        self.__context_manager_connection = self.open()
        return self.__context_manager_connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__context_manager_connection.close()
