"""
This module stores the code used for creating the directory and code for a
citrine.cluster.DbModule object.
"""
from os import path


def create_dbmodule(module_path: str = '.', name: str = None,
                    overwrite: bool = False):
    """
    Creates the directory and code at the specified path with the specified
    name.

    If the path already has an ``__init__.py`` and a ``cluster_tools.db`` file,
    an exception will be thrown unless the ``overwrite`` param is True.

    If ``overwrite`` is True, the existing files will be COMPLETELY REPLACED.
    This operation cannot be undone! Use of overwrite is strongly discouraged!
    """


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
