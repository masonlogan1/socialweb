"""
This module stores the code used for creating the directory and code for a
citrine.cluster.DbModule object.
"""
from uuid import uuid4

from os import mkdir, listdir, rmdir, remove
from os.path import join, exists, split, isfile
from shutil import rmtree
from citrine.cluster_tools.dbmodule.consts import DBMODULE_DISCOVERABLE_INIT, \
    DBMODULE_UNDISCOVERABLE_INIT


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
