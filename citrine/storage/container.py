import logging
from math import ceil
from uuid import uuid4

from persistent import Persistent
from persistent.mapping import PersistentMapping

# if the zope people would like to make sure the BTree class is directly
# importable rather than the current "cleverer than you" bs they have going on,
# that would be FANTASTIC.
from BTrees import _OOBTree
BTree = _OOBTree.BTree

from citrine.cluster_tools.clusterdb import container

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CollectionCapacityError(Exception):
    """
    Raised when an operation will exceed the capacity of a collection.
    """


class RestrictedItemError(Exception):
    """
    Raised when attempting to access or alter an item in a collection that
    is not meant to be accessed or altered.
    """


def groupfn(fn):
    def decorator(obj, key, *args, **kwargs):
        index = int.from_bytes(key.encode()) % (len(obj.collections))
        collection = obj.collections[index]
        fn(obj, collection, key, *args, **kwargs)
    return decorator


class CollectionView:
    obj = None
    fn = None

    def __iter__(self):
        return self.fn()

    def __len__(self):
        count = 0
        for _ in self.fn():
            count += 1
        return count

    def __getitem__(self, key):
        if isinstance(key, int):
            if key > self.obj.size:
                raise IndexError('CollectionKeys index out of range')
            indexes = [key]
        elif isinstance(key, slice):
            indexes = list(range(key.start, key.stop, key.step))
        else:
            raise TypeError('CollectionKeys indices must be integers ' +
                            f'or slice, not {type(key)}')
        found = list()
        for index, val in enumerate(self.fn()):
            if index in indexes:
                found.append(val)
        return found if isinstance(key, slice) else found[0]

    def __contains__(self, item):
        for key in self.fn():
            if item == key:
                return True
        return False


class CollectionKeys(CollectionView):
    def __init__(self, obj):
        self.obj = obj
        self.fn = obj.iterkeys


class CollectionValues(CollectionView):

    def __init__(self, obj):
        self.obj = obj
        self.fn = obj.itervalues


class CollectionItems(CollectionView):

    def __init__(self, obj):
        self.obj = obj
        self.fn = obj.iteritems


