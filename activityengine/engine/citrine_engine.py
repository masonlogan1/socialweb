"""
Implementations of the ``jsonld.JsonLdEngine`` that can work on top of both
a local Citrine database or as a client for a CitrineServer database
"""

from typing import Iterable as typeIterable

import warnings
from ZODB.DB import getTID

from jsonld import JsonLdEngine, JsonLdPackage
from citrine import (CitrineDB, CitrineConnection, CitrineClient, Crystal,
                     CitrineThreadTransaction, CitrineTransaction)


class CitrineEngineConnection(JsonLdEngine, CitrineConnection):

    def __init__(self, db, cache_size=400, before=None,
                 cache_size_bytes=0, transaction_manager=None, autocommit=True,
                 packages=None):
        CitrineConnection.__init__(
            self, db, cache_size, before, cache_size_bytes,
            transaction_manager, autocommit
        )
        JsonLdEngine.__init__(self, packages)

    def _add_class_to_engine(self, cls, name=None, prefix='create_'):
        """

        :param cls: the class to make available as an attribute of the engine
        :param name: the name to use
        :return:
        """

        def create(id, *args, **kwargs):
            """
            Creates a new instance of the class, crystallizes it, persists that
            crystallized form into the database, and returns the object
            :param id: the id of the object
            :return: a new object
            """
            new_obj = cls(id, *args, **kwargs)
            crystallized_obj = Crystal.crystallize(new_obj)
            self.create(id, crystallized_obj)

            return new_obj

        name = str(prefix) + (name if name else cls.__name__)
        self.logger.info(f"Adding {cls.__name__} to engine as '{name}'")
        setattr(self, name, create)

    def read(self, id, default=None, autocommit=False):
        crystal = CitrineConnection.read(self, id, default)
        if (hasattr(crystal, '__namespace__') and
                crystal.__namespace__ in self.class_registry.keys()):
            recovered = Crystal.decrystallize(
                crystal, self.class_registry.get(crystal.__namespace__)
            )
            setattr(crystal, 'autocommit', autocommit)
        else:
            recovered = crystal

        return recovered


class CitrineEngine(CitrineDB):
    """
    Implementation of the JsonLdEngine that functions as the connection for a
    local CitrineDB
    """
    klass = CitrineEngineConnection

    def __init__(self, storage,
                 pool_size: int = 7,
                 pool_timeout: int = 2147483648, cache_size: int = 400,
                 cache_size_bytes: int = 0, historical_pool_size: int = 3,
                 historical_cache_size: int = 1000,
                 historical_cache_size_bytes: int = 0,
                 historical_timeout: int = 300, database_name: str = 'unnamed',
                 databases: dict = None, xrefs: bool = True,
                 large_record_size: int = 16777216,
                 packages: JsonLdPackage | typeIterable[JsonLdPackage] = None,
                 **storage_args):
        # packages should be an iterable of JsonLdPackages (or an empty list)
        if packages:
            self.packages = (
                tuple(packages) if isinstance(packages, typeIterable)
                else (packages,))
        else:
            self.packages = tuple()

        CitrineDB.__init__(self, storage, pool_size, pool_timeout, cache_size,
                           cache_size_bytes, historical_pool_size,
                           historical_cache_size, historical_cache_size_bytes,
                           historical_timeout, database_name, databases, xrefs,
                           large_record_size, **storage_args)

    def open(self, transaction_manager=None, at=None, before=None,
             packages: JsonLdPackage | typeIterable[JsonLdPackage] = None):
        """

        :param transaction_manager:
        :param at:
        :param before:
        :return:
        """
        # packages should be a combination of provided and existing packages
        if packages:
            packages = (tuple(packages) if isinstance(packages, typeIterable)
                        else (packages,))
        packages = ((packages if packages else tuple()) +
                    (self.packages if self.packages else tuple()))

        # if we don't provide one explicitly every time, we end up with the
        # ZODB standard transaction, which causes a lot of problems
        if not transaction_manager:
            transaction_manager = CitrineThreadTransaction()

        # there isn't an easy way to change the arguments provided to self.klass
        # so the only real way to make this happen is to replicate the entire
        # method with the necessary changes
        before = getTID(at, before)
        if (before is not None and
                before > self.lastTransaction() and
                before > getTID(self.lastTransaction(), None)):
            raise ValueError(
                'cannot open an historical connection in the future.')

        # TODO: move this logic deeper into the inheritance stack, replace
        #   packages=packages with **kwargs, and rewrite this method so it adds
        #   packages as a mandatory param and passes it in like a kwarg to the
        #   superclass method
        with self._lock:
            # result <- a connection
            if before is not None:
                result = self.historical_pool.pop(before)
                if result is None:
                    c = self.klass(self,
                                   self._historical_cache_size,
                                   before,
                                   self._historical_cache_size_bytes,
                                   packages=packages,
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
                                   packages=packages,
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
