import logging
from typing import List
from math import ceil
from uuid import uuid4

from persistent import Persistent
from citrine.storage.group import Group

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DEFAULT_SIZE = 65536


class Metadata(Persistent):
    """
    Object used by a CitrineConnection as a form of metadata on the contents of
    the database
    """

    def __init__(self, size=None, cache=None):
        super().__init__()
        self.size = size
        self.cache = cache


class ContainerMeta(Persistent):
    """
    Allows for tracking the internal status of Container objects in a way
    that can be stored as an independent persistent object.
    """

    @property
    def size(self):
        """

        :return:
        """
        return

    @property
    def max_size(self):
        """

        :return:
        """
        return

    @property
    def usage(self):
        """

        """
        return

    @property
    def status(self):
        """

        """
        return

    def __init__(self, obj):
        self.obj = obj


class ContainerProperties:

    # The actual purpose of this class is to make it easier to separate the
    # boilerplate property logic and docstrings from the actual functionality

    # should be overridden by instances of implementing class
    ___metadata___ = None
    ___primary___ = None
    ___groups___ = tuple()

    @property
    def meta(self):
        """
        Quick reference to the metadata object
        :return:
        """
        return self.___metadata___

    @property
    def primary_group(self):
        return self.___primary___

    @property
    def groups(self):
        return self.___groups___

    @property
    def size(self):
        """
        Number of items in the container
        :return:
        """
        return

    @property
    def max_size(self):
        """
        Limit of items that a container can hold in strict mode
        :return:
        """
        return

    @property
    def usage(self):
        """
        Percentage of the container's max_size that has been used
        """
        return

    @property
    def status(self):
        """
        Enumerated type giving a brief summary of how full the container is
        """
        return


class Container(Persistent, ContainerProperties):
    """
    Object used to manage a collection of PersistentMapping objects within
    an object database. Uses the hash value of the object to determine which
    container it should be kept in.
    """

    def __init__(self, groups: tuple, primary_group: Group,
                 strict: bool = False, **kwargs):
        """
        Creates the Container. If the primary_group is not in the groups, it
        will be added, however if it is in the groups it will just be set as
        the primary_group property
        :param groups: all groups to include in the container
        :param primary_group: the primary group for the container
        :param strict: whether to enforce size restrictions
        """
        super().__init__()
        self.___primary___ = primary_group
        self.___groups___ = groups
        if self.primary not in self.groups:
            self.___groups___ += (self.primary,)
        self.___metadata___ = ContainerMeta(self)

    def resize(self, size: int):
        """
        Changes the size of the container. Raises a ValueError if the provided
        size value is smaller than the current number of stored objects
        :param size:
        :return:
        """

    def condense(self, transfer: bool = True) -> List[Group]:
        """
        Condenses all groups in the container into the primary group. If
        transfer is True (default), the operation will be performed in-place
        and the original groups will be depopulated. All secondary groups will
        be removed from the container at the end of the operation
        :param transfer: whether to empty the secondary containers
        :return: secondary groups removed from the container
        """

    def has(self, id) -> bool:
        """
        Return a bool describing whether the object is already present in the
        database
        :param id: the identifier of the object
        :return: whether the object exists
        """

    def read(self, id):
        """
        Return an object by the given id
        :param id: identifier of the stored object
        :return:
        """

    def write(self, id, obj):
        """
        Save an object to the database at the given id location
        :param id: identifier for the object to be stored
        :param obj: the object to be stored
        :return:
        """

    def delete(self, id):
        """
        Remove an object from the database by the given id
        :param id: identifier of the object
        :return: removed object
        """

    @staticmethod
    def new(size: int = DEFAULT_SIZE, strict=False):
        """
        Creates a new container with the given size and capacity enforcement.
        :param size: the item capacity for the container
        :param strict: whether to enforce restrictions on exceeding capacity
        :return:
        """

    def __add__(self, other):
        """
        Combines either two containers or a container and a group. The
        container on the left side of the operation will acquire the group(s)
        from the container/group on the right as secondary containers.
        :param other:
        :return:
        """

    def __contains__(self, item):
        """
        Determines whether a value is used as an id in the container.
        :param item:
        :return:
        """

    def __iter__(self):
        """
        Iterates over all items stored in the group as key-value pairs.
        :return:
        """
