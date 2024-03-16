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
from os.path import join
from typing import Iterable
from uuid import uuid4

from citrine.citrinedb import CitrineDB
from citrine.cluster_tools.dbmodule import create_dbmodule, delete_dbmodule


class DbModule:
    """
    Manages the creation, migration, and deletion of a Citrine Database object
    that is treated like an independent, importable code module.

    This object is responsible for creating a directory structure with an
    ``__init__.py`` file that provides a single importable object in the format
    ``from <uuid> import get_db``
    """

    def __init__(self, path: str = '.'):
        self.path = path
        self.db = self.load_db()

    def load_db(self):
        if not hasattr(self, 'path'):
            raise AttributeError(f'No path selected for DbModule!')
        # imports the db, opens it, and returns the object
        from importlib.util import spec_from_file_location, module_from_spec
        init_path = join(self.path, '__init__.py')
        spec = spec_from_file_location('db', init_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.db()

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
        return self.db.open(transaction_manager=transaction_manager,
                            at=at, before=before)

    @classmethod
    def create(cls, path: str, name: str, overwrite: bool = False):
        """
        Creates a new module at the path location, if one does not exist.

        The provided name will be given to the newly created database
        """
        import importlib.util
        module_path = create_dbmodule(path, name, overwrite)
        return DbModule(module_path)

    @classmethod
    def destroy(cls, path: str):
        """
        Destroys a module at the path location
        """

    def __call__(self):
        return self.db


class DbPool:
    """
    A collection of databases. Will create databases as importable modules under
    a common directory and provide managed storage across all databases in the
    collection.

    It is STRONGLY RECOMMENDED to use the discovery process, and ONLY the
    discovery process, to manage the contents of the pool.
    """

    def __init__(self, path: str = '.', dbs: Iterable = None, discovery=True):
        """
        Creates the pool, using the path as the root of the group. Any modules
        stored in the root directory that can be imported in the format:
        ``import module.db``
        will be automatically retrieved by the pool if discovery is True
        """
        self.db_pool = {}
        self.root = path
        if discovery:
            self.discover()

    def create_db(self, name):
        """
        Creates a new database using the provided name, at the path. If no
        path is specified, the directory of execution will be used
        :param name: The name to assign the database
        """

    def add_db(self, name):
        """
        Adds an existing db to the cluster
        :param name: The name of the database to add to the group
        """

    def remove_db(self, name):
        """
        Removes an existing db from the cluster
        :param name: The name of the database to remove from the group
        """

    def get_db(self, name):
        """
        Returns a db object from the pool
        :param name: The name of the desired database
        """

    def destroy_db(self, name):
        """
        Destroys a db object from the pool entirely. This action is irreversible
        :param name: The name of the database to be destroyed
        """

    def discover(self):
        """
        Collects all database modules from the provided path and adds anything
        into the pool that is not yet added
        """


class ClusterDb:
    """
    Data access and management object for an object database cluster
    """


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