class CollectionByValue(CollectionView):

    def __init__(self, obj):
        self.obj = obj
        self.fn = lambda: ((value, key) for key, value in obj.iteritems())


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
    ALERT = 70
    WARNING = 80
    CRITICAL = 90
    LEVELS = [HEALTHY, ACCEPTABLE, ALERT, WARNING, CRITICAL]
    # Things can become unstable over 5000 using the default ZODB DB cache size
    DEFAULT_MAX = 5000

    @property
    def size(self):
        """Number of items in the collection."""
        return len(self.obj.keys())

    @property
    def usage(self):
        """Percent of used space as a float value"""
        return self.size / self.max_size

    @property
    def status(self):
        """
        Helpful map for tracking the status of a collection. Can indicate if it
        may be time to either prune or create another collection that holds
        more objects.
        """
        return max(v for v in self.LEVELS if v <= ceil(self.usage * 100))

    def __init__(self, obj, uuid, max_size, strict, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj
        self.uuid = uuid
        self.max_size = max_size
        self.strict = strict


class Collection(BTree):
    """
    Modified version of a OOBTree that provides a metadata object and several
    properties derived from it for easily keeping track of the size and health
    of the collection. Also provides a "strict" mode that will put a hard limit
    on the number of items the collection can store to ensure stability.
    """

    # "why list these out when you can just use obj.meta.whatever?"
    # because I like things to be easier to reach.
    @property
    def uuid(self):
        return self.meta.uuid

    @property
    def size(self):
        # subtract one to account for stored metadata object
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

    @property
    def strict(self):
        return self.meta.strict

    @strict.setter
    def strict(self, value: bool):
        self.meta.strict = value

    @property
    def meta(self):
        # TODO: THE OBJECT NEEDS TO BE CACHED AFTER GETTING IT THE FIRST TIME
        # set up a new CollectionMeta value if one does not exist
        if 'meta' in self.keys():
            return self.get('meta')
        super().insert('meta', CollectionMeta(
                    self,
                    uuid=str(uuid4()),
                    max_size=CollectionMeta.DEFAULT_MAX,
                    strict=True
                )
            )
        return BTree.get(self, 'meta')

    @meta.setter
    def meta(self, value):
        # TODO: TYPE CHECK FOR COLLECTIONMETA OBJECTS AND THAT THE META POINTS
        #   TO THIS COLLECTION; DO NOT ALLOW METAS POINTED TO OTHER OBJECTS TO
        #   BE SET AS THE META FOR THIS COLLECTION!
        super().insert('meta', value)

    def __init__(self, uuid: str = None, max_size: int = None, strict=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        meta = CollectionMeta(
            self,
            uuid=uuid if uuid else str(uuid4()),
            max_size=max_size if max_size else CollectionMeta.DEFAULT_MAX,
            strict=strict
        )
        self.meta = meta

    def get(self, key, default=None):
        """
        Retrieve a value from the collection.
        :param key: the key associated with the desired item
        :param default: value to return if the key does not exist
        """
        if key == 'meta':
            raise RestrictedItemError('Cannot directly retrieve meta object')
        return super().get(key, default)

    def insert(self, key, value):
        if self.size >= self.max_size and self.strict:
            raise CollectionCapacityError(
                f'Cannot insert "{key}"; maximum size reached!'
            )
        if key == 'meta':
            raise RestrictedItemError('Cannot alter protected value "meta"')
        return super().insert(key, value)

    def update(self, collection):
        new_keys = [key for key in collection.keys() if key not in self.keys()]
        if self.size + len(new_keys) > self.max_size and self.strict:
            raise CollectionCapacityError(
                f'Cannot update collection; maximum size reached!'
            )
        if 'meta' in collection.keys():
            raise RestrictedItemError('Cannot alter protected value "meta"')
        return super().update(collection)

    def pop(self, key, default=None):
        """
        Pop a key from the collection and return its value.
        :param key:
        :param default:
        :return:
        """
        if key == 'meta':
            raise RestrictedItemError('Cannot remove protected value "meta"')
        if key not in self.keys() and default is None:
            raise KeyError(f'Key "{key}" not found in collection')
        return super().pop(key, default)

    def popitem(self):
        """
        Pop a key from the collection and return the key-value pair. Raises
        a KeyError if the
        :param key:
        :return:
        """
        key = self.minKey()
        return key, self.pop(key)

    def setdefault(self, key, value):
        """
        Sets the value at the key to the provided value. If the key already
        exists then return the previous value stored there, else return the
        value provided
        :param key: id of item to write to
        :param value: the value to write
        :return: existing value or provided value if no value currently exists
        """
        if key == 'meta':
            raise RestrictedItemError('Cannot alter protected value "meta"')
        prior = self.get(key) if key in self.keys() else value
        self.update({key: value})
        return prior

    def clear(self):
        # save the meta element!
        meta = super().get('meta')
        super().clear()
        super().insert('meta', meta)

    # I know iterkeys, itervalues, and iteritems are supposed to be deprecated,
    # but OOBTree.BTree still uses them, and I'd rather not have loose ends.
    # Additionally, we only have to lean on one function to filter out 'meta'.
    def keys(self):
        return CollectionKeys(self)

    def iterkeys(self, min=None, max=None):
        return (key for key, value in self.iteritems(min, max))

    def values(self):
        return CollectionValues(self)

    def itervalues(self, min=None, max=None):
        for value in super().itervalues(min, max):
            if not isinstance(value, CollectionMeta):
                yield value

    def items(self):
        return CollectionItems(self)

    def iteritems(self, min=None, max=None):
        for key, value in super().iteritems(min, max):
            if key != 'meta':
                yield key, value

    def byValue(self, min=None):
        """
        Returns anything where key >= min in (value, key) pairs
        :param min: minimum value to start from
        :return:
        """
        return CollectionByValue(self)

    def maxKey(self, max=None):
        # gonna be honest, this method seems useless any time strings are the
        # keys, but for the sake of completeness we provide an implementation
        if (key := super().maxKey(max)) != 'meta':
            return key
        if not self.size:
            raise ValueError('empty tree')
        return super().maxKey(super().keys()[-2])

    def minKey(self, min=None):
        # same as above, this seems useless in practice if strings are involved
        if (key := super().minKey(min)) != 'meta':
            return key
        if not self.size:
            raise ValueError('empty tree')
        return super().minKey(super().keys()[1])

    def has_key(self, key):
        return key in self.keys()


class CollectionGroupMeta(Persistent):
    """
    Allows for tracking the internal status of CollectionGroup objects in a way
    that can be stored as an independent persistent object.
    """

    @property
    def size(self):
        return sum(collection.size for collection in self.collections)

    @property
    def max_size(self):
        return sum(collection.max_size for collection in self.collections)

    @property
    def max_collection_size(self):
        return max(collection.max_size for collection in self.collections)

    @property
    def usage(self):
        """Percent of used space"""
        return self.size / self.max_size

    @property
    def collection_usage(self):
        """Percent of used space by collection"""
        return {collection: collection.usage for collection in self.collections}

    @property
    def highest_collection_usage(self):
        return max(self.collection_usage.values())

    @property
    def lowest_collection_usage(self):
        return min(self.collection_usage.values())

    @property
    def status(self):
        """
        Provides the status of the collection group. Will use the highest status
        from the collections; if one collection is unstable it threatens the
        stability of the entire group.
        """
        return max(collection.status for collection in self.collections)

    def __init__(self, obj):
        self.obj = obj
        self.collections = tuple(self.obj.collections)


class CollectionGroup(Persistent):
    """
    A collection of multiple Collection objects.

    Intended to act as an immutable set. Collections created by/managed by a
    CollectionGroup should not be modified directly as their contents may not
    be reachable when attempting to use any of the standard operations.

    These objects should be saved to a database immediately if possible, keeping
    them in memory can cause a number of issues if they start to grow too large
    before the initial commit.
    """
    def __init__(self, collections, **kwargs):
        super().__init__(**kwargs)
        # repeating UUID values
        if len({col.uuid for col in collections}) != len(collections):
            raise KeyError("Collections must not have conflicting UUID values")
        self.collections = collections
        self.meta = CollectionGroupMeta(self)

    @groupfn
    def get(self, collection: Collection, key: str, value):
        return collection.get(key)

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