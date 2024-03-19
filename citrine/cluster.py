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
from os.path import join, exists
from typing import Iterable
from uuid import uuid4

from citrine.citrinedb import CitrineDB
from citrine.cluster_tools.dbmodule import create_dbmodule, delete_dbmodule, \
    import_db, find_dbmodules


class DbModule:
    """
    Manages the creation, migration, and deletion of a Citrine Database object
    that is treated like an independent, importable code module.

    This object is responsible for creating a directory structure with an
    ``__init__.py`` file that provides a single importable object in the format
    ``from <uuid> import get_db``
    """

    @property
    def path(self):
        """
        Returns the path
        :return:
        """
        return getattr(self, '___path___', None)

    @path.setter
    def path(self, value: str):
        """
        Sets the path. Only allows it to be set once and raises a
        FileNotFoundError if attempting to set a path that does not exist
        :param value: the path value
        :return:
        """
        if hasattr(self, '___path___'):
            raise AttributeError('Cannot change "path" attribute of DbModule')
        if not exists(value):
            raise FileNotFoundError(value)
        setattr(self, '___path___', value)

    def __init__(self, path: str = '.'):
        self.path = path
        self.db = import_db(self.path)
        self.name = self.db.database_name

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
        module_path = create_dbmodule(path, name, overwrite)
        return DbModule(module_path)

    @classmethod
    def destroy(cls, path: str, remove_empty: bool = True,
                remove: bool = False):
        """
        Destroys a module at the path location
        """
        delete_dbmodule(path, remove_empty, remove)

    def __call__(self):
        return self.db


class DbGroup:
    """
    A collection of databases as a single object. Will create databases as
    importable modules under a common directory and provide managed storage
    across all databases in the collection.

    It is STRONGLY RECOMMENDED to use the discovery process, and ONLY the
    discovery process, to manage the contents of the group, and is also strongly
    encouraged to load an existing group rather than create a new one every
    runtime.
    """
    @property
    def databases(self):
        if not hasattr(self, '___databases___'):
            setattr(self, '___databases___', {
                name: module.db for name, module in self.modules.items()
            })
        return getattr(self, '___databases___', dict())

    @databases.deleter
    def databases(self):
        delattr(self, '___databases___')

    @property
    def modules(self):
        return getattr(self, '___modules___', dict())

    @modules.setter
    def modules(self, value):
        setattr(self, '___modules___', value)
        # refresh database list (derived from modules)
        if hasattr(self, '___databases___'):
            del self.databases
        _ = self.databases

    def __init__(self, root: str = '.', discovery=True, modules: dict = None):
        """
        Creates the pool, using the path as the root of the group. Any DbModules
        in the root directory will be automatically retrieved and added to the
        group if discovery is True
        """
        self.root = root
        # uses modules if provided, discovers if instructed
        self.modules = self.discover(root) | (modules if modules else dict()) \
            if discovery else (modules if modules else dict())

    def create_dbmodule(self, name: str = None, overwrite: bool = False):
        """
        Creates a new database using the provided name, at the path. If no
        path is specified, the directory of execution will be used
        :param name: The name to assign the database
        """
        new = DbModule.create(self.root, name=name, overwrite=overwrite)
        self.modules[new.name] = new

    def destroy_dbmodule(self, name):
        """
        Destroys a db object from the pool entirely. This action is irreversible
        :param name: The name of the database to be destroyed
        """
        DbModule.destroy(join(self.root, name))

    @staticmethod
    def discover(root):
        """
        Collects all database modules from the provided path and adds anything
        into the pool that is not yet added
        """
        module_paths = find_dbmodules(root)
        db_modules = [DbModule(path) for path in module_paths]
        return {module.name: module for module in db_modules}


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
