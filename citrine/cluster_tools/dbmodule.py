"""
This module stores the code used for creating the directory and code for a
citrine.cluster.DbModule object.
"""
from uuid import uuid4

from os import mkdir
from os.path import join, exists
from citrine.cluster_tools.consts import DBMODULE_INIT


def create_dbmodule(path: str = '.', name: str = None,
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
        writer.write(DBMODULE_INIT)
    return path


def delete_dbmodule(module_path: str, remove_empty: bool = True,
                    remove: bool = False):
    """
    Deletes the ``__init__.py`` and ``cluster_tools.db`` files from the
    specified directory.

    If ``remove_empty`` is True (default), then the directory will be removed
    if the directory is empty after deleting the ``__init__.py`` and db file.

    If ``remove`` is True, then the entire directory will be destroyed no matter
    what. This will supersede ``remove_empty``.
    """
