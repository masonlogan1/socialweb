"""
Specialized container for handling the ClusterDB database registry
"""
from datetime import datetime

from persistent import Persistent
from persistent.mapping import PersistentMapping


class DbModuleRegistry(Persistent):
    """
    Representation of a DbModule object that can be persisted into a database.
    Contains information on the file name, database name, create date,
    size limit, and migration/reallocation status
    """
    def __init__(self, name, path, created: datetime = None,
                 size_limit: int = None, in_migration: bool = False,
                 in_reallocation: bool = False):
        self.name = name
        self.path = path
        self.created = created
        self.size_limit = size_limit
        self.in_migration = in_migration
        self.in_reallocation = in_reallocation

    @staticmethod
    def from_dbmodule(module, created: datetime = None, size_limit: int = None,
                      in_migration: bool = False, in_reallocation: bool = False):
        return DbModuleRegistry(module.name, module.path, created, size_limit,
                                in_migration, in_reallocation)


class ClusterRegistryContainer(Persistent):
    """
    Container with similar method fingerprint to
    ``citrine.persistence.DbContainer`` that replaces the internal logic for
    handling containers with logic for tracking the status of multiple
    databases in a group.
    """

    def __init__(self, modules: dict | PersistentMapping = None):
        super().__init__()
        self.modules = modules if modules else PersistentMapping()

    def has(self, id) -> bool:
        """
        Return a bool describing whether the object is already present in the
        database
        :param id:
        :return:
        """
        return id in self.modules.keys()

    def read(self, id):
        """
        Return an object by the given id
        :param id:
        :return:
        """
        return self.modules.get(id, None)

    def write(self, id, obj):
        """
        Save an object to the database at the given id location
        :param obj:
        :param id:
        :return:
        """
        self.modules[id] = DbModuleRegistry.from_dbmodule(obj)

    def delete(self, id):
        """
        Remove an object from the database by the given id
        :param id:
        :return:
        """
        del self.modules[id]

    def expand_size(self, new_size: int):
        """
        Irrelevant but kept for compatibility with regular DbContainer users.
        Does nothing.
        """
