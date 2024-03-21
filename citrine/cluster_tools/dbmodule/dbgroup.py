"""
Class for creating, destroying, and locating a group of db modules
"""
from os.path import join

from citrine.cluster_tools.dbmodule.dbmodule import DbModule, find_dbmodules


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
        """
        Dictionary of names and database objects. Will derive a set from all
        modules registered to the cluster unless a value has been manually set
        """
        if hasattr(self, '___databases___'):
            return getattr(self, '___databases___', dict())
        return {name: module.db for name, module in self.modules.items()}

    @databases.setter
    def databases(self, value):
        setattr(self, '___databases___', value)

    @databases.deleter
    def databases(self):
        delattr(self, '___databases___')

    @property
    def modules(self):
        return getattr(self, '___modules___', dict())

    @modules.setter
    def modules(self, value):
        setattr(self, '___modules___', value)

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
        return new

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