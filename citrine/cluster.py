"""
Classes and functions for managing a Zope Database Cluster. A cluster is a
collection of object databases that all store the same type of object and
provides CRUD functionality as well as index, caching, and search.

The cluster manager is responsible for ensuring an adequate number of nodes are
available, indexing objects across the cluster for easy lookup, and rapidly
recalling objects. The user or process using a cluster should not have to know
anything about the internal logic, only the standard methods used to get
details on what the cluster contains and how to create, update, and delete the
contents.
"""

# a CitrineDb is a managed storage with easy read/write capability
# a DbModule is a class that wraps the CitrineDb as a module for easy loading
# a DbPool is a class that can discover and manage many DbModules
# a CitrineCluster is a DbPool that can treat the modules as a single collective
#   database where the objects are distributed among the many modules and
#   accessible through a single CRUD interface. The cluster will self-scale
#   as necessary and contain its own internal database that stores a record of
#   ever transaction and any ClassCrystal objects necessary for the contents.
#   Ideally, a cluster will be responsible for a single type of object so
#   indexes and views can be efficiently written.
import logging
from os.path import join

from ZODB import DB

from citrine.citrinedb import CitrineDB
from citrine.cluster_tools.dbmodule.dbgroup import DbGroup
from citrine.cluster_tools.clusterdb.container import ClusterRegistryContainer


