"""
Implementations of the ``jsonld.JsonLdEngine`` that can work on top of both
a local Citrine database or as a client for a CitrineServer database
"""

from typing import Iterable as typeIterable

import warnings
from ZODB.DB import getTID

from jsonld import JsonLdEngine, JsonLdPackage
from citrine import CitrineDB, CitrineConnection, CitrineClient, Crystal


class CitrineEngineConnection(JsonLdEngine, CitrineConnection):

    def __init__(self, db, cache_size=400, before=None,
                 cache_size_bytes=0, transaction_manager=None, autocommit=True,
                 packages=None):
        CitrineConnection.__init__(
            self, db, cache_size, before, cache_size_bytes,
            transaction_manager, autocommit
        )
        JsonLdEngine.__init__(self, packages)


class CitrineEngine(CitrineDB):
    """
    Implementation of the JsonLdEngine that functions as the connection for a
    local CitrineDB
    """
    klass = CitrineEngineConnection

    def __init__(self, storage,
                 packages: JsonLdPackage | typeIterable[JsonLdPackage],
                 pool_size: int = 7,
                 pool_timeout: int = 2147483648, cache_size: int = 400,
                 cache_size_bytes: int = 0, historical_pool_size: int = 3,
                 historical_cache_size: int = 1000,
                 historical_cache_size_bytes: int = 0,
                 historical_timeout: int = 300, database_name: str = 'unnamed',
                 databases: dict = None, xrefs: bool = True,
                 large_record_size: int = 16777216,
                 **storage_args):
        self.packages = packages
        CitrineDB.__init__(self, storage, pool_size, pool_timeout, cache_size,
                           cache_size_bytes, historical_pool_size,
                           historical_cache_size, historical_cache_size_bytes,
                           historical_timeout, database_name, databases, xrefs,
                           large_record_size, **storage_args)

    @classmethod
    def load(cls,
             storage,
             packages: JsonLdPackage | typeIterable[JsonLdPackage],
             pool_size: int = 7, pool_timeout: int = 2147483648,
             cache_size: int = 400, cache_size_bytes: int = 0,
             historical_pool_size: int = 3, historical_cache_size: int = 1000,
             historical_cache_size_bytes: int = 0,
             historical_timeout: int = 300, database_name: str = 'unnamed',
             databases: dict = None, xrefs: bool = True,
             large_record_size: int = 16777216):
        """

        :param packages: the packages to load into the engine

        :param storage: the filestorage to use

        :param pool_size: expected max number of connections

        :param pool_timeout: max age for inactive connections

        :param cache_size: target maximum number of non-ghost objects in each
        connection cache

        :param cache_size_bytes: target total memory usage of non-ghost objects
        in each connection cache

        :param historical_pool_size: expected max number of historical
        connections

        :param historical_cache_size: target maximum number of non-ghost
        objects in each historical connection cache

        :param historical_cache_size_bytes: target total memory usage of
        non-ghost objects in each historical connection cache

        :param historical_timeout: max age for inactive historical connections

        :param database_name: name of the database

        :param databases: additional databases in a multi-database configuration

        :param xrefs: whether cross-database references are allowed from this
        database to other databases in a multi-database configuration

        :param large_record_size: size at which warnings are issued that blobs
        should be used rather than records

        :return: ``CitrineEngine`` at the location
        """
        return cls(storage, packages, pool_size, pool_timeout, cache_size,
                   cache_size_bytes, historical_pool_size,
                   historical_cache_size, historical_cache_size_bytes,
                   historical_timeout, database_name, databases, xrefs,
                   large_record_size)

    def open(self, transaction_manager=None, at=None, before=None):
        """

        :param transaction_manager:
        :param at:
        :param before:
        :return:
        """
        # there isn't an easy way to change the arguments provided to self.klass
        # so the only real way to make this happen is to replicate the entire
        # method with the necessary changes
        before = getTID(at, before)
        if (before is not None and
                before > self.lastTransaction() and
                before > getTID(self.lastTransaction(), None)):
            raise ValueError(
                'cannot open an historical connection in the future.')

        if isinstance(transaction_manager, str):
            if transaction_manager:
                raise TypeError("Versions aren't supported.")
            warnings.warn(
                "A version string was passed to open.\n"
                "The first argument is a transaction manager.",
                DeprecationWarning, 2)
            transaction_manager = None

        with self._lock:
            # result <- a connection
            if before is not None:
                result = self.historical_pool.pop(before)
                if result is None:
                    c = self.klass(self,
                                   self._historical_cache_size,
                                   before,
                                   self._historical_cache_size_bytes,
                                   packages=self.packages,
                                   )
                    self.historical_pool.push(c, before)
                    result = self.historical_pool.pop(before)
            else:
                result = self.pool.pop()
                if result is None:
                    c = self.klass(self,
                                   self._cache_size,
                                   None,
                                   self._cache_size_bytes,
                                   packages=self.packages,
                                   )
                    self.pool.push(c)
                    result = self.pool.pop()
            assert result is not None

            # A good time to do some cache cleanup.
            # (note we already have the lock)
            self.pool.availableGC()
            self.historical_pool.availableGC()

        result.open(transaction_manager)
        return result


class CitrineClientEngine(JsonLdEngine, CitrineClient):
    """
    Implementation of the JsonLdEngine that functions as the client for a
    remote CitrineServer
    """
