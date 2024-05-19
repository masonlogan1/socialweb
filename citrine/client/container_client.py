"""
Classes and functions for creating and working with ``ContainerDb`` objects,
an implementation of ``ZODB.DB`` that provides an easy interface for managed
storage using a ``Container`` object.
"""
from ZODB import DB
from ZODB.FileStorage import FileStorage

from ZEO.ClientStorage import ClientStorage
from ZEO.asyncio.client import ClientThread

from citrine.connection.container_connection import ContainerConnection
from citrine.database.containerdb import ContainerDb
from citrine.storage.consts import DEFAULT_CONTAINER_SIZE
from citrine.storage.container import Container

MB = 1024**2


class ContainerClient(ContainerDb):
    """

    """

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError("'Create' process only valid for local " +
                                  "databases, not client databases")

    # "why are there so many kwargs??" BECAUSE THIS IS A COMPLEX PROCESS
    @classmethod
    def connect(cls, addr, storage_path, pool_size: int = 7,
            pool_timeout: int = 2147483648, cache_size: int = 400,
            cache_size_bytes: int = 0, historical_pool_size: int = 3,
            historical_cache_size: int = 1000,
            historical_cache_size_bytes: int = 0,
            historical_timeout: int = 300, database_name: str = 'unnamed',
            databases: dict = None, xrefs: bool = True,
            large_record_size: int = 16777216, strict: bool = False,
            storage_type='1', storage_cache_size=20 * MB,
            name='', wait_timeout=None, disconnect_poll=None,
            read_only=0, read_only_fallback=0,
            blob_dir=None, shared_blob_dir=False,
            blob_cache_size=None, blob_cache_size_check=10,
            client_label=None, cache=None,
            ssl=None, ssl_server_hostname=None,
            # Mostly ignored backward-compatability options
            client=None, var=None,
            min_disconnect_poll=1, max_disconnect_poll=None, wait=True,
            drop_cache_rather_verify=True,
            credentials=None, server_sync=False,
            # The ZODB-define ZConfig support may ball these:
            username=None, password=None, realm=None,
            create_missing_container=True,
            # For tests:
            _client_factory=ClientThread):
        """
        Connects to a ZEO database

        :param addr: The server address(es).  This is either a list of
        addresses or a single address.  Each address can be a
        (hostname, port) tuple to signify a TCP/IP connection or
        a pathname string to signify a Unix domain socket
        connection.  A hostname may be a DNS name or a dotted IP
        address.  Required.

        All addresses are assumed to serve (essentially)
        the same (potentially replicated) storage.

        A connection tries to connect to those addresses;
        the first successful connection establishment with
        the called for ("read_only" or "writable") capabilities
        is selected and used for storage interaction until
        the connection is lost. In that case, a
        reconnection is tried.

        If ``ClientStorage`` calls for the "writable" capability
        but allows for a "read only" fallback, a read only connection can be
        used as a fallback; if a writable connection becomes available later, a
        switch to this connection is performed.

        :param storage: The server storage name, defaulting to '1'.  The name
        must match one of the storage names supported by the server(s)
        specified by the addr argument.

        :param cache_size: The disk cache size, defaulting to 20 megabytes.
        This is passed to the ClientCache constructor.

        :param name: The storage name, defaulting to a combination of the
        address and the server storage name.  This is used to
        construct the response to getName()

        :param wait_timeout: Maximum time (seconds) to wait for connections,
        defaulting to 30; applies only to [re]connect.

        :param read_only: A flag indicating whether this should be a read-only
        storage, defaults False

        :param read_only_fallback: A flag indicating whether a read-only
        remote storage should be acceptable as a fallback when no
        writable storages are available; defaults false

        :param blob_dir: directory path for data retrieved via the loadBlob API

        :param shared_blob_dir: Flag whether the blob_dir is a server-shared
        filesystem that should be used instead of transferring blob data over
        the ZEO protocol

        :param blob_cache_size: Maximum size of the ZEO blob cache, in bytes.
        If not set, the cache size isn't checked and the blob directory will
        grow without bound; ignored if shared_blob_dir is True

        :param blob_cache_size_check: Cache check size as percent of
        blob_cache_size. The ZEO cache size will be checked when this many
        bytes have been loaded into the cache; defaults to 10%, ignored if
        shared_blob_dir is True

        :param client_label: label to include in client log messages

        :param cache: cache object or a file path; defaults None

        :param ssl: ssl client context (i.e. with purpose "ServerAuth")
        to call for SSL connections.

        :param ssl_server_hostname: The server hostname - used during the SSL
        authentication check

        :param client:

        :param var: If cache is None, client determines the cache: if it is
        None, then a non persistent cache is used;
        otherwise, client is used together with var (defaults
        to the current working directory) to construct the
        file path for the persistent cache file

        :param wait: Wait for server connection, defaulting to true.

        :param server_sync: Whether sync() should make a server round trip,
        thus causing client to wait for outstanding invalidations.

        The `sync` is called in `transaction.begin`. A server round trip
        at this place guarantees that the transaction takes notice of all
        prior modifications.

        This may be important when several client processes share the same
        ZODB as the following examples demonstrate.

        Defaults to false.

        credentials
        username
        password
        realm
        disconnect_poll
        min_disconnect_poll
        max_disconnect_poll
        drop_cache_rather_verify
            ignored; retained (as parameters) for compatibility

        """
        # Connect to the database
        client = ClientStorage(
            addr, storage=storage_type, cache_size=storage_cache_size,
            name=name, wait_timeout=wait_timeout,
            disconnect_poll=disconnect_poll,
            read_only=read_only, read_only_fallback=read_only_fallback,
            blob_dir=blob_dir, shared_blob_dir=shared_blob_dir,
            blob_cache_size=blob_cache_size,
            blob_cache_size_check=blob_cache_size_check,
            client_label=client_label, cache=storage_path or cache,
            ssl=ssl, ssl_server_hostname=ssl_server_hostname,
            client=client, var=var,
            min_disconnect_poll=min_disconnect_poll,
            max_disconnect_poll=max_disconnect_poll, wait=wait,
            drop_cache_rather_verify=drop_cache_rather_verify,
            credentials=credentials, server_sync=server_sync,
            # The ZODB-define ZConfig support may ball these:
            username=username, password=password, realm=realm,
            # For tests:
            _client_factory=_client_factory)

        # Link to a local ContainerDb
        client = cls.load(client, pool_size=pool_size,
            pool_timeout=pool_timeout, cache_size=cache_size,
            cache_size_bytes=cache_size_bytes,
            historical_pool_size=historical_pool_size,
            historical_cache_size=historical_cache_size,
            historical_cache_size_bytes=historical_cache_size_bytes,
            historical_timeout=historical_timeout, database_name=database_name,
            databases=databases, xrefs=xrefs,
            large_record_size=large_record_size)

        # If not connection.container and create==True, create a new Container
        with client as connection:
            if not getattr(connection.root, 'container', None):
                with connection.transaction_manager as tm:
                    connection.root.container = Container.new(strict=strict)
                    tm.commit()
        return client
