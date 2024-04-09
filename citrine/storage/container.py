import logging
from math import ceil
from uuid import uuid4

from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import BTree

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CollectionMeta(Persistent):
    """
    Metadata object for managing a Collection. Keeps information on the size,
    object size limit, and groups the Collection belongs to.

    This object is ONLY intended to be used with ``citrine.storage.Collection``
    objects.
    """
    # I picked these numbers because anything under 60% of the default seems to
    # work perfectly well, but performance drops off after that point
    HEALTHY = 0
    ACCEPTABLE = 60
    MODERATE = 70
    WARNING = 80
    CRITICAL = 90
    LEVELS = [HEALTHY, ACCEPTABLE, MODERATE, WARNING, CRITICAL]
    # Things can become unstable over 5000 using the default ZODB DB cache size
    DEFAULT_MAX = 5000

    @property
    def size(self):
        return len(self.obj.keys())

    @property
    def usage(self):
        """Percent of used space"""
        return self.size / self.max_size

    @property
    def status(self):
        """
        Helpful map for tracking the status of a collection. Can indicate if it
        may be time to either prune or create another collection that holds
        more objects.
        """
        return max(v for v in self.LEVELS if v <= ceil(self.usage) * 100)

    def __init__(self, obj, uuid, max_size):
        self.obj = obj
        self.uuid = uuid
        self.max_size = max_size


class Collection(BTree):
    """
    Modified version of a PersistentMapping that allows for accessing objects
    stored inside as attributes
    """

    # "why list these out when you can just use obj.meta.whatever?"
    # because I like things to be easier to reach.
    @property
    def uuid(self):
        return self.meta.uuid

    @property
    def size(self):
        return self.meta.size

    @property
    def usage(self):
        return self.meta.usage

    @property
    def status(self):
        return self.meta.status

    @property
    def max_size(self):
        return self.meta.max_size

    def __init__(self, uuid: str = None, max_size: int = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta = CollectionMeta(
            self,
            uuid=uuid if uuid else str(uuid4()),
            max_size=max_size if max_size else CollectionMeta.DEFAULT_MAX
        )

    def insert(self, key, value):
        if self.size >= self.max_size:
            raise IndexError(
                f'Cannot insert "{key}"; maximum size reached!'
            )
        super().insert(key, value)

    def update(self, collection):
        if self.size + len(collection.keys()) > self.max_size:
            raise IndexError(
                f'Cannot update collection; maximum size reached!'
            )
        super().update(collection)


class CollectionGroup(Persistent):
    """
    A collection of multiple Collection objects.

    Intended to act as an immutable set. Collections created by/managed by a
    CollectionGroup should not be modified directly as their contents may not
    be reachable when attempting to use any of the standard operations.
    """
    def __init__(self, collections: tuple = None, **kwargs):
        super().__init__(**kwargs)
        if not (collections and
                len({col.uuid for col in collections}) == len(collections)):
            raise KeyError("Collections must not have conflicting UUID values")
        self.collections = collections if collections else (Collection(),)

    @staticmethod
    def groupfn(fn):
        def decorator(obj, key, *args, **kwargs):
            index = int.from_bytes(key.encode()) % (len(obj.collections))
            collection = obj.collections[index]
            fn(obj, collection, key, *args, **kwargs)
        return decorator

    @groupfn
    def insert(self, collection: Collection, key: str, value):
        return collection.insert(key, value=value)

    @groupfn
    def update(self, collection: Collection, incoming_collection):
        return collection.update(incoming_collection)


class Metadata(Persistent):
    """
    Object used by a CitrineConnection as a form of metadata on the contents of
    the database
    """

    def __init__(self, size=None, cache=None):
        super().__init__()
        self.size = size
        self.cache = cache


class Container(Persistent):
    """
    Object used to manage a collection of PersistentMapping objects within
    an object database. Uses the hash value of the object to determine which
    container it should be kept in.
    """

    @property
    def size(self):
        return sum((len(con.keys()) for con in self.containers.values()))

    def __init__(self, containers: dict | PersistentMapping = None):
        super().__init__()
        # Containers will be stored as a PM of PMs
        self.containers = containers if containers is not None else \
            PersistentMapping({0: Collection()})

    def expand_size(self, new_size: int):
        if new_size <= self.containers_size:
            raise ValueError(f'Cannot expand from {self.containers_size} ' +
                             f'containers to {new_size} containers, new size ' +
                             f'must be larger than existing size')
        self.containers = PersistentMapping({
            key: self.containers.get(key, PersistentMapping())
            for key in range(new_size)
        })

    def has(self, id) -> bool:
        """
        Return a bool describing whether the object is already present in the
        database
        :param id:
        :return:
        """
        return id in self.__locate_container(id).keys()

    def read(self, id):
        """
        Return an object by the given id
        :param id:
        :return:
        """
        return self.__locate_container(id).get(id, None)

    def write(self, id, obj):
        """
        Save an object to the database at the given id location
        :param obj:
        :param id:
        :return:
        """
        self.__locate_container(id)[id] = obj

    def delete(self, id):
        """
        Remove an object from the database by the given id
        :param id:
        :return:
        """
        self.__locate_container(id).pop(id)

    def __locate_container(self, id: str):
        """
        Locate the appropriate container based on the provided id value
        :param id:
        :return:
        """
        # ensure we get the same value each time
        val = int.from_bytes(str(id).encode(), 'big')
        val = val % self.containers_size
        return self.containers[val]