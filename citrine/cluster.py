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
from citrine.cluster_tools.dbmodule.dbgroup import ManagedGroupDB
from citrine.cluster_tools.clusterdb.container import ClusterRegistryContainer



class ClusterDB(ManagedGroupDB):
    def create(self, id: str, obj):
        """
        Converts the object into a persistable format and stores it to the
        database
        :param id:
        :param obj:
        :return:
        """
        raise NotImplementedError

    def read(self, id):
        """
        Retrieves the object from the database and returns it to its original
        format
        :param id:
        :return:
        """
        raise NotImplementedError

    def update(self, id, obj: object):
        """
        Locates the object by the given id and updates it to the new object
        :param id:
        :param obj:
        :return:
        """
        raise NotImplementedError

    def delete(self, id):
        """
        Locates the object by the given id and removes it from the database
        :param id:
        :return:
        """
        raise NotImplementedError

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