class ClusterDB(DbGroup, CitrineDB):
    """
    Data access and management object for an object database cluster.

    Functions as both a database and a database manager. The database stores
    information on the DbModule objects stored in the directory and information
    on the overall number of objects. The primary use of this is to keep track
    of the number of DbModules and what hash values the UUIDs are mapped to. If
    a DbModule has disappeared, the Cluster will raise several warnings in
    the logs.

    Additional functionality includes the ability to expand the number of
    modules in-place, as well as caching recently retrieved objects, creating
    indexes, and running queries.
    """

    @property
    def databases(self):
        """
        Dictionary of names and database objects. Will derive a set from all
        modules registered to the cluster unless a value has been manually set
        """
        if hasattr(self, '___databases___'):
            return getattr(self, '___databases___', dict())
        return {**{name: module.db for name, module in self.modules.items()},
                **{getattr(self, 'database_name', 'unnamed'): self}}

    @databases.setter
    def databases(self, value):
        setattr(self, '___databases___', value)

    @databases.deleter
    def databases(self):
        # del is really just a reset to the default derived value
        delattr(self, '___databases___')

    def __init__(self, root: str, pool_size: int = 7,
                 pool_timeout: int = 2147483648, cache_size: int = 400,
                 cache_size_bytes: int = 0, historical_pool_size: int = 3,
                 historical_cache_size: int = 1000,
                 historical_cache_size_bytes: int = 0,
                 historical_timeout: int = 300, database_name: str = 'unnamed',
                 xrefs: bool = True, large_record_size: int = 16777216,
                 **storage_args):
        self.logger = logging.getLogger(f'{database_name}_cluster')
        DbGroup.__init__(self, root)
        CitrineDB.__init__(self,
            storage=join(root, database_name), pool_size=pool_size,
            pool_timeout=pool_timeout, cache_size=cache_size,
            cache_size_bytes=cache_size_bytes,
            historical_pool_size=historical_pool_size,
            historical_cache_size=historical_cache_size,
            historical_cache_size_bytes=historical_cache_size_bytes,
            historical_timeout=historical_timeout,
            database_name=database_name, databases=self.databases,
            xrefs=xrefs, large_record_size=large_record_size, **storage_args)
        # zodb sets the databases value, so we reset to the derived version
        del self.databases
        self.validate_module_registration()

    def validate_module_registration(self, strict=False):
        """
        Checks that all detected modules match the previous registry, and logs
        inconsistencies if not.

        If any expected modules are not detected, a check will be run to see
        if the file exists but is corrupt before creating a new module to
        replace it. If a directory containing a database is found, an attempt
        will be made to create a connection, and if successful the database will
        be copied directly into the new module.

        If new modules are found their presence will be noted and they will
        be accessible, but the contents will not be readable or written to by
        standard operations unless the database is explicitly instructed to
        merge the contents into the existing structure.

        If strict is enabled and a check fails, an exception will be raised.

        :param strict: whether to fail if a check fails
        """
        found_modules = self.modules
        with self as conn:
            # check that we aren't missing modules and log modules we find that
            # we aren't prepared to handle yet
            known_modules = conn.container.modules.items()
            for name, module in known_modules.items():
                if name not in found_modules.keys():
                    raise ModuleNotFoundError(f'Expected module "{name}" not found')
            for name, module in found_modules.items():
                if name not in known_modules.keys():
                    self.logger.info(f'Found unrecognized module "{name}"; ' +
                                     'module will be held but UNUSED UNTIL REBUILD')
            checkable_modules = {name: mod for name, mod in found_modules.items()
                                 if name in known_modules.keys()}
        # check that every found module has a database we can use
        for name, module in checkable_modules.items():
            db = module.db
            # check the db is an instance of ZODB.DB, can be opened, and has
            # CRUD functions (all of these are fatal errors)
            if not isinstance(db, DB):
                raise TypeError(f'db {name} is not a recognizable type of database!')
            conn = db.open()
            for name in ('create', 'read', 'update', 'delete'):
                fn = getattr(conn, name, None)
                if fn is None or not callable(fn):
                    raise NotImplementedError(f'db missing necessary method {name}, ' +
                                              'cannot proceed!')


    def create_dbmodule(self, name: str = None, overwrite: bool = False):
        """
        Creates a new database using the provided name, at the path. If no
        path is specified, the directory of execution will be used
        :param name: The name to assign the database
        """
        with self as conn:
            with conn:
                new = DbGroup.create_dbmodule(self, name=name,
                                              overwrite=overwrite)
                conn.create(new.name, new)

    def destroy_dbmodule(self, name):
        """
        Destroys a db object from the pool entirely. This action is irreversible
        :param name: The name of the database to be destroyed
        """
        with self as conn:
            with conn:
                conn.delete(name)
                DbGroup.destroy_dbmodule(self, name)

    @classmethod
    def new(cls, root, pool_size: int = 7,
            pool_timeout: int = 2147483648, cache_size: int = 400,
            cache_size_bytes: int = 0, historical_pool_size: int = 3,
            historical_cache_size: int = 1000,
            historical_cache_size_bytes: int = 0,
            historical_timeout: int = 300, database_name: str = 'unnamed',
            xrefs: bool = True, large_record_size: int = 16777216,
            **storage_args):
        """
        Creates a new ClusterDB at the root location and returns the object.
        The directory will be scanned for existing databases and
        """
        db = ClusterDB(root=root, pool_size=pool_size,
                       pool_timeout=pool_timeout, cache_size=cache_size,
                       cache_size_bytes=cache_size_bytes,
                       historical_pool_size=historical_pool_size,
                       historical_cache_size=historical_cache_size,
                       historical_cache_size_bytes=
                       historical_cache_size_bytes,
                       historical_timeout=historical_timeout,
                       database_name=database_name, xrefs=xrefs,
                       large_record_size=large_record_size, **storage_args)
        with db as conn:
            conn.setup()
            with conn:
                conn.root.container = ClusterRegistryContainer(db.modules)
        return db


# STEP 2: NODE MANAGEMENT
# TODO: Cluster MUST be able to dynamically create new nodes based on the
#   overall number of objects

# TODO: Cluster MUST be able to migrate existing nodes to new nodes

# TODO: Cluster MUST be able to validate that one set of nodes contains the
#   contents of another

# TODO: Cluster MUST be able to change primary object cluster if more than one
#   set of nodes is available

# TODO: Cluster MUST be able to update dependent objects to use different set
#   of nodes

# TODO: Cluster MUST be able to disable and enable automatic resizing


# STEP 3: INDEX, CACHE, AND SEARCH

# TODO: Cluster SHOULD be able to create indexes that make searching for
#   objects easier

# TODO: Cluster SHOULD be able to cache objects:
#   - CACHE results with a request-per-minute rate >= 1
#   - UNCACHE results unrequested for 15 minutes

# TODO: Cluster SHOULD be able to accept a query and return a TUPLE of objects
#   matching the query parameters
