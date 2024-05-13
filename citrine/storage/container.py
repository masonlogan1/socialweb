import logging
from typing import List, Tuple

from persistent import Persistent
from citrine.storage.group import Group
from citrine.storage.consts import (DEFAULT_CONTAINER_SIZE,
                                    DEFAULT_COLLECTION_SIZE)
from citrine.storage.utils import (number_of_collections,
                                   next_number_of_collections)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        The number of all items in all groups
        """
        return sum(grp.size for grp in self.obj.groups)

    @property
    def max_size(self):
        """
        The maximum size of all groups in the container
        """
        return sum(grp.max_size for grp in self.obj.groups)

    @property
    def capacity(self):
        """
        The maximum size of the primary group
        """
        return self.obj.primary.max_size

    @property
    def used(self):
        """
        The number of items in the primary group
        """
        return self.obj.primary.size

    @property
    def usage(self):
        """
        The usage percentage of the primary group
        """
        return self.obj.primary.usage

    @property
    def status(self):
        """
        The health of the primary group
        """
        return self.obj.primary.status

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
    def meta(self) -> ContainerMeta:
        """
        Quick reference to the metadata object
        :return:
        """
        return self.___metadata___

    @property
    def primary(self) -> Group:
        """
        The primary read/write group of the container
        :return:
        """
        return self.___primary___

    @property
    def groups(self) -> Tuple[Group]:
        """
        The ordered set of groups in the container
        :return:
        """
        return self.___groups___

    @property
    def size(self) -> int:
        """
        Number of items in the container
        :return:
        """
        return self.meta.size

    @property
    def max_size(self) -> int:
        """
        Limit of items that a container can hold in strict mode
        :return:
        """
        return self.meta.max_size

    @property
    def capacity(self):
        """
        The maximum size of the primary group
        """
        return self.meta.capacity

    @property
    def used(self) -> float:
        """
        The number of items in the primary group
        :return:
        """
        return self.meta.used

    @property
    def usage(self) -> float:
        """
        Percentage of the container's max_size that has been used
        """
        return self.meta.usage

    @property
    def status(self) -> int:
        """
        Enumerated type giving a brief summary of how full the container is
        """
        return self.meta.status

    @property
    def strict(self) -> bool:
        return self.primary.strict

    @strict.setter
    def strict(self, value):
        if not isinstance(value, bool):
            raise TypeError("'strict' must be a boolean")
        self.primary.strict = value


class Container(Persistent, ContainerProperties):
    """
    Object used to manage a collection of PersistentMapping objects within
    an object database. Uses the hash value of the object to determine which
    container it should be kept in.
    """

    def __init__(self, primary_group: Group, groups: tuple = tuple(),
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
            self.___groups___ = (self.primary,) + self.groups
        self.___metadata___ = ContainerMeta(self)
        self.strict = strict

    @classmethod
    def new(cls, capacity: int = DEFAULT_CONTAINER_SIZE,
            collection_max_size: int = DEFAULT_COLLECTION_SIZE,
            strict: bool = False):
        """
        Creates a new Container object with the given size. The number each
        internal collection can store will be capped to the
        ``collection_max_size`` value.
        :param capacity: the maximum number of objects the Container can hold
        :param collection_max_size: the maximum size of each collection
        :param strict: whether to enforce size restrictions with exceptions
        :return: new ``Container`` object
        """
        size = number_of_collections(
            capacity,
            max_collection_size=collection_max_size
        )
        if size * capacity < collection_max_size:
            collection_max_size = size * capacity
        primary = Group.new(
            size=size,
            max_collection_size=collection_max_size,
            strict=strict
        )
        return Container(primary, strict=strict)

    def resize(self, capacity: int,
               max_collection_size: int = DEFAULT_COLLECTION_SIZE,
               condense=False, transfer=True, transaction_manager=None) \
            -> List[Group]:
        """
        Changes the size of the container. The previous primary group will be
        condensed into the new primary. Raises a ValueError if the provided
        size value is smaller than the current number of stored objects

        The primary group cannot be resized in place without breaking the
        ability to read the objects inside, however the primary will be placed
        into the group list so all objects will be accessible during the
        resizing process.

        If ``transfer`` is set to True, any groups merged into the new primary
        will have their contents moved in-place, emptying the group. This
        operation will take place in reverse order, ensuring that groups earlier
        in the listing have their contents prioritized.

        If ``condense`` is set to True, the secondary groups will be condensed
        into the primary group.

        If ``transfer`` is set to True alongside ``condense``, the secondary
        groups will be emptied of their contents, which is an irreversible
        action. This action is equivalent to  ``condense(transfer=True)``.
        See the documentation of ``condense`` for more information.

        If ``transaction_manager`` is provided, each action will be performed
        as an individual transaction.

        :param capacity: the desired new size
        :param max_collection_size: the maximum size of each ``Collection``
        :param condense: whether to condense all secondary groups
        :param transfer: whether to transfer objects between primary groups
        :param transaction_manager: transaction manager to use, if any
        :return: groups removed from the container
        """
        # create a new group with a prime number of containers capable of
        # handling the capacity
        size = number_of_collections(
            capacity,
            max_collection_size=max_collection_size
        )
        if size * capacity < max_collection_size:
            collection_max_size = size * capacity
        new_primary = Group.new(
            size=size,
            max_collection_size=max_collection_size,
            strict=self.strict
        )

        # set the new group as the primary and makes the old primary a secondary
        self.___groups___ = (new_primary,) + self.groups
        self.___primary___ = new_primary

        if condense:
            removed = self.condense(transfer=transfer,
                                    transaction_manager=transaction_manager)
        else:
            # if we only want to move over the data from the old primary,
            # set aside all other groups, use condense, and put them back after
            secondaries = self.groups[2:]
            self.___groups___ = self.___groups___[:2]
            removed = self.condense(transfer=transfer,
                                    transaction_manager=transaction_manager)
            self.___groups___ += secondaries
        return removed

    def condense(self, transfer: bool = True, transaction_manager=None) \
            -> List[Group]:
        """
        Condenses all groups in the container into the primary group.

        If the primary group is in strict mode and the number of objects that
        will be added exceeds the capacity, a CapacityException will be raised.

        If ``transfer`` is True (default), the operation will be performed
        in-place and the original groups will be depopulated. All secondary
        groups will be removed from the container at the end of the operation
        and returned.

        If ``transaction_manager`` is provided, each action will be performed
        as an individual transaction.

        :param transfer: whether to empty the secondary containers
        :param transaction_manager: transaction manager to use, if any
        :return: secondary groups removed from the container
        """
        source_groups = self.groups[1:]

        if transfer:
            fn = lambda group, key: self.primary.insert(key, group.pop(key))
        else:
            fn = lambda group, key: self.primary.insert(key, group.get(key))

        for group in source_groups:
            for key in list(group.keys()):
                fn(group, key)

        if transfer:
            discarded = list(self.groups[1:])
            self.___groups___ = (self.groups[0],)
            return discarded
        return []

    def has(self, id) -> int:
        """
        Return a bool describing whether the object is already present in the
        database
        :param id: the identifier of the object
        :return: whether the object exists
        """
        return sum(1 for group in self.groups if group.has_key(id))

    def read(self, id, default=None):
        """
        Return an object by the given id
        :param id: identifier of the stored object
        :param default: default value to return if the object does not exist
        :return: the desired object if it exists, or the default if provided
        """
        for group in self.groups:
            if ret := group.get(id):
                return ret
        return default

    def write(self, id, obj):
        """
        Save an object to the database at the given id location
        :param id: identifier for the object to be stored
        :param obj: the object to be stored
        """
        if not (res := self.primary.insert(id, obj)):
            return self.primary.update({id: obj})
        return res

    def delete(self, id) -> Tuple:
        """
        Remove an object from the database by the given id
        :param id: identifier of the object
        :return: removed object
        """
        return tuple(group.pop(id) for group in self.groups if self.has(id))

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
