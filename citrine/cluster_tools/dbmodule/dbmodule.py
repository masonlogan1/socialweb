"""
This module stores the code used for creating the directory and code for a
citrine.cluster.DbModule object.
"""
from uuid import uuid4

from os import mkdir, listdir, rmdir, remove
from os.path import join, exists, split, isfile
from shutil import rmtree
from persistent import Persistent
from persistent.mapping import PersistentMapping
from citrine.cluster_tools.dbmodule.consts import DBMODULE_DISCOVERABLE_INIT, \
    DBMODULE_UNDISCOVERABLE_INIT
from uuid import uuid4


def create_dbmodule(path: str = '.', name: str = None, discoverable: bool = True,
                    overwrite: bool = False):
    """
    Creates the directory and code at the specified path with the specified
    name.

    If the path already has an ``__init__.py`` and a ``cluster_tools.db`` file,
    an exception will be thrown unless the ``overwrite`` param is True.

    If ``overwrite`` is True, the existing files will be COMPLETELY REPLACED.
    This operation cannot be undone! Use of overwrite is strongly discouraged!
    """
    name = name if name else str(uuid4()).replace('-', '_')
    path = join(path, name)
    if not overwrite and exists(path):
        raise IOError(f'DbModule already exists at "{path}"')
    mkdir(path)
    init_path = join(path, '__init__.py')
    with open(init_path, 'w') as writer:
        if discoverable:
            writer.write(DBMODULE_DISCOVERABLE_INIT)
        else:
            writer.write(DBMODULE_UNDISCOVERABLE_INIT)
    return path


def delete_dbmodule(path: str, remove_empty: bool = True,
                    remove_all: bool = False):
    """
    Deletes the ``__init__.py`` and ``cluster_tools.db`` files from the
    specified directory.

    If ``remove_empty`` is True (default), then the directory will be removed
    if the directory is empty after deleting the ``__init__.py`` and db file.

    If ``remove`` is True, then the entire directory will be destroyed no matter
    what. This will supersede ``remove_empty``.
    """
    if remove_all:
        rmtree(path)
        return
    name = split(path)[1]
    affected = [join(path, file) for file in listdir(path)
                if (isfile(join(path, file)) and file.startswith(name))
                    or file == '__init__.py']
    for file in affected:
        remove(file)
    if remove_empty and not len(listdir(path)):
        rmdir(path)


def is_path_dbmodule(path):
    from importlib.util import spec_from_file_location, module_from_spec
    try:
        init_path = join(path, '__init__.py')
        spec = spec_from_file_location('DB_MODULE', init_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.DB_MODULE
    except Exception:
        # there are many things that can raise an exception, so let's just
        # assume that if something happens this is not a DbModule directory
        return False


def find_dbmodules(path: str):
    # find every directory with an init file
    potential_dbmodules = [join(path, file) for file in listdir(path)
                           if exists(join(path, file, '__init__.py'))
                           and file != path]
    # import the init files and look for DB_MODULE == True
    return (mod for mod in potential_dbmodules if is_path_dbmodule(mod))


def import_db(path):
    """
    Imports the module database from a DbModule directory and returns it
    :param path: the location of the directory to find the __init__.py file
    :return:
    """
    # imports the db, opens it, and returns the object
    from importlib.util import spec_from_file_location, module_from_spec
    init_path = join(path, '__init__.py')
    if not exists(init_path):
        raise FileNotFoundError(init_path)
    spec = spec_from_file_location('db', init_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.db()


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

    @property
    def size(self):
        with self.db as connection:
            return connection.size

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


class DbModuleRegistry(Persistent):
    """
    Object representative of a DbModule that can be saved to a database
    """
    def __init__(self, module_path: str, name: str, size: int = 0):
        self.module_path = module_path
        self.name = name
        self.size = size

    def update_from_dbmodule(self, dbmodule: DbModule):
        """
        Updates the registry object by providing a new dbmodule. Only updates
        attributes expected to change, like the size.
        :param dbmodule:
        :return:
        """
        self.size = dbmodule.size

    @staticmethod
    def from_dbmodule(dbmodule: DbModule):
        """
        Creates a registry object from a DbModule
        :param dbmodule:
        :return:
        """
        return DbModuleRegistry(dbmodule.path, dbmodule.name, dbmodule.size)
